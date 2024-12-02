'''
Given two different databases, this script will run logistic regression on them, with everything from preparing the data to running 
the regression to testing the model. 
'''

import os
import json
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt

PROJECT_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_DIR = PROJECT_BASE_DIR[:PROJECT_BASE_DIR.find('logistic-regression')]
SIMULATION_DIR = os.path.join(REPO_DIR, 'simulation')
DATA_DIR = os.path.join(SIMULATION_DIR, 'data')

database_1_name = input("Please input the name of the first database you would like to analyze: ")
database_1_path = os.path.join(DATA_DIR, database_1_name)

database_1_simulation = input("Please input the simulation number of database_1 you would like to analyze (e.g. simulation_1): ")

database_2_name = input("Please input the name of the second database you would like to analyze: ")
database_2_path = os.path.join(DATA_DIR, database_2_name)

database_2_simulation = input("Please input the simulation number of database_2 you would like to analyze (e.g. simulation_1): ")

with open(database_1_path, 'r') as json_file:
    database_1 = json.load(json_file)

with open(database_2_path, 'r') as json_file:
    database_2 = json.load(json_file)

# Prepare data for population 1, adding labels as well
population_1_speeds = database_1["simulation_results"][database_1_simulation]["organism_speeds"]
population_1_sizes = database_1["simulation_results"][database_1_simulation]["organism_sizes"]
population_1_senses = database_1["simulation_results"][database_1_simulation]["organism_senses"]
population_1_labels = [0 for i in range(len(population_1_speeds))] # label 0 for population_1

population_1_tuples = list(zip(population_1_speeds, population_1_sizes, population_1_senses, population_1_labels))

# Prepare data for population 2, adding labels as well
population_2_speeds = database_2["simulation_results"][database_2_simulation]["organism_speeds"]
population_2_sizes = database_2["simulation_results"][database_2_simulation]["organism_sizes"]
population_2_senses = database_2["simulation_results"][database_2_simulation]["organism_senses"]
population_2_labels = [1 for i in range(len(population_2_speeds))] # label 1 for population_2

population_2_tuples = list(zip(population_2_speeds, population_2_sizes, population_2_senses, population_2_labels))

# Split data into train and test
def train_test_split(data, test_size=0.2):
    np.random.shuffle(data)
    split_index = int(len(data) * (1 - test_size))
    train_data = data[:split_index]
    test_data = data[split_index:]

    return train_data, test_data

combined_data = population_1_tuples + population_2_tuples
train_data, test_data = train_test_split(combined_data)

# Get baseline accuracy, as in just guessing 1 or just guessing 0 
baseline_option_1 = len(population_1_labels) / (len(population_1_labels) + len(population_2_labels))
baseline_option_2 = 1 - baseline_option_1

baseline_accuracy = 0
offset = 0
if baseline_option_1 > baseline_option_2:
    baseline_accuracy = baseline_option_1
    offset = np.log(baseline_option_1 / baseline_option_2)
else:
    baseline_accuracy = baseline_option_2
    offset = np.log(baseline_option_2 / baseline_option_1)

def train_model(train_data, alpha, num_iterations, offset, record_intermediate=False):
    intermediate_steps = []
    if record_intermediate:
        intermediate_steps = [i for i in range(num_iterations) if i % 1000 == 0] # Intermediate steps are every 1000 iterations, and we measure accuracy
    
    intermediate_thetas = []

    # Go ahead and run logistic regression on the training data
    thetas = [0 for i in range(3)] # We have 3 features: speed, size, and sense

    # We will do num_iterations training iterations
    for i in tqdm(range(num_iterations)):
        gradient = [0 for i in range(3)]
        for j in range(len(train_data)):
            speed, size, sense, label = train_data[j]

            # calculate gradients changes for speed, size, and sense features
            prediction = 1 / (1 + np.exp(-(thetas[0] * speed + thetas[1] * size + thetas[2] * sense + offset)))

            gradient[0] += speed * (label - prediction)

            gradient[1] += size * (label - prediction)
                                
            gradient[2] += sense * (label - prediction)

        # Update thetas based on gradient
        thetas[0] += alpha * gradient[0]
        thetas[1] += alpha * gradient[1]
        thetas[2] += alpha * gradient[2]

        if record_intermediate and i in intermediate_steps:
            intermediate_thetas.append(thetas.copy())

    return thetas, intermediate_thetas, intermediate_steps

thetas, intermediate_thetas, intermediate_steps = train_model(train_data, 0.01, 10000, offset, record_intermediate=True)

def accuracy_calculation(data, thetas, offset):
    correct = 0
    total = 0

    for i in range(len(data)):
        speed, size, sense, label = data[i]

        prediction = 1 / (1 + np.exp(-(thetas[0] * speed + thetas[1] * size + thetas[2] * sense + offset)))

        if prediction > 0.5:
            prediction = 1
        else:
            prediction = 0

        if prediction == label:
            correct += 1

        total += 1

    return correct / total

train_accuracy = accuracy_calculation(train_data, thetas, offset)
print(f"Train Accuracy: {train_accuracy}")

test_accuracy = accuracy_calculation(test_data, thetas, offset)
print(f"Test Accuracy: {test_accuracy}")

print(f"Baseline Accuracy: {baseline_accuracy}")

# Get intermediate accuracies to plot them
intermediate_train_accuracies = []
intermediate_test_accuracies = []
if len(intermediate_thetas) > 0:
    for i in range(len(intermediate_thetas)):
        intermediate_train_accuracy = accuracy_calculation(train_data, intermediate_thetas[i], offset)
        intermediate_test_accuracy = accuracy_calculation(test_data, intermediate_thetas[i], offset)

        intermediate_train_accuracies.append(intermediate_train_accuracy)
        intermediate_test_accuracies.append(intermediate_test_accuracy)

    plt.figure()
    plt.plot(intermediate_steps, intermediate_train_accuracies, label="Train")
    plt.plot(intermediate_steps, intermediate_test_accuracies, label="Test")
    plt.plot(intermediate_steps, [baseline_accuracy for i in range(len(intermediate_steps))], label="Baseline")
    plt.legend(loc="lower right")
    plt.xlabel("Iterations")
    plt.ylabel("Accuracy")
    plt.title(f"Iterative Training Accuracies for Logistic Regression ({database_1_name} {database_1_simulation} vs {database_2_name} {database_2_simulation})")
    plt.show()

def examine_data(population_1_speeds, population_1_sizes, population_1_senses, population_2_speeds, population_2_sizes, population_2_senses):
    plt.figure()
    plt.hist(population_1_speeds, bins=20, color="blue", label=f"{database_1_name} {database_1_simulation}")
    plt.hist(population_2_speeds, bins=20, color="red", label=f"{database_2_name} {database_2_simulation}")
    plt.title("Speeds for the Two Populations")
    plt.legend(loc="upper right")

    plt.figure()
    plt.hist(population_1_sizes, bins=20, color="blue", label=f"{database_1_name} {database_1_simulation}")
    plt.hist(population_2_sizes, bins=20, color="red", label=f"{database_2_name} {database_2_simulation}")
    plt.title("Sizes for the Two Populations")
    plt.legend(loc="upper right")

    plt.figure()
    plt.hist(population_1_senses, bins=20, color="blue", label=f"{database_1_name} {database_1_simulation}")
    plt.hist(population_2_senses, bins=20, color="red", label=f"{database_2_name} {database_2_simulation}")
    plt.title("Senses for the Two Populations")
    plt.legend(loc="upper right")

    plt.show()

examine_data(population_1_speeds, population_1_sizes, population_1_senses, population_2_speeds, population_2_sizes, population_2_senses)