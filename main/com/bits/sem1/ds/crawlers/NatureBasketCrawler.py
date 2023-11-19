# Import the necessary libraries
import requests
from bs4 import BeautifulSoup

base_dir = 'C:\GitDev\M.Tech.Assignments\data-science-assignment\data\\raw\\'


def soupproc(url,parsed_data1):
    # Send an HTTP GET request to the URL
    response = requests.get(url)
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the webpage using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        # Example: Extract the title of the webpage
        title = soup.title.string
        print(f"Title of the webpage: {title}")
    else:
        print("Failed to retrieve the webpage. Status code:", response.status_code)


    def split_sentence(sentence):
        # Using the split() method to split the sentence into two halves
        halves = sentence.split('|')

        # Check if there are exactly two halves
        if len(halves) == 2:
            # Return the two halves
            return halves
        else:
            # If there are not exactly two halves, return an error message
            return "Error: The sentence does not contain exactly one '|' character."

    # Example usage:
    result = split_sentence(title)
    website1 = result[1].strip()
    catagory1 = result[0].strip()

    title1 = soup.find_all('div',class_ = 'divSuperCategoryTitle')
    catagory_title =[title.text.strip() for title in title1]
    #print(catagory_title)

    divs = soup.find_all('div',id = 'ctl00_ContentPlaceHolder1_divSearchData')
    parsed_data = []
    # Iterate through the div elements and add their contents to the array
    for div in divs:
        # Use div.get_text() to get the text content inside the div
        parsed_data.append(div.get_text())
    #print(parsed_data)

    data = parsed_data
    # Split the input into individual records by separating them based on "Add To Favourites"
    records = data[0].split('Add To Favourites')[1:]
    #print(records)

    # Initialize lists to store parsed data
    Online_Grocery_Site = []
    Product_Catagory =[]
    product_names = []
    netweight = []
    quantities = []
    mrps = []
    dmrps = []

    import re
    def split_product_info(line):
        # Remove leading and trailing whitespaces
        line = line.strip()

        # Initialize variables
        product = ""
        quantity = ""
        original_price = 0.0
        discounted_price = 0.0

        # Split the line based on whitespace
        parts = line.split()

        # Regular expression pattern to match quantity like "500Ml", "1L", etc.
        quantity_pattern = re.compile(r'\b(\d+(\.\d+)?)\s*([a-zA-Z]+)\b')

        # Iterate through parts to identify product, quantity, and price
        for part in parts:
            if part.startswith("MRP"):
                # Set the flag to assign the next '₹' to discounted price
                assign_to_discounted = True
            elif part.startswith("₹"):
                # Assign '₹' to either original or discounted price based on the flag
                if assign_to_discounted:
                    original_price = float(part[1:])
                    assign_to_discounted = False
                else:
                    discounted_price = float(part[1:])
            elif part == '1' and 'Pc' in parts:
                # Skip '1' when it is part of '1 Pc -0+'
                continue
            elif part == 'Pc' in parts:
                # Skip '1' when it is part of '1 Pc -0+'
                continue
            elif part == '-0+' in parts:
                # Skip '1' when it is part of '1 Pc -0+'
                continue
            else:
                # Check if the part matches the quantity pattern
                match = quantity_pattern.match(part)
                if match:
                    # Assign the matched quantity
                    quantity = match.group(0)
                    # Remove the quantity part from the product name
                    product += part[len(quantity):] + " "
                else:
                    # Assuming anything else is part of the product name
                    product += part + " "

        # Remove trailing whitespace from the product name
        product = product.strip()
        #print(discounted_price)
        if discounted_price == 0.0:
            discounted_price = original_price
        #print(discounted_price)
        return product, quantity, original_price, discounted_price

    # Display the result
    for line in records:
        result = split_product_info(line)
        if result:
            website = website1
            catagory = catagory1
            product_name = result[0]
            weight = result[1]
            mrp = result[2]
            dmrp = result[3]
            Online_Grocery_Site.append(website)
            Product_Catagory.append(catagory)
            product_names.append(product_name)
            netweight.append(weight)
            mrps.append(mrp)
            dmrps.append(dmrp)

    import csv

    # Specify the CSV file name
    csv_file = base_dir + 'Naturebasket_data1.csv'

    # Open the CSV file for writing
    with open(csv_file, 'a', newline='',encoding='utf-8') as file:
        writer = csv.writer(file)

        # Write the data to the CSV file
        for i in range(len(product_names)):
            writer.writerow([Online_Grocery_Site[i],Product_Catagory[i],product_names[i], netweight[i], mrps[i],dmrps[i]])
    print(f'Data has been saved to {csv_file}')
    #print(parsed_data1)
    return(parsed_data1)

# Get sub urls from main page
base_url = 'https://www.naturesbasket.co.in'
def get_main_page_contents(uri):
    response = requests.get(uri)
    html = response.content
    soup = BeautifulSoup(html, 'html.parser')

    url_list = list()
    for h in soup.findAll('div', class_ = 'divSuperCategoryTitle'):
        if(h != None):
            ref = h.find('a')
            if(ref != None):
                href = ref['href']
                url_list.append(uri + href)

    return url_list

# Define the URL of the webpage you want to scrape
urls = get_main_page_contents(base_url)


import csv
# Specify the CSV file name
csv_file = base_dir + 'Naturebasket_data1.csv'
# Open the CSV file for writing
with open(csv_file, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Write the header row
    writer.writerow(['Online_Grocery_Site','Product_Catagory','Product_Name', 'Quantity', 'Original_Price', 'Discounted_Price'])
parsed_data1 = []
for url in urls:
    soupproc(url,parsed_data1)