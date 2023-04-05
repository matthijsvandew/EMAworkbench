from mesa import Agent
from enum import Enum
import inspect
import pandas as pd
import random

# ---------------------------------------------------------------
class Infra(Agent):
    """
    Base class for all infrastructure components

    Attributes
    __________
    vehicle_count : int
        the number of vehicles that are currently in/on (or totally generated/removed by)
        this infrastructure component

    length : float
        the length in meters
    ...

    """

    def __init__(self, unique_id, model, length=0,
                 name='Unknown', road_name='Unknown'):
        super().__init__(unique_id, model)
        self.length = length
        self.name = name
        self.road_name = road_name
        self.vehicle_count = 0

    def step(self):
        pass

    def __str__(self):
        return type(self).__name__ + str(self.unique_id)


# ---------------------------------------------------------------
class Bridge(Infra):
    """
    Creates delay time

    Attributes
    __________
    condition:
        condition of the bridge

    delay_time: int
        the delay (in ticks) caused by this bridge
    ...

    """

    def __init__(self, unique_id, model, dict_scenario,length=0,
                 name='Unknown', road_name='Unknown', condition='Unknown'):
        super().__init__(unique_id, model, length, name, road_name)

        self.dict_scenario = dict_scenario

        self.condition = condition

        # The following lines determine whether the bridge breaks down based on the probability to break down and condition.
        randomizer = random.randrange(0, 100)
        if self.condition == 'A' and randomizer < self.dict_scenario['A']:
            self.condition = 'broken'  # Change the condition from 'A' to 'broken'.
        elif self.condition == 'B' and randomizer < self.dict_scenario['B']:
            self.condition = 'broken'  # Change the condition from 'B' to 'broken'.
        elif self.condition == 'C' and randomizer < self.dict_scenario['C']:
            self.condition = 'broken'  # Change the condition from 'C' to 'broken'.
        elif self.condition == 'D' and randomizer < self.dict_scenario['D']:
            self.condition = 'broken'  # Change the condition from 'D' to 'broken'.

    def get_delay_time(self):
        self.delay_time = 0 # If the bridge is not broken, the delay time is 0.
        if self.condition == 'broken': # If the bridge is broken, the delay time is based on length of the bridge.
            if self.length > 200:
                self.delay_time = random.triangular(1, 2, 4)
            elif 200 > self.length > 50:
                self.delay_time = random.uniform(45, 90)
            elif 50 > self.length > 10:
                self.delay_time = random.uniform(15, 60)
            elif self.length < 10:
                self.delay_time = random.uniform(10, 20)
        else:
            self.delay_time = 0

        #list_cars_passed = []
        if self.delay_time != 0:
            caller = inspect.currentframe().f_back.f_locals.get('self')
            print('caller', caller)
            #list_cars_passed.append(self.vehicle_unique_id)
            #print('list',list_cars_passed)
            if ((self.model.df_bridges.id == self.unique_id) & (self.model.df_bridges.replication == self.model.replication) & (self.model.df_bridges.scenario == self.model.scenario)).any() == True:
                row_number = self.model.df_bridges.loc[(self.model.df_bridges.id == self.unique_id) & (
                            self.model.df_bridges.replication == self.model.replication) & (
                                                     self.model.df_bridges.scenario == self.model.scenario)].index[0]
                self.model.df_bridges.loc[row_number, 'caused_delay_time'] += self.delay_time
                self.model.df_bridges.loc[row_number, 'number_of_vehicles'] += 1
            else:
                self.dictionary_bridge = {'id': self.unique_id, 'caused_delay_time': self.delay_time, 'replication': self.model.replication,
                                    'scenario': self.model.scenario, 'number_of_vehicles': 1}
                # print(self.dictionary_bridge)
                self.delay_caused = pd.DataFrame.from_dict([self.dictionary_bridge])
                #print(self.delay_caused)
                self.model.df_bridges = pd.concat([self.model.df_bridges, self.delay_caused])
                #print(self.model.df_bridge)

        return self.delay_time


# ---------------------------------------------------------------
class Link(Infra):
    pass


# ---------------------------------------------------------------
class Intersection(Infra):
    pass


