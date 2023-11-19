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
        discount = []
        df[mrp_col] = df[mrp_col].astype(float)
        df[offer_col] = df[offer_col].astype(float)
        # size = df.size
        # axis = df.axes
        # data = df.loc[0].at[mrp_col]
        # data = df.items
        # print(f'Axis = {axis}')
        # print(f'DataType = {type(data)}')
        # print(f'Data = {data}')
        # matrix = pd.to_numpy()
        # print(f'Matrix = {matrix}')
        # print(f'Data Size = {size}')
        for index in df.index:
            mrp_values = (df.loc[index, mrp_col])
            offer_values = (df.loc[index, offer_col])
            for i in range(0, len(mrp_values)):
                diff = mrp_values[i] - offer_values
                print(diff)
            # discount = [(1 - offer_values[i]/mrp_values[i]) * 100 for i in range(len(mrp_values)]
            # discount = (1 - offer_values/mrp_values) * 100
            # print(f'MRP = {mrp_values}\t\t\tOffer = {offer_values}')
            # print(f'Data Size = {len(mrp_values)}')
            # for value in df.loc[index, ]
            # name = f.removesuffix('.csv')
            # df = pd.read_csv(raw_dir + f)
        # Insert a column discount in %, in column 6
        # df.insert(loc=6, column='Discount %', value=discount)
        print()
        # print(df.keys())
        # df.assign(G = df['MRP'] - df['Offer'])
        # df.to_csv(self.processed_dir + file_name)
        # return df


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
# cleaner.add_discount_col(kirana_df, 'Original Price', 'Special Price', 'KiranaMarket.csv')
# df.to_csv(processed_dir+'NatureBasket.csv')