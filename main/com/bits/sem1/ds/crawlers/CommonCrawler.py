# Import the necessary libraries
import calendar
import os
import re
import uuid

import mysql.connector
from datetime import date
from datetime import datetime

import pandas as pd
import requests
from bs4 import BeautifulSoup

######## Common Variables ########
today_date = datetime.now().strftime('%d %b %Y')
day = today_date.replace(' ', '_')
base_dir = os.getcwd()
raw_dir = f'{base_dir}\\raw\\'
processed_dir = f'{base_dir}\\processed\\'
processed_file_name = f'Common_data_{day}.csv'
today_day = calendar.day_name[date.today().weekday()]

######## DB Credentials & Variables ########
host = 'localhost'
user = 'root'
password = 'Abhi$hek_1982'
schema = 'mtech_ids'
table = 'Online_Grocery_Items'


###### Crawling Starts Here ######

###### Nature Basket Crawler ######
######## Nature Basket Crawler Starts ########
class NatureBasketCrawler:
    file_name = f'Naturebasket_{day}.csv'
    base_url = 'https://www.naturesbasket.co.in'

    def get_child_urls_from_main_page_contents(self):
        response = requests.get(self.base_url)
        html = response.content
        soup = BeautifulSoup(html, 'html.parser')

        url_list = list()
        for h in soup.findAll('div', class_='divSuperCategoryTitle'):
            if (h != None):
                ref = h.find('a')
                if (ref != None):
                    href = ref['href']
                    url_list.append(self.base_url + href)

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
        if(product_category == ''):
            product_category = 'UNKNOWN'
        website = title_arr[1].lstrip().rstrip()
        if (~self.base_url.__contains__(website)):
            website = self.base_url[12:]

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
                        'Date': today_date,
                        'Original_Price': original_price,
                        'Discounted_Price': offer_price,
                        'Discount %': discount_percent
                    }
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

    def write_to_csv(self, data):
        item_file_name = raw_dir + self.file_name
        if not os.path.exists(raw_dir):
            os.mkdir(path=raw_dir)
        df = pd.DataFrame(data)
        df.to_csv(item_file_name, index=False, header=True)

    def remove_special_chars(self, target):
        return target \
            .replace('\"', '') \
            .replace(',', '') \
            .replace('\'', '')

    def start_crawlling(self):
        urls = self.get_child_urls_from_main_page_contents()
        page_data = []
        for url in urls:
            page_data.append(self.get_page_data(url))

        page_data = [json for sublist in page_data for json in sublist]

        self.write_to_csv(page_data)
        print(f'Crawling done for {self.base_url} and csv file is stored in {base_dir}. Total items = {len(page_data)}')


### Crawler class def ends here ####
### Call crawler functions to crawl and write data into csv ###
nb_crawler = NatureBasketCrawler()
nb_crawler.start_crawlling()


######## Nature Basket Crawler Ends ########


