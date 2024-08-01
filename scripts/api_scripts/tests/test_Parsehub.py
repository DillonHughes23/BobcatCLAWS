#IMPORTS
import pytest
import tempfile
import json
import os
from dotenv import dotenv_values
from unittest.mock import Mock, patch, mock_open, call
from pprint import pprint
from Parsehub import env_parser, url_creator, is_valid_url, run_proj, send_error, check_values, formatter, rm_duplicate, main

#FIXTURES AND MOCKS

#Get configs
@pytest.fixture
def config_data():
    env_values = dotenv_values("api.env")
    env_values = dict(env_values)                               #Read env_values into a dictionary of the same name
    projects = json.loads(env_values["projects"])               #A list of tuples each containing:
                                                                    #A project token to a project that scrapes a particular store
                                                                    #The related store's name
                                                                    #The string used in that store's URLs to represent a space in a search
                                                                    #A URL template that when contatenated with a search "term" will pull up a search results page
    ph_config = {                                               #The configurations needed to run any parsehub project
        "api_key":env_values["ParsehubAPI"],                        #The developer's API key
        "start_url":None                                        #The URL to start the scraping from, Default: None
    }
    em_config = {                                               #The configurations needed to send an error email to the developer
        "sender_email":env_values["sender_email"],              #The email address of the message sender
        "app_password":env_values["app_password"],              #The password to the email address of the message sender
        "receiver_email":env_values["receiver_email"]           #The email address of the message receiver
    }

    return ph_config, em_config, projects                       #Return the Parsehub configurations, email configurations, and project tuples 



#ENV_PARSER TESTS
#Open and return the env file to be parsed and tested
def env_data():                                         
    env_values = dotenv_values("api.env")
    return env_values
    

#Test that env_parser() is returning three variables and that each variable is the correct size 
def test_env_parser():
    #Run the env_parser to be tested
    data = env_data()
    results = env_parser(data)

    #Test1: Check that all env variables and fields within are present
    r_size = len(results)
    assert r_size == 3, f"env_parser() returned {r_size} results, expected 3."      

    #Test2: Check that the size of the parsehub configurations is 2
    ph_config = results[0]
    ph_size = len(ph_config)
    assert ph_size == 2, f"env_parser() returned {ph_size} fields in the Parsehub Config, expected 2."

    #Test3: Check that the size of the email configurations is 3
    em_config = results[1]
    em_size = len(em_config)
    assert em_size == 3, f"env_parser() returned {em_size} fields in the Email Config, expected 3."

    #Test4: Check that each tuple in projects is a size of 4
    projects = results[2]
    count = 0
    for proj in projects:
        proj_size = len(proj)
        assert proj_size == 4, f"Tuple {count} in projects has {proj_size} fields, expected 4."
        count += 1



#URL_CREATOR TESTS
#Create the variables needed to run the function
def url_creator_data():
    #Create a temporary file to hold search terms both with and without trailing spaces
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
        temp_file.write("Refrigerator\n")                                                 #Single word without trailing spaces
        temp_file.write("Coffee Maker\n")                                                 #Two words without trailing spaces
        temp_file.write("Television \n")                                                  #Single word with trailing spaces
        temp_file.write("Oven Timer \n")                                                  #Two words with trailing spaces
    temp_file_name = temp_file.name                                                     #Get file name
    
    #project tuples, project key and store name unnecessary for test, includes different space and url template strings
    projects = [["_", "_", "%20", "https://www.website.com/site/searchpage.st="],        
                ["_", "_", "+", "https://www.store.com/site/searchpage.st="]]
    
    return temp_file_name, projects, temp_file


#Test that url_creator() is returning the correct number of urls, and that it is replacing spaces in the search terms with the correct space string.
def test_url_creator():
    with patch('Parsehub.is_valid_url') as mock_is_valid_url, patch('Parsehub.send_error') as mock_send_error:
        mock_is_valid_url.return_value = True
        mock_send_error.return_value = None

        #variable declaration
        em_config = {}
        url_list = []
        temp_file_str, projects, temp_file = url_creator_data()
        
        #loop to create each url
        for proj in projects:
            urls = url_creator(em_config, temp_file_str, proj)
            url_list.extend(urls)

        #Test1: Check that 8 URLs have been created
        assert len(url_list) == 8, f"url_creator() returned {len(url_list)} urls, expected 8."

        #Test2: Check that each of the 8 urls are of the correct format
        assert url_list[0] == "https://www.website.com/site/searchpage.st=Refrigerator", f"url_creator() returned {url_list[0]}, expected https://www.website.com/site/searchpage.st=Refrigerator"
        assert url_list[1] == "https://www.website.com/site/searchpage.st=Coffee%20Maker", f"url_creator() returned {url_list[1]}, expected https://www.website.com/site/searchp0age.st=Coffee%20Maker"
        assert url_list[2] == "https://www.website.com/site/searchpage.st=Television", f"url_creator() returned {url_list[2]}, expected https://www.website.com/site/searchpage.st=Television"
        assert url_list[3] == "https://www.website.com/site/searchpage.st=Oven%20Timer", f"url_creator() returned {url_list[3]}, https://www.website.com/site/searchpage.st=Oven%20Timer"
        assert url_list[4] == "https://www.store.com/site/searchpage.st=Refrigerator", f"url_creator() returned {url_list[4]}, expected https://www.store.com/site/searchpage.st=Refrigerator"
        assert url_list[5] == "https://www.store.com/site/searchpage.st=Coffee+Maker", f"url_creator() returned {url_list[5]}, expected https://www.store.com/site/searchpage.st=Coffee+Maker"
        assert url_list[6] == "https://www.store.com/site/searchpage.st=Television", f"url_creator() returned {url_list[6]}, expected https://www.store.com/site/searchpage.st=Television"
        assert url_list[7] == "https://www.store.com/site/searchpage.st=Oven+Timer", f"url_creator() returned {url_list[7]}, expected https://www.store.com/site/searchpage.st=Oven+Timer"

        #Remove the temporary file
        os.remove(temp_file.name)



