#IMPORTS
import requests
import json
import sys
import time
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import dotenv_values

#MAIN DEFINITION
def main():
    """
    Main function that creates all the shared variables, then runs a loop over each project and each url for the store the project is associated with so as to scrape all 
    the necesary product data from a particular website using a particular pareshub project.
    
    Paramerters:
    None
    
    Returns:
    None
    """
    #Script Specific Variable Declaration
    env_values = dotenv_values("api.env")                                    #Create a dictionary using the data in a .env file
    ph_config, em_config, projects = env_parser(env_values)                  #Call env_parser(), return parsed data in three variables
    
    json_path = "../json_files/"                                             #Path tot he location all of the JSON output files will be placed
    searchTerms = "searchTerms.txt"                                          #Path to the text file used to generate urls
    
    #Iterate through the project tuples, performing necessary operations to create a final JSON containing all data scraped from the relevant store.
    for project in projects:                                                 #For each project
        #Project Specific Variable Declaration
        final_dict = {                                                       #Initialize dictionary that will be saved as a JSON for a particular store
            "Store": project[1],                                             #Holds store name
            "Products": []                                                   #List of dictionaries of product data
        }
        final_list = []                                                      #List that will be used to perform operation on the data before being passed to "Products" in final_dict
        url_list = url_creator(em_config, searchTerms, project)              #Call url_creator(), return a list of URLs to scrape
        
        #Iterate through the url_list, scraping, checking, and formating the product data dictionaries
        for url in url_list:                                                 #For each url
            raw_dict = run_proj(url, 0, ph_config, em_config, project[0])    #Call run_proj on the current url with an error count of 0, return a dictionary of scraped data
            if raw_dict == {}:
                continue
            checked_dict = check_values(raw_dict, em_config)                 #Call check_values, return the corrected dictionary
            formatted_list = formatter(checked_dict)                         #Call formatter, return a list with the fields in the dictionaries in the desired order.
            final_list.extend(formatted_list)                                #Combine the formated list with the growing final_list list
                                                                            
        
        #Remove all duplicate product dictionaries in the final list and insert the list into final_dict["Products"]
        filtered_list = rm_duplicate(final_list)                             #Call rm_duplicate, return a list with no duplicate product dictionaries
        final_dict["Products"].extend(filtered_list)                         #Set "Products" in final_dict to the filtered_list
    
        #Save the final_dict as a JSON file with the store name as the file name.
        path = json_path + project[1] + ".json"                              #Define the full path to the JSON, as well as name the JSON after the store the data comes from 
        with open(path, 'w') as json_file:                                   #Create and write to the file defined in path
            json.dump(final_dict, json_file, indent = 4)                     #Convert final_dict to a JSON, displayed vertically, to be written to the JSON file

#DEBUG_SEND_ERROR DEFINITION
def debug_send_error(code, string):                                          #DEBUG: Print a message to the screen instead of emailing
    """
    This function is for debugging purposes only, and is meant to replace send_error() during debugging. It reduces the number of emails sent to the developer, 
    by instead printing the messages to the screen.

    Parameters:
    code (int): An error code, indicating which error message to use.
    string (string): A word or url that clarifies what exactly is causing the error.

    Returns:
    Nothing
    """
    
    if code == 1:                                                            #If the code is 1
        print(f"ERROR 1: INVALID URL\n{string}")                             #Print that the URL is invalid
    elif code == 2:                                                          #If the code is 2
        print(f"ERROR 2: UNABLE TO SCRAPE URL\n{string}")                    #Print that the project is unable to scrape data from the URL
    elif code == 3:                                                          #If the code is 3
        print(f"ERROR 3: UNABLE TO SCRAPE FIELD\n{string}")                  #Print that the project is not scraping the field

