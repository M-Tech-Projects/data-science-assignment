import string

import requests
from bs4 import BeautifulSoup
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
                item = p.find('a').find('img')['alt']
                item_cost = p.parent.find('span', class_='search_PSellingP').get_text()
                mrp = p.parent.find('span', class_='search_PMRP')
                item_mrp = mrp.get_text() if(mrp != None)  else item_cost
                item_cost_list.append({'Item': item, 'MRP': item_mrp, 'Offer':item_cost})

        # item_dict = dict((x, y) for x, y in item_cost_list)
        return item_cost_list

    ## Function to write data in file in csv format, data is in list(tuple) format
    def write_into_csv_file(self, file_name, data):
        item_file_name = self.base_dir + '\\' + file_name
        df = pd.DataFrame(data)
        df.to_csv(item_file_name, index=False, header=True)


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
for item in itemMap:
    item_file_name = remove_special_chars(item[0]) + '.csv'
    # item_file_name = item[0].translate({ord(c): None for c in string.whitespace}).replace('&', '_and_').replace(',', '_').lower() + '.csv'
    print(item_file_name)
    uri = base_url + item[1]
    print(uri)
    item_price = crawler.get_page_data(uri)
    crawler.write_into_csv_file(item_file_name, item_price)
