import random

from mesa import Agent
from enum import Enum
import pandas as pd
from mesa.datacollection import DataCollector

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

    def __init__(self,unique_id, model, length=0,
                 name='Unknown', road_name='Unknown', condition='Unknown',scenario=0):
        super().__init__(unique_id, model, length, name, road_name)

        self.condition = condition
        df_scenario = pd.read_csv(r'C:\Github\epa1352advancedsimulation\assignment_2\EPA1352-G13-A2\experiment\experimental_input.csv')
        self.down_A = df_scenario.iloc[scenario, 1]
        self.down_B = df_scenario.iloc[scenario, 2]
        self.down_C = df_scenario.iloc[scenario, 3]
        self.down_D = df_scenario.iloc[scenario, 4]

        # TODO
        self.change_A = self.random.randrange(0,100)
        self.change_B = self.random.randrange(0, 100)
        self.change_C = self.random.randrange(0, 100)
        self.change_D = self.random.randrange(0, 100)
        if self.condition == 'A' and self.change_A < self.down_A and self.length > 200:
            self.delay_time = self.random.triangular(60,120,240)

        elif self.condition == 'A' and self.change_A < self.down_A and self.length < 10:
            self.delay_time = self.random.uniform(10,20)

        elif self.condition == 'A' and self.change_A < self.down_A and self.length > 10 and self.length < 50:
            self.delay_time = self.random.uniform(10,20)

        elif self.condition == 'A' and self.change_A < self.down_A and self.length < 200 and self.length > 50:
            self.delay_time = self.random.uniform(10,20)

        elif self.condition == 'B' and self.change_B < self.down_B and self.length > 200:
            self.delay_time = self.random.triangular(60, 120, 240)

        elif self.condition == 'B' and self.change_B < self.down_B and self.length < 10:
            self.delay_time = self.random.uniform(10, 20)

        elif self.condition == 'B' and self.change_B < self.down_B and self.length > 10 and self.length < 50:
            self.delay_time = self.random.uniform(10, 20)

        elif self.condition == 'B' and self.change_B < self.down_B and self.length < 200 and self.length > 50:
            self.delay_time = self.random.uniform(10, 20)

        elif self.condition == 'C' and self.change_C < self.down_C and self.length > 200:
            self.delay_time = self.random.triangular(60, 120, 240)

        elif self.condition == 'C' and self.change_C < self.down_C and self.length < 10:
            self.delay_time = self.random.uniform(10, 20)

        elif self.condition == 'C' and self.change_C < self.down_C and self.length > 10 and self.length < 50:
            self.delay_time = self.random.uniform(10, 20)

        elif self.condition == 'C' and self.change_C < self.down_C and self.length < 200 and self.length > 50:
            self.delay_time = self.random.uniform(10, 20)

        elif self.condition == 'D' and self.change_D < self.down_D and self.length > 200:
            self.delay_time = self.random.triangular(60, 120, 240)

        elif self.condition == 'D' and self.change_D < self.down_D and self.length < 10:
            self.delay_time = self.random.uniform(10, 20)

        elif self.condition == 'D' and self.change_D < self.down_D and self.length > 10 and self.length < 50:
            self.delay_time = self.random.uniform(10, 20)

        elif self.condition == 'D' and self.change_D < self.down_D and self.length < 200 and self.length > 50:
            self.delay_time = self.random.uniform(10, 20)

        else:
            self.delay_time = self.random.randrange(0, 10)
        # print(self.delay_time)

    # TODO
    def get_delay_time(self):
        return self.delay_time


# ---------------------------------------------------------------
class Link(Infra):
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
        print(str(self) + ' REMOVE ' + str(vehicle))


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
    generation_frequency = 5
    vehicle_generated_flag = False

    def step(self):
        if self.model.schedule.steps % self.generation_frequency == 0:
            self.generate_truck()
        else:
            self.vehicle_generated_flag = False

    def generate_truck(self):
        """
        Generates a truck, sets its path, increases the global and local counters
        """
        try:
            agent = Vehicle('Truck' + str(Source.truck_counter), self.model, self)
            if agent:
                self.model.schedule.add(agent)
                agent.set_path()
                Source.truck_counter += 1
                self.vehicle_count += 1
                self.vehicle_generated_flag = True
                print(str(self) + " GENERATE " + str(agent))
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

    # 50 km/h translated into meter per min
    speed = 50 * 1000 / 60
    # One tick represents 1 minute
    step_time = 1

    class State(Enum):
        DRIVE = 1
        WAIT = 2

    def __init__(self, unique_id, model, generated_by,
                 location_offset=0, path_ids=None):
        super().__init__(unique_id, model)
        self.generated_by = generated_by
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
        #self.datacollector = DataCollector(agent_reporters={self.removed_at_step - self.generated_at_step})

    def __str__(self):
        return "Vehicle" + str(self.unique_id) + \
               " +" + str(self.generated_at_step) + " -" + str(self.removed_at_step) + \
               " " + str(self.state) + '(' + str(self.waiting_time) + ') ' + \
               str(self.location) + '(' + str(self.location.vehicle_count) + ') ' + str(self.location_offset)

    def set_path(self):
        """
        Set the origin destination path of the vehicle
        """
        self.path_ids = self.model.get_random_route(self.generated_by.unique_id)

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

        #self.datacollector.collect(self)
        """
        To print the vehicle trajectory at each step
        """
        print(self)

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


