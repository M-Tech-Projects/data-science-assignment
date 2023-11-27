# Import the necessary libraries
import calendar
from datetime import date

import pandas as pd
import requests
from bs4 import BeautifulSoup

base_dir = 'C:\GitDev\M.Tech.Assignments\data-science-assignment\data\\raw\\'
file_name = 'Naturebasket_test_data.csv'
base_url = 'https://www.naturesbasket.co.in'


class NatureBasketCrawler:

    def get_child_urls_from_main_page_contents(self, uri):
        response = requests.get(uri)
        html = response.content
        soup = BeautifulSoup(html, 'html.parser')

        url_list = list()
        for h in soup.findAll('div', class_='divSuperCategoryTitle'):
            if (h != None):
                ref = h.find('a')
                if (ref != None):
                    href = ref['href']
                    url_list.append(uri + href)

        return url_list

    def get_page_data(self, url):
        # Send an HTTP GET request to the URL
        response = requests.get(url)
        # Parse the HTML content of the webpage using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        # Example: Extract the title of the webpage
        title = soup.title.string.lstrip().rstrip()
        title_arr = title.split('|')
        product_category = self.remove_special_chars(title_arr[0].lstrip().rstrip())
        website = title_arr[1].lstrip().rstrip()
        if (~base_url.__contains__(website)):
            website = base_url[12:]
        day = calendar.day_name[date.today().weekday()]
        # print(f'Title of the webpage: {title}\tProduct Category = {product_category}\tWebsite={website}')

        divs = soup.find_all('div', id='ctl00_ContentPlaceHolder1_divSearchData')
        parsed_data = list()
        # Iterate through the div elements and add their contents to the array
        for div in divs:
            # Use div.get_text() to get the text content inside the div
            product_divs = div.find_all_next('div', class_='hide')
            for pd in product_divs:
                try:
                    product_name = self.remove_special_chars(pd.find('a').find('img')['alt'].lstrip().rstrip())
                    qty = pd.find('div', class_='search_PSelectedSize')
                    if (qty == None):
                        qty = pd.find('span', class_='search_PSelectedSize')
                    prices = pd.find('div', class_='productlist-price')
                    offer_span = prices.find('span', class_='search_PSellingP')
                    mrp_span = prices.find('span', class_='search_PMRP')
                    if(offer_span != None):
                        offer_span = offer_span.get_text().split()
                    else:
                        offer_span = offer_span.get_text
                    if(mrp_span != None):
                        mrp_span = mrp_span.get_text().split()
                    else:
                        mrp_span = offer_span
                    mrp = 0
                    offer_price = 0
                    if(len(offer_span) == 1):
                        offer_price = float(offer_span[0][1:])
                    else:
                        offer_price = float(offer_span[1][1:])
                    if(len(mrp_span) == 0):
                        mrp = mrp_span
                    elif(len(mrp_span) == 1):
                        mrp = float(mrp_span[0][1:])

                    qty = self.extract_weight_and_unit(qty.get_text())
                    weight = qty[0]
                    unit = qty[1]

                    if(mrp == 0):
                        original_price = float(offer_price)
                    else:
                        original_price = float(mrp)

                    discount_percent = (1 - offer_price / original_price) * 100
                    json = {
                        'Online_Grocery_Site': website,
                        'Product_Catagory': product_category,
                        'Product_Name': product_name,
                        'Weight': weight,
                        'Unit': unit,
                        'DayOfDeal': day,
                        'Original_Price': original_price,
                        'Discounted_Price': offer_price,
                        'Discount %': discount_percent
                    }
                    # print(json)
                    parsed_data.append(json)
                except Exception as e:
                    print(f'Exception class: {e.__class__}\nException occurred: {e}, passing...')
                    pass

        return parsed_data

    def extract_weight_and_unit(self, raw_weight):
        rw_arr = raw_weight.split()
        weight = int(rw_arr[0])
        unit = self.rationalize_unit(rw_arr[1])

        return (weight, unit)

    def rationalize_unit(self, raw_unit):
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

    def write_to_csv(self, file_name, data):
        item_file_name = base_dir + file_name
        df = pd.DataFrame(data)
        df.to_csv(item_file_name, index=False, header=True)

    def remove_special_chars(self, target):
        return target\
            .replace('\"', '')\
            .replace(',', '')\
            .replace('\'', '')

### Crawler class def ends here ####
# Define the URL of the webpage you want to scrape


crawler = NatureBasketCrawler()
urls = crawler.get_child_urls_from_main_page_contents(base_url)
# print(f'URLS = {urls}')
page_data = []
for url in urls:
    page_data.append(crawler.get_page_data(url))

page_data = [json for sublist in page_data for json in sublist]
# print(f'Size = {len(page_data)}')

csv_file = base_dir + file_name
crawler.write_to_csv(file_name, page_data)
print(f'Crawling done for {base_url} and csv file is stored in {base_dir}. Total items = {len(page_data)}')
