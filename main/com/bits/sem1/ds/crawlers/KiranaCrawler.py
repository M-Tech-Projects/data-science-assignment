# Import the necessary libraries
import calendar
import re
from datetime import date

import pandas as pd
import requests
from bs4 import BeautifulSoup

base_dir = 'C:\GitDev\M.Tech.Assignments\data-science-assignment\data\\raw\\'
file_name = 'Kiranamarket_data3.csv'
base_url = 'https://www.kiranamarket.com'
page_size = f'?p=1&product_list_limit=36'
items = list()


def get_child_urls_from_main_page_contents(url):
    def valid_url(url):
        if (url.startswith('https')):
            return True
        else:
            return False

    # Send an HTTP GET request to the URL
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html, 'html.parser')

    url_list = list()

    # Example: Extract the title of the webpage
    title = soup.title.string
    # print(f"Title of the webpage: {title}")

    # for div in soup.findAll('div', class_ = 'owl-item active'):
    for div in soup.findAll('li', class_='product-category product-col'):
        if (div != None):
            ref = div.find('a')
            if (ref != None):
                href = ref['href']
                if (valid_url(href)):
                    url_list.append((href))

    return url_list

def calculate_page(url):
    # print(f'URL = {url}')
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html, 'html.parser')

    # Example: Extract the title of the webpage
    next_page = soup \
        .find('div', id='layer-product-list') \
        .find('div', class_='pages') \
        .find('ul', class_='items pages-items') \
        .find('li', class_='item pages-item-next')

    if(next_page != None):
        next_page = next_page.find('a')['href']
    # print(f'NextPage = {next_page}')

    return next_page

day = calendar.day_name[date.today().weekday()]

def get_page_data(url):
    # Send an HTTP GET request to the URL
    # print(f'URL = {url}')
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html, 'html.parser')

    # Example: Extract the title of the webpage
    title = soup.title.string
    # print(f"Title of the inner webpage: {title}")
    category = title.split('-')[0]
    website = title.split('|')[1].lstrip()
    # print(category)
    # print(website)

    # Content extraction for current page
    next_page = soup \
        .find('div', id='layer-product-list') \
        .find('div', class_='pages') \
        .find('ul', class_='items pages-items') \
        .find('li', class_='item pages-item-next')
    if(next_page != None):
        next_page = next_page.find('a')['href']
    # print(f'NextPage = {next_page}')
    item_name = ''
    for div in soup.findAll('div', class_='price-box price-final_price'):
        # print(price_div)
        item = div.parent.find('strong', class_='product name product-item-name')
        unit = ''
        weight = ''
        if (item != None):
            item = item.find('a').get_text().lstrip().rstrip()
            # Extract Product name, weight and unit
            names = item.split()
            item_name = ' '.join(names[0:-1]).removesuffix(',')
            size = len(names)
            # weight = names[-1]
            alpha = re.findall('(\d+)', names[-1])
            if (len(alpha) == 0):
                unit = names[-1]
                weight = names[-2]
                item_name = ' '.join(names[0:-2]).removesuffix(',').removesuffix('-').lstrip().rstrip()
            elif (len(alpha) == 2):
                weight = float('.'.join(alpha))
                unit = names[-1].split('.'.join(alpha))[-1]
            elif (len(alpha) == 1):
                weight = float(''.join(alpha))
                unit = names[-1].split('.'.join(alpha))[-1]
            # print(f'Name: {item_name}\t\t\tweight: {weight}\t\t\tunit: {unit}')
            unit = rationalize_unit(unit)
        else:
            item = ''
        # print(f'Name: {item}')
        prices_new_label = ''
        prices_old = 0
        prices_new = 0
        try:
            price_div = div.find_all_next('span', class_='price-container price-final_price tax weee')
            prices_new = 0
            prices_label = None
            prices_new = price_div[0].find('span', class_='price-wrapper')['data-price-amount']
            prices_new_label = price_div[0].find('span', class_='price-label')

            if(len(price_div) > 1):
                prices_label = price_div[1].find('span', class_='price-label')

            prices_old = 0
            if (prices_label != None):
                # prices_label = prices_label.get_text()
                prices_old = price_div[1].find('span', class_='price-wrapper')['data-price-amount']
            else:
                prices_old = prices_new
            if (prices_new_label != None):
                prices_new_label = prices_new_label.get_text()
                # prices_old = price_div[1].find('span', class_='price-wrapper')['data-price-amount']
        except Exception as e:
            print(f'Exception class: {e.__class__}\nException occurred: {e}, passing...')
            pass
        # else:
        #     prices_old = prices_new
        # print(f'{prices_new_label}\t\t{prices_new}\t\t{prices_label}\t\t{prices_old}')
        discount = 0
        prices_old = float(prices_old)
        prices_new = float(prices_new)
        if (prices_new_label != None):
            discount = (1 - prices_old / prices_new) * 100
        # print(prices_old)
        # print()
        json = {
            'Online_Grocery_Site': website,
            'Product_Category': category,
            'Product_Name': item_name,
            'Weight': weight,
            'Unit': unit,
            'DayOfDeal': day,
            'Original_Price': prices_new,
            'Special_Price': prices_old,
            'Discount': discount
        }
        if(unit != ''):
            items.append(json)
            # print(f'JSON: {json}')

    next_url = calculate_page(url)
    if(next_url != None):
        get_page_data(next_url)



def extract_weight_and_unit(raw_weight):
    rw_arr = raw_weight.split()
    weight = rw_arr[0]
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


def write_to_csv(file_name, data):
    item_file_name = base_dir + file_name
    df = pd.DataFrame(data)
    df.to_csv(item_file_name, index=False, header=True)


urls = get_child_urls_from_main_page_contents(base_url)
# print(f'URLS = {urls}')

for url in urls:
    get_page_data(url + page_size)

write_to_csv(file_name, items)

print(f'Crawling done for {base_url} and csv file is stored in {base_dir}. Total items = {len(items )}')
