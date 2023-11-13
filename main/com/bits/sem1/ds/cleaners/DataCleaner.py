import pandas as pd

base_dir = 'C:\\GitDev\M.Tech.Assignments\data-science-assignment\data\\'
raw_dir = base_dir + 'raw\\'
processed = base_dir + 'processed\\'

def panda_read(fileName):
    df = pd.read_csv(raw_dir+fileName)
    print(df)

data = panda_read('fruits_and_vegetables.csv')

print(data)