'''
This is the class definition of an organism in the natural selection simulation. 
'''

import random

class organism():

    # Each organism is a tuple, with element 0 = speed, 1 = size, 2 = sense, 3 = energy, 4 = required energy, 5 = hunt energy, 6 = run energy. Initiailization takes in initial values for each of these parameters. We only initialize if this organism is not in the living list and we are at a new generation. 
    def __init__(self, speed_0, size_0, sense_0, energy_0, required_energy_0, hunt_energy_0, run_energy_0, living_ids_list, living_traits_list):
        self.traits = [speed_0, size_0, sense_0, energy_0, required_energy_0, hunt_energy_0, run_energy_0]
        self.food_opportunities = 3
        self.id = len(living_ids_list)

        living_ids_list.append(self.id)
        living_traits_list.append(self.traits)

    def reproduce(self, living_ids_list, living_traits_list):
        child_traits = self.traits.copy()

        # Mutations. We allow fairly large mutations such that the mutations a quarter of the organism's current trait magnitudes can occur. Traits can also become negative. 
        max_mutation_factor = 0.25

        speed_mutation = random.uniform(-1 * max_mutation_factor * self.traits[0], max_mutation_factor * self.traits[0])
        size_mutation = random.uniform(-1 * max_mutation_factor * self.traits[1], max_mutation_factor * self.traits[1])
        sense_mutation = random.uniform(-1 * max_mutation_factor * self.traits[2], max_mutation_factor * self.traits[2])

        # Calculate new speed, size, and sense
        new_speed = self.traits[0] + speed_mutation
        new_size = self.traits[1] + size_mutation
        new_sense = self.traits[2] + sense_mutation

        required_energy = ((speed_mutation + size_mutation + sense_mutation) / 3) * self.traits[4] # Take weighted average of difference from previous generation traits to determine required energy. 

        # Need to define hunt energy and run energy. 

    # For deaths, we need to just append the organism's id to the dead list, then process all of the dead at the end by removing them from the living backwards. We need to make sure not to simulate dead organisms by checking if the organism is dead before running things. 
    

'''
TESTS FOR ORGANISM CLASS
'''
# Test 1: Test that the organism class initializes correctly.
def test1():
    speed_0 = 10
    size_0 = 10
    sense_0 = 10
    energy_0 = 10
    required_energy_0 = 10
    hunt_energy_0 = 10
    run_energy_0 = 10
    living_list = []
    o = organism(speed_0, size_0, sense_0, energy_0, required_energy_0, hunt_energy_0, run_energy_0, living_list)
    assert o.traits == [speed_0, size_0, sense_0, energy_0, required_energy_0, hunt_energy_0, run_energy_0]
    assert o.food_opportunities == 3

if __name__ == '__main__':
    test1()