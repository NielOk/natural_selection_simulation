'''
This is the file that actually runs the simulation. 
'''

import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import os
import random
import statistics
import json

from organism import organism

PROJECT_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENVIRONMENTS_DIR = os.path.join(PROJECT_BASE_DIR, 'environments')
ORGANISM_CONFIGS_DIR = os.path.join(PROJECT_BASE_DIR, 'organism-configs')
DATA_DIR = os.path.join(PROJECT_BASE_DIR, 'data')

def bernoulli_trial(p):
    return random.choices([1, 0], weights=[p, 1-p], k=1)[0]

### Initialize parameters###

# Unchanging simulation parameters
food_opportunities = 2

# Environments will be defined by dictionaries in json files. 
environment_to_use = input("Input the filename for environment you would like to use (e.g. environment_1.json): ")
environment_path = os.path.join(ENVIRONMENTS_DIR, environment_to_use)

with open(environment_path, 'r') as json_file:
    environment_def_dict = json.load(json_file)

initial_count = environment_def_dict["initial_count"] # Initial number of organisms in simulation
initial_food = environment_def_dict["initial_food"] # Initial amount of food available in the simulation. 
area = environment_def_dict["area"] # Numerical representation of amount of space available in the environment
harshness = environment_def_dict["harshness"] # Probabilistic representation of how harsh the environment is. This is the probability an organism dies because of outside factors in a given generation. 

# Organism parameters
organism_configs_to_use = input("Input the filename for the organism configs you would like to use (e.g. organism_config_1.json): ")
organism_config_path = os.path.join(ORGANISM_CONFIGS_DIR, organism_configs_to_use)

with open(organism_config_path, 'r') as json_file:
    organism_config_dict = json.load(json_file)

initial_energy = organism_config_dict["initial_energy"]
required_energy = organism_config_dict["required_energy"]
initial_speed = organism_config_dict["initial_speed"]
initial_size = organism_config_dict["initial_size"]
initial_sense = organism_config_dict["initial_sense"]
hunt_energy = organism_config_dict["hunt_energy"]
run_energy = organism_config_dict["run_energy"]

# Simulation parameters
num_simulations = int(input("How many times would you like to repeat the simulation?: "))
num_generations = int(input("How many generations would you like to run each simulation for?: "))

# Initialize database. 
database_name = input("Please input the name of the database you would like to update. If the database name does not exist, a new database will be created with the name you provide: ")
database_path = os.path.join(DATA_DIR, database_name)

if not os.path.exists(database_path):
    database = {}
    database["environment_configs"] = environment_def_dict
    database["organism_paramaters"] = organism_config_dict
    database["simulation_parameters"] = {
        "num_simulations": num_simulations,
        "num_generations": num_generations
    }
    with open(database_path, 'w') as json_file:
        json.dump(database, json_file, indent=4)

with open(database_path, 'r') as json_file:
    database = json.load(json_file)

database["simulation_results"] = {}

# Get into the actual simulation
for i in (range(num_simulations)):
    print(f"Simulation number {i + 1} out of {num_simulations}")

    organisms_list = []
    
    # Initialize generation 0
    for j in range(initial_count):
        o = organism(initial_speed, initial_size, initial_sense, initial_energy, required_energy, hunt_energy, run_energy, organisms_list)

    # Simulate generations
    for g in tqdm(range(num_generations)):
        
        food_count = initial_food
        
        # Simulate each organism
        new_organisms_list = []

        for o in organisms_list:
            # Skip simulating organisms that are not alive
            if not o.living:
                continue

            # This hunt only runs through fully if organism is alive
            o.hunt(organisms_list, area, food_opportunities, initial_speed, initial_sense)

            # This gather_food only runs through fully if organism is alive
            food_count = o.gather_food(area, initial_food, food_opportunities, initial_speed, initial_sense)
            
            # Reproduce if energy is sufficient. Function already takes care of whether or not organism is alive.
            if o.cur_energy >= o.traits[4]:
                o.reproduce(organisms_list)
            
            if o.cur_energy < 0 and o.living:
                o.living = False

            # Kill off organisms based on harshness
            if bernoulli_trial(harshness):
                o.cur_energy = 0
                o.living = False
            
            # Reset energy after each day
            o.cur_energy = o.traits[4]

            # If still alive, append to new organisms list
            if o.living:
                new_organisms_list.append(o)

        organisms_list = new_organisms_list
            
    num_living = 0
    for o in organisms_list:
        if o.living:
            print(o.traits)
            print(o.cur_energy)
            num_living += 1
    print(f"Number of organisms alive: {num_living}")