###### Kirana Market Crawler ######
######## Kirana Market Crawler Starts ########
class KiranaMarketCrawler:
    base_url = 'https://www.kiranamarket.com'
    page_size = f'?p=1&product_list_limit=36'
    file_name = f'Kiranamarket_{day}.csv'
    items = list()

    def get_child_urls_from_main_page_contents(self):
        def valid_url(url):
            if (url.startswith('https')):
                return True
            else:
                return False

        # Send an HTTP GET request to the URL
        response = requests.get(self.base_url)
        html = response.content
        soup = BeautifulSoup(html, 'html.parser')

        url_list = list()

        # Example: Extract the title of the webpage
        title = soup.title.string

        # for div in soup.findAll('div', class_ = 'owl-item active'):
        for div in soup.findAll('li', class_='product-category product-col'):
            if (div != None):
                ref = div.find('a')
                if (ref != None):
                    href = ref['href']
                    if (valid_url(href)):
                        url_list.append((href))

        return url_list

    def calculate_page(self, url):
        response = requests.get(url)
        html = response.content
        soup = BeautifulSoup(html, 'html.parser')

        # Example: Extract the title of the webpage
        next_page = soup \
            .find('div', id='layer-product-list') \
            .find('div', class_='pages') \
            .find('ul', class_='items pages-items') \
            .find('li', class_='item pages-item-next')

        if (next_page != None):
            next_page = next_page.find('a')['href']

        return next_page

    def get_page_data(self, url):
        # Send an HTTP GET request to the URL
        response = requests.get(url)
        html = response.content
        soup = BeautifulSoup(html, 'html.parser')

        # Example: Extract the title of the webpage
        title = soup.title.string
        category = title.split('-')[0]
        if(category == ''):
            category = 'UNKNOWN'
        website = title.split('|')[1].lstrip()

        # Content extraction for current page
        next_page = soup \
            .find('div', id='layer-product-list') \
            .find('div', class_='pages') \
            .find('ul', class_='items pages-items') \
            .find('li', class_='item pages-item-next')
        if (next_page != None):
            next_page = next_page.find('a')['href']
        item_name = ''
        for div in soup.findAll('div', class_='price-box price-final_price'):
            item = div.parent.find('strong', class_='product name product-item-name')
            unit = ''
            weight = ''
            if (item != None):
                item = item.find('a').get_text().lstrip().rstrip()
                # Extract Product name, weight and unit
                names = item.split()
                item_name = ' '.join(names[0:-1]).removesuffix(',')
                size = len(names)
                alpha = re.findall('(\d+)', names[-1])
                if (len(alpha) == 0):
                    unit = names[-1]
                    weight = names[-2]
                    item_name = ' '.join(names[0:-2]).removesuffix(',').removesuffix('-').lstrip().rstrip()
                elif (len(alpha) == 2):
                    weight = float('.'.join(alpha))
                    unit = names[-1].split('.'.join(alpha))[-1]
                elif (len(alpha) == 1):
                    weight = float(''.join(alpha))
                    unit = names[-1].split('.'.join(alpha))[-1]
                unit = self.rationalize_unit(unit)
            else:
                item = ''
            prices_new_label = ''
            prices_old = 0
            prices_new = 0
            try:
                price_div = div.find_all_next('span', class_='price-container price-final_price tax weee')
                prices_new = 0
                prices_label = None
                prices_new = price_div[0].find('span', class_='price-wrapper')['data-price-amount']
                prices_new_label = price_div[0].find('span', class_='price-label')

                if(len(price_div) > 1):
                    prices_label = price_div[1].find('span', class_='price-label')

                prices_old = 0
                if (prices_label != None):
                    prices_old = price_div[1].find('span', class_='price-wrapper')['data-price-amount']
                else:
                    prices_old = prices_new
                if (prices_new_label != None):
                    prices_new_label = prices_new_label.get_text()
            except Exception as e:
                print(f'Exception class: {e.__class__}\nException occurred: {e}, passing...')
                pass
            discount = 0
            prices_old = float(prices_old)
            prices_new = float(prices_new)
            if (prices_new_label != None):
                discount = (1 - prices_old / prices_new) * 100
            json = {
                'Online_Grocery_Site': website,
                'Product_Category': category,
                'Product_Name': item_name,
                'Weight': weight,
                'Unit': unit,
                'DayOfDeal': today_day,
                'Date': today_date,
                'Original_Price': prices_new,
                'Discounted_Price': prices_old,
                'Discount %': discount
            }
            if (unit != ''):
                self.items.append(json)

        next_url = self.calculate_page(url)
        if (next_url != None):
            self.get_page_data(next_url)

    def extract_weight_and_unit(self, raw_weight):
        rw_arr = raw_weight.split()
        weight = rw_arr[0]
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

    def write_to_csv(self):
        item_file_name = raw_dir + self.file_name
        if not os.path.exists(raw_dir):
            os.mkdir(path=raw_dir)
        df = pd.DataFrame(self.items)
        df.to_csv(item_file_name, index=False, header=True)

    def start_crawling(self):
        urls = self.get_child_urls_from_main_page_contents()

        for url in urls:
            self.get_page_data(url + self.page_size)

        self.write_to_csv()


