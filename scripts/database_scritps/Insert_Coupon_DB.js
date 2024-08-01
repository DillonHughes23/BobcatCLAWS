const fs = require('fs');
const mysql = require('mysql2');

// Create a MySQL database connection
const connection = mysql.createConnection({
    host: 'localhost',
    user: 'BobcatClawsDev',
    password: 'CS#4398DB',
    database: 'BobcatClawsDB'
});

// Connect to the MySQL database
connection.connect((err) => {
    if (err) {
        console.error('Error connecting to MySQL:', err);
        return;
    }
    console.log('Connected to MySQL database');
});

// Read the JSON file
fs.readFile('coupon_template.json', 'utf8', (err, data) => {
    if (err) {
        console.error('Error reading the JSON file:', err);
        return;
    }
    // Parse the JSON data
    try {
        const dataArray = JSON.parse(data);

        // Function to check if a store exists
        function checkIfStoreExists(storeName, callback) {
            const checkStoreStatement = `
                SELECT ID FROM Store WHERE Name = ?
            `;

            connection.query(checkStoreStatement, [storeName], (err, results) => {
                if (err) {
                    console.error('Error checking if the store exists:', err);
                    callback(err, null);
                } else {
                    if (results[0]) {
                    callback(null, results[0].ID);
                    }
                    else {
                        callback(null, null)
                    }
                }
            });
        }

        // Function to check if a product exists
        function checkIfProductExists(productName, callback) {
            const checkProductStatement = `
                SELECT ID FROM Product WHERE Name = ?
            `;

            connection.query(checkProductStatement, [productName], (err, results) => {
                if (err) {
                    console.error('Error checking if the product exists:', err);
                    callback(err, null);
                } else {
                    if (results[0]) {
                    callback(null, results[0].ID);
                    }
                    else {
                        callback(null, null)
                    }
                }
            });
        }

        function getNewInsertedID(URL, callback) {
            const lookforID = `
            SELECT ID FROM Coupon WHERE URL = ?
            `;
            connection.query(lookforID, [URL], (err, results) => {
                if (err) {
                    console.error('Error checking if the product exists:', err);
                    callback(err, null);
                } else {
                    if (results[0]) {
                    callback(null, results[0].ID);
                    }
                    else {
                        callback(null, null)
                    }
                }
            });
        }

        const store = dataArray.Store;

            // Check if the store exists
            checkIfStoreExists(store.Name, (err, storeExists) => {
                if (err) {
                    return; // Handle the error as needed
                }
                if (storeExists != null) {
    
                const coupons = store.Coupon;
                coupons.forEach(coupon => {
                    const insertCoupon = `
                        INSERT INTO Coupon (URL, Start_Date, End_Date, Description)
                        VALUES (?, ?, ?, ?)
                    `;

                    connection.query(insertCoupon, [coupon.URL, coupon.Start_Date, coupon.End_Date, coupon.description], (err, couponresults) => {
                        if (err) {
                            console.error('Error inserting coupon data:', err);
                        } else {
                            console.log(`Coupon data inserted successfully with ID: ${couponresults.insertId}`);
                        }
                    });
                    
                    getNewInsertedID(coupon.URL, (err, couponID) => {
                        if (couponID == null){
                            console.log('Did not find ID');
                        }
                        else {
                            checkIfProductExists(coupon.Product_Name, (err, productExists) => {
                                if (err) {
                                    return; 
                                }
                                if (productExists != null) {
                                    const insertCoupon_Product = `
                                        INSERT INTO Product_Coupon (Product_ID, Coupon_ID)
                                        VALUES (?, ?)
                                    `;
                                    connection.query(insertCoupon_Product, [productExists, couponID], (err, Coupon_Prod) => {
                                        if (err) {
                                            console.error('Error inserting product data:', err);
                                        } else {
                                            console.log(`Coupon product data inserted successfully with ID: ${Coupon_Prod.insertId}`);
                                        }
                                    });
                                }     
                            });


                            const insertCoupon_Store = `
                                INSERT INTO Store_Coupon (Store_ID, Coupon_ID)
                                VALUES (?, ?)
                            `;
                            connection.query(insertCoupon_Store, [storeExists, couponID], (err, Coupon_Prod) => {
                                if (err) {
                                    console.error('Error inserting store data:', err);
                                } else {
                                    console.log(`Coupon Store data inserted successfully with ID: ${Coupon_Prod.insertId}`);
                                }
                            });
                        }


                    });
                });
            }
                else {
                    console.log(`Store with name '${store.Name}' is not on the databases`);
                }
        });
    } catch (parseError) {
        console.error('Error parsing JSON:', parseError);
    }
});