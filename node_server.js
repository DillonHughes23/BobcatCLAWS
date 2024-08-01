const express = require('express');
const mysql = require('mysql2/promise');
const cors = require('cors');
const https = require('https');
const fs = require('fs');

const app = express();
const serverPort = 3010;
app.use(cors()); // Enable CORS for all requests if your front-end is on a different origin

const pool = mysql.createPool({
  host: 'localhost',
  user: 'root',
  password: 'baddog01',
  database: 'BobcatClawsDB',
  port: 3306,
  waitForConnections: true,
  connectionLimit: 10,
  queueLimit: 0
});

// API endpoint to get items by subcategory ID and stored procedure name
app.get('/api/:procedure/:proc_param/', async (req, res) => {
  let catId = req.params.proc_param; // Parse the ID to an integer
  let procedureName = req.params.procedure; // Get the procedure name from the request

  try {
    // Using a prepared statement to safely call the specified stored procedure
    const query = `CALL ${mysql.escapeId(procedureName)}(?)`;
    const [results] = await pool.query(query, [catId]);
    // Sending the results to the client
    res.json(results[0]);
  } catch (error) {
    // Handle any errors during the database connection or query execution
    console.error('Error during database query:', error.message);
    res.status(500).send('Internal Server Error: ' + error.message);
  }
});
/*
const certificate = fs.readFileSync('/etc/nginx/ssl/certificates.crt','utf8');
const privateKey = fs.readFileSync('/etc/nginx/ssl/server.key','utf8');
const httpsOptions = {
	key : privateKey,
	cert: certificate
};
*/
// Start the Express server on the specified port
app.listen(serverPort, () => {
  console.log(`Server is running on port ${serverPort}`);
});

