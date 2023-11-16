import re

import pandas as pd

base_dir = 'C:\\GitDev\M.Tech.Assignments\data-science-assignment\data\\'
raw_dir = base_dir + 'raw\\'
processed_dir = base_dir + 'processed\\'


def panda_headers(fileName):
    df = pd.read_csv(raw_dir + fileName)
    keys = df.keys()
    # print(keys)


def concat_data(files):
    dfs = list()
    for f in files:
        name = f.removesuffix('.csv')
        df = pd.read_csv(raw_dir + f)
        df.insert(loc=0, column='Product Category', value=name)
        # print(df.keys())
        # df.assign(G = df['MRP'] - df['Offer'])
        dfs.append(df)
    return pd.concat(dfs)


nature_basket_files = ['bakery_and_dairy.csv',
                       'bakingingredients_and_tools.csv',
                       'beverages.csv',
                       'breakfast_jams_honey_spreads.csv',
                       'chocolates_confectionary_and_desserts.csv',
                       'delicatessen_and_cheese.csv',
                       'fruits_and_vegetables.csv',
                       'gourmetplatters.csv',
                       'grocery.csv',
                       'health_and_wellness.csv',
                       'kitchenaids_and_accessories.csv',
                       'meats_seafood_and_eggs.csv',
                       'snacking.csv',
                       'thegiftstudio.csv',
                       'worldfoods.csv']

jio_df = pd.read_csv(raw_dir + 'JIOMArt_data1.csv')  # .drop('Website', axis=1, inplace=True)
jio_df.drop('Website', axis=1, inplace=True)
# print(jio_df.to_string())
print(jio_df.info())

kirana_df = pd.read_csv(raw_dir + 'Kiranamarket_data1.csv')
kirana_df.drop('Website', axis=1, inplace=True)
# print(jio_df.to_string())
print(jio_df.info())

nature_df = concat_data(nature_basket_files)
nature_df.to_csv(processed_dir + 'NatureBasket.csv', index=False, header=True)
print(nature_df)
print(nature_df.info())
x = (nature_df['Item'])
# print(x)
# for c in (nature_df['Item']).values:
#     for v in c.split():
        # if v.containts('\d+'):
        #     print(v)
        # num = re.findall('\b\d+\w+\b', v)
        # print(num)
# nums = [value.split() for value in x.values]
nums = list()
for item in x.values:
    for i in item.split():
        if(i.isnumeric()):
            nums.append(i)
print(nums)