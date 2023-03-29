import pandas as pd

file_name = ('../data\elevant_N_roads_AADT_overview4.csv')

df = pd.read_csv(file_name,index_col=False)

print(df.head())

print(df.columns)

df = df.drop(columns=['(AADT)'])

print(df.head())

df.to_csv('../data\elevant_N_roads_AADT_overview5.csv',index=False)

file_name = ('../data\elevant_N_roads_AADT_overview5.csv')

df = pd.read_csv(file_name,index_col=False)

print(df.head())

print(df.columns)