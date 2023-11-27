# Import the necessary libraries
import calendar
import os
import queue
import re
import uuid
import time
from webbrowser import Chrome

from selenium import webdriver
from selenium.webdriver import chrome
from selenium.webdriver.common.by import By

import mysql.connector
from datetime import date
from datetime import datetime

import pandas as pd
import requests
from bs4 import BeautifulSoup

file_name = f'Kisankonnect.csv'
base_url = 'https://www.kisankonnect.in'

def get_child_urls_from_main_page_contents():
    # urls = queue.PriorityQueue()
    # response = requests.get(base_url)
    # html = response.content
    # soup = BeautifulSoup(html, 'html.parser')
    # elements = soup.select('script[src]')
    # print(elements)
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.page_load_strategy = 'none'
    driver = webdriver.Chrome(options)
    driver.implicitly_wait(5)

    driver.get(base_url)
    time.sleep(10)

    content = driver.find_element(By.CSS_SELECTOR, 'div[class*=\'row justify-content-md-center\'')

    breads = content.find_elements(By.CSS_SELECTOR, 'div[class*=\'col-lg-3 col-md-3 col-4 mb-4 text-center cat-box-width ng-star-inserted\']')
    # breads1 = content.find_elements(By.PARTIAL_LINK_TEXT, 'div[class*=\'col-lg-3 col-md-3 col-4 mb-4 text-center cat-box-width ng-star-inserted\']')
    # print(f'Content = {content}')
    br = breads[0].get_attribute('textContent')
    imgs = breads[0].find_elements(By.TAG_NAME, 'img')
    for img in imgs:
        print(f'Attr = {img}')
        link = img.get_attribute('src')
        print(link)
        dat = img.click()
        print(dat)

    # for bread in breads:
    #     dat = bread.click()
    #     print(dat)


    # print(f'Breads = {breads}')
    # print(f'Bread Size = {(len(breads))}')
    # print(f'Bread = {br}')
    # print(f'Bread1 = {imgs}')


    # for elem in elements:
    #     url = elem['src']

        # if re.match(r'https://(?:.*\.)?', url):
        #     print(f'Its a match {url}')
        #     urls.put(url)

    # print(urls)

get_child_urls_from_main_page_contents()