#SEND_ERROR DEFINITION
def send_error(code, string, config):
    """
    This function is meant to be used when not debugging. It sends a personalized message to the developer about an error or mistake made in the script or 
    the parsehub project.

    Parameters:
    code (int): An error code, indicating which error message to use.
    string (string): A word or url that clarifies what exactly is causing the error.
    config (dictionary): A dictionary of key:value pairs needed to send send an email.

    Returns:
    Nothing
    """
    
    #Get sender and receiver data from config
    sender_email = config["sender_email"]                                    #Set the sender email address
    app_password = config["app_password"]                                    #Set the sender email password
    receiver_email = config["receiver_email"]                                #Set the receiver email address
    
    # Create an email message
    msg = MIMEMultipart()                                                    #Create a message
    msg['From'] = sender_email                                               #Set the sender to the sender email address
    msg['To'] = receiver_email                                               #Set the receiver to the receiver email address
    msg['Subject'] = "Error Running Parsehub Script"                         #Set the Subject of the email

    #Set and attach the body to the message
    if code == 1:                                                            #If the code is 1 set the body of the message to show that the URL is invalid
        body = f"BobcatCLAWS Dev Team,\nThe Parsehub script was unable to validate the url:\n{string}\nPlease inspect the url and make any needed corrections in the script."
    elif code == 2:                                                          #If the code is 2 set the body of the message to show that the project cannot scrape data from a URL
        body = f"BobcatCLAWS Dev Team,\nThe Parsehub script was unable to scrape the url:\n{string}\nPlease inspect the url and project and make any needed corrections."
    elif code == 3:                                                          #If the code is 3 set the body of the message to show that the project cannot scrape some field
        body = f"BobcatCLAWS Dev Team,\nThe Parsehub script was unable to scrape {string} data.\nPlease inspect the Parsehub project and make any needed corrections."
    msg.attach(MIMEText(body, 'plain'))                                      #Attach the body to the message

    #Connect to the Gmail's SMTP server
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_connection = smtplib.SMTP(smtp_server, smtp_port)

    # Start the TLS (Transport Layer Security) session
    smtp_connection.starttls()
    
    # Log in to the email account and send the message
    smtp_connection.login(sender_email, app_password)
    smtp_connection.sendmail(sender_email, receiver_email, msg.as_string())
    
    # Close the SMTP connection
    smtp_connection.quit()

#ENV_PARSER DEFINITION
def env_parser(env_values):
    """
    Parses the sensitive data of an .env file into 3 variables needed to run the script.

    Parameters:
    env_values (dictionary): A dictionary containing all of the sensititve data needed to run the script.

    Returns:
    ph_config (dictionary): Contains the API key and search term field needed to run a parsehub project.
    em_config (dictionary): Contains the email address of the sender and receiver and the sender's password.
    projects (list): Tuples each containing a project token, store name, a string representing a space, a url template
    """
    
    env_values = dict(env_values)                                            #Read env_values into a dictionary of the same name
    projects = json.loads(env_values["projects"])                            #A list of tuples each containing:
                                                                             #A project token to a project that scrapes a particular store
                                                                             #The related store's name
                                                                             #The string used in that store's URLs to represent a space in a search
                                                                             #A URL template that when contatenated with a search "term" will pull up a search results page
    ph_config = {                                                            #The configurations needed to run any parsehub project
        "api_key":env_values["ParsehubAPI"],                                 #The developer's API key
        "start_url":None                                                     #The URL to start the scraping from, Default: None
    }
    em_config = {                                                            #The configurations needed to send an error email to the developer
        "sender_email":env_values["sender_email"],                           #The email address of the message sender
        "app_password":env_values["app_password"],                           #The password to the email address of the message sender
        "receiver_email":env_values["receiver_email"]                        #The email address of the message receiver
    }

    return ph_config, em_config, projects                                    #Return the Parsehub configurations, email configurations, and project tuples

