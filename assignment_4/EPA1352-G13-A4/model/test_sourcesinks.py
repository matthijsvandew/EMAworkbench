import pandas as pd

df_sourcesinks = pd.read_csv('../data\input_origin_destination_trucks.csv')
for row in range(len(df_sourcesinks)):
    road_origin = (df_sourcesinks.loc[row, 'origin'])
    road_destination = (df_sourcesinks.loc[row, 'destination'])
    LRP_origin = (df_sourcesinks.loc[row, 'LRP1'])
    LRP_destination = (df_sourcesinks.loc[row, 'LRP2'])
    row_number_sourcesink_origin = merge_right.loc[(merge_right.road == road_origin) & (merge_right.LRPName == LRP_origin)].index[0]
    row_number_sourcesink_destination = merge_right.loc[(merge_right.road == road_destination) & (merge_right.LRPName == LRP_destination)].index[0]
    merge_right.loc[row_number_sourcesink_origin, 'model_type'] = 'sourcesink'
    merge_right.loc[row_number_sourcesink_destination, 'model_type'] = 'sourcesink'