### Crawler class def ends here ####
### Call crawler functions to crawl and write data into csv ###
km_crawler = KiranaMarketCrawler()
km_crawler.start_crawling()

print(
    f'Crawling done for {km_crawler.base_url} and csv file is stored in {base_dir}. Total items = {len(km_crawler.items)}')

######## Kirana Market Crawler Ends ########



###### JIO Mart Crawler ######
######## JIO Mart Crawler Starts ########
class JioMartCrawler:

    file_name = f'JIOMart_{day}.csv'

    def extract_weight_and_unit(self, raw_weight):
        rw_arr = self.add_space_in_weight_unit(raw_weight).split()
        weight = float(rw_arr[0])
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

    def add_space_in_weight_unit(self, raw_weight):
        if(len(raw_weight.split()) < 2 ):
            nums = re.findall(r'\d+', raw_weight)
            num = '.'.join(nums)
            unit = raw_weight.replace(f'{num}', '')
            weight = [num, unit]
            wt = ' '.join(weight)
            return wt
        else:
            return raw_weight

    def soupproc2(self, url,parsed_data):
        # Send an HTTP GET request to the URL
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content of the webpage using BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')

            # Example: Extract the title of the webpage
            title = soup.title.string
        else:
            print("Failed to retrieve the webpage. Status code:", response.status_code)
        title1 = soup.find_all('div',class_ = 'jm-col-4 jm-mt-base')
        catagory_title =[title.text.strip() for title in title1]

        input_data = catagory_title

        # Initialize empty lists for each attribute
        product_names = []
        weights = []
        original_prices = []
        # discounted_prices = []
        discount_percentages = []
        import re
        day = calendar.day_name[date.today().weekday()]
        for product_string in input_data:
            pattern = re.compile(r'^(.*?)\s+(\d+\s*[gG])\s+₹(\d+\.\d{2})\s+₹(\d+\.\d{2})\s+(\d+)%\s+OFF\s+.*$')
            match = pattern.match(product_string)
            if match:
                product_name = match.group(1).strip()
                raw_weight = match.group(2).strip()
                qty = self.extract_weight_and_unit(raw_weight)
                weight = qty[0]
                unit = self.rationalize_unit(qty[1])
                discounted_price = match.group(3).strip()
                discounted_price = float(discounted_price)
                original_price = match.group(4).strip()
                original_price = float(original_price)
                discount_percentage = match.group(5).strip()
                website = 'jiomart.com'
                titlename = title[0:22]
                if(titlename == ''):
                    titlename = 'UNKNOWN'
                json = {
                        'Online_Grocery_Site': website,
                        'Product_Category': titlename,
                        'Product_Name': product_name,
                        'Weight': weight,
                        'Unit': unit,
                        'DayOfDeal': today_day,
                        'Date': today_date,
                        'Original_Price': original_price,
                        'Discounted_Price': discounted_price,
                        'Discount %': discount_percentage
                    }
                parsed_data.append(json)
        return(parsed_data)

    urls = ['https://www.jiomart.com/c/groceries/snacks-branded-foods/biscuits-cookies/11',
            'https://www.jiomart.com/c/groceries/snacks-branded-foods/noodle-pasta-vermicelli/86',
            'https://www.jiomart.com/c/groceries/snacks-branded-foods/snacks-namkeen/43',
            'https://www.jiomart.com/c/groceries/snacks-branded-foods/chocolates-candies/70',
            'https://www.jiomart.com/c/groceries/snacks-branded-foods/breakfast-cereals/98',
            'https://www.jiomart.com/c/groceries/snacks-branded-foods/ready-to-cook-eat/53',
            'https://www.jiomart.com/c/groceries/dairy-bakery/bakery-snacks/281',
            'https://www.jiomart.com/c/groceries/dairy-bakery/toast-khari/102',
            'https://www.jiomart.com/c/groceries/dairy-bakery/cakes-muffins/125',
            'https://www.jiomart.com/c/groceries/dairy-bakery/breads-and-buns/267',
            'https://www.jiomart.com/c/groceries/beverages/tea/34',
            'https://www.jiomart.com/c/groceries/beverages/coffee/94',
            'https://www.jiomart.com/c/groceries/beverages/energy-soft-drinks/40',
            'https://www.jiomart.com/c/groceries/beverages/fruit-juices/96',
            'https://www.jiomart.com/c/groceries/beverages/soda-flavoured-water/115',
            'https://www.jiomart.com/c/groceries/beverages/health-drink-supplement/49',
            'https://www.jiomart.com/c/groceries/personal-care/skin-care/122',
            'https://www.jiomart.com/c/groceries/personal-care/hair-care/92',
            'https://www.jiomart.com/c/groceries/personal-care/oral-care/132',
            'https://www.jiomart.com/c/groceries/personal-care/bath-hand-wash/119',
            'https://www.jiomart.com/c/groceries/personal-care/body-wash-bathing-accessories/179',
            'https://www.jiomart.com/c/groceries/staples/atta-flours-sooji/26',
            'https://www.jiomart.com/c/groceries/staples/dals-pulses/17',
            'https://www.jiomart.com/c/groceries/staples/rice-rice-products/14',
            'https://www.jiomart.com/c/groceries/staples/salt-sugar-jaggery/23',
            'https://www.jiomart.com/c/groceries/staples/edible-oils/58',
            'https://www.jiomart.com/c/groceries/staples/dry-fruits-nuts/657',
            'https://www.jiomart.com/c/groceries/staples/ghee/12903',
            'https://www.jiomart.com/c/groceries/staples/masalas-spices/21',
            'https://www.jiomart.com/c/groceries/staples/combo-offer/1281',
            'https://www.jiomart.com/c/groceries/home-care/detergents/37']

    def start_crawling(self):
        parsed_data = []
        for url in self.urls:
            self.soupproc2(url, parsed_data)
        csv_file = raw_dir + self.file_name
        if not os.path.exists(raw_dir):
            os.mkdir(path=raw_dir)
        df = pd.DataFrame(parsed_data)
        df.to_csv(csv_file, index=False, header=True)