# ---------------------------------------------------------------
class Sink(Infra):
    """
    Sink removes vehicles

    Attributes
    __________
    vehicle_removed_toggle: bool
        toggles each time when a vehicle is removed
    ...

    """
    vehicle_removed_toggle = False

    def remove(self, vehicle):
        self.model.schedule.remove(vehicle)
        self.vehicle_removed_toggle = not self.vehicle_removed_toggle
        #print(str(self) + ' REMOVE ' + str(vehicle))


# ---------------------------------------------------------------

class Source(Infra):
    """
    Source generates vehicles

    Class Attributes:
    -----------------
    truck_counter : int
        the number of trucks generated by ALL sources. Used as Truck ID!

    Attributes
    __________
    generation_frequency: int
        the frequency (the number of ticks) by which a truck is generated

    vehicle_generated_flag: bool
        True when a Truck is generated in this tick; False otherwise
    ...

    """
    truck_counter = 0
    def __init__(self, unique_id, length,
                 name, road_name, model,number_of_trucks):
        super().__init__(unique_id, length, name, road_name, model)
        #super(Agent).__init__(unique_id, model)
        self.number_of_trucks = number_of_trucks
        #print(self.unique_id)
        #print(self.length)
        #print(self.name)
        #print(self.road_name)
        #print('name',self.name,'trucks',self.number_of_trucks,'road name',self.road_name,'id',self.unique_id,'length',self.length)
        self.vehicle_count = 0

        #self.truck_counter = 0
        if self.number_of_trucks == None:
            self.generation_frequency = 999999999999#float('inf')
            #print('inf gen freq', self.generation_frequency)
        elif self.number_of_trucks == 0:
            self.generation_frequency = 999999999999#float('inf')
            #print('inf gen freq',self.generation_frequency)
        elif pd.isna(self.number_of_trucks) == True:
            self.generation_frequency = 999999999999#float('inf')
            #print('inf gen freq', self.generation_frequency)
        else:
            self.generation_frequency = 50#round((1/((self.number_of_trucks)/6704)))
            #print('trucks',self.number_of_trucks)
            #print('gen_frequency',self.generation_frequency)
        self.vehicle_generated_flag = False

    def step(self):
        #print('truck_counter',Source.truck_counter)
        #if (self.number_of_trucks/6704) > random.random():
        if self.model.schedule.steps % self.generation_frequency == 0:
            self.generate_truck()
        else:
            self.vehicle_generated_flag = False

    def generate_truck(self):
        """
        Generates a truck, sets its path, increases the global and local counters
        """
        try:
            #print(0)
            #print('str self.truck_counter',str(Source.truck_counter))
            #print('self',self)
            agent = Vehicle('Truck' + str(Source.truck_counter), self.model, self)
            #print(1)
            if agent:
                #print(2)
                #self.truck_counter += 1
                #print('agent',agent)
                self.model.schedule.add(agent)
                #print('a')
                agent.set_path()
                #print('b')
                Source.truck_counter += 1
                #print('c')
                self.vehicle_count += 1
                self.vehicle_generated_flag = True
                #print(str(self) + " GENERATE " + str(agent))
        except Exception as e:
            print("Oops!", e.__class__, "occurred.")


# ---------------------------------------------------------------
class SourceSink(Source, Sink):
    """
    Generates and removes trucks
    """
    pass


