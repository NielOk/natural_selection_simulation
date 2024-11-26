'''
This is the file that actually runs the simulation. 
'''

import numpy as np
import matplotlib.pyplot as plt
import os
import random
import statistics
import json

PROJECT_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENVIRONMENTS_DIR = os.path.join(PROJECT_BASE_DIR, 'environments')
ORGANISM_CONFIGS_DIR = os.path.join(PROJECT_BASE_DIR, 'organism-configs')
DATA_DIR = os.path.join(PROJECT_BASE_DIR, 'data')

# Unchanging simulation parameters
food_opportunities = 3

# Environments will be defined by dictionaries in json files. 
environment_to_use = input("Input the filename for environment you would like to use (e.g. environment_1.json): ")
environment_path = os.path.join(ENVIRONMENTS_DIR, environment_to_use)

with open(environment_path, 'r') as json_file:
    environment_def_dict = json.load(json_file)

initial_count = environment_def_dict["initial_count"] # Initial number of organisms in simulation
initial_food = environment_def_dict["initial_food"] # Initial amount of food available in the simulation. 
days_to_regenerate_food = environment_def_dict["days_to_regenerate_food"] # Number of days it takes to regenerate food after being eaten.
area = environment_def_dict["area"] # Numerical representation of amount of space available in the environment

# Organism parameters
organism_configs_to_use = input("Input the filename for the organism configs you would like to use (e.g. organism_configs_1.json): ")
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