#IS_VALID_URL TESTS
#Test if is_valid_url() correctly identifies urls to pages that do and do not exist
def test_is_valid_url():
    #Test URLs
    valid_url = "https://www.google.com/"                                     #url to page that exists
    invalid_url = "https://www.store.com/invalid-url"                       #url to page that does not exist

    #Test1: Check that is_valid_url returns True for a valid URL
    result = is_valid_url(valid_url)                                         
    assert result == True, f"is_valid_url() returned {result} for a valid url, expected True."

    #Test2: Check that is_valid_url returns False for an invalid URL
    result = is_valid_url(invalid_url)
    assert result == False, f"is_valid_url() returned {result} for a invalid url, expected False."



#SEND_ERROR TESTS
#Test that send_error() calls all of the functions needed to send an email.
#Cannot test that error message was received without human intervention.
def test_send_error(config_data):
    with patch('smtplib.SMTP') as mock_smtp_class:
        # Configure the mock SMTP class
        mock_smtp_instance = mock_smtp_class.return_value

        #Get the email config data
        _, em_config, _ = config_data

        #Call the send_error() with a code, message, and config data
        send_error(1, "https://www.website.com/invalid-url", em_config)

        #Test that each function was called the correct amount of times (once each)
        assert mock_smtp_class.call_count == 1, f"SMTP class was not instantiated as expected."
        assert mock_smtp_instance.starttls.call_count == 1, f"starttls() was not called as expected."
        assert mock_smtp_instance.login.call_count == 1, f"login() was not called as expected."
        assert mock_smtp_instance.sendmail.call_count == 1, f"sendmail() was not called as expected."
        assert mock_smtp_instance.quit.call_count == 1, f"quit() was not called as expected."



#CHECK_VALUES TESTS
#Create the dictionaries that check_value will work on
def check_values_data():
    no_name = {"Product":[{"URL": "https://www.bestbuy.com/site/apple-magsafe-iphone-charger-white/6341029.p?skuId=6341029",
                 "UPC": "placeholder_value",
                 "Price": "$39.00",
                 "Category_ID": "placeholder_value",
                 "Sub_Category_ID": "placeholder_value",
                 "Description": "Apple - MagSafe iPhone Charger - White",
                 "Keywords": [],
                 "Img_URL": "https://pisces.bbystatic.com/image2/BestBuy_US/images/products/6341/6341029_sd.jpg;maxHeight=200;maxWidth=300"
                 }]}
    no_description = {"Product":[{"URL": "https://www.bestbuy.com/site/apple-magsafe-iphone-charger-white/6341029.p?skuId=6341029",
                 "UPC": "placeholder_value",
                 "Name": "Apple - MagSafe iPhone Charger - White",
                 "Price": "$39.00",
                 "Category_ID": "placeholder_value",
                 "Sub_Category_ID": "placeholder_value",
                 "Keywords": [],
                 "Img_URL": "https://pisces.bbystatic.com/image2/BestBuy_US/images/products/6341/6341029_sd.jpg;maxHeight=200;maxWidth=300"
                 }]}
    no_name_desc = {"Product":[{"URL": "https://www.bestbuy.com/site/apple-magsafe-iphone-charger-white/6341029.p?skuId=6341029",
                 "UPC": "placeholder_value",
                 "Price": "$39.00",
                 "Category_ID": "placeholder_value",
                 "Sub_Category_ID": "placeholder_value",
                 "Keywords": [],
                 "Img_URL": "https://pisces.bbystatic.com/image2/BestBuy_US/images/products/6341/6341029_sd.jpg;maxHeight=200;maxWidth=300"
                 }]}
    no_price = {"Product":[{"URL": "https://www.bestbuy.com/site/apple-magsafe-iphone-charger-white/6341029.p?skuId=6341029",
                 "UPC": "placeholder_value",
                 "Name": "Apple - MagSafe iPhone Charger - White",
                 "Category_ID": "placeholder_value",
                 "Sub_Category_ID": "placeholder_value",
                 "Description": "Apple - MagSafe iPhone Charger - White",
                 "Keywords": [],
                 "Img_URL": "https://pisces.bbystatic.com/image2/BestBuy_US/images/products/6341/6341029_sd.jpg;maxHeight=200;maxWidth=300"
                 }]}
    no_img = {"Product":[{"URL": "https://www.bestbuy.com/site/apple-magsafe-iphone-charger-white/6341029.p?skuId=6341029",
                 "UPC": "placeholder_value",
                 "Name": "Apple - MagSafe iPhone Charger - White",
                 "Price": "$39.00",
                 "Category_ID": "placeholder_value",
                 "Sub_Category_ID": "placeholder_value",
                 "Description": "Apple - MagSafe iPhone Charger - White",
                 "Keywords": [],
                 }]}
    no_url = {"Product":[{"UPC": "placeholder_value",
                "Name": "Apple - MagSafe iPhone Charger - White",
                "Price": "$39.00",
                "Category_ID": "placeholder_value",
                "Sub_Category_ID": "placeholder_value",
                "Description": "Apple - MagSafe iPhone Charger - White",
                "Keywords": [],
                "Img_URL": "https://pisces.bbystatic.com/image2/BestBuy_US/images/products/6341/6341029_sd.jpg;maxHeight=200;maxWidth=300"
              }]}

    return no_name, no_description, no_name_desc, no_price, no_img, no_url

