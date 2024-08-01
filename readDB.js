const mysql = require('mysql2');
const bodyParser = require('body-parser');
const cors = require('cors');

app.use(cors());
app.use(bng odyParser.json());

const db = mysql.createConnection({
  host: 'localhost',
  user: 'dah249',
  password: 'baddog01',
  database: 'BobcatClawsDB'
});

app.get('/api/table', (req, res) => {
  db.query('SELECT * FROM Product', (err, results) => {
    if (err) throw err;
    res.json(results);
  });
});
