import cohere 
from getpass import getpass
from mysql.connector import connect, Error
import mysql.connector



# Initialize the key variable as None
key = None

# Open the file "db.env" for reading
with open("db.env", "r") as file:
    # Read the file line by line
    for line in file:
        # Check if the line contains "cohere"
        if "cohere" in line:
            # Assuming the line has a key-value format like "key=value"
            # You can split the line to extract the key
            parts = line.strip().split('" = "')
            if len(parts) == 2:
                key = parts[1]
                key = key.strip('"')
            break  # Stop searching after the first occurrence

# Print the extracted key (or None if not found)
co = cohere.Client(key)
del line

claws = mysql.connector.connect(
        host='localhost',
        user='root',
        database='BobcatClawsDB'
)


db_query = "SELECT * FROM Product WHERE Keywords LIKE '%[]%'  ;"
cursor = claws.cursor();
list = []



cursor.execute(db_query)
results = cursor.fetchall()

print(len(results))




for item in results:
    print(item[0])
    words = []
    response = co.generate(
        prompt = "Generate 5 single words that can be used as search terms for a product with the following description: " + item[2] + ". Make sure you index them by number",
        max_tokens=100
    )
    lines = response.generations[0].text.split("\n")
    for line in lines:
        word = line[3:]
        words.append(word)
    
    entry = ""
    for word in words:
        entry += word
        entry += " "

    
    query = "UPDATE Product SET Keywords =\"%s\" WHERE ID = %d" %(entry, item[0])
    try:
        cursor.execute(query)
        claws.commit()
        print(cursor.rowcount, "record(s) affected")
    except Error as e:
        print(e)
        continue
                    


