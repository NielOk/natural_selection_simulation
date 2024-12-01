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
        self.living = True

        organisms_list.append(self)

    def reproduce(self, organisms_list, initial_speed, initial_size, initial_sense):
        if not self.living:
            return

        # Mutations. We allow fairly large mutations such that the mutations a quarter of the organism's current trait magnitudes can occur. Traits can also become negative. 
        max_mutation_factor = 0.025

        speed_mutation = random.uniform(-1 * max_mutation_factor * self.traits[0], max_mutation_factor * self.traits[0])
        size_mutation = random.uniform(-1 * max_mutation_factor * self.traits[1], max_mutation_factor * self.traits[1])
        sense_mutation = random.uniform(-1 * max_mutation_factor * self.traits[2], max_mutation_factor * self.traits[2])

        # Calculate new speed, size, and sense
        new_speed = self.traits[0] + speed_mutation
        new_size = self.traits[1] + size_mutation
        new_sense = self.traits[2] + sense_mutation

        # Calculated required energies. This should make it so that if its traits increase in stats, the required energy increase, and if the traits decrease, required energy decreases. These should also be fairly proportional. 
        required_energy = squeeze_with_tanh((((new_speed - initial_speed) + (new_size - initial_size) + (new_sense - initial_sense)) / 3)) * self.traits[4] + self.traits[4]# Take weighted average of difference from previous generation traits to determine required energy. 
        hunt_energy = squeeze_with_tanh((((new_speed - initial_speed) + (new_size - initial_size) + (new_sense - initial_sense)) / 3)) * self.traits[5] + self.traits[5]
        run_energy = squeeze_with_tanh((((new_speed - initial_speed) + (new_size - initial_size) + (new_sense - initial_sense)) / 3)) * self.traits[6] + self.traits[6]

        child_traits = [new_speed, new_size, new_sense, self.cur_energy, required_energy, hunt_energy, run_energy]

        # Create child organism
        child = organism(child_traits[0], child_traits[1], child_traits[2], child_traits[3], child_traits[4], child_traits[5], child_traits[6], organisms_list)

        self.cur_energy = self.cur_energy / 2 # Half energy goes to child.

    # Hunting mechanism. Both hunting and running away will cost energy. 
    def hunt(self, organisms_list, area, food_opportunities, initial_speed, initial_sense):

        if not self.living:
            return

        temp_living_list = []
        for o in organisms_list:
            if o.living and o != self:
                temp_living_list.append(o)
        
        # In this simulation, organisms move food_opportunities times a day. This means each organism will take up food_opportunities different area squares per day. 
        base_hunt_prob = (len(temp_living_list)) / area

        if base_hunt_prob > 1:
            base_hunt_prob = 1

        # Calculate num_food_opportunities boost. Based on speed and sense.
        food_opportunities_boost = int(squeeze_with_tanh(((0.5 * self.traits[0] - initial_speed) + (self.traits[2] - initial_sense)) / 2) * food_opportunities)
        new_food_opportunities = food_opportunities + food_opportunities_boost

        # Hunt until first successful hunt
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
                        self.cur_energy += prey.traits[3] + self.cur_energy # Gain energy from eating prey
                        self.cur_energy -= self.traits[5] # Hunt energy cost
                        temp_living_list.remove(prey)

                        break # stop after one successful hunt
                    
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
                        break

    # Gather food mechanism. 2 opportunities to gather food besides hunting, plus any boosts do to traits. 
    def gather_food(self, area, food_count, food_opportunities, initial_speed, initial_sense):
        
        if not self.living:
            return food_count

        base_food_prob = food_count / area

        if base_food_prob > 1:
            base_food_prob = 1
        
        # Calculate num_food_opportunities boost. Based on speed and sense.
        food_opportunities_boost = int(squeeze_with_tanh((0.5 * (self.traits[0] - initial_speed) + (self.traits[2] - initial_sense)) / 2) * food_opportunities)
        new_food_opportunities = food_opportunities + food_opportunities_boost

        for i in range(new_food_opportunities):
            found_food = bernoulli_trial(base_food_prob)
            if found_food:
                self.cur_energy += 1
                food_count -= 1

        return food_count