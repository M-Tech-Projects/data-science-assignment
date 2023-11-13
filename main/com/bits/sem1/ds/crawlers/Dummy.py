import string

import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd

class NatureBasketCrawler:
    ## Function definition to get main content data

    # base_dir = 'data\\raw'
    base_dir = 'C:\GitDev\M.Tech.Assignments\data-science-assignment\data\\raw'
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
        res = requests.get(uri).content
        soup = BeautifulSoup(res, 'html.parser')

        item_cost_list = list()
        for main_div in soup.findAll('div', class_='source_Class'):
            product = main_div.findAll('div', class_='pro-bucket')
            for p in product:
                parent = p.parent
                x = parent.children
                # print(x)
                item = p.find('a').find('img')['alt']
                item_cost = p.parent.find('span', class_='search_PSellingP').get_text()
                item_cost_list.append((item, item_cost))

        item_dict = dict((x, y) for x, y in item_cost_list)
        return item_dict

    ## Function to write data in file in csv format, data is in list(tuple) format
    def write_into_csv_file(self, file_name, data):
        fields = ['Item', 'Cost']
        item_file_name = self.base_dir + '\\' + file_name
        with open(item_file_name, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)

            writer.writerow(fields)
            for item in data:
                writer.writerow([item[0], item[1]])

        file.close()



## Sequential approach

def remove_special_chars(name):
    return name \
        .translate({ord(c): None for c in string.whitespace}) \
        .replace('&', '_and_') \
        .replace(',', '_') \
        .replace('@', '_') \
        .replace('!', '_') \
        .replace('#', '_') \
        .replace('%', '_') \
        .lower()

base_url = 'https://www.naturesbasket.co.in'
crawler = NatureBasketCrawler()
itemMap = crawler.get_main_page_contents(base_url)
print(itemMap)
# for item in itemMap:
#     item_file_name = remove_special_chars(item[0]) + '.csv'
#     # item_file_name = item[0].translate({ord(c): None for c in string.whitespace}).replace('&', '_and_').replace(',', '_').lower() + '.csv'
#     print(item_file_name)
#     uri = base_url + item[1]
#     print(uri)
#     item_price = crawler.get_page_data(uri)
#     crawler.write_into_csv_file(item_file_name, item_price)

item_file_name = remove_special_chars(itemMap[0][0]) + '.csv'
print(item_file_name)
uri = base_url + itemMap[0][1]
print(uri)
item_price = crawler.get_page_data(uri)
# crawler.write_into_csv_file(item_file_name, item_price)
print(item_price)
keys = item_price.keys()
vals = item_price.values()
data = {'sl': '', 'product': keys, 'price': vals}
df = pd.DataFrame(data)
print(df)
# for key in keys:
#     print(key + '\t' + item_price.get(key))