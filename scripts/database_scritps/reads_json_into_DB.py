import json
import mysql.connector

# Configuration for the MySQL connection
config = {
    'user': 'BobcatClawsDev',
    'password': 'CS#4398DB',
    'host': 'localhost',
    'database': 'BobcatClawsDB'
}

# Read the JSON file
with open('data.json', 'r') as file:
    data = json.load(file)

# Connect to the MySQL database
connection = mysql.connector.connect(**config)
cursor = connection.cursor()

# Check and insert into the Store table if not exists and get its ID
store_name = data['Store']
cursor.execute("SELECT ID FROM Store WHERE Name=%s", (store_name,))
result = cursor.fetchone()

if result:
    store_id = result[0]
else:
    cursor.execute("INSERT INTO Store (Name) VALUES (%s)", (store_name,))
    store_id = cursor.lastrowid

# Iterate over products
for product in data['Products']:
    # Check and insert into the Product table if UPC not exists
    cursor.execute("SELECT ID FROM Product WHERE UPC=%s", (product['UPC'],))
    result = cursor.fetchone()

    if result:
        product_id = result[0]
    else:
        cursor.execute("""
            INSERT INTO Product (UPC, Name, Category_ID, Sub_category_ID, Description, Keywords, Img_URL) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            product['UPC'], 
            product['Name'], 
            product['Category_ID'],
            product['Sub_Category_ID'],
            product['Description'],
            ','.join(product['Keywords']),
            product['Img_URL']
        ))
        
        product_id = cursor.lastrowid

    # Insert into the Product_Store_Price table
    cursor.execute("""
        INSERT INTO Product_Store_Price (Product_ID, Store_ID, Price, URL) 
        VALUES (%s, %s, %s, %s)
    """, (
        product_id, 
        store_id, 
        product['Price'], 
        product['Img_URL']
    ))

# Commit the transactions
connection.commit()

# Close the database connection
cursor.close()
connection.close()

