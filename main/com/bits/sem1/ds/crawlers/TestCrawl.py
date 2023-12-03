import re
import time

from selenium import webdriver
from selenium.webdriver.common.by import By

base_dir = 'C:\GitDev\M.Tech.Assignments\data-science-assignment\data\\raw\\'
file_name = 'JIOMart_data3.csv'
base_url = 'https://www.jiomart.com'
website = base_url[12:]


def make_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.page_load_strategy = 'none'
    web_driver = webdriver.Chrome(options)
    web_driver.implicitly_wait(5)

    return web_driver


def get_sub_urls_for_jiomart():
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


def remove_spl_chars(text):
    return text.lstrip().rstrip().replace(',', '')


def get_main_content_for_jiomart(web_driver, url):
    def extract_weight_and_unit(category, text):
        wt = 0
        ut = ''
        if (category != 'UNKNOWN'):
            try:
                arr = text.split()
                # print(arr)
                wt = float(arr[-2])
                ut = (arr[-1])
                # print(f'Weight = {wt}\tUnit = {ut}')
            except Exception as e:
                print(f'Exception class: {e.__class__}\nException occurred: {e}, passing...')
                wt = 1
                ut = 'Pc'
                # print(f'Weight = {wt}\tUnit = {ut}')
                pass
        else:
            wt = 1
            ut = 'Pc'
            # print(f'Weight = {wt}\tUnit = {ut}')

        return (wt, ut)

    web_driver.get(url)
    ol = web_driver.find_element(By.CSS_SELECTOR, 'ol[class*=\'ais-InfiniteHits-list jm-row jm-mb-massive\'')
    lis = ol.find_elements(By.CSS_SELECTOR, 'li[class*=\'ais-InfiniteHits-item jm-col-4 jm-mt-base\'')
    # print(f'LIs = {lis}')
    for li in lis:
        a = li.find_element(By.CSS_SELECTOR, 'a')
        product_name = remove_spl_chars(a.get_attribute('title'))
        a_tag = a.find_element(By.CSS_SELECTOR, 'div[class*=\'gtmEvents\'')
        product_category = a_tag.get_attribute('data-vertical')
        if (product_category == None):
            product_category = 'UNKNOWN'
        # print(f'A Tag = {a_tag}')
        div = a.find_element(By.CSS_SELECTOR, 'div[class*=\'plp-card-image-wrapper\'')
        price_div = a.find_element(By.CSS_SELECTOR, 'div[class*=\'plp-card-details-price\'')
        prices_div = price_div.find_elements(By.CSS_SELECTOR, 'span')
        # print(prices_div)
        offer_price = 0
        mrp_price = 0
        discount = '00'
        # if(len(prices_div) > 0):
        offer_price = float((re.search(r'\d*\.\d+', prices_div[0].text)).group())
        if (len(prices_div) > 1):
            mrp_price = float((re.search(r'\d*\.\d+', prices_div[1].text)).group())
            if (len(prices_div) > 2):
                discount = (prices_div[2].text.split()[0][:-1])
        else:
            mrp_price = offer_price

        if (mrp_price < offer_price):
            mrp_price = float(discount[1:])
        try:
            discount = (1 - offer_price / mrp_price) * 100
        except Exception as e:
            print(f'Exception class: {e.__class__}\nException occurred: {e}, passing...')
            pass
        # print(f'Offer = {offer_price}\t\tMRP = {mrp_price}\t\t\tDiscount = {discount}')
        # raw_weight = ((re.search(r'\d*\.\d+', product_name)).group())
        # print(f'Title : {product_name}, Weight : {raw_weight}')
        wt_ut = extract_weight_and_unit(product_category, product_name)
        weight = wt_ut[0]
        unit = wt_ut[1]

        json = {
            'Online_Grocery_Site': website,
            'Product_Category': product_category,
            'Product_Name': product_name,
            'Weight': weight,
            'Unit': unit,
            # 'DayOfDeal': today_day,
            # 'Date': today_date,
            'Original_Price': mrp_price,
            'Discounted_Price': offer_price,
            'Discount %': discount
        }
        print(json)


driver = make_driver()
url_list = get_sub_urls_for_jiomart()
for url in url_list:
    get_main_content_for_jiomart(driver, url)


##############################################################################################################################################
##############################################################################################################################################
##############################################################################################################################################
##############################################################################################################################################

