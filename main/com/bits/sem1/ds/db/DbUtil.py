import mysql.connector
import pandas as pd

class DatabaseUtil:

    schema = 'mtech'
    table = 'Online_Grocery_Items'
    # col_names = ['site', 'product_category', 'product_name', 'quantity', 'original_price', 'special_price', 'discount_percentage']

    def __int__(self):
        self.connection = mysql.connector.connect(host='localhost', user='root', password='Abhi$hek_1982')

    def create_table(self):
        curser = self.connection.cursor()
        # curser.execute('show databases')
        create_schema = f'CREATE SCHEMA IF NOT EXISTS {self.schema}'
        curser.execute(create_schema)
        curser.execute(f'use {self.schema}')

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

        curser.execute(create_table)

    # ToDo - Complete the implementation
    def insert_data_into_table(self, read_file):
        reader = pd.read_csv(read_file, index_col= 0, header=None)
        cols = reader.columns
        print(f'{cols}\t\t\t\t{reader[1].count()}')

        for row in range(1, reader[1].count()):
            for col in cols:
                print(f'{reader[row].iloc[col]}')        #giving column values
                # print(type(reader[i].iloc[i]))
            print()
                # print(reader.get(i).name)

util = DatabaseUtil()
base_dir = 'C:\\GitDev\M.Tech.Assignments\data-science-assignment\data\\'
raw_dir = base_dir + 'raw\\'
processed_dir = base_dir + 'processed\\'

util.insert_data_into_table(processed_dir + 'NatureBasket.csv')
# for d in curser:
#     print(d)
# curser.execute('use sakila')
# for x in curser:
#     print(x)
# result = curser.execute('select * from actor')
# for r in curser:
#     print(r)
#