#Test that check_values will either fill in the missing data correctly, send an error email or both
def test_check_values():
    with patch('Parsehub.send_error') as mock_send_error:
        #Mock send_error()
        mock_send_error.return_value = None

        #Get the lists of dictionaries data
        no_name, no_description, no_name_desc, no_price, no_img, no_url = check_values_data()

        config = {}
        
        #Test1: Check that the Name field was filled
        result = check_values(no_name, config)["Product"][0]
        assert "Name" in result, "check_values() returned a dictionary with no Name field."
        
        #Test2: Check that the Description field was filled
        result = check_values(no_description, config)["Product"][0]
        assert "Description" in result, "check_values() returned a dictionary with no Description field."

        #Test3: Check that the mock_send_error was called because neither Name or Description were properly scraped
        result = check_values(no_name_desc, config)
        assert mock_send_error.call_count == 1, "check_values() did not send an email when Name and Description were empty."
        mock_send_error.call_count = 0
        
        #Test4: Check that the Price field exists and that an email was sent because price data is not being scraped
        result = check_values(no_price, config)["Product"][0]
        assert "Price" in result, "check_values() returned a dictionary with no Price field."
        assert mock_send_error.call_count == 1, "check_values() did not send an email when Price was empty."
        mock_send_error.call_count = 0

        #Test5: Check that the Img_URL field exists and that an email was sent because Img_URL data is not being scraped
        result = check_values(no_img, config)["Product"][0]
        assert "Img_URL" in result, "check_values() returned a dictionary with no Img_URL field."
        assert mock_send_error.call_count == 1, "check_values() did not send an email when Img_URL was empty."
        mock_send_error.call_count = 0

        #Test6: Check that the URL field exists and that an email was sent because URL data is not being scraped
        result = check_values(no_url, config)["Product"][0]
        assert "URL" in result, "check_values() returned a dictionary with no URL field."
        assert mock_send_error.call_count == 1, "check_values() did not send an email when URL was empty."


#FORMATTER TESTS
#List of dictionary for formatter to work on
def formatter_data():
    correct = [{"URL": "https://www.bestbuy.com/site/apple-magsafe-iphone-charger-white/6341029.p?skuId=6341029",
                 "UPC": "placeholder_value",
                 "Name": "Apple - MagSafe iPhone Charger - White",
                 "Price": "$39.00",
                 "Category_ID": "placeholder_value",
                 "Sub_Category_ID": "placeholder_value",
                 "Description": "Apple - MagSafe iPhone Charger - White",
                 "Keywords": [],
                 "Img_URL": "https://pisces.bbystatic.com/image2/BestBuy_US/images/products/6341/6341029_sd.jpg;maxHeight=200;maxWidth=300"
                 }]
    in_order = {"Product":[{"URL": "https://www.bestbuy.com/site/apple-magsafe-iphone-charger-white/6341029.p?skuId=6341029",
                 "UPC": "placeholder_value",
                 "Name": "Apple - MagSafe iPhone Charger - White",
                 "Price": "$39.00",
                 "Category_ID": "placeholder_value",
                 "Sub_Category_ID": "placeholder_value",
                 "Description": "Apple - MagSafe iPhone Charger - White",
                 "Keywords": [],
                 "Img_URL": "https://pisces.bbystatic.com/image2/BestBuy_US/images/products/6341/6341029_sd.jpg;maxHeight=200;maxWidth=300"
                 }]}
    out_of_order = {"Product":[{"Img_URL": "https://pisces.bbystatic.com/image2/BestBuy_US/images/products/6341/6341029_sd.jpg;maxHeight=200;maxWidth=300",
                     "Name": "Apple - MagSafe iPhone Charger - White",
                     "Sub_Category_ID": "placeholder_value",
                     "URL": "https://www.bestbuy.com/site/apple-magsafe-iphone-charger-white/6341029.p?skuId=6341029",
                     "UPC": "placeholder_value",
                     "Keywords": [],
                     "Description": "Apple - MagSafe iPhone Charger - White",
                     "Price": "$39.00",
                     "Category_ID": "placeholder_value",
                     }]}
    missing_fields = {"Product":[{"UPC": "placeholder_value",
                       "Name": "Apple - MagSafe iPhone Charger - White",
                       "Category_ID": "placeholder_value",
                       "Sub_Category_ID": "placeholder_value",
                       "Img_URL": "https://pisces.bbystatic.com/image2/BestBuy_US/images/products/6341/6341029_sd.jpg;maxHeight=200;maxWidth=300"
                      }]}
    miss_out_of_order = {"Product":[{"Name": "Apple - MagSafe iPhone Charger - White",
                       "Category_ID": "placeholder_value",
                       "UPC": "placeholder_value",
                       "Img_URL": "https://pisces.bbystatic.com/image2/BestBuy_US/images/products/6341/6341029_sd.jpg;maxHeight=200;maxWidth=300",
                       "Sub_Category_ID": "placeholder_value"
                      }]}
    filled_fields = [{"URL": None,
                      "UPC": "placeholder_value",
                      "Name": "Apple - MagSafe iPhone Charger - White",
                      "Price": None,
                      "Category_ID": "placeholder_value",
                      "Sub_Category_ID": "placeholder_value",
                      "Description": None,
                      "Keywords": [],
                      "Img_URL": "https://pisces.bbystatic.com/image2/BestBuy_US/images/products/6341/6341029_sd.jpg;maxHeight=200;maxWidth=300"
                      }]
    return in_order, out_of_order, missing_fields, miss_out_of_order, filled_fields, correct

