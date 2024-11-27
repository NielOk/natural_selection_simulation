'''
This is the class definition of an organism in the natural selection simulation. 
'''

class organism():

    # Each organism is a tuple, with element 0 = speed, 1 = size, 2 = sense, 3 = energy, 4 = required energy, 5 = hunt energy, 6 = run energy. Initiailization takes in initial values for each of these parameters. We only initialize if this organism is not in the living list and we are at a new generation. 
    def __init__(self, speed_0, size_0, sense_0, energy_0, required_energy_0, hunt_energy_0, run_energy_0, living_ids_list, living_traits_list, cur_organism_amount):
        self.traits = [speed_0, size_0, sense_0, energy_0, required_energy_0, hunt_energy_0, run_energy_0]
        self.food_opportunities = 3
        self.id = cur_organism_amount

        living_ids_list.append(self.id)
        living_traits_list.append(self.traits)

    def reproduce(self):
        pass

    

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