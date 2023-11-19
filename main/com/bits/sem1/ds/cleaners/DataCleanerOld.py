import pandas as pd

base_dir = 'C:\\GitDev\M.Tech.Assignments\data-science-assignment\data\\'
raw_dir = base_dir + 'raw\\'
processed_dir = base_dir + 'processed\\'


def format_price_col(col_name, df, full_file_path):
    for index in df.index:
        for value in df.loc[index, col_name]:
            if type(value) == str:
                for x in value.split():
                    if (x != 'MRP'):
                        nature_df.loc[index, col_name] = float(''.join(list(x)[1:]))
            # else:
            #     nature_df.loc[index, 'MRP'] = float(''.join(list(value)[1:]))
            # print(value)
    nature_df.to_csv(full_file_path, index=False, header=True)


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

# ToDo - implement this function for learning
# def add_discount_col(df):
    # dfs = list()
    # for f in files:
    #     name = f.removesuffix('.csv')
    #     df = pd.read_csv(raw_dir + f)
    # df.insert(loc=0, column='Discount %', value=name)
        # print(df.keys())
        # df.assign(G = df['MRP'] - df['Offer'])
        # dfs.append(df)
    # return pd.concat(dfs)


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
item_col = (nature_df['Item'])
mrp_col = (nature_df['MRP'])
offer_col = (nature_df['Offer'])

# working code
nums = list()
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
format_price_col('MRP', nature_df, processed_dir + 'NatureBasket.csv')
format_price_col('Offer', nature_df, processed_dir + 'NatureBasket.csv')
# add_discount_col(nature_df)