import requests
import os
import pymysql
import configparser

# Read API key from a file
def read_key():
    key = "key"
    with open('api.env', 'r') as file:
        lines = file.readlines()
        for line in lines:
            if "RedCircle" in line:
                parts = line.split('" = "')
                if len(parts) == 2:
                    key = parts[1].replace('"', '').strip()
                    break
    return key


# Read database credentials from db_credentials.cnf
def read_db_params():
    config = configparser.ConfigParser()
    config.read('db_credentials.cnf')
    db_params = {
        'host': config['database']['host'],
        'user': config['database']['user'],
        'password': config['database']['password'],
        'db': config['database']['db'],
        'charset': 'utf8mb4',  # Use the appropriate charset for your database
        'cursorclass': pymysql.cursors.DictCursor
    }
    return db_params



# Function to handle API response and file writing
def handle_api_response(connection, search_term, response):
    data = response.json()  # Assuming the response is in JSON format
    products = data['Store']['Products']  # Assuming this is the path to the products in your response

    with connection.cursor() as cursor:
        for product in products:
            # Create an INSERT statement for each product
            insert_query = """
            INSERT INTO Product (UPC, Name, Category_ID, Sub_category_ID, Description, Keywords, Img_URL, Update_Count)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            upc = product.get('UPC', '')
            name = product.get('Name', '')
            category_id = product.get('Category_ID', '')
            sub_category_id = product.get('Sub_category_ID', '')
            description = product.get('Description', '')
            keywords = product.get('Keywords', '')
            img_url = product.get('Img_URL', '')
            update_count = product.get('Update_Count', 0)

            # Execute the INSERT statement
            cursor.execute(insert_query, (upc, name, category_id, sub_category_id, description, keywords, img_url, update_count))

    # Commit the transaction
    connection.commit()


# Define search terms
search_terms = [
    'Bedding', 'Linens', 'Room Decorations', 'Kitchen and Dining', 'Storage', 'Desk Supplies',
    'Office Supplies', 'Laptops', 'Electronics', 'Gaming', 'Smart Home', 'cables', 'mini fridge',
    'microwave', 'cookware', 'appliances', 'coffee makers', 'tea makers', 'cleaning supplies',
    'laundry', 'clothing', 'heating and cooling'
]


# Loop over each search term and make the API call
def main(search_terms):
    # Connect to the database
    db_params = read_db_params()
    connection = pymysql.connect(**db_params)

    for search_term in search_terms:
        # Set up the request parameters for each search term
        key = read_key()
        params = {
            'api_key': key,  # Assuming 'key' is your API key
            'search_term': search_term,
            'type': "search"
        }
    
        # Make the HTTP GET request to RedCircle API
        try:
            response = requests.get('https://api.redcircleapi.com/request', params=params)
            response.raise_for_status()  # Raise an HTTPError if the HTTP request returned an unsuccessful status code
            handle_api_response(connection, search_term, response)
        except requests.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as err:
            print(f"An error occurred: {err}")

    connection.close()
