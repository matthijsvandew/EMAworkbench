class run_experiments():
    def __init__(self,random_seed=False,scenarios=[0, 1], run_length=10000, amount_trucks=1): #default values
        self.random_seed = random_seed
        self.scenarios = scenarios
        self.run_length = run_length
        self.amount_trucks = amount_trucks

    def __str__(self):
        return str(self.random_seed) + str(self.scenarios) + str(self.run_length) + str(self.amount_trucks)

scenarios = [0] # Only scenario 1 is used
random_seed = False # Use the default seed
run_length = 7200 # 5 times 24 days every tick is 1 minute
amount_trucks = 1
experiments = run_experiments(random_seed,scenarios,run_length,amount_trucks)
print(experiments)