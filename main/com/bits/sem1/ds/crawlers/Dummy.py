import re
import pandas as pd
import requests
from bs4 import BeautifulSoup

### ToDo - This code is buggy and must not be used until it is resolved.
class KiranaMarketCrawler:
    # Define the URL of the webpage you want to scrape
    base_url = 'https://www.kiranamarket.com/'
    items = list()
    base_dir = 'C:\GitDev\M.Tech.Assignments\data-science-assignment\data\\raw\\'
    prev_url = ''

    def get_main_page_contents(self, url):

        # Send an HTTP GET request to the URL
        response = requests.get(url)
        html = response.content
        soup = BeautifulSoup(html, 'html.parser')

        url_list = list()

        # Example: Extract the title of the webpage
        title = soup.title.string
        print(f"Title of the webpage: {title}")

        # for div in soup.findAll('div', class_ = 'owl-item active'):
        for div in soup.findAll('li', class_ = 'product-category product-col'):
            if(div != None):
                ref = div.find('a')
                if(ref != None):
                    href = ref['href']
                    url_list.append((href))

        return url_list

    def content_for_url(self, url):
        # Send an HTTP GET request to the URL
        print(f'URL = {url}')
        self.prev_url = url
        response = requests.get(url)
        html = response.content
        soup = BeautifulSoup(html, 'html.parser')
        # print(soup)

        # Example: Extract the title of the webpage
        title = soup.title.string
        print(f"Title of the inner webpage: {title}")
        category = title.split('-')[0]
        website = title.split('|')[1].lstrip()
        print(category)
        print(website)

        # Content extraction for current page
        # price_div = soup.findAll('div', class_ = 'price-box price-final_price')[1]
        # print(price_div)
        item_name = ''
        for div in soup.findAll('div', class_ = 'price-box price-final_price'):
            # print(price_div)
            item = div.parent.find('strong', class_='product name product-item-name')
            unit = ''
            weight = ''
            if(item != None):
                item = item.find('a').get_text().lstrip().rstrip()
                # Extract Product name, weight and unit
                names = item.split()
                item_name = ' '.join(names[0:-1]).removesuffix(',')
                size = len(names)
                # weight = names[-1]
                alpha = re.findall('(\d+)', names[-1])
                if(len(alpha) == 0):
                    unit = names[-1]
                    weight = names[-2]
                    item_name = ' '.join(names[0:-2]).removesuffix(',').removesuffix('-').lstrip().rstrip()
                elif(len(alpha) == 2):
                    weight = float('.'.join(alpha))
                    unit = names[-1].split('.'.join(alpha))[-1]
                elif(len(alpha) == 1):
                    weight = float(''.join(alpha))
                    unit = names[-1].split('.'.join(alpha))[-1]
                print(f'Name: {item_name}\t\t\tweight: {weight}\t\t\tunit: {unit}')
                unit = self.rationalize_unit(unit)
            else:
                item = ''
            print(f'Name: {item}')
            prices_new_label = ''
            prices_old = 0
            prices_new = 0
            try:
                price_div = div.find_all_next('span', class_ = 'price-container price-final_price tax weee')
                # prices_new = type(price_div)
                prices_new = price_div[0].find('span', class_='price-wrapper')['data-price-amount']
                prices_new_label = price_div[0].find('span', class_='price-label')
                prices_label = price_div[1].find('span', class_='price-label')
                prices_old = 0
                if(prices_label != None):
                    prices_label = prices_label.get_text()
                    prices_old = price_div[1].find('span', class_='price-wrapper')['data-price-amount']
                else:
                    prices_old = prices_new
                if(prices_new_label != None):
                    prices_new_label = prices_new_label.get_text()
                    # prices_old = price_div[1].find('span', class_='price-wrapper')['data-price-amount']
            except:
                print(f'Error in extracting page data... Continuing...')
                pass
            # else:
            #     prices_old = prices_new
            # print(f'{prices_new_label}\t\t{prices_new}\t\t{prices_label}\t\t{prices_old}')
            discount = 0
            if(prices_new_label != None):
                discount = (1 - float(prices_old)/float(prices_new)) * 100
            # print(prices_old)
            print()
            js_data = {'Website': website, 'Product_Category': category, 'Product_Name': item_name, 'Weight': weight, 'Unit': unit, 'Original_Price': prices_new, 'Special_Price': prices_old, 'Discount': discount}
            self.items.append(js_data)
            print(js_data)

        # ToDo - Keep this code and uncomment once working finalized
        # Next page calculation and continuation
        try:
            while True:
                next = soup.findAll('li', class_ = 'item pages-item-next')
                n = next[0].find('a')['href']
                print(n)

                if(n == self.prev_url):
                    break
                self.content_for_url(n)

        except:
            print(f'Exception in next page calculation... Continuing...')
            pass

    def write_to_file(self):
        df = pd.DataFrame(data=self.items)
        df.to_csv(self.base_dir + 'Kiranamarket_data_new.csv')

    def rationalize_unit(self, raw_unit):
        unit = ''
        match raw_unit.lower():
            case 'g': unit = 'gm'
            case 'gm': unit = 'gm'
            case 'l': unit = 'Litre'
            case 'ltr': unit = 'Litre'
            case 'litre': unit = 'Litre'
            case 'ml': unit = 'ml'
            case 'kg': unit = 'Kg'
            case _: unit = 'Unit'

        return unit

#### Cass Def Ends Here #####

kirana_crawler = KiranaMarketCrawler()
urls = kirana_crawler.get_main_page_contents(kirana_crawler.base_url)

for url in urls:
    kirana_crawler.content_for_url(url)
# kirana_crawler.content_for_url(urls[0])
kirana_crawler.write_to_file()



# divs = soup.find_all('div',class_ = 'product details product-item-details')
# parsed_data = []
# cleaned_data =[]
# parsed_data1 = []
# Iterate through the div elements and add their contents to the array
# for div in divs:
    # Use div.get_text() to get the text content inside the div
    # parsed_data.append(div.get_text())
    # Replace '\n' with 'null' in the string
    # cleaned_data = [s.replace('\n', ' ') for s in parsed_data]
#print(cleaned_data)

# data = cleaned_data
# parsed_data = []

# for item in data:
#     item_parts = item.split('\r')
#     cleaned_parts = [part.strip() for part in item_parts if part.strip()]
#     parsed_data.append(cleaned_parts)

# Printing the parsed data
#for item in parsed_data:
#print(item)

# import re
# import csv

# Define a regular expression pattern to match product name and price
# pattern = r'^(.*?)\s+Rating:.*?₹([\d.]+)\s+Special Price  ₹([\d.]+)'

# for item in cleaned_data:
#     match = re.match(pattern, item)
#     if match:
#         product_name = match.group(1).strip()
#         product_parts = product_name.split(',')
#         if len(product_parts) == 2:
#             product_name = product_parts[0].strip()
#             weight = product_parts[1].strip()
#         else:
#             product_name = product_parts
#             weight = "N/A"
#         original_price = match.group(2)
#         special_price = match.group(3)
#         parsed_data1.append([product_name, weight, original_price, special_price])

# Specify the CSV file name
# csv_file = 'C:\GitDev\M.Tech.Assignments\data-science-assignment\data\\raw\kiranamarket_data.csv'

# Open the CSV file for writing
# with open(csv_file, 'w', newline='', encoding='utf-8') as file:
#     writer = csv.writer(file)

    # Write the header row
    # writer.writerow(['Product Name', 'Weight', 'Original Price', 'Special Price'])

    # Write the parsed data to the CSV file
    # writer.writerows(parsed_data1)

# print(f'Data has been saved to {csv_file}')