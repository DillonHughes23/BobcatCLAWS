const fs = require('fs');
const mysql = require('mysql');
const path = require('path');

// Database configuration
const dbConfig = {
  host: 'localhost',
  user: 'root',
  password: '',
  database: 'BobcatClawsDB',
};


const dir = 'json_files';
const dirOld = 'json_files/old';


//function parseNewFile(filepath){

        // Read the JSON file
        fs.readFile('laptop_final.json', 'utf8', (err, data) => {
          if (err) {
            console.error('Error reading the file: ' + err);
            return;
          }
	console.log("File Read");




          try {
            const jsonData = JSON.parse(data);
	console.log("Creating Database Connection");
            // Create a MySQL database connection
            const connection = mysql.createConnection(dbConfig);
	console.log("Connecting....");
            // Connect to the database
            connection.connect((err) => {
              if (err) {
                console.error('Error connecting to the database: ' + err.stack);
                return;
              }
              console.log('Connected to the database as ID ' + connection.threadId);



/**
              // Insert JSON data into the database
              jsonData.forEach((item) => {
                const sql = 'INSERT INTO peopletable (name, age) VALUES (?, ?)';
                const values = [item.name, item.age];

                connection.query(sql, values, (err, result) => {
                  if (err) {
                    console.error('Error inserting data: ' + err.message);
                  } else {
                    console.log('Inserted row ID: ' + result.insertId);
                  }
                });
              });
**/



		console.log(jsonData.search_results[0]);
		for ( i = 0; i < jsonData.search_results.length; i++){
			upc = jsonData.search_results[i].product.item_id;
		
			name  = jsonData.search_results[i].product.title;
			desc  = jsonData.search_results[i].product.title;
		
			img_url  = jsonData.search_results[i].product.images[0];
			console.log(img_url);
		/**
			id = jsonData.search_results[i]
			id = jsonData.search_results[i]
			id = jsonData.search_results[i]
			id = jsonData.search_results[i]
			id = jsonData.search_results[i]
			id = jsonData.search_results[i]
			id = jsonData.search_results[i]
		**/

		}
//		jsonData.search_results.forEach();
              // Close the database connectioni
              connection.end((err) => {
                if (err) {
                  console.error('Error closing the database connection: ' + err.message);
                } else {
                  console.log('Database connection closed.');
                }
              });
            });
          } catch (error) {
            console.error('Error parsing JSON: ' + error);
          }
        });
/**
        const fileName = path.basename(filepath);
 const newFilePath = path.join(dirOld, fileName);

        fs.rename(filepath, newFilePath, (err) => {
                if (err) {
                        console.log('Error moving file: ' + err);
                } else {
                        console.log('File moved to: ${newFilePath}');
                }


        });
//}
**/
/**
//watch new directory for JSON files
fs.watch(dir, (eventType, fileName) => {
        if (eventType == 'rename' && path.extname(fileName) === '.json'){
                const filePath = path.join(dir, fileName);
                parseNewFile(filePath);

        }






});
**/