# ---------------------------------------------------------------
class Vehicle(Agent):
    """

    Attributes
    __________
    speed: float
        speed in meter per minute (m/min)

    step_time: int
        the number of minutes (or seconds) a tick represents
        Used as a base to change unites

    state: Enum (DRIVE | WAIT)
        state of the vehicle

    location: Infra
        reference to the Infra where the vehicle is located

    location_offset: float
        the location offset in meters relative to the starting point of
        the Infra, which has a certain length
        i.e. location_offset < length

    path_ids: Series
        the whole path (origin and destination) where the vehicle shall drive
        It consists the Infras' uniques IDs in a sequential order

    location_index: int
        a pointer to the current Infra in "path_ids" (above)
        i.e. the id of self.location is self.path_ids[self.location_index]

    waiting_time: int
        the time the vehicle needs to wait

    generated_at_step: int
        the timestamp (number of ticks) that the vehicle is generated

    removed_at_step: int
        the timestamp (number of ticks) that the vehicle is removed
    ...

    """

    # 48 km/h translated into meter per min
    speed = 48 * 1000 / 60
    #print(speed)
    # One tick represents 1 minute
    step_time = 1

    class State(Enum):
        DRIVE = 1
        WAIT = 2

    def __init__(self, unique_id, model, generated_by,
                 location_offset=0, path_ids=None):
        #print('AA')
        super().__init__(unique_id, model)
        self.generated_by = generated_by
        #print(self.generated_by)
        self.generated_at_step = model.schedule.steps
        self.location = generated_by
        self.location_offset = location_offset
        self.pos = generated_by.pos
        self.path_ids = path_ids
        # default values
        self.state = Vehicle.State.DRIVE
        self.location_index = 0
        self.waiting_time = 0
        self.waited_at = None
        self.removed_at_step = None
        #print(self.path_ids)

    def __str__(self):
        return "Vehicle" + str(self.unique_id) + \
               " +" + str(self.generated_at_step) + " -" + str(self.removed_at_step) + \
               " " + str(self.state) + '(' + str(self.waiting_time) + ') ' + \
               str(self.location) + '(' + str(self.location.vehicle_count) + ') ' + str(self.location_offset)

    def set_path(self):
        """
        Set the origin destination path of the vehicle
        """
        self.path_ids = self.model.get_route(self.generated_by.unique_id)
        #print('self.path_ids',self.path_ids)

    def step(self):
        """
        Vehicle waits or drives at each step
        """
        if self.state == Vehicle.State.WAIT:
            self.waiting_time = max(self.waiting_time - 1, 0)
            if self.waiting_time == 0:
                self.waited_at = self.location
                self.state = Vehicle.State.DRIVE

        if self.state == Vehicle.State.DRIVE:
            self.drive()

        """
        To print the vehicle trajectory at each step
        """
        #print(self)

    def drive(self):

        # the distance that vehicle drives in a tick
        # speed is global now: can change to instance object when individual speed is needed
        distance = Vehicle.speed * Vehicle.step_time
        distance_rest = self.location_offset + distance - self.location.length

        if distance_rest > 0:
            # go to the next object
            self.drive_to_next(distance_rest)
        else:
            # remain on the same object
            self.location_offset += distance

    def drive_to_next(self, distance):
        """
        vehicle shall move to the next object with the given distance
        """

        self.location_index += 1
        next_id = self.path_ids[self.location_index]
        next_infra = self.model.schedule._agents[next_id]  # Access to protected member _agents

        if isinstance(next_infra, Sink):
            # arrive at the sink
            self.arrive_at_next(next_infra, 0)
            self.removed_at_step = self.model.schedule.steps

            # The following line determine the total driving time of a vehicle. This value is stored in dictionary format.
            self.drive_time = self.removed_at_step - self.generated_at_step
            # print(self.drive_time)
            #self.dictionary = {'id': self.unique_id, 'drive_time': self.drive_time,
                              # 'replication': self.model.replication, 'scenario': self.model.scenario}
            #print(self.dictionary)
            # df_delay = pd.DataFrame.from_dict([self.dictionary]) # Convert the dictionary format to a dataframe format.
            # self.model.df_trucks = pd.concat([self.model.df_trucks, df_delay]) # The driving time for the trucks is stored in the dataframe of the model.
            # #print(self.model.df_trucks)

            self.location.remove(self)
            return

        elif isinstance(next_infra, Bridge):
            self.waiting_time = next_infra.get_delay_time()
            if self.waiting_time > 0:
                # arrive at the bridge and wait
                self.arrive_at_next(next_infra, 0)
                self.state = Vehicle.State.WAIT
                return
            # else, continue driving

        if next_infra.length > distance:
            # stay on this object:
            self.arrive_at_next(next_infra, distance)
        else:
            # drive to next object:
            self.drive_to_next(distance - next_infra.length)

    def arrive_at_next(self, next_infra, location_offset):
        """
        Arrive at next_infra with the given location_offset
        """
        self.location.vehicle_count -= 1
        self.location = next_infra
        self.location_offset = location_offset
        self.location.vehicle_count += 1

# EOF -----------------------------------------------------------