#URL_CREATOR DEFINITION
def url_creator(email_config, searchTerms, project):
    """
    Concatenates a URL template for a specific website with a particular search term to create a URL. If the URL is valid it is added to a list of URLs if not an error
    message is sent.

    Parameters:
    email_config (dictionary): contains the key:value pairs needed to send an email.
    searchTerms (list): A list of strings representing categories and subcategories of products that need to be scraped from a website.
    project (tuple): A tuple of strings that contains the string representing a space, and a URL template needed to create a real URL.

    Returns:
    url_list (list): Contains all the valid URLs created.
    """
    
    #URL Specific Variable Declaration
    space = project[2]                                                       #The string representing a space in the particular store's URLs
    template = project[3]                                                    #The URL template that when concatented with a search "term" produces a search results page
    url_list = []                                                            #An empty list to hold the newly created URLs
    
    #Iterate through the terms in the searchTerms.txt file, using them to create URLs
    with open(searchTerms, 'r') as file:                                     #Open and read from the searchTerms.txt file
        for term in file:                                                    #For each line in the file    
            #Read and alter the lines to fit the store's URL schema and then form a complete URL
            name = term.strip()                                              #Read the line as a name with no trailing spaces
            name = name.replace(" ", space)                                  #Replace any spaces between words with the string used to replace spaces in the store's URLs
            url = template + name                                            #Concatenate the template and the name to form a complete URL
            
            #Call is_valid_url() on url, respond appropriately
            if is_valid_url(url):                                            #If url is valid
                url_list.append(url)                                         #Append it to the url list
            else:                                                            #If url is not valid
                send_error(1, url, email_config)                             #Call send_error with a code of 1 and the url
                
    return url_list                                                          #Return the completed URL list

#IS_VALID_URL DEFINITION
def is_valid_url(url):
    """
    Uses the request module to determine if a URL leads to a webpage that exists.

    Parameters:
    url (string): Represents a url that should lead to a webpage that exists

    Returns:
    bool: True if a URL leads to a page that exists, false if for any reason the request was unable to reach an existing webpage.
    """
    
    #Send a request for the url and get it's status code if possible, return true or false based on results
    try:
        response = requests.head(url)                                        #Send a request for the metadata of the URL
        return response.status_code != 404                                   #Return true if the URL exists
    except requests.exceptions.RequestException:                             #If for any reason the URL was not able be pulled up
        return False                                                         #Return false

#RUN_PROJ DEFINITION
def run_proj(url, err_count, ph_config, em_config, proj_token):
    """
    Runs a particular parsehub project on a particular URL, waits for the run to complete, checks that the run was successful and if not retry the run (a maximum of two
    times). Pulls the successfully scraped data and converts it to a dictionary.

    Parameters:
    url (string): A valid URL leading to a search results webpage for a particular category or subcategory.
    err_count (int): A number indicating the number of times a run was done on a particular URL for a particular project.
    ph_config (dictionary): A dictionary containing key:value pairs needed to run a parsehub project.
    em_config (dictionary): A dictionary containing key:value pairs needed to send an email.
    proj_token (string): A string representing a particular parsehub project in the parsehub server.

    Returns:
    data_dict (dictionary): A dictionary containing all of the product data scraped from a particular URL using a particular project.
    """
    
    #Setup and start a project run
    ph_config["start_url"]=url                                               #Set the "start_url" to the current URL
                                                                             #Start a project run using the ph_config and proj_token, return the data associated with the project run
    r = requests.post(f'https://www.parsehub.com/api/v2/projects/{proj_token}/run', data=ph_config)
    rjson = r.json()                                                         #Parse project run data into a dictionary
    run_token = rjson['run_token']                                           #Extract the run_token from the dictionary
                                                                                                            
    #Continue to check the status of the run until it either completes successfully or not, handle accordingly
    while True:
        run = requests.get(f'https://www.parsehub.com/api/v2/runs/{run_token}', params=ph_config)                    #Pull the run data at the moment using the ph_config and run_token
        run_json = run.json()                                                                                        #Parse the run data into a dictionary
        run_status = run_json['status']                                                                              #Extract the status of the run from the dictionary
        print(run_status)                                                                                            #DEBUG
        if (run_status == 'complete' or run_status == 'error'):                                                      #If the status is 'complete' or 'error'
            if (run_status == 'error'):                                                                              #If the status is 'error'
                if err_count == 1:                                                                                   #If the error count is 1
                    send_error(2, url, em_config)                                                                    #Call send_error with a code of 2 and the url
                    data_dict = {}                                                                                   #Create an empty dictionary to return
                else:                                                                                                #If the error count is less than 1
                    data_dict = run_proj(url, 1, ph_congfig, em_config)                                              #Try running the project again with an error count of 1 instead
            elif(run_status == 'complete'):                                                                          #If the status is 'complete'
                data_json =requests.get(f'https://www.parsehub.com/api/v2/runs/{run_token}/data', params=ph_config)  #Get the scraped data from the run using ph_config and run_token 
                if data_json == {}:                                                                                  #If data_json is an empty json
                    data_dict = {}                                                                                   #Set data_dict to an empty dictionary
                else:                                                                                                #Else
                    data_dict = data_json.json()                                                                     #Convert the returned JSON to a dictionary
            break                                                                                                    #Exit the loop
        time.sleep(60)                                                                                               #Else wait for 60 seconds before checking the status again
    return data_dict                                                                                                 #Return the scraped data in dictionary format

