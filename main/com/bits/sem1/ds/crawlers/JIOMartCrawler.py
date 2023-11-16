# Import the necessary libraries
import requests
from bs4 import BeautifulSoup

def soupproc2(url,parsed_data):
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
    title1 = soup.find_all('div',class_ = 'jm-col-4 jm-mt-base')
    catagory_title =[title.text.strip() for title in title1]
    #print(catagory_title)

    input_data = catagory_title
    #print(input_data)
    import pandas as pd

    # Initialize empty lists for each attribute
    product_names = []
    weights = []
    original_prices = []
    discounted_prices = []
    discount_percentages = []
    import re
    for product_string in input_data:
        pattern = re.compile(r'^(.*?)\s+(\d+\s*[gG])\s+₹(\d+\.\d{2})\s+₹(\d+\.\d{2})\s+(\d+)%\s+OFF\s+.*$')
        match = pattern.match(product_string)
        if match:
            product_name = match.group(1).strip()
            weight = match.group(2).strip()
            discounted_price = match.group(3).strip()
            original_price = match.group(4).strip()
            discount_percentage = match.group(5).strip()
            website = 'JIO Market'
            titlename = title[0:22]
            parsed_data.append([website, titlename, product_name, weight, original_price, discounted_price, discount_percentage])
    return(parsed_data)

urls = ['https://www.jiomart.com/c/groceries/snacks-branded-foods/biscuits-cookies/11',
        'https://www.jiomart.com/c/groceries/snacks-branded-foods/noodle-pasta-vermicelli/86',
        'https://www.jiomart.com/c/groceries/snacks-branded-foods/snacks-namkeen/43',
        'https://www.jiomart.com/c/groceries/snacks-branded-foods/chocolates-candies/70',
        'https://www.jiomart.com/c/groceries/snacks-branded-foods/breakfast-cereals/98',
        'https://www.jiomart.com/c/groceries/snacks-branded-foods/ready-to-cook-eat/53',
        'https://www.jiomart.com/c/groceries/dairy-bakery/bakery-snacks/281',
        'https://www.jiomart.com/c/groceries/dairy-bakery/toast-khari/102',
        'https://www.jiomart.com/c/groceries/dairy-bakery/cakes-muffins/125',
        'https://www.jiomart.com/c/groceries/dairy-bakery/breads-and-buns/267',
        'https://www.jiomart.com/c/groceries/beverages/tea/34',
        'https://www.jiomart.com/c/groceries/beverages/coffee/94',
        'https://www.jiomart.com/c/groceries/beverages/energy-soft-drinks/40',
        'https://www.jiomart.com/c/groceries/beverages/fruit-juices/96',
        'https://www.jiomart.com/c/groceries/beverages/soda-flavoured-water/115',
        'https://www.jiomart.com/c/groceries/beverages/health-drink-supplement/49',
        'https://www.jiomart.com/c/groceries/personal-care/skin-care/122',
        'https://www.jiomart.com/c/groceries/personal-care/hair-care/92',
        'https://www.jiomart.com/c/groceries/personal-care/oral-care/132',
        'https://www.jiomart.com/c/groceries/personal-care/bath-hand-wash/119',
        'https://www.jiomart.com/c/groceries/personal-care/body-wash-bathing-accessories/179',
        'https://www.jiomart.com/c/groceries/staples/atta-flours-sooji/26',
        'https://www.jiomart.com/c/groceries/staples/dals-pulses/17',
        'https://www.jiomart.com/c/groceries/staples/rice-rice-products/14',
        'https://www.jiomart.com/c/groceries/staples/salt-sugar-jaggery/23',
        'https://www.jiomart.com/c/groceries/staples/edible-oils/58',
        'https://www.jiomart.com/c/groceries/staples/dry-fruits-nuts/657',
        'https://www.jiomart.com/c/groceries/staples/ghee/12903',
        'https://www.jiomart.com/c/groceries/staples/masalas-spices/21',
        'https://www.jiomart.com/c/groceries/staples/combo-offer/1281',
        'https://www.jiomart.com/c/groceries/home-care/detergents/37']

import csv
# Specify the CSV file name
csv_file1 = 'C:\GitDev\M.Tech.Assignments\data-science-assignment\data\\raw\JIOMart_data1.csv'
# Open the CSV file for writing
with open(csv_file1, 'w', newline='', encoding='utf-8') as file:
    pass
parsed_data = []
for url in urls:
    soupproc2(url,parsed_data)

#print(parsed_data)
import csv
# Specify the CSV file name
csv_file = 'C:\GitDev\M.Tech.Assignments\data-science-assignment\data\\raw\JIOMart_data1.csv'
# Open the CSV file for writing
with open(csv_file, 'a', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Write the header row
    #writer.writerow(['Website','Product Catagory','Product Name', 'Weight', 'Original Price', 'Special Price'])
    writer.writerow(['Website','Product Catagory','Product Name', 'Weight', 'Original Price', 'Special Price','Discount'])
    # Write the parsed data to the CSV file
    writer.writerows(parsed_data)
    file.close()

#import csv
# Specify the CSV file name
#csv_file2 = 'C:/Users/sperumal/OneDrive - BMC Software, Inc/Personal/BITS Pilani Doc/1st Semester/Assignment/IDS/JIOMart_data1.csv'
#with open(csv_file2, mode='r') as file:
#    reader = csv.reader(file)
#    for row in reader:
#        print(row)