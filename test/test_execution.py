import unittest
import os
import copy
import numpy as np
from creatures import population, creature
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
NUM_OF_GENERATION = 10

def is_arr_equal(arr1:np.ndarray, arr2:np.ndarray):
    if not arr1.shape == arr2.shape:
        return False
    else:
        return np.equal(arr1, arr2).all()


class SimulationRunTest(unittest.TestCase):
    def testDeterministicNature(self):
        pop = population.Population(10)
        sim = simulator.Simulator()
        sim.eval_population(pop)
        old_dists = [cr.get_distance() for cr in pop.creatures]
        for _ in range(10):
            sim.eval_population(pop)
            for i, cr in enumerate(pop.creatures):
                self.assertNotEqual(cr.get_distance(), old_dists[i])
        
    def testSimRun(self):
        pop = population.Population(NUM_OF_CR, DEFAULT_GEN_COUNT)
        sim = simulator.MultiSimulator(NUM_OF_PROCESSES)
        sim.eval_population(pop, MAX_SIM_FRAMES)

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
            
            # print(f"{_}\t{np.mean(new_dist):.2f}\t{np.min(new_dist):.2f}\t{np.max(new_dist):.2f}")

            pop.to_csvs(".tmp/testsim/data", "dna")
            pop.generate_report(NUM_OF_GENERATION, ".tmp/testsim/report")
            self.assertTrue(os.path.exists(".tmp/data"))

            old_creatures = []
            old_distances = []
            for cr in pop.creatures:
                old_creatures.append(copy.copy(cr))
                old_distances.append(cr.get_distance())
                del cr
            del pop

            pop = population.Population(1)
            pop.from_csvs(".tmp/testsim/data", "dna")
            for i, cr in enumerate(pop.creatures):
                self.assertEqual(cr.dna.shape, old_creatures[i].dna.shape)
                self.assertTrue((cr.dna == old_creatures[i].dna).all())
                self.assertEqual(cr.get_xml().toprettyxml(), old_creatures[i].get_xml().toprettyxml())
                # self.assertEqual(cr.get_distance(), old_distances[i])