#CHECK_VALUES DEFINITION
def check_values(dict, config):
    """
    Checks that the parsehub project was able to successfully scrape particular product fields. If it was determined that a field is not being properly scraped the field is 
    added to the dictionary with the best possible value and an error message is sent to the developer.

    Parameters:
    dict (dictionary): A dictionary containing a "Product" list consisting of product dictionaries with various fields which may or may not have values.

    Returns:
    dict (dictionary): A dictionary containing a "Product" list consisting of product dictionaries 
    """
    
    #Flag Variabel Declarations
    name_desc_flag = 1                                                       #Flag indicating that the project is not scraping product names or descriptions
    price_flag = 1                                                           #Flag indicating that the project is not scraping product prices
    img_flag = 1                                                             #Flag indicating that the project is not scraping product image URLs
    url_flag = 1                                                             #Flag indicating that the project is not scraping product URLs

    #Iterate through dictionary to evaluate the presence and values of fields in each product
    for prod in dict["Product"]:                                             #For each product in the dictionary

        #Handle missing "Name" and "Description" fields
        if "Name" not in prod:                                               #If the Name is not in the product dictionary
            prod["Name"] = ""                                                #Add it to the dictionary with an empty string as the value
        if "Description" not in prod:                                        #If the Description is not in the product dictionary
            prod["Description"] = ""                                         #Add it to the dictionary with an empty string as the value
        if prod["Name"] == "" and prod["Description"] != "":               #If the product Name is not filled but the Description is filled
            prod["Name"] = prod.get("Description")                           #Fill the Name with the Description's value
        elif prod["Description"] == "" and prod["Name"] != "":               #If the product Description is not filled but the Name is filled
            prod["Description"] = prod.get("Name")                           #Fill the Description with the Name's value
        if prod["Name"] != "" and prod["Description"] != "":                 #If the product Name and Description are filled
            name_desc_flag = 0                                               #Change the name flag to indicate that the project is scraping product names

        #Handle missing "Price" field
        if "Price" not in prod:                                              #If the Price is not in the product dictionary (Not all products have prices on the web page)
            prod["Price"] = "Check store for price"                          #Add it to the dictionary with a value indicating to check the store page for the price
        if prod["Price"] != "Check store for price":                         #If the product Price is filled
            price_flag = 0                                                   #Change the price flag to indicate that the project is scraping product prices

        #Handle missing "Img_URL" field
        if "Img_URL" not in prod:                                            #If the Img_URL is not in the product dictionary
            prod["Img_URL"] = ""                                             #Set the Img_URL to the empty string
        if prod["Img_URL"] != "":                                            #If the product Img_URL is filled
            img_flag = 0                                                     #Change the img flag to indicate that the project is scraping image URLs

        #Handle missing "URL" field
        if "URL" not in prod:                                                #If the URL is not in the product dictionary
            prod["URL"] = ""                                                 #Set the URL to the empty string
        if prod["URL"] != "":                                                #If the URL is filled
            url_flag = 0                                                     #Change the url flag to indicate that the project is scraping URLs
            
    #Send error messages for all flags indicating that a field is not being scraped by the project
    if name_desc_flag == 1:                                                  #If the name flag still indicates that names are not being scraped
        send_error(3, "Name and Description", config)                        #Call send_error with a code of 3 and the field "Name"
    if price_flag == 1:                                                      #If the price flag still indicates that prices are not being scraped
        send_error(3, "Price", config)                                       #Call send_error with a code of 3 and the field "Price"
    if img_flag == 1:                                                        #If the img flag still indicates that image URLs are not being scraped
        send_error(3, "Img_URL", config)                                     #Call send_error with a code of 3 and the field "Img_URL"
    if url_flag == 1:                                                        #If the url flag still indicates that URLs are not being scraped
        send_error(3, "URL", config)                                         #Call send_error with a code of 3 and the field "URL" 
    
    return dict                                                              #Return the newly checked and filled dictionary

