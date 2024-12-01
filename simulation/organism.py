'''
This is the class definition of an organism in the natural selection simulation. 
'''

import random
import numpy as np

def squeeze_with_tanh(x):
    return np.tanh(x)

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def bernoulli_trial(p):
    return random.choices([1, 0], weights=[p, 1-p], k=1)[0]

class organism():

    # Each organism is a tuple, with element 0 = speed, 1 = size, 2 = sense, 3 = energy, 4 = required energy, 5 = hunt energy, 6 = run energy. Initiailization takes in initial values for each of these parameters. We only initialize if this organism is not in the living list and we are at a new generation. 
    def __init__(self, speed_0, size_0, sense_0, energy_0, required_energy_0, hunt_energy_0, run_energy_0, organisms_list):
        self.parent_traits = [speed_0, size_0, sense_0, energy_0, required_energy_0, hunt_energy_0, run_energy_0]
        self.traits = [speed_0, size_0, sense_0, energy_0, required_energy_0, hunt_energy_0, run_energy_0]
        self.cur_energy = energy_0 # Marker for current energy of organism. Save it separately since we want to pass down initial energy unchanged to children. 
        self.food_opportunities = 3
        self.id = len(organisms_list)
        self.living = True

        organisms_list.append(self)

    def reproduce(self, organisms_list):
        # Mutations. We allow fairly large mutations such that the mutations a quarter of the organism's current trait magnitudes can occur. Traits can also become negative. 
        max_mutation_factor = 0.25

        speed_mutation = random.uniform(-1 * max_mutation_factor * self.traits[0], max_mutation_factor * self.traits[0])
        size_mutation = random.uniform(-1 * max_mutation_factor * self.traits[1], max_mutation_factor * self.traits[1])
        sense_mutation = random.uniform(-1 * max_mutation_factor * self.traits[2], max_mutation_factor * self.traits[2])

        # Calculate new speed, size, and sense
        new_speed = self.traits[0] + speed_mutation
        new_size = self.traits[1] + size_mutation
        new_sense = self.traits[2] + sense_mutation

        # Calculated required energies. This should make it so that if its traits increase in stats, the required energy increase, and if the traits decrease, required energy decreases. These should also be fairly proportional. 
        required_energy = squeeze_with_tanh(((speed_mutation + size_mutation + sense_mutation) / 3)) * self.traits[4] + self.traits[4]# Take weighted average of difference from previous generation traits to determine required energy. 
        hunt_energy = squeeze_with_tanh(((speed_mutation + size_mutation + sense_mutation) / 3)) * self.traits[5] + self.traits[5]
        run_energy = squeeze_with_tanh(((speed_mutation + size_mutation + sense_mutation) / 3)) * self.traits[6] + self.traits[6]

        child_traits = [new_speed, new_size, new_sense, self.cur_energy, required_energy, hunt_energy, run_energy]

        # Create child organism
        child = organism(child_traits[0], child_traits[1], child_traits[2], child_traits[3], child_traits[4], child_traits[5], child_traits[6], organisms_list)

    # Hunting mechanism. Both hunting and running away will cost energy. 
    def hunt(self, organisms_list, area, food_opportunities, initial_speed, initial_sense):

        temp_living_list = []
        for o in organisms_list:
            if o.living and o.id != self.id:
                temp_living_list.append(o)
        
        # In this simulation, organisms move food_opportunities times a day. This means each organism will take up food_opportunities different area squares per day. 
        base_hunt_prob = (len(temp_living_list)) / area

        # Calculate num_food_opportunities boost. Based on speed and sense.
        food_opportunities_boost = int(squeeze_with_tanh(((self.traits[0] - initial_speed) + (self.traits[2] - initial_sense)) / 2) * food_opportunities)
        new_food_opportunities = food_opportunities + food_opportunities_boost

        for i in range(new_food_opportunities):

            # This is case where there are no prey left. 
            if (len(temp_living_list) == 0):
                break

            found_prey = bernoulli_trial(base_hunt_prob) # boolean that tells you if you found prey.
            if found_prey:
                prey = random.choice(temp_living_list)

                # Check if faster than prey. 
                if self.traits[0] > prey.traits[0]:
                    
                    # Now, if bigger than prey, eat it. If smaller than prey, run away.
                    if self.traits[1] > prey.traits[1]:
                        prey.living = False
                        self.cur_energy += prey.traits[3] + prey.cur_energy # Gain energy from eating prey
                        self.cur_energy -= self.traits[5] # Hunt energy cost
                        temp_living_list.remove(prey)
                    
                    else:
                        self.cur_energy -= self.traits[6] # Run away energy cost
                
                # If slower than prey
                else:
                    
                    # If bigger than prey, prey runs away. If smaller than prey, get killed
                    if self.traits[1] > prey.traits[1]:
                        prey.cur_energy -= prey.traits[6] # Run away energy cost
                    else:
                        self.living = False
                        prey.cur_energy += self.traits[3] + self.cur_energy # Transfer energy to prey
                        prey.cur_energy -= prey.traits[5] # Hunt energy cost
                        temp_living_list.remove(self)
                        break

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