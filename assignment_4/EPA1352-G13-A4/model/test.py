import pandas as pd

file_name = ('../data\AADT_N_roads_overview.csv')

df = pd.read_csv(file_name,index_col=False)

print(df.head())

print(df.columns)