### Crawler class def ends here ####
### Call crawler functions to crawl and write data into csv ###
jm_crawler = JioMartCrawler()
jm_crawler.start_crawling()

print(f'Crawling done for JIOMart and csv file is stored in {base_dir}')

######## JIO Mart Crawler Ends ########

###### Crawling Ends Here ######


####### Data Cleaning Begins Here #######


class DataCleaner:

    raw_files = [f'Naturebasket_{day}.csv', f'Kiranamarket_{day}.csv', f'JIOMArt_{day}.csv']

    def merge_data(self):
        dfs = list()
        # df = pd.concat((pd.read_csv((raw_dir + filename), index_col=None, header=0) for filename in  self.raw_files), axis=0, ignore_index=True)
        for fname in self.raw_files:
            df = pd.read_csv(raw_dir + fname, index_col=None, header=0)
            dfs.append(df)
        frame = pd.concat(dfs, axis=0, ignore_index=True)
        if not os.path.exists(processed_dir):
            os.mkdir(path=processed_dir)
        frame.to_csv(processed_dir + processed_file_name, index=False, header=True)
        print(f'Columns = {frame.columns}')

cleaner = DataCleaner()

cleaner.merge_data()

####### Data Cleaning Ends Here #######


####### DB Ingestion Begins Here #######

