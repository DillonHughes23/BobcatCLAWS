const mysql = require('mysql2/promise');

const pool = mysql.createPool({
  host: 'localhost',
  user: 'BobcatClawsDev',
  password: 'CS#4398DB',
  database: 'BobcatClawsDB',
  waitForConnections: true,
  connectionLimit: 1,
  queueLimit: 0
});

// Select which subcategory to pull from (see cats_subcats.txt for IDs)
let cat_id = 4;
pool.query(`CALL Get_20_by_subcat(${cat_id})`)
  .then(([results]) => {
    console.log('Results: ', results[0]);
    
  })
  .catch(error => {
    console.error('Database connection failed:', error);
  });
