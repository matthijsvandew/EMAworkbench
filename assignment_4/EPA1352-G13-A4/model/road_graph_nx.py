import networkx as nx
from collections import defaultdict
import pandas as pd
import matplotlib.pyplot as plt
import scipy

class road_graph():
    def find_shortest_path(file_name = '../data\demo-4.csv'):

        df = pd.read_csv(file_name)

        roads = df["road"].unique() # A list of names of roads to be generated.

        G = nx.Graph() # Create a NetworkX graph.

        for i in roads: # Iterate over all roads.
            # print()
            # print()
            # print(i)
            road_sections = df.loc[df['road']==i] # Select all the rows that belong to the current road (i in the loop). So all the rows that belong to the N1, for example.
            for i in range(len(road_sections)): # Loop over the row length of the current road.
                current_section = road_sections.iloc[i] # The current (i'th) row in the df / place on the road we are looking at.
                #print(current_section.id)
                # Add the current place on the road / LRP as node to the graph. Give as position it's lonitute and latitude; as model type wheter it is a link/bridge etc and save the id of the node.
                G.add_node(current_section.id,pos=(current_section.lon,current_section.lat),model_type=current_section.model_type, id=current_section.id)
                #print(nx.get_node_attributes(G,'model_type'))
            for i in range(len(road_sections)-1): # Loop again over the road sections, but now till the second-last point on the road, because we look one step ahead.
                current_section = road_sections.iloc[i] # The current (i'th) row in the df / place on the road we are looking at.
                next_section = road_sections.iloc[i+1] # The next row in the df / place on the road / LRP we are looking at.
                # print(current_section.id)
                # print(next_section.id)
                if i != (len(road_sections)-1): # As long as we are not at the second-last step:
                    # Add an edge between the current point and the next point, with a length that is specified in the csv file at the row of the current point on the road.
                    G.add_edge(u_of_edge=current_section.id,v_of_edge=next_section.id,length=current_section.length)
                    #print(current_section.id,current_section.length)
                else: # If we are at the second-last point on the road:
                    # Add an edge between the second-last node and the last node, with length equal to the sum of the road between the nodes and the length of the last node.
                    G.add_edge(u_of_edge=current_section.id, v_of_edge=next_section.id, length=(current_section.length + next_section.length) )

        pos = nx.get_node_attributes(G, 'pos') # Get the position of the nodes based on lat,lon.
        nx.draw_networkx(G,pos,node_size=10,with_labels=False) # Draw the network: graph G, with its positions according to lon,lat.
        #plt.show()

        sourcesinks = set() # Create a set (which consists of unique values only).
        for i in G.nodes(): # Loop over all the nodes in the graph.
            for attribute in G.nodes[i]['model_type']: # Loop over every model type.
                if G.nodes[i]['model_type'] == 'sourcesink':
                    #print(G.nodes[i])
                    sourcesinks.add(G.nodes[i]['id']) # If the model type is a sourcesink, then add the node to the set.

        sourcesinks_routes = {} # Create a dictionary with keys giving the source and the sink and as values the shortest path between the source and the sink.
        for i in sourcesinks:
            for j in sourcesinks: # Loop in a loop over all the sourcesinks to find every possible combination of source and sink.
                if i !=j: # Obviously, there is no shortest path between a source and a sink if these are the same.
                    sp = nx.shortest_path(G, i, j, weight='length') # Shortest path between sourcesinks i and j.
                    splen = nx.shortest_path_length(G,i,j,weight='length') # Length of the shortest path.
                    #print(i,j,splen)

                    route = {(i, j): sp}
                    sourcesinks_routes.update(route) # Add the shortest path (sp, i.e. the route) as value to de dictionary with as key the origin, destination set.

        return sourcesinks_routes