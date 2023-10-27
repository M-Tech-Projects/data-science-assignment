### NOT WORKING

import requests
from bs4 import BeautifulSoup

url = 'https://www.flipkart.com/'

response = requests.get(url)
html = response.content
soup = BeautifulSoup(html, 'html.parser')

headings = list()
refs = list()
itemMap = list()
for h in soup.findAll('div', class_ = '_3sdu8W emupdz'):
    if(h != None):
        print(h)
        # head = h.get_text().lstrip('\n').rstrip('\n')
        # headings.append(head)
        # ref = h.find('a')
        # if(ref != None):
        #     href = ref['href']
        #     refs.append(href)
        #     itemMap.append((head, href))

print(itemMap)