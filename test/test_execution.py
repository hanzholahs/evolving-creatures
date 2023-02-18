import unittest
import numpy as np
from creatures import population
from environment import simulator

# Generation parameters
DEFAULT_GEN_COUNT = 5
NUM_OF_CR = 20
NUM_OF_ELITES = 3
NUM_OF_RANDOM = 3
MIN_LEN = 2
MAX_LEN = 7
MAX_GROWTH_RT = 1.2
MUTATION_FREQ = 0.15
MUTATION_AMNT = 0.15

# Simulation parameters
NUM_OF_PROCESSES  = 10
MAX_SIM_FRAMES    = 2400
NUM_OF_GENERATION = 30

def is_arr_equal(arr1:np.ndarray, arr2:np.ndarray):
    if not arr1.shape == arr2.shape:
        return False
    else:
        return np.equal(arr1, arr2).all()


class SimulationRunTest(unittest.TestCase):
    def testSimRun(self):
        pop = population.Population(NUM_OF_CR, DEFAULT_GEN_COUNT)
        sim = simulator.MultiSimulator(NUM_OF_PROCESSES)
        sim.eval_population(pop, MAX_SIM_FRAMES)

        equality_data = []
        equality_dist = []
        old_data = [cr.dna for cr in pop.creatures]
        old_dist = [cr.get_distance() for cr in pop.creatures]

        for _ in range(NUM_OF_GENERATION):            
            pop.new_generation(
                NUM_OF_ELITES,
                NUM_OF_RANDOM,
                MIN_LEN,
                MAX_LEN,
                MAX_GROWTH_RT,
                MUTATION_FREQ,
                MUTATION_AMNT
            )

            sim.eval_population(pop, MAX_SIM_FRAMES)
            
            new_data = [cr.dna for cr in pop.creatures]
            new_dist = [cr.get_distance() for cr in pop.creatures]

            for i in range(len(new_data)):
                equality_data.append(is_arr_equal(np.asarray(old_data[i]), np.asarray(new_data[i])))
                equality_dist.append(old_dist[i] == new_dist[i])

            self.assertLess(np.mean(equality_data), 0.1)
            self.assertLess(np.mean(equality_dist), 0.1)

            # print(f"{_}\t{np.mean(new_dist):.2f}\t{np.min(new_dist):.2f}\t{np.max(new_dist):.2f}")