#FORMATTER DEFINITION
def formatter(dict):
    """
    Takes a dictionary's "Product" list, which consists of dictionaries of product data, and reorganizes the fields in each product dictionary in a desired format.

    Parameters:
    dict (dictionary): A dictionary containing a list called "Products" that consists of product dictionaries with unorganized fields.

    Returns:
    formated_list (list): A list of product dictionaries with organized fields.
    """
    #Create and fill a new list with the dictionaries of product data in the desired order
    formated_list = []                                                       #Create an empty list to fill with formatted product dictionaries
    for raw_prod in dict["Product"]:                                         #For each raw product dictionary in the dictionary's Product list
        prod = {                                                             #Create a new product dictionary with the fields in the following order:
            "URL": raw_prod.get("URL"),                                      #Product page URL
            "UPC": "placeholder_value",                                      #Default product UPC field
            "Name": raw_prod.get("Name"),                                    #Product name
            "Price": raw_prod.get("Price"),                                  #Product price
            "Category_ID": raw_prod.get("Category_ID"),                      #Product category
            "Sub_Category_ID": raw_prod.get("Sub_Category_ID"),              #Product subcategory
            "Description": raw_prod.get("Description"),                      #Product description (same value as name)
            "Keywords": [],                                                  #Empty list of product keywords
            "Img_URL": raw_prod.get("Img_URL")                               #Product image URL
        }
        formated_list.append(prod)                                           #Attach the new product dictionary to the end of the new list
    return formated_list                                                     #Return the new list of formatted product dictionaries

#RM_DUPLICATE DEFINITION
def rm_duplicate(list):
    """
    Removes any duplicate product dictionaries in the given list by comapring the name fields of each dictionary.

    Parameters:
    list (list): A list of dictionaries each containing the data for a single product, some dictionaries may be duplicates.

    Returns:
    filtered_list (list): A list of dictionaries each containing the data for a single unique product.
    """
    
    #Duplicate Removal Specific Variable Declaration
    seen_names = set()                                                       #Create a set to keep track of seen names
    filtered_list = []                                                       #Create a new list to store the filtered dictionaries

    #Iterate through the products of the list looking for and removing duplicate products
    for prod in list:                                                        #For each product in the list
        name = prod["Name"]                                                  #Retrieve the product name
        if name not in seen_names:                                           #If the name has not already been seen
            seen_names.add(name)                                             #Add the name to the set of seen names
            filtered_list.append(prod)                                       #Add the dictionary to the filtered list
    return filtered_list                                                     #Return the new list