import mysql.connector

#Database Config
db_config = {
    "host": "localhost",
    "user": 'BobcatClawsDev',
    "password": 'CS#4398DB',
    "database": 'BobcatClawsDB'
}
# Connect to the MySQL database
connection = mysql.connector.connect(**db_config)
cursor = connection.cursor()

# Query to fetch names from the first table
category_query = "SELECT Name FROM Category"
cursor.execute(category_query)
category_names = cursor.fetchall()

# Query to fetch names from the second table
Subcategory_query = "SELECT Name FROM Sub_category"
cursor.execute(Subcategory_query)
subcategory_names = cursor.fetchall()

# Combine the names from both tables
all_names = category_names + subcategory_names

# Write names to a txt file
with open("../api_scripts/searchTerms.txt", "w") as f:
    for name in all_names:
        f.write(name[0] + "\n")

# Close the database connection
cursor.close()
connection.close()

print("Names from both tables have been written to searchTerms.txt!")

