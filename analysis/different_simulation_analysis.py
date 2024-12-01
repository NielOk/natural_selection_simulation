'''
This is a script to analyze the simulation data for two conditinally different simulations. It is mainly for checking the p-values of the simulation data
of two different simulations. This file expects there to only be one simulation done for each database. 
Result for comparing database_3 and database_4. With 50000 bootstrapped samples, we found that the p-values for the differences in means of speed, size, and sense between the two simulations were 0.0, 0.0, and 0.0, respectively. This means that the differences in means were statistically significant.
'''

import matplotlib.pyplot as plt
import statistics
from tqdm import tqdm
import json
import os
import random

PROJECT_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_DIR = PROJECT_BASE_DIR[:PROJECT_BASE_DIR.find('analysis')]
SIMULATION_DIR = os.path.join(REPO_DIR, 'simulation')
DATA_DIR = os.path.join(SIMULATION_DIR, 'data')

database_1_name = input("Please input the name of the first database you would like to analyze: ")
database_1_path = os.path.join(DATA_DIR, database_1_name)

database_2_name = input("Please input the name of the second database you would like to analyze: ")
database_2_path = os.path.join(DATA_DIR, database_2_name)

with open(database_1_path, 'r') as json_file:
    database_1 = json.load(json_file)

with open(database_2_path, 'r') as json_file:
    database_2 = json.load(json_file)

def plot_simulation_results(database_1, database_2):
    all_organism_speeds = []
    all_organism_sizes = []
    all_organism_senses = []

    speed_means = []
    size_means = []
    sense_means = []

    # database 1
    simulation_results_dict = database_1["simulation_results"]["simulation_1"]
    organism_speeds = simulation_results_dict["organism_speeds"]
    organism_sizes = simulation_results_dict["organism_sizes"]
    organism_senses = simulation_results_dict["organism_senses"]

    for speed in organism_speeds:
        all_organism_speeds.append(speed)

    for size in organism_sizes:
        all_organism_sizes.append(size)

    for sense in organism_senses:
        all_organism_senses.append(sense)

    speed_means.append(statistics.mean(organism_speeds))
    size_means.append(statistics.mean(organism_sizes))
    sense_means.append(statistics.mean(organism_senses))

    # database 2
    simulation_results_dict = database_2["simulation_results"]["simulation_1"]
    organism_speeds = simulation_results_dict["organism_speeds"]
    organism_sizes = simulation_results_dict["organism_sizes"]
    organism_senses = simulation_results_dict["organism_senses"]

    for speed in organism_speeds:
        all_organism_speeds.append(speed)

    for size in organism_sizes:
        all_organism_sizes.append(size)

    for sense in organism_senses:
        all_organism_senses.append(sense)

    speed_means.append(statistics.mean(organism_speeds))
    size_means.append(statistics.mean(organism_sizes))
    sense_means.append(statistics.mean(organism_senses))

    plt.figure()
    plt.hist(all_organism_speeds, bins=20)
    plt.title("Combined Speeds")
    plt.show()

    plt.figure()
    plt.hist(all_organism_sizes, bins=20)
    plt.title("Combined Sizes")
    plt.show()

    plt.figure()
    plt.hist(all_organism_senses, bins=20)
    plt.title("Combined Senses")
    plt.show()

# Helper to concatenate simulation 1 and simulation 2 organism traits
def concatenate_simulations(simulation_1, simulation_2):
    concatenated_speeds = simulation_1["organism_speeds"] + simulation_2["organism_speeds"]
    concatenated_sizes = simulation_1["organism_sizes"] + simulation_2["organism_sizes"]
    concatenated_senses = simulation_1["organism_senses"] + simulation_2["organism_senses"]

    return concatenated_speeds, concatenated_sizes, concatenated_senses

# Helper to normalize all data in preparation for bootstrapping
def normalize_data(list_of_data):
    value_counts_dict = {}
    for value in list_of_data:
        if value in value_counts_dict:
            value_counts_dict[value] += 1
        else:
            value_counts_dict[value] = 1

    all_values = []
    all_value_probs = []
    for key in value_counts_dict.keys():
        all_values.append(key)
        all_value_probs.append(value_counts_dict[key] / len(list_of_data))

    return all_values, all_value_probs

