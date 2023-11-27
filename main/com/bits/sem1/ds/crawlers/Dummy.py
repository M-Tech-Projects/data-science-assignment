import os

import pandas as pd
import numpy as np
import matplotlib.pylab as plot
import seaborn as sns
plot.style.use('ggplot')
# pd.set_option('max_columns', 200)

base_dir = 'C:\\GitDev\M.Tech.Assignments\data-science-assignment\data\\'
read_dir = f'{base_dir}raw\\'
write_dir = f'{base_dir}processed\\'
baseDir = os.getcwd()
work_dir = baseDir+' ..\\'
print(f'BASE DIR = {baseDir}')
print(f'WORK DIR = {work_dir}')

df = pd.read_csv(f'{read_dir}Naturebasket_data2.csv')
# print(df.columns)
# print(df['Weight'])
# print(df.iloc[2])
# print(df.shape)
# print(df.describe())
# nature_df.m
