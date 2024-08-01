import requests
import json
import pymysql
import configparser

# Read the API key from 'api.env'
def read_key():
    key = "key"
    with open('api.env', 'r') as file:
        lines = file.readlines()
        for line in lines:
            if "BlueCart" in line:
                parts = line.split('" = "')
                if len(parts) == 2:
                    key = parts[1].replace('"', '').strip()
                    break
    return key

# Read database credentials from a configuration file
def read_db_params():
    config = configparser.ConfigParser()
    config.read('db_credentials.cnf')
    db_params = {
        'host': config['database']['host'],
        'user': config['database']['user'],
        'password': config['database']['password'],
        'db': config['database']['db'],
        'charset': 'utf8mb4',
        'cursorclass': pymysql.cursors.DictCursor
    }
    return db_params


# Function to insert products into the database
def handle_api_response(connection, search_term, response):
    data = response.json() # Assuming the response is in JSON format
    products = data['Store']['Products'] if 'Store' in data and 'Products' in data['Store'] else [] # Assuming this is the path to the products
    
    with connection.cursor() as cursor:
        for product in products:
            # Define the INSERT statement
            insert_query = """
            INSERT INTO Product (UPC, Name, Category_ID, Sub_category_ID, Description, Keywords, Img_URL, Update_Count)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            # Retrieve product details, use None for any missing fields
            upc = product.get('UPC')
            name = product.get('Name')
            category_id = product.get('Category_ID')
            sub_category_id = product.get('Sub_category_ID')
            description = product.get('Description')
            keywords = product.get('Keywords')
            img_url = product.get('Img_URL')
            update_count = product.get('Update_Count')

            # Execute the INSERT statement, with NULLs for missing fields
            cursor.execute(insert_query, (upc, name, category_id, sub_category_id, description, keywords, img_url, update_count))

    # Commit the changes to the database
    connection.commit()

# Define an array of search terms
search_terms = [
    'Bedding', 'Linens', 'Room Decorations', 'Kitchen and Dining', 'Storage',
    'Desk Supplies', 'Office Supplies', 'Laptops', 'Electronics', 'Gaming',
    'Smart Home', 'cables', 'mini fridge', 'microwave', 'cookware', 'appliances',
    'coffee makers', 'tea makers', 'cleaning supplies', 'laundry', 'clothing',
    'heating and cooling'
]

def main(search_terms):
    # Connect to the database
    db_params = read_db_params()
    connection = pymysql.connect(**db_params)
    
    # Iterate over each search term, make the API call, and process the data
    for search_term in search_terms:
        key = read_key()
        params = {
            'api_key': key,
            'search_term': search_term,
            'type': "search",
            'output': "json"
        }
    
        try:
            response = requests.get('https://api.bluecartapi.com/request', params=params)
            response.raise_for_status()
            handle_api_response(connection, search_term, response)
        except requests.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as err:
            print(f"An error occurred: {err}")
    
    # Close the database connection
    connection.close()