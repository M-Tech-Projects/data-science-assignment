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
url = 'https://www.naturesbasket.co.in'

response = requests.get(url)
html = response.content
soup = BeautifulSoup(html, 'html.parser')

headings = list()
refs = list()
itemMap = list()
for h in soup.findAll('div', class_ = 'divSuperCategoryTitle'):
    if(h != None):
        head = h.get_text().lstrip('\n').rstrip('\n')
        # headings.append(head)
        ref = h.find('a')
        if(ref != None):
            href = ref['href']
            # refs.append(href)
            itemMap.append((head, href))

print(itemMap)
uri = itemMap[0][1]
res = requests.get(url+uri).content
soup = BeautifulSoup(res, 'html.parser')

item_cost_list = list()
for main_div in soup.findAll('div', class_='source_Class'):
    product = main_div.findAll('div', class_='pro-bucket')
    for p in product:
        item = p.find('a').find('img')['alt']
        # print(item)
        item_cost = p.parent.find('span', class_='search_PSellingP').get_text()
        item_cost_list.append((item, item_cost))

# item_dict = dict((x, y) for x, y in item_cost_list)
print(item_cost_list)
# print(item_dict)
fields = ['Item', 'Cost']
fileName = itemMap[0][0].translate({ord(c): None for c in string.whitespace}).replace('&', '_and_').lower() + '.csv'
print(fileName)

# print(len(item_cost_list))
with open(fileName, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)

    writer.writerow(fields)
    for item in item_cost_list:
        writer.writerow([item[0], item[1]])

    file.close()