import os
import time
import calendar
from datetime import datetime, date
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By

base_url = 'https://www.bigbasket.com'
website = base_url[12:]
today_date = datetime.now().strftime('%d %b %Y')
day = today_date.replace(' ', '_')
today_day = calendar.day_name[date.today().weekday()]
base_dir = os.getcwd()
raw_dir = f'{base_dir}\\raw\\'
file_name = f'Bigbasket_{day}.csv'
def make_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.page_load_strategy = 'none'
    web_driver = webdriver.Chrome(options)
    web_driver.implicitly_wait(5)

    return web_driver


def get_sub_urls_for_bigbasket(driver):
    urls = list()
    driver.get(base_url)
    time.sleep(10)

    content = driver.find_elements(By.CSS_SELECTOR, 'div[type*=\'LinearCollage\'')
    print(len(content))
    for div in content:
        category = div.get_attribute('title')
        hrefs = list()
        if (category == 'Bank Offers' or category == 'Top Offers' or category == 'Brand Store'):
            pass
        else:
            links = div.find_elements(By.CSS_SELECTOR, 'a')
            for link in links:
                href = link.get_attribute('href')
                hrefs.append(href)
                # print(f'{category}\t\t\t{href}')

        if (len(hrefs) != 0):
            urls.append((category, hrefs))

    return urls


products = list()
def get_content_for_bigbasket(category, url, driver):
    def extract_weight_and_unit(raw_weight):
        rw_arr = raw_weight.split()
        weight = int(rw_arr[0])
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

    driver.get(url)
    time.sleep(10)

    content = driver.find_elements(By.CSS_SELECTOR, 'ul[class*=\'mt-5 grid gap-6 grid-cols-9\'')
    for ul in content:
        li_list = ul.find_elements(By.CSS_SELECTOR, 'li')
        # print(f'li: {len(li_list)}')
        for li in li_list:
            try:
                items = li.find_elements(By.CSS_SELECTOR, 'div[class*=\'SKUDeck___StyledDiv-sc-1e5d9gk-0 eA-dmzP\'')
                # print(f'Items in category:\t{items}')
                for item in items:
                    header = item.find_element(By.CSS_SELECTOR, 'h3[class*=\'flex flex-col xl:gap-1 lg:gap-0.5\'')
                    title = header\
                        .find_element(By.CSS_SELECTOR, 'a')\
                        .find_element(By.CSS_SELECTOR, 'div')\
                        .find_element(By.CSS_SELECTOR, 'h3')\
                        .text
                    raw_weight = header\
                        .find_element(By.CSS_SELECTOR, 'span[class*=\'Label-sc-15v1nk5-0 PackChanger___StyledLabel-sc-newjpv-1 gJxZPQ cWbtUx\'')\
                        .text
                    prices = header\
                        .parent\
                        .find_element(By.CSS_SELECTOR, 'div[class*=\'Pricing___StyledDiv-sc-pldi2d-0 bUnUzR\'')\
                        .find_elements(By.CSS_SELECTOR, 'span')
                    offer_price = float(prices[0].text[1:])
                    mrp_price = float(prices[1].text[1:])
                    discount = (1 - offer_price / mrp_price) * 100
                    wt_ut_tuple = extract_weight_and_unit(raw_weight)
                    weight = wt_ut_tuple[0]
                    unit = rationalize_unit(wt_ut_tuple[1])
                    # print(f'title = {title}\t\tweight = {raw_weight}\t\t\toffer: {offer_price}\t\tmrp: {mrp_price}')
                    json = {
                        'Online_Grocery_Site': website,
                        'Product_Catagory': category,
                        'Product_Name': title,
                        'Weight': weight,
                        'Unit': unit,
                        'DayOfDeal': today_day,
                        'Date': today_date,
                        'Original_Price': mrp_price,
                        'Discounted_Price': offer_price,
                        'Discount %': discount
                    }
                    products.append(json)
                    # print(json)
            except Exception as e:
                print('Exception')
                # time.sleep(10)
                pass

def write_to_csv(data):
    item_file_name = raw_dir + file_name
    if not os.path.exists(raw_dir):
        os.mkdir(path=raw_dir)
    df = pd.DataFrame(data)
    df.to_csv(item_file_name, index=False, header=True)

bb_driver = make_driver()
item_map = get_sub_urls_for_bigbasket(bb_driver)
# print(len(item_map))
# print(item_map)
bb_driver.close()
# item = item_map[0][1][0]
# print(f'uri: {item}')
for data in item_map:
    category = data[0]
    for uri in data[1]:
        bb_driver = make_driver()
        get_content_for_bigbasket(category, uri, bb_driver)
        bb_driver.close()

write_to_csv(products)
print(f'Crawling for {website} is Done...')
