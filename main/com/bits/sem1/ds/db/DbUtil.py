import mysql.connector
import pandas as pd

class DatabaseUtil:

    connection = mysql.connector.connect(host='localhost', user='root', password='')
    curser = connection.cursor()

    schema = 'mtech'
    table = 'Online_Grocery_Items'

    def create_table(self):
        create_schema = f'CREATE SCHEMA IF NOT EXISTS {self.schema}'
        self.curser.execute(create_schema)
        self.curser.execute(f'use {self.schema}')

        #Day to be any of 7 days on which data collected, say Wednesday
        create_table = f'CREATE TABLE IF NOT EXISTS {self.table} (' \
                       f'Id INT(11) NOT NULL AUTO_INCREMENT, ' \
                       f'OnlineGrocerySite VARCHAR(150) NOT NULL, ' \
                       f'ProductCategory VARCHAR(350) NOT NULL, ' \
                       f'ProductName VARCHAR(350) NOT NULL, ' \
                       f'Quantity VARCHAR(50) NOT NULL, ' \
                       f'DayOfDeal VARCHAR(50), ' \
                       f'OriginalPrice FLOAT(10, 2) NOT NULL, ' \
                       f'SpecialPrice FLOAT(10, 2) NOT NULL, ' \
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
        quantity_data = df[cols[3]]
        mrp_data = df[cols[4]]
        offer_data = df[cols[5]]
        discount_data = df[cols[6]]

        # We can add day on which data collected for now it is hard coded to Tuesday
        day = 'Tuesday'
        self.curser.execute(f'use {self.schema}')

        insert_command = f'INSERT INTO {self.table} ' \
                         f'(OnlineGrocerySite, ProductCategory, ProductName, Quantity, DayOfDeal, OriginalPrice, SpecialPrice, DiscountPercentage)' \
                         f'VALUES '

        for i in range(0, size):
            values = f'(\'{self.remove_special_chars(web_data[i])}\', \'{self.remove_special_chars(category_data[i])}\', ' \
                     f'\'{self.remove_special_chars(name_data[i])}\',\'{quantity_data[i]}\', ' \
                     f'\'{day}\', {mrp_data[i]}, {offer_data[i]}, {discount_data[i]});'

            print(f'{values}')
            curser = self.connection.cursor()
            curser.execute(insert_command + values)
            curser.execute('commit')

    def remove_special_chars(self, string):
        return string\
            .replace('\'', '_')


## class def ends here
util = DatabaseUtil()
base_dir = 'C:\\GitDev\M.Tech.Assignments\data-science-assignment\data\\'
raw_dir = base_dir + 'raw\\'
processed_dir = base_dir + 'processed\\'

nature_df = pd.read_csv(processed_dir + 'NatureBasket.csv')
util.insert_data_into_table(nature_df)
