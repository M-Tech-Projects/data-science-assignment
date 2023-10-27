import string

import requests
from bs4 import BeautifulSoup
import csv

class NatureBasketCrawler:
    ## Function definition to get main content data
    def get_main_page_contents(self, uri):
        response = requests.get(uri)
        html = response.content
        soup = BeautifulSoup(html, 'html.parser')

        itemMap = list()
        for h in soup.findAll('div', class_ = 'divSuperCategoryTitle'):
            if(h != None):
                head = h.get_text().lstrip('\n').rstrip('\n')
                ref = h.find('a')
                if(ref != None):
                    href = ref['href']
                    itemMap.append((head, href))

        return itemMap

    ## Function to get page wise data
    def get_page_data(self, uri):
        res = requests.get(url+uri).content
        soup = BeautifulSoup(res, 'html.parser')

        item_cost_list = list()
        for main_div in soup.findAll('div', class_='source_Class'):
            product = main_div.findAll('div', class_='pro-bucket')
            for p in product:
                item = p.find('a').find('img')['alt']
                item_cost = p.parent.find('span', class_='search_PSellingP').get_text()
                item_cost_list.append((item, item_cost))

        item_dict = dict((x, y) for x, y in item_cost_list)
        return item_dict

    ## Function to write data in file in csv format, data is in list(tuple) format
    def write_into_csv_file(self, item_name, data):
        fields = ['Item', 'Cost']
        fileName = item_name + '.csv'
        with open(fileName, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)

            writer.writerow(fields)
            for item in data:
                writer.writerow([item[0], item[1]])

        file.close()



## Sequential approach
# Define the URL of the webpage you want to scrape
url = 'https://www.kiranamarket.com/categories/coffee-tea-beverages?product_list_limit=36'  # Replace with the URL of the webpage you want to scrape

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
#print(soup.prettify())

divs = soup.find_all('div',class_ = 'product details product-item-details')
parsed_data = []
cleaned_data =[]
parsed_data1 = []
# Iterate through the div elements and add their contents to the array
for div in divs:
    # Use div.get_text() to get the text content inside the div
    parsed_data.append(div.get_text())
    # Replace '\n' with 'null' in the string
    cleaned_data = [s.replace('\n', ' ') for s in parsed_data]
#print(cleaned_data)

data = cleaned_data
parsed_data = []

for item in data:
    item_parts = item.split('\r')
    cleaned_parts = [part.strip() for part in item_parts if part.strip()]
    parsed_data.append(cleaned_parts)

# Printing the parsed data
#for item in parsed_data:
#print(item)

import re
import csv

# Define a regular expression pattern to match product name and price
pattern = r'^(.*?)\s+Rating:.*?₹([\d.]+)\s+Special Price  ₹([\d.]+)'

for item in cleaned_data:
    match = re.match(pattern, item)
    if match:
        product_name = match.group(1).strip()
        product_parts = product_name.split(',')
        if len(product_parts) == 2:
            product_name = product_parts[0].strip()
            weight = product_parts[1].strip()
        else:
            product_name = product_parts
            weight = "N/A"
        original_price = match.group(2)
        special_price = match.group(3)
        parsed_data1.append([product_name, weight, original_price, special_price])

# Specify the CSV file name
csv_file = 'Kiranamarket_data1.csv'

# Open the CSV file for writing
with open(csv_file, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)

    # Write the header row
    writer.writerow(['Product Name', 'Weight', 'Original Price', 'Special Price'])

    # Write the parsed data to the CSV file
    writer.writerows(parsed_data1)

print(f'Data has been saved to {csv_file}')
# print(len(item_cost_list))
# with open(fileName, 'w', newline='', encoding='utf-8') as file:
#     writer = csv.writer(file)
#
#     writer.writerow(fields)
#     for item in item_cost_list:
#         writer.writerow([item[0], item[1]])
#
#     file.close()