#Test that formatter is putting the fields in the correct order and filling in fields as necessary
def test_formatter():
    in_order, out_of_order, missing_fields, miss_out_of_order, filled_fields, correct = formatter_data()

    #Test1: Check that formatter returns an ordered dictionary when given an ordered dictionary
    result = formatter(in_order)
    assert result == correct, f"formatter() returned:\n{pprint(result)},\n expected:{pprint(correct)}."

    #Test2: Check that formatter returns an ordered dictionary when given a unordered dictionary
    result = formatter(out_of_order)
    assert result == correct, f"formatter() returned:\n{pprint(result)},\n expected:{pprint(correct)}."

    #Test3: Check that formatter returns an ordered dictionary with missing fields filled in when given a dictionary with missing fields
    result = formatter(missing_fields)
    assert result == filled_fields, f"formatter() returned:\n{pprint(result)},\n expected:{pprint(filled_fields)}."

    #Test4: Check that formatter returns an ordered dictionary with missing fields filled in when given an unordered dictionary with missing fields
    result = formatter(miss_out_of_order)
    assert result == filled_fields, f"formatter() returned:\n{pprint(result)},\n expected:{pprint(filled_fields)}."

#RM_DUPLICATE TESTS
#List of dictionaries for rm_duplicate to work on
def rm_duplicate_data():
    no_duplicates = [{"URL": "https://www.bestbuy.com/site/apple-magsafe-iphone-charger-white/6341029.p?skuId=6341029",
                      "UPC": "placeholder_value",
                      "Name": "Apple - MagSafe iPhone Charger - White",
                      "Price": "$39.00",
                      "Category_ID": "placeholder_value",
                      "Sub_Category_ID": "placeholder_value",
                      "Description": "Apple - MagSafe iPhone Charger - White",
                      "Keywords": [],
                      "Img_URL": "https://pisces.bbystatic.com/image2/BestBuy_US/images/products/6341/6341029_sd.jpg;maxHeight=200;maxWidth=300"
                     },
                     {"URL": "https://www.bestbuy.com/site/uag-monarch-pro-series-case-with-magsafe-for-apple-iphone-15-pro-carbon-fiber/6548413.p?skuId=6548413",
                      "UPC": "placeholder_value",
                      "Name": "UAG - Monarch Pro Series Case with Magsafe for Apple iPhone 15 Pro - Carbon Fiber",
                      "Price": "$79.95",
                      "Category_ID": "placeholder_value",
                      "Sub_Category_ID": "placeholder_value",
                      "Description": "UAG - Monarch Pro Series Case with Magsafe for Apple iPhone 15 Pro - Carbon Fiber",
                      "Keywords": [],
                      "Img_URL": "https://pisces.bbystatic.com/image2/BestBuy_US/images/products/6548/6548413_sd.jpg;maxHeight=200;maxWidth=300"  
                     },
                     {"URL": "https://www.bestbuy.com/site/smart-choice-5-8-safety-plus-stainless-steel-gas-range-connector/6684698.p?skuId=6684698",
                      "UPC": "placeholder_value",
                      "Name": "Smart Choice - 5/8'' Safety+PLUS Stainless-Steel Gas Range Connector",
                      "Price": "$39.99",
                      "Category_ID": "placeholder_value",
                      "Sub_Category_ID": "placeholder_value",
                      "Description": "Smart Choice - 5/8'' Safety+PLUS Stainless-Steel Gas Range Connector",
                      "Keywords": [],
                      "Img_URL": "https://pisces.bbystatic.com/image2/BestBuy_US/images/products/6684/6684698_sd.jpg;maxHeight=200;maxWidth=300"
                     }]
    all_duplicates = [{"URL": "https://www.bestbuy.com/site/apple-magsafe-iphone-charger-white/6341029.p?skuId=6341029",
                      "UPC": "placeholder_value",
                      "Name": "Apple - MagSafe iPhone Charger - White",
                      "Price": "$39.00",
                      "Category_ID": "placeholder_value",
                      "Sub_Category_ID": "placeholder_value",
                      "Description": "Apple - MagSafe iPhone Charger - White",
                      "Keywords": [],
                      "Img_URL": "https://pisces.bbystatic.com/image2/BestBuy_US/images/products/6341/6341029_sd.jpg;maxHeight=200;maxWidth=300"
                     },
                     {"URL": "https://www.bestbuy.com/site/uag-monarch-pro-series-case-with-magsafe-for-apple-iphone-15-pro-carbon-fiber/6548413.p?skuId=6548413",
                      "UPC": "placeholder_value",
                      "Name": "UAG - Monarch Pro Series Case with Magsafe for Apple iPhone 15 Pro - Carbon Fiber",
                      "Price": "$79.95",
                      "Category_ID": "placeholder_value",
                      "Sub_Category_ID": "placeholder_value",
                      "Description": "UAG - Monarch Pro Series Case with Magsafe for Apple iPhone 15 Pro - Carbon Fiber",
                      "Keywords": [],
                      "Img_URL": "https://pisces.bbystatic.com/image2/BestBuy_US/images/products/6548/6548413_sd.jpg;maxHeight=200;maxWidth=300"  
                     },
                     {"URL": "https://www.bestbuy.com/site/apple-magsafe-iphone-charger-white/6341029.p?skuId=6341029",
                      "UPC": "placeholder_value",
                      "Name": "Apple - MagSafe iPhone Charger - White",
                      "Price": "$39.00",
                      "Category_ID": "placeholder_value",
                      "Sub_Category_ID": "placeholder_value",
                      "Description": "Apple - MagSafe iPhone Charger - White",
                      "Keywords": [],
                      "Img_URL": "https://pisces.bbystatic.com/image2/BestBuy_US/images/products/6341/6341029_sd.jpg;maxHeight=200;maxWidth=300"
                     },
                     {"URL": "https://www.bestbuy.com/site/smart-choice-5-8-safety-plus-stainless-steel-gas-range-connector/6684698.p?skuId=6684698",
                      "UPC": "placeholder_value",
                      "Name": "Smart Choice - 5/8'' Safety+PLUS Stainless-Steel Gas Range Connector",
                      "Price": "$39.99",
                      "Category_ID": "placeholder_value",
                      "Sub_Category_ID": "placeholder_value",
                      "Description": "Smart Choice - 5/8'' Safety+PLUS Stainless-Steel Gas Range Connector",
                      "Keywords": [],
                      "Img_URL": "https://pisces.bbystatic.com/image2/BestBuy_US/images/products/6684/6684698_sd.jpg;maxHeight=200;maxWidth=300"
                     },
                     {"URL": "https://www.bestbuy.com/site/uag-monarch-pro-series-case-with-magsafe-for-apple-iphone-15-pro-carbon-fiber/6548413.p?skuId=6548413",
                      "UPC": "placeholder_value",
                      "Name": "UAG - Monarch Pro Series Case with Magsafe for Apple iPhone 15 Pro - Carbon Fiber",
                      "Price": "$79.95",
                      "Category_ID": "placeholder_value",
                      "Sub_Category_ID": "placeholder_value",
                      "Description": "UAG - Monarch Pro Series Case with Magsafe for Apple iPhone 15 Pro - Carbon Fiber",
                      "Keywords": [],
                      "Img_URL": "https://pisces.bbystatic.com/image2/BestBuy_US/images/products/6548/6548413_sd.jpg;maxHeight=200;maxWidth=300"  
                     },
                     {"URL": "https://www.bestbuy.com/site/smart-choice-5-8-safety-plus-stainless-steel-gas-range-connector/6684698.p?skuId=6684698",
                      "UPC": "placeholder_value",
                      "Name": "Smart Choice - 5/8'' Safety+PLUS Stainless-Steel Gas Range Connector",
                      "Price": "$39.99",
                      "Category_ID": "placeholder_value",
                      "Sub_Category_ID": "placeholder_value",
                      "Description": "Smart Choice - 5/8'' Safety+PLUS Stainless-Steel Gas Range Connector",
                      "Keywords": [],
                      "Img_URL": "https://pisces.bbystatic.com/image2/BestBuy_US/images/products/6684/6684698_sd.jpg;maxHeight=200;maxWidth=300"
                     }]
    some_duplicates = [{"URL": "https://www.bestbuy.com/site/apple-magsafe-iphone-charger-white/6341029.p?skuId=6341029",
                      "UPC": "placeholder_value",
                      "Name": "Apple - MagSafe iPhone Charger - White",
                      "Price": "$39.00",
                      "Category_ID": "placeholder_value",
                      "Sub_Category_ID": "placeholder_value",
                      "Description": "Apple - MagSafe iPhone Charger - White",
                      "Keywords": [],
                      "Img_URL": "https://pisces.bbystatic.com/image2/BestBuy_US/images/products/6341/6341029_sd.jpg;maxHeight=200;maxWidth=300"
                     },
                     {"URL": "https://www.bestbuy.com/site/apple-magsafe-iphone-charger-white/6341029.p?skuId=6341029",
                      "UPC": "placeholder_value",
                      "Name": "Apple - MagSafe iPhone Charger - White",
                      "Price": "$39.00",
                      "Category_ID": "placeholder_value",
                      "Sub_Category_ID": "placeholder_value",
                      "Description": "Apple - MagSafe iPhone Charger - White",
                      "Keywords": [],
                      "Img_URL": "https://pisces.bbystatic.com/image2/BestBuy_US/images/products/6341/6341029_sd.jpg;maxHeight=200;maxWidth=300"
                     },
                     {"URL": "https://www.bestbuy.com/site/uag-monarch-pro-series-case-with-magsafe-for-apple-iphone-15-pro-carbon-fiber/6548413.p?skuId=6548413",
                      "UPC": "placeholder_value",
                      "Name": "UAG - Monarch Pro Series Case with Magsafe for Apple iPhone 15 Pro - Carbon Fiber",
                      "Price": "$79.95",
                      "Category_ID": "placeholder_value",
                      "Sub_Category_ID": "placeholder_value",
                      "Description": "UAG - Monarch Pro Series Case with Magsafe for Apple iPhone 15 Pro - Carbon Fiber",
                      "Keywords": [],
                      "Img_URL": "https://pisces.bbystatic.com/image2/BestBuy_US/images/products/6548/6548413_sd.jpg;maxHeight=200;maxWidth=300"  
                     },
                     {"URL": "https://www.bestbuy.com/site/smart-choice-5-8-safety-plus-stainless-steel-gas-range-connector/6684698.p?skuId=6684698",
                      "UPC": "placeholder_value",
                      "Name": "Smart Choice - 5/8'' Safety+PLUS Stainless-Steel Gas Range Connector",
                      "Price": "$39.99",
                      "Category_ID": "placeholder_value",
                      "Sub_Category_ID": "placeholder_value",
                      "Description": "Smart Choice - 5/8'' Safety+PLUS Stainless-Steel Gas Range Connector",
                      "Keywords": [],
                      "Img_URL": "https://pisces.bbystatic.com/image2/BestBuy_US/images/products/6684/6684698_sd.jpg;maxHeight=200;maxWidth=300"
                     },
                     {"URL": "https://www.bestbuy.com/site/uag-monarch-pro-series-case-with-magsafe-for-apple-iphone-15-pro-carbon-fiber/6548413.p?skuId=6548413",
                     "UPC": "placeholder_value",
                     "Name": "UAG - Monarch Pro Series Case with Magsafe for Apple iPhone 15 Pro - Carbon Fiber",
                     "Price": "$79.95",
                     "Category_ID": "placeholder_value",
                     "Sub_Category_ID": "placeholder_value",
                     "Description": "UAG - Monarch Pro Series Case with Magsafe for Apple iPhone 15 Pro - Carbon Fiber",
                     "Keywords": [],
                     "Img_URL": "https://pisces.bbystatic.com/image2/BestBuy_US/images/products/6548/6548413_sd.jpg;maxHeight=200;maxWidth=300"  
                     }]
    return no_duplicates, all_duplicates, some_duplicates
                        
