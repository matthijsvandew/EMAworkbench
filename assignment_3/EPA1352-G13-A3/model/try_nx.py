import networkx as nx
from collections import defaultdict
import pandas as pd
import matplotlib.pyplot as plt
import scipy

file_name = '../data/input_data_roads_test.csv'

df = pd.read_csv(file_name)

# a list of names of roads to be generated
roads = df["road"].unique()

G = nx.Graph()

for i in roads:
    # print()
    # print()
    # print(i)
    road_sections = df.loc[df['road']==i]
    for i in range(len(road_sections)):
        current_section = road_sections.iloc[i]
        #print(current_section.id)
        G.add_node(current_section.id,pos=(current_section.lon,current_section.lat))
    for i in range(len(road_sections)-1):
        current_section = road_sections.iloc[i]
        next_section = road_sections.iloc[i+1]
        # print(current_section.id)
        # print(next_section.id)
        if i != (len(road_sections)-1):
            G.add_edge(u_of_edge=current_section.id,v_of_edge=next_section.id,length=current_section.length)
            print(current_section.id,current_section.length)
        else:
            G.add_edge(u_of_edge=current_section.id, v_of_edge=next_section.id, length=(current_section.length + next_section.length) )

nx.draw_networkx(G)
plt.show()

# for i in path_ids_dict1:
#     print()
#     print(i)
#     print(path_ids_dict1[i])