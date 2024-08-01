import requests
import json

# Set up the request parameters
params = {
    "api_key": "F416ED92D840422DBE072AAE919B95ED",
    "type": "search",
    "search_term": "fridge",
    "output": "json"
}

# Define the endpoint URL
url = "https://api.bluecartapi.com/request"

try:
    # Make the HTTP GET request to BlueCart API
    response = requests.get(url, params=params)

    # Ensure the request was successful
    response.raise_for_status()

    # Parse the JSON response
    raw_data = response.json()

    # Extract the search results
    search_results = raw_data.get("search_results", [])

    # Process each result and convert it to the desired format
    formatted_results = []
    for result in search_results:
        product_data = result.get("product", {})
        offer_data = result.get("offers", {}).get("primary", {})

        formatted_product = {
                "Product": {
                    "UPC": "placeholder_value",  # placeholder as UPC isn't available
                    "Name": product_data.get("title", ""),
                    "Price": str(offer_data.get("price", "")),
                    "Category_ID": "placeholder_value",  # placeholder as Category ID isn't available
                    "Sub_Category_ID": "placeholder_value",  # placeholder as Sub-Category ID isn't available
                    "Description": product_data.get("title", ""),  # Using title as description isn't available
                    "Keywords": [],  # placeholder as keywords aren't available
                    "Img_URL": product_data.get("main_image", "")
                }
        }
        formatted_results.append(formatted_product)

    # Write the processed data to a file
    with open("../json_files/bluecart_output.json", "w") as outfile:
        json.dump(formatted_results, outfile, indent=2)

    print("Data written to output.json")

except requests.exceptions.RequestException as error:
    print(f"Error occurred: {error}")