def find_p_values(database_1, database_2):

    simulation_1_speeds = database_1["simulation_results"]["simulation_1"]["organism_speeds"]
    simulation_2_speeds = database_2["simulation_results"]["simulation_1"]["organism_speeds"]

    simulation_1_sizes = database_1["simulation_results"]["simulation_1"]["organism_sizes"]
    simulation_2_sizes = database_2["simulation_results"]["simulation_1"]["organism_sizes"]

    simulation_1_senses = database_1["simulation_results"]["simulation_1"]["organism_senses"]
    simulation_2_senses = database_2["simulation_results"]["simulation_1"]["organism_senses"]

    concatenated_speeds, concatenated_sizes, concatenated_senses = concatenate_simulations(database_1["simulation_results"]["simulation_1"], database_2["simulation_results"]["simulation_1"])

    all_speeds, all_speed_probs = normalize_data(concatenated_speeds)
    all_sizes, all_size_probs = normalize_data(concatenated_sizes)
    all_senses, all_sense_probs = normalize_data(concatenated_senses)

     # Now, we can bootstrap. Specifically, we want to compare differences of means
    mean_diffs_speeds = []
    mean_diffs_sizes = []
    mean_diffs_senses = []

    for i in tqdm(range(50000)):
        sample_speeds_1 = random.choices(all_speeds, weights=all_speed_probs, k=len(simulation_1_speeds))
        sample_speeds_2 = random.choices(all_speeds, weights=all_speed_probs, k=len(simulation_2_speeds))

        sample_sizes_1 = random.choices(all_sizes, weights=all_size_probs, k=len(simulation_1_sizes))
        sample_sizes_2 = random.choices(all_sizes, weights=all_size_probs, k=len(simulation_2_sizes))

        sample_senses_1 = random.choices(all_senses, weights=all_sense_probs, k=len(simulation_1_senses))
        sample_senses_2 = random.choices(all_senses, weights=all_sense_probs, k=len(simulation_2_senses))

        mean_diffs_speeds.append(abs(statistics.mean(sample_speeds_1) - statistics.mean(sample_speeds_2)))
        mean_diffs_sizes.append(abs(statistics.mean(sample_sizes_1) - statistics.mean(sample_sizes_2)))
        mean_diffs_senses.append(abs(statistics.mean(sample_senses_1) - statistics.mean(sample_senses_2)))

    # Now, we can calculate p-values
    actual_speed_diff = abs(statistics.mean(simulation_1_speeds) - statistics.mean(simulation_2_speeds))
    actual_size_diff = abs(statistics.mean(simulation_1_sizes) - statistics.mean(simulation_2_sizes))
    actual_sense_diff = abs(statistics.mean(simulation_1_senses) - statistics.mean(simulation_2_senses))

    speed_p_value = len([diff for diff in mean_diffs_speeds if diff >= actual_speed_diff]) / len(mean_diffs_speeds)
    size_p_value = len([diff for diff in mean_diffs_sizes if diff >= actual_size_diff]) / len(mean_diffs_sizes)
    sense_p_value = len([diff for diff in mean_diffs_senses if diff >= actual_sense_diff]) / len(mean_diffs_senses)

    plt.figure()
    plt.hist(mean_diffs_speeds, bins=20)
    plt.title("Bootstrapped Speed Differences")

    plt.figure()
    plt.hist(mean_diffs_sizes, bins=20)
    plt.title("Bootstrapped Size Differences")

    plt.figure()
    plt.hist(mean_diffs_senses, bins=20)
    plt.title("Bootstrapped Sense Differences")

    print("Actual differences:")
    print(f"Speed: {actual_speed_diff}")
    print(f"Size: {actual_size_diff}")
    print(f"Sense: {actual_sense_diff}")

    print(f"Speed p-value: {speed_p_value}")
    print(f"Size p-value: {size_p_value}")
    print(f"Sense p-value: {sense_p_value}")

    plt.show()

if __name__ == '__main__':
    find_p_values(database_1, database_2)
    plot_simulation_results(database_1, database_2)