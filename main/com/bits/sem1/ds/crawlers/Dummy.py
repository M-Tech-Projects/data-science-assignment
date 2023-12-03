import os

import pandas as pd
import numpy as np
import matplotlib.pylab as plot
import seaborn as sns
plot.style.use('ggplot')
# pd.set_option('max_columns', 200)
import calendar
import os
import re
import uuid

import mysql.connector
from datetime import date
from datetime import datetime

# base_dir = 'C:\\GitDev\M.Tech.Assignments\data-science-assignment\data\\'
base_dir = os.getcwd()
raw_dir = f'{base_dir}\\raw\\'
proc_dir = f'{base_dir}\\processed\\'
today_date = datetime.now().strftime('%d %b %Y')
day = today_date.replace(' ', '_')

file_name = f'Common_data_{day}.csv'
df = pd.read_csv(f'{proc_dir}{file_name}')
# pd.StringDtype('Product_Category')
# print(df.columns)
# print(df['Weight'])
# print(df.iloc[2])
print(df.shape)
# print(df.describe())
print(df[['Online_Grocery_Site','Product_Catagory','Product_Name','Weight','Unit','DayOfDeal','Date','Original_Price','Discounted_Price','Discount %']])
# nature_df.m
