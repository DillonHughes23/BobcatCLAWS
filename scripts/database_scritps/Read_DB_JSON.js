const mysql = require('mysql2');
const fs = require('fs');

// Database connection parameters
const connection = mysql.createConnection({
  host: 'localhost',
  user: 'BobcatClawsDev',
  password: 'CS#4398DB',
  database: 'BobcatClawsDB'
});

// Connect to the database
connection.connect((err) => {
  if (err) {
    console.error('Database connection error:', err);
    throw err;
  }
  console.log('Connected to the database');

  // SQL query to fetch data from Product and Product_Store_Price tables
  const query = `
  SELECT
    s.Name AS Store_Name,
    p.Img_URL,
    p.Name AS Product_Name,
    ps.Price AS Product_Price,
    ps.URL,
    p.Category_ID,
    p.Sub_Category_ID,
    p.Description,
    p.Keywords
  FROM Store s
  INNER JOIN Product_Store_Price ps ON s.ID = ps.Store_ID
  INNER JOIN Product p ON ps.Product_ID = p.ID;
  `;

  // Execute the query
  connection.query(query, (err, results) => {
    if (err) {
      console.error('Error executing SQL query:', err);
      throw err;
    }

    // Organize the data into the desired JSON structure
    const jsonData = {};

    results.forEach((row) => {
      const storeName = row.Store_Name;
      if (!jsonData[storeName]) {
        jsonData[storeName] = {
          Name: storeName,
          Product: []
        };
      }

      jsonData[storeName].Product.push({
        Img_URL: row.Img_URL,
        URL: row.URL,
        Name: row.Product_Name,
        Price: row.Product_Price,
        Category_ID: row.Category_ID,
        Sub_Category_ID: row.Sub_Category_ID,
        Keywords: row.Keywords,
        Description: row.Description
      });
    });

    // Convert the results to JSON
    const jsonText = JSON.stringify(jsonData, null, 2);

    // Save the JSON data to a file
    let file_name = 'DB_Data.json';
    fs.writeFile(file_name, jsonText, (err) => {
      if (err) {
        console.error('Error writing JSON to file:', err);
        throw err;
      }
      console.log(`JSON data saved to ${file_name}`);
    });

    // Close the database connection
    connection.end();
  });
});
