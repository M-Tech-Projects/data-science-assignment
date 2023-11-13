import pandas as pd

base_dir = 'C:\\GitDev\M.Tech.Assignments\data-science-assignment\data\\raw\\'

def panda_read(fileName):
    df = pd.read_csv(base_dir+fileName)
    print(df)

panda_read('grocery.csv')