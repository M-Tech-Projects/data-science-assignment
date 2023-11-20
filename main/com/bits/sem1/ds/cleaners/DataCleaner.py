import re

import pandas as pd

class DataCleaner:
    base_dir = 'C:\\GitDev\M.Tech.Assignments\data-science-assignment\data\\'
    raw_dir = base_dir + 'raw\\'
    processed_dir = base_dir + 'processed\\'

    def make_data_frame(self, file_name):
        return pd.read_csv(self.raw_dir + file_name, index_col=0)

    def write_csv(self, df, file_name):
        df.to_csv(self.processed_dir + file_name, index=False, header=True)

    def format_price_col(self, col_name, df, file_name):
        for index in df.index:
            for value in df.loc[index, col_name]:
                if type(value) == str:
                    for x in value.split():
                        if (x != 'MRP'):
                            nature_df.loc[index, col_name] = float(''.join(list(x)[1:]))
        self.write_csv(df, file_name)


    def add_discount_col(self, df, mrp_col, offer_col, file_name):
        discount = list()
        df[mrp_col] = df[mrp_col].astype(float)
        df[offer_col] = df[offer_col].astype(float)
        mrp = df[mrp_col]
        offer = df[offer_col]
        size = offer.count()
        for index in range(0, size):
            dic = (1 - offer[index]/mrp[index]) * 100
            discount.append(dic)

        print(discount)
        df.insert(5, 'Discount %', discount, allow_duplicates=True)
        df.to_csv(self.processed_dir + file_name)

    # ToDo - Not in use
    def split_weight_unit(self, df, weight_col, product_name_col):
        raw_weight = df[weight_col]
        product_name = df[product_name_col]
        weight = list()
        unit = list()
        # print(raw_weight)
        for index in range(0, raw_weight.count()):
            wt = raw_weight[index]
            name = product_name[index]
            alpha = re.findall()
            print(f'Name = {name}\t\t\t\t\t\tweight = {wt}')



raw_files = ['Naturebasket_data1.csv', 'Kiranamarket_data1.csv', 'JIOMArt_data1.csv']

cleaner = DataCleaner()

jio_df = cleaner.make_data_frame('JIOMArt_data1.csv')  # .drop('Website', axis=1, inplace=True)
# jio_df.drop('Website', axis=1, inplace=True)
# print(jio_df.to_string())
# print(jio_df.info())

kirana_df = cleaner.make_data_frame('Kiranamarket_data1.csv')
# kirana_df[kirana_df['Website'].ne('Website')]
var = kirana_df.select_dtypes(include='object')
# var = kirana_df.loc['Website']
# df = kirana_df[kirana_df['Website']]
# ser = pd.Series
# print(kirana_df[kirana_df['Website'].str.contains('Website')])
# print(kirana_df)
# print(var)
cleaner.write_csv(kirana_df, 'Kiranamarket_data.csv')
# kirana_df.drop('Website', axis=1, inplace=True)
# print(jio_df.to_string())
# print(kirana_df.info())

# nature_df = concat_data(nature_basket_files)
nature_df = cleaner.make_data_frame('Naturebasket_data1.csv')

cleaner.write_csv(nature_df, 'NatureBasket.csv')
# print(nature_df)
# print(nature_df.info())
# item_col = (nature_df['Item'])
# mrp_col = (nature_df['MRP'])
# offer_col = (nature_df['Offer'])
#
# working code
# nums = list()
# for item in item_col.values:
# for item in mrp_col.values:
# for item in offer_col.values:
#     for i in item.split():
#         if(i != 'MRP'):
#             print(len(i))
# num = float(''.join(list(i)[1:]))
# nums.append(float(''.join(list(i)[1:])))
# nums.append(i.removeprefix('\Ue282b9'))
# print(nums)
# print(len(nums))
# format_price_col('MRP', nature_df, processed_dir + 'NatureBasket.csv')
# format_price_col('Offer', nature_df, processed_dir + 'NatureBasket.csv')
cleaner.add_discount_col(nature_df, 'Original_Price', 'Discounted_Price', 'NatureBasket.csv')
cleaner.add_discount_col(kirana_df, 'Original Price', 'Special Price', 'KiranaMarket.csv')
# cleaner.split_weight_unit(nature_df, 'Quantity', 'Product_Name')