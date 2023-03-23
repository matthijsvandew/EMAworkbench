import networkx as nx
from collections import defaultdict
import pandas as pd
import matplotlib.pyplot as plt
import scipy

class road_network():
    def __init__(self,file_name = '../data\demo-4.csv'):
        self.file_name = file_name

    def find_shortest_path(self):

        df = pd.read_csv(self.file_name)

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
                G.add_node(current_section.id,pos=(current_section.lon,current_section.lat),model_type=current_section.model_type, id=current_section.id)
                #print(nx.get_node_attributes(G,'model_type'))
            for i in range(len(road_sections)-1):
                current_section = road_sections.iloc[i]
                next_section = road_sections.iloc[i+1]
                # print(current_section.id)
                # print(next_section.id)
                if i != (len(road_sections)-1):
                    G.add_edge(u_of_edge=current_section.id,v_of_edge=next_section.id,length=current_section.length)
                    #print(current_section.id,current_section.length)
                else:
                    G.add_edge(u_of_edge=current_section.id, v_of_edge=next_section.id, length=(current_section.length + next_section.length) )

        pos = nx.get_node_attributes(G, 'pos')
        nx.draw_networkx(G,pos,node_size=10,with_labels=False)
        #plt.show()

        sourcesinks = set()
        for i in G.nodes():
            for attribute in G.nodes[i]['model_type']:
                if G.nodes[i]['model_type'] == 'sourcesink':
                    #print(G.nodes[i])
                    sourcesinks.add(G.nodes[i]['id'])

        sourcesinks_routes = {}
        for i in sourcesinks:
            for j in sourcesinks:
                if i !=j:
                    sp = nx.shortest_path(G, i, j, weight='length')
                    splen = nx.shortest_path_length(G,i,j,weight='length')
                    #print(i,j,splen)

                    route = {(i, j): sp}
                    sourcesinks_routes.update(route)

        return sourcesinks_routes