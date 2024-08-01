const axios = require('axios');
const fs = require('fs');

// set up the request parameters
const params = {
	api_key: "9EE834DD409E48C08B3DEC5859DF7BFD",
	search_term: "laptop",
	type: "search",
	output: "json"
}
console.log('HERE!');
// make the http GET request to BlueCart API
axios.get('https://api.bluecartapi.com/request', { params })
.then(response => {

    // print the JSON response from BlueCart APiI
    //var finaldata = JSON.stringify(response.data, 0, 2);
    fs.writeFile(params.search_term + ".json", JSON.stringify(response.data,0,2) , function (err, file) {
        if (err) console.log(err);

    });




    //console.log(JSON.stringify(response.data, 0, 2));


  }).catch(error => {
// catch and print the error
	console.log(error);
});
