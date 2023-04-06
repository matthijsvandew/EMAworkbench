from mesa import Model
from mesa.time import BaseScheduler
from mesa.space import ContinuousSpace
from components import Source, Sink, SourceSink, Bridge, Link, Intersection
import pandas as pd
from collections import defaultdict
import networkx as nx

# ---------------------------------------------------------------
def set_lat_lon_bound(lat_min, lat_max, lon_min, lon_max, edge_ratio=0.02):
    """
    Set the HTML continuous space canvas bounding box (for visualization)
    give the min and max latitudes and Longitudes in Decimal Degrees (DD)

    Add white borders at edges (default 2%) of the bounding box
    """

    lat_edge = (lat_max - lat_min) * edge_ratio
    lon_edge = (lon_max - lon_min) * edge_ratio

    x_max = lon_max + lon_edge
    y_max = lat_min - lat_edge
    x_min = lon_min - lon_edge
    y_min = lat_max + lat_edge
    return y_min, y_max, x_min, x_max


# ---------------------------------------------------------------
class BangladeshModel(Model):
    """
    The main (top-level) simulation model

    One tick represents one minute; this can be changed
    but the distance calculation need to be adapted accordingly

    Class Attributes:
    -----------------
    step_time: int
        step_time = 1 # 1 step is 1 min

    path_ids_dict: defaultdict
        Key: (origin, destination)
        Value: the shortest path (Infra component IDs) from an origin to a destination

        Only straight paths in the Demo are added into the dict;
        when there is a more complex network layout, the paths need to be managed differently

    sources: list
        all sources in the network

    sinks: list
        all sinks in the network

    """

    step_time = 1



    def __init__(self,file, seed=None, x_max=500, y_max=500, x_min=0, y_min=0,scenario=0,replication=0):

        self.schedule = BaseScheduler(self)
        self.running = True
        self.path_ids_dict = defaultdict(lambda: pd.Series(dtype='int64'))

        self.space = None
        self.sources = []
        self.sinks = []

        self.replication = replication
        self.scenario = scenario
        self.file = file
       # self.shortest_routes_sourcesinks = shortest_routes_sourcesinks # Load in the shortest path from every sourcesink to every other sourcesink.

        self.df_trucks = pd.DataFrame(columns=['id', 'drive_time', 'replication', 'scenario']) # Create a dataframe to store the driving time of every vehicle.
        self.df_bridges = pd.DataFrame(columns=['id', 'caused_delay_time', 'replication', 'scenario'])

        df_scenario = pd.read_csv(r'../experiment\experimental_input.csv') # Load in all the scenarios.
        df_scenario = df_scenario.loc[[scenario]] # Choose the current scenario.
        df_scenario = df_scenario.reset_index(drop=True)
        self.dict_scenario = {}
        self.dict_scenario['A'] = df_scenario.loc[0, "Cat A %"]
        self.dict_scenario['B'] = df_scenario.loc[0, "Cat B %"]
        self.dict_scenario['C'] = df_scenario.loc[0, "Cat C %"]
        self.dict_scenario['D'] = df_scenario.loc[0, "Cat D %"]

        self.generate_model()


    def generate_model(self):
        """
        generate the simulation model according to the csv file component information

        Warning: the labels are the same as the csv column labels
        """

        #df = pd.read_csv(self.file)
        # print(df)

        # a list of names of roads to be generated
        #roads = df["road"].unique()

        #df_objects_all = []
        #for row in range(len(df)):
            # Select all the objects on a particular road in the original order as in the cvs
            #df_objects_on_road = df[df['road'] == road]

            #if not df_objects_on_road.empty:
                #df_objects_all.append(df_objects_on_road)
                #print(df_objects_all)


        df = pd.read_csv(self.file)
        df_objects_on_road = df
        #print(df_objects_on_road)
        for objects in range (len(df_objects_on_road)):
            if df_objects_on_road.loc[objects, 'model_type'] == 'sourcesink':
                intersection_index = df_objects_on_road.loc[objects, 'id']
                if intersection_index == len(df_objects_on_road):
                    break
                for j in range(intersection_index+1,len(df_objects_on_road)):
                    if df_objects_on_road.loc[j, 'model_type'] == 'sourcesink':
                        next_intersection_index = df_objects_on_road.loc[j, 'id']
                        df_objects_till_intersection = df_objects_on_road.loc[(df_objects_on_road['id'] >= intersection_index) & (df_objects_on_road['id'] <= next_intersection_index)]
                        path_ids = df_objects_till_intersection['id']
                        path_ids.reset_index(inplace=True, drop=True)
                        self.path_ids_dict[path_ids.iloc[0], path_ids.iloc[-1]] = path_ids
                        self.path_ids_dict[path_ids.iloc[0], None] = path_ids
                        #print(self.path_ids_dict)
                        # path_ids = path_ids[::-1]
                        # path_ids.reset_index(inplace=True, drop=True)
                        # self.path_ids_dict[path_ids[0], path_ids.iloc[-1]] = path_ids
                        # self.path_ids_dict[path_ids[0], None] = path_ids
                        #print(self.path_ids_dict)
                        break


        # put back to df with selected roads so that min and max and be easily calculated
        df = pd.concat([df,df_objects_on_road])
        y_min, y_max, x_min, x_max = set_lat_lon_bound(
            df['lat'].min(),
            df['lat'].max(),
            df['lon'].min(),
            df['lon'].max(),
            0.05
        )

        # ContinuousSpace from the Mesa package;
        # not to be confused with the SimpleContinuousModule visualization
        self.space = ContinuousSpace(x_max, y_max, True, x_min, y_min)


        # df_objects_all = []
        # for all in df_objects_on_road:
        #     df_objects_all.append(all)
        # print(df_objects_all)

        # for df in df_objects_all:
        #     #print(df)
        #     #print(df_objects_all)

        for _, row in df_objects_on_road.iterrows():  # index, row in ...
            # create agents according to model_type
            model_type = row['model_type'].strip()
            agent = None

            name = row['name']
            if pd.isna(name):
                name = ""
            else:
                name = name.strip()

            if model_type == 'source':
                agent = Source(row['id'], self, row['length'], name, row['road'])
                self.sources.append(agent.unique_id)
            elif model_type == 'sink':
                agent = Sink(row['id'], self, row['length'], name, row['road'])
                self.sinks.append(agent.unique_id)
            elif model_type == 'sourcesink':
                agent = SourceSink(row['id'], self, row['length'], name, row['road'], row['number_of_trucks'])
                self.sources.append(agent.unique_id)
                self.sinks.append(agent.unique_id)
            elif model_type == 'bridge':
                agent = Bridge(row['id'], self, self.dict_scenario, row['length'], row['name'], row['road'],
                               row['condition']) # Add self.dict_scenario so that a bridge knows the 'broken down bridges' scheme.
            elif model_type == 'link':
                agent = Link(row['id'], self, row['length'], name, row['road'])
            elif model_type == 'intersection':
                if not row['id'] in self.schedule._agents:
                    agent = Intersection(row['id'], self, row['length'], name, row['road'])
            if agent:
                self.schedule.add(agent)
                y = row['lat']
                x = row['lon']
                self.space.place_agent(agent, (x, y))
                agent.pos = (x, y)


    def get_random_route(self, source):
        """
        pick up a random route given an origin
        """
        while True:
            # different source and sink
            sink = self.random.choice(self.sinks)
            if sink is not source:
                break

        shortestpath = pd.Series(self.shortest_routes_sourcesinks[(source, sink)]) # Turn the values from the dictionary (shortest path between two sourcesinks) given an key (origin-destination) in a Series format so that there are no formatting issues.
        shortestpath = shortestpath.rename('id')

        return shortestpath

    # TODO
    def get_route(self, source):
        return self.get_straight_route(source) # Choose a random destination.

    def get_straight_route(self, source):
        """
        pick up a straight route given an origin
        """

        #print(self.path_ids_dict)
        return self.path_ids_dict[source, None]

    def step(self):
        """
        Advance the simulation by one step.
        """
        self.schedule.step()

    def save_results(self):
        """
        Return the dataframe that contains all data from current replication. Intended for use at end simulation.
        """
        return self.df_trucks, self.df_bridges

# EOF -----------------------------------------------------------