class DatabaseUtil:

    connection = mysql.connector.connect(host=host, user=user, password=password)
    curser = connection.cursor()

    def create_table(self):
        create_schema = f'CREATE SCHEMA IF NOT EXISTS {schema}'
        self.curser.execute(create_schema)
        self.curser.execute(f'use {schema}')

        #Day to be any of 7 days on which data collected, say Wednesday
        create_table = f'CREATE TABLE IF NOT EXISTS {table} (' \
                       f'Id VARCHAR(100) NOT NULL, ' \
                       f'OnlineGrocerySite VARCHAR(150) NOT NULL, ' \
                       f'ProductCategory VARCHAR(350) NOT NULL, ' \
                       f'ProductName VARCHAR(350) NOT NULL, ' \
                       f'Weight FLOAT(10, 2) NOT NULL, ' \
                       f'Unit VARCHAR(20) NOT NULL, ' \
                       f'DayOfDeal VARCHAR(50), ' \
                       f'Date VARCHAR(50), ' \
                       f'OriginalPrice FLOAT(10, 2) NOT NULL, ' \
                       f'DiscountedPrice FLOAT(10, 2) NOT NULL, ' \
                       f'DiscountPercentage FLOAT(10, 2) NOT NULL, ' \
                       f'PRIMARY KEY (`Id`)' \
                       f');'

        self.curser.execute(create_table)

    def insert_data_into_table(self, df):
        cols = df.columns
        size = df[cols[0]].count()

        web_data = df[cols[0]]
        category_data = df[cols[1]]
        name_data = df[cols[2]]
        weight_data = df[cols[3]]
        unit_data = df[cols[4]]
        dod_data = df[cols[5]]
        date_data = df[cols[6]]
        mrp_data = df[cols[7]]
        offer_data = df[cols[8]]
        discount_data = df[cols[9]]

        # We can add day on which data collected for now it is hard coded to Tuesday
        self.curser.execute(f'use {schema}')

        insert_command = f'INSERT INTO {table} ' \
                         f'(ID,OnlineGrocerySite,ProductCategory,ProductName,Weight,Unit,DayOfDeal,Date,OriginalPrice,DiscountedPrice,DiscountPercentage)' \
                         f'VALUES '

        for i in range(0, size):
            row_id = uuid.uuid5(uuid.uuid5(uuid.uuid5(uuid.uuid4(), (web_data[i])), name_data[i]), name_data[i])
            # values = f'(\'{row_id}\', \'{self.remove_special_chars(web_data[i])}\', \'{self.remove_special_chars(category_data[i])}\', ' \
            values = f'(\'{row_id}\', \'{self.remove_special_chars(web_data[i])}\', \'{(category_data[i])}\', ' \
                     f'\'{self.remove_special_chars(name_data[i])}\', {weight_data[i]}, \'{unit_data[i]}\', ' \
                     f'\'{dod_data[i]}\', \'{date_data[i]}\', {mrp_data[i]}, {offer_data[i]}, {discount_data[i]});'

            # print(f'{values}')
            try:
                curser = self.connection.cursor()
                curser.execute(insert_command + values)
                curser.execute('commit')
            except Exception as e:
                print(f'Some error in fetching data {e}....Passing...')
                pass

    def remove_special_chars(self, string):
        if('\'' in string):
            return string \
                .replace('\'', '_')
        else:
            return string

    def process_db(self):
        df = pd.read_csv(processed_dir + processed_file_name)
        self.create_table()
        self.insert_data_into_table(df)

    def query_data(self, product_name):
        select_query = f'SELECT * FROM {table} WHERE ProductName LIKE \'%{product_name}%\';'
        try:
            self.curser.execute(f'use {schema}')
            self.curser.execute(select_query)
            result = self.curser.fetchall()
            self.connection.close()
            return result
        except Exception as e:
            print(f'Some exception in Querying data: {e}...Passing...')
            pass


## class def ends here
util = DatabaseUtil()
util.process_db()
## Sample query function call
res = util.query_data('Blueberries')
for row in res:
    print(row)


####### DB Ingestion Ends Here #######


####### Prediction Begins Here #######

####### Prediction Ends Here #######