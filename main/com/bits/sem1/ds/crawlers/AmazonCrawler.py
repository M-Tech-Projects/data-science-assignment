import requests
from bs4 import BeautifulSoup
import datetime

url = 'https://www.amazon.in/alm/storefront'

response = requests.get(url)
html = response.content
soup = BeautifulSoup(html, 'html.parser')
sprite = soup.findAll('i', class_ = 'hm-icon nav-sprite')
print(soup)
print(sprite)