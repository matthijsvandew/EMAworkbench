import pandas as pd

file_name = ('../data\elevant_N_roads_AADT_overview4.csv')

df = pd.read_csv(file_name)

print(df.head())

print(df.columns)