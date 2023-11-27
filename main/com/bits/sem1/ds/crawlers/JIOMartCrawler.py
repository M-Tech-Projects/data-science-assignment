# Import the necessary libraries
import calendar
import re
import time
from datetime import date

import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

base_url = 'https://www.jiomart.com'

def make_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.page_load_strategy = 'none'
    web_driver = webdriver.Chrome(options)
    web_driver.implicitly_wait(5)

    return web_driver


def get_sub_urls_for_jiomart(driver):
    urls = list()
    driver.get(base_url)
    time.sleep(10)

    content = driver.find_element(By.CSS_SELECTOR, 'div[class*=\'header-nav-container\'')
    uls = content.find_elements(By.CSS_SELECTOR, 'ul[class*=\'header-nav-l1 custom-scrollbar\']')
    lis = uls[0].find_elements(By.CSS_SELECTOR, 'li[class*=\'header-nav-l1-item\']')
    for li in lis:
        a = li.find_element(By.CSS_SELECTOR, 'a[class*=\'header-nav-l1-item-link\']')
        link = a.get_attribute('href')
        # print(f'Link = {link}')
        urls.append(link)

    return urls


def extract_weight_and_unit(raw_weight):
    rw_arr = add_space_in_weight_unit(raw_weight).split()
    weight = float(rw_arr[0])
    unit = rationalize_unit(rw_arr[1])

    return (weight, unit)


def rationalize_unit(raw_unit):
    unit = ''
    match raw_unit.lower():
        case 'g':
            unit = 'gm'
        case 'gm':
            unit = 'gm'
        case 'l':
            unit = 'Litre'
        case 'ltr':
            unit = 'Litre'
        case 'litre':
            unit = 'Litre'
        case 'ml':
            unit = 'ml'
        case 'kg':
            unit = 'Kg'
        case 'pc':
            unit = 'Pc/Box'
        case _:
            unit = 'Pc/Box'

    return unit


def add_space_in_weight_unit(raw_weight):
    if (len(raw_weight.split()) < 2):
        nums = re.findall(r'\d+', raw_weight)
        num = '.'.join(nums)
        unit = raw_weight.replace(f'{num}', '')
        weight = [num, unit]
        wt = ' '.join(weight)
        return wt
    else:
        return raw_weight


def soupproc2(url, parsed_data):
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
    # print(soup.prettify())
    title1 = soup.find_all('div', class_='jm-col-4 jm-mt-base')
    catagory_title = [title.text.strip() for title in title1]
    # print(catagory_title)

    input_data = catagory_title
    # print(input_data)

    # Initialize empty lists for each attribute
    product_names = []
    weights = []
    original_prices = []
    # discounted_prices = []
    discount_percentages = []
    import re
    day = calendar.day_name[date.today().weekday()]
    for product_string in input_data:
        pattern = re.compile(r'^(.*?)\s+(\d+\s*[gG])\s+₹(\d+\.\d{2})\s+₹(\d+\.\d{2})\s+(\d+)%\s+OFF\s+.*$')
        match = pattern.match(product_string)
        if match:
            product_name = match.group(1).strip()
            raw_weight = match.group(2).strip()
            qty = extract_weight_and_unit(raw_weight)
            weight = qty[0]
            unit = rationalize_unit(qty[1])
            discounted_price = match.group(3).strip()
            discounted_price = float(discounted_price)
            original_price = match.group(4).strip()
            original_price = float(original_price)
            discount_percentage = match.group(5).strip()
            website = 'jiomart.com'
            titlename = title[0:22]
            json = {
                'Online_Grocery_Site': website,
                'Product_Catagory': titlename,
                'Product_Name': product_name,
                'Weight': weight,
                'Unit': unit,
                'DayOfDeal': day,
                'Original_Price': original_price,
                'Discounted_Price': discounted_price,
                'Discount %': discount_percentage
            }
            print(json)
            # parsed_data.append([website, titlename, product_name, weight, unit, day, original_price, discounted_price, discount_percentage])
            parsed_data.append(json)
    return (parsed_data)


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

# Specify the CSV file name
csv_file1 = 'C:\GitDev\M.Tech.Assignments\data-science-assignment\data\\raw\JIOMart_data3.csv'
# Open the CSV file for writing
# with open(csv_file1, 'w', newline='', encoding='utf-8') as file:
#     pass
parsed_data = []
jio_urls = get_sub_urls_for_jiomart(make_driver())
# for url in urls:
print(jio_urls)
for url in jio_urls:
    soupproc2(url, parsed_data)

# print(parsed_data)
# Specify the CSV file name
csv_file = 'C:\GitDev\M.Tech.Assignments\data-science-assignment\data\\raw\JIOMart_data3.csv'
df = pd.DataFrame(parsed_data)
df.to_csv(csv_file, index=False, header=True)

# Open the CSV file for writing
# with open(csv_file, 'a', newline='', encoding='utf-8') as file:
#     writer = csv.writer(file)
#     # Write the header row
#     #writer.writerow(['Website','Product Catagory','Product Name', 'Weight', 'Original Price', 'Special Price'])
#     writer.writerow(['Online_Grocery_Site','Product_Category','Product_Name', 'Weight', 'Unit', 'DayOfDeal', 'Original_Price', 'Special_Price','Discount'])
#     # Write the parsed data to the CSV file
#     writer.writerows(parsed_data)
#     file.close()

# import csv
# Specify the CSV file name
# csv_file2 = 'C:/Users/sperumal/OneDrive - BMC Software, Inc/Personal/BITS Pilani Doc/1st Semester/Assignment/IDS/JIOMart_data1.csv'
# with open(csv_file2, mode='r') as file:
#    reader = csv.reader(file)
#    for row in reader:
#        print(row)