#Test that rm_duplicate is correctly removing duplicates dictionaries so that each dictionary is unique
def test_rm_duplicate():
    #Get the lists of dictionaries data
    no_duplicates, all_duplicates, some_duplicates = rm_duplicate_data()

    #Test1: Check that rm_duplicate returns a list with no duplicate dictionaries when given a list with no duplicate dictionaries
    result = rm_duplicate(no_duplicates)
    assert result == no_duplicates, f"no_duplicate() returned: {pprint(result)},\n expected {pprint(no_duplicates)}."

    #Test2: Check that rm_duplicate returns a list with no duplicate dictionaries when given a list where every dictionary has a duplicate
    result = rm_duplicate(all_duplicates)
    assert result == no_duplicates, f"no_duplicate() returned {pprint(result)},\n expected {pprint(no_duplicates)}."

    #Test3: Check that rm_duplicate returns a list with no duplicate dictionaries when given a list with some duplicate dictionaries
    result = rm_duplicate(some_duplicates)
    assert result == no_duplicates, f"no_duplicate() returned {pprint(result)},\n expected {pprint(no_duplicates)}."


    
#RUN_PROJECT TESTS
#Test the logic of run_proj() and that the correct output is being created every time
def test_run_proj(config_data):
    with patch('requests.get') as mock_requests_get,\
    patch('requests.Response.json') as mock_json,\
    patch('Parsehub.run_proj') as mock_run_proj,\
    patch('Parsehub.send_error') as mock_send_error,\
    patch('time.sleep'):
        mock_requests_get.return_value = Mock(status_code=200)
        mock_json.return_value = {'run_token': '123'}  # Replace with the desired JSON response
        mock_run_proj.return_value = {'key1': 'value1'}
        mock_send_error.return_value = True

        ph_config, em_config, _ = config_data
        
        #Test1: Check that the outcome where run_status == 'complete' and data_dict is not empty is correct
        mock_requests_get.side_effect = [
            Mock(status_code=200, json=lambda: {'status': 'running'}), 
            Mock(status_code=200, json=lambda: {'status': 'complete'}),
            Mock(status_code=200, json=lambda: {'key1': 'value1', 'key2': 'value2'})
        ]
        result1 = run_proj('www.url.com', 0, ph_config, em_config, 'abc')

        assert mock_json.call_count == 1, f"Test1: run_proj() called json() {mock_json.call_count} times, expected 1."
        assert mock_requests_get.call_count == 3, f"Test1: run_proj() called requests.get() {mock_requests_get.call_count} times, expected 3."
        assert result1 == {'key1': 'value1', 'key2': 'value2'}, f"Test1: run_proj() returned {result1} exepced {{'key1': 'value1', 'key2': 'value2'}}."

        mock_requests_get.call_count = 0
        mock_json.call_count = 0

        #Test2: Check that the outcome where run_status == 'complete' and data_dict is empty is correct
        mock_requests_get.side_effect = [
            Mock(status_code=200, json=lambda: {'status': 'running'}),
            Mock(status_code=200, json=lambda: {'status': 'complete'}),
            Mock(status_code=200, json=lambda: {})
        ]
        result2 = run_proj('www.url.com', 0, ph_config, em_config, 'abc')

        assert mock_json.call_count == 1, f"Test2: run_proj() called json() {mock_json.call_count} times, expected 1."
        assert mock_requests_get.call_count == 3, f"Test2: run_proj() called requests.get() {mock_requests_get.call_count} times, expected 3."
        assert result2 == {}, f"Test2: run_proj() returned {result2}, expected {{}}."

        mock_requests_get.call_count = 0
        mock_json.call_count = 0

        #Test3: Check that the outcome where run_status == 'error' and err_count == 0 is correct
        mock_requests_get.side_effect = [
            Mock(status_code=200, json=lambda: {'status': 'running'}),
            Mock(status_code=200, json=lambda: {'status': 'error'})
        ]
        result3 = run_proj('www.url.com', 0, ph_config, em_config, 'abc')

        assert mock_requests_get.call_count == 2, f"Test3: run_proj() called requests.get() {mock_requests_get.call_count} times, expected 2."
        assert mock_run_proj.call_count == 1, f"Test3: run_proj() called run_proj() {run_proj.call_count} times. expected 1."
        assert result3 == {'key1': 'value1'}, f"Test3: run_proj() returned {result3}, expected {{'key1': 'value1'}}."

        mock_requests_get.call_count = 0
        mock_run_proj.call_count = 0

        #Test4: Check that the outcome where run_status == 'error' and err_count == 1 is correct
        mock_requests_get.side_effect = [
            Mock(status_code=200, json=lambda: {'status': 'running'}),
            Mock(status_code=200, json=lambda: {'status': 'error'})
        ]
        result4 = run_proj('www.url.com', 1, ph_config, em_config, 'abc')
        
        assert mock_requests_get.call_count == 2, f"Test4: run_proj() called requests.get() {mock_requests_get.call_count} times, expected 2."
        assert mock_send_error.call_count == 1, f"Test4: run_proj() called send_error() {send_error.call_count} times, expected 1."
        assert result4 == {}, f"Test4 run_proj() returned {result4}, execpted {{}}."
        

#MAIN TESTS
#Test the logic of main() and that the correct output is being created every time
def test_main():
    with patch('Parsehub.dotenv_values') as mock_dotenv_values,\
    patch('Parsehub.env_parser') as mock_env_parser,\
    patch('Parsehub.url_creator') as mock_url_creator,\
    patch('Parsehub.run_proj') as mock_run_proj,\
    patch('Parsehub.check_values') as mock_check_values,\
    patch('Parsehub.formatter') as mock_formatter,\
    patch('Parsehub.rm_duplicate') as mock_rm_duplicate,\
    patch('Parsehub.open', mock_open()) as mock_open_func:
        
        
        #Test1: Check that the correct functions are called when projects is empty.
        mock_dotenv_values.return_value = {}
        mock_env_parser.return_value = ("v1", "v2", [])     #CAN'T PASS EMPTY LIST?
        mock_url_creator.return_value = []
        mock_run_proj.return_value = {}
        mock_check_values.return_value = {}
        mock_formatter.return_value = []
        mock_rm_duplicate.return_value = []

        main()

        assert mock_dotenv_values.call_count == 1, f"Test1: main() called dotenv_values {mock_dotenv_values.call_count} times, expected 1."
        assert mock_env_parser.call_count == 1, f"Test1: main() called env_parser {mock_env_parser.call_count} times, expected 1."
        assert mock_url_creator.call_count == 0, f"Test1: main() called url_creator {mock_url_creator.call_count} times, expected 0."
        assert mock_run_proj.call_count == 0, f"Test1: main() called run_proj {mock_run_proj.call_count} times, expected 0."
        assert mock_check_values.call_count == 0, f"Test1: main() called check_values {mock_check_values.call_count} times, expected 0."
        assert mock_formatter.call_count == 0, f"Test1: main() called formatter {mock_formatter.call_count} times, expected 0."
        assert mock_rm_duplicate.call_count == 0, f"Test1: main() called rm_duplicate {mock_rm_duplicate.call_count} times, expected 0."
        #assert mock_open_func.call_count == 0, f"Test1: main() called open {mock_open_func.call_count} times, expected 0."
        
        mock_dotenv_values.call_count = 0
        mock_env_parser.call_count = 0
        
        #Test2: Check that the correct functions are called and that final_dict is correct when projects is filled, and url_list is empty
        mock_env_parser.return_value = ("v1", "v2", [["abc", "store1"]])
        mock_url_creator.return_value = []

        main()

        assert mock_dotenv_values.call_count == 1, f"Test2: main() called dotenv_values {mock_dotenv_values.call_count} times, expected 1."
        assert mock_env_parser.call_count == 1, f"Test2: main() called env_parser {mock_env_parser.call_count} times, expected 1."
        assert mock_url_creator.call_count == 1, f"Test2: main() called url_creator {mock_url_creator.call_count} times, expected 1."
        assert mock_run_proj.call_count == 0, f"Test2: main() called run_proj {mock_run_proj.call_count} times, expected 0."
        assert mock_check_values.call_count == 0, f"Test2: main() called check_values {mock_check_values.call_count} times, expected 0."
        assert mock_formatter.call_count == 0, f"Test2: main() called formatter {mock_formatter.call_count} times, expected 0."
        assert mock_rm_duplicate.call_count == 1, f"Test2: main() called rm_duplicate {mock_rm_duplicate.call_count} times, expected 1."

        mock_open_func.assert_called_once_with("../json_files/store1.json", "w")

        expected_contents = '{\n    "Store": "store1",\n    "Products": []\n}'

        # Extract all the write calls made during the execution
        write_calls = mock_open_func().write.call_args_list

        # Concatenate all the writes into a single string
        actual_contents = ''.join(args[0] for args, _ in write_calls)
        
        # Assert that the actual content matches the expected content
        assert actual_contents == expected_contents
        
        mock_dotenv_values.call_count = 0
        mock_env_parser.call_count = 0
        mock_url_creator.call_count = 0
        mock_rm_duplicate.call_count = 0
        mock_open_func.call_count = 0
        mock_open_func().reset_mock()
        
        #Test3: Check that the correct functions are called and that final_dict is correct when projects and url_list are filled but raw_dict is empty
        mock_url_creator.return_value = ["url1"]

        main()
        
        assert mock_dotenv_values.call_count == 1, f"Test3: main() called dotenv_values {mock_dotenv_values.call_count} times, expected 1."
        assert mock_env_parser.call_count == 1, f"Test3: main() called env_parser {mock_env_parser.call_count} times, expected 1."
        assert mock_url_creator.call_count == 1, f"Test3: main() called url_creator {mock_url_creator.call_count} times, expected 1."
        assert mock_run_proj.call_count == 1, f"Test3: main() called run_proj {mock_run_proj.call_count} times, expected 1."
        assert mock_check_values.call_count == 0, f"Test3: main() called check_values {mock_check_values.call_count} times, expected 0."
        assert mock_formatter.call_count == 0, f"Test3: main() called formatter {mock_formatter.call_count} times, expected 0."
        assert mock_rm_duplicate.call_count == 1, f"Test3: main() called rm_duplicate {mock_rm_duplicate.call_count} times, expected 1."

        # Access the content written to the file without using write
        mock_file = mock_open_func()

        # Extract all the write calls made during the execution
        write_calls = mock_open_func().write.call_args_list

        # Concatenate all the writes into a single string
        actual_contents = ''.join(args[0] for args, _ in write_calls)
        
        # Assert that the actual content matches the expected content
        assert actual_contents == expected_contents
        
        mock_dotenv_values.call_count = 0
        mock_env_parser.call_count = 0
        mock_url_creator.call_count = 0
        mock_run_proj.call_count = 0
        mock_rm_duplicate.call_count = 0
        mock_open_func.call_count = 0
        mock_open_func.reset_mock()
        
        #Test4: Check that the correct functions are called and that final_dict is correct when projects, url_list, and raw_dict are filled
        mock_env_parser.return_value = ("v1", "v2", [["abc", "store1"], ["def", "store2"]])
        mock_url_creator.return_value = ["url1", "url2"]
        mock_run_proj.return_value = {'key', 'value'}
        mock_formatter.side_effect = [
            [{'key1': 'value1'}],
            [{'key2': 'value2'}],
            [{'key3': 'value3'}],
            [{'key4': 'value4'}]
        ]
        # Mock rm_duplicate to return the same list passed to it
        mock_rm_duplicate.side_effect = lambda x: x

        main()
        
        assert mock_dotenv_values.call_count == 1, f"Test4: main() called dotenv_values {mock_dotenv_values.call_count} times, expected 1."
        assert mock_env_parser.call_count == 1, f"Test4: main() called env_parser {mock_env_parser.call_count} times, expected 1."
        assert mock_url_creator.call_count == 2, f"Test4: main() called url_creator {mock_url_creator.call_count} times, expected 2."
        assert mock_run_proj.call_count == 4, f"Test4: main() called run_proj {mock_run_proj.call_count} times, expected 4."
        assert mock_check_values.call_count == 4, f"Test4: main() called check_values {mock_check_values.call_count} times, expected 4."
        assert mock_formatter.call_count == 4, f"Test4: main() called formatter {mock_formatter.call_count} times, expected 4."
        assert mock_rm_duplicate.call_count == 2, f"Test4: main() called rm_duplicate {mock_rm_duplicate.call_count} times, expected 1."

        mock_open_func.assert_has_calls([
            call("../json_files/store1.json", "w"),
            call("../json_files/store2.json", "w")
        ], any_order=True)

        expected_contents = '''{\n    "Store": "store1",\n    "Products": [\n        {\n            "key1": "value1"\n        },\n        {\n            "key2": "value2"\n        }\n    ]\n}{\n    "Store": "store2",\n    "Products": [\n        {\n            "key3": "value3"\n        },\n        {\n            "key4": "value4"\n        }\n    ]\n}'''

        # Access the content written to the file without using write
        mock_file = mock_open_func()

        # Extract all the write calls made during the execution
        write_calls = mock_open_func().write.call_args_list

        # Concatenate all the writes into a single string
        actual_contents = ''.join(args[0] for args, _ in write_calls)


        print(expected_contents)
        print(actual_contents)
        
        # Assert that the actual content matches the expected content
        assert actual_contents == expected_contents