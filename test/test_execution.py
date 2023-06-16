import os
import copy
import shutil
import unittest
import numpy as np
from creatures import population
from environment import simulator

# Base directories
BASE_DIR = ".tmp/test_execution"        
if os.path.exists(BASE_DIR):
    shutil.rmtree(BASE_DIR)

# Simulation parameters
NUM_OF_PROCESSES  = 10
MAX_SIM_FRAMES    = 2400
NUM_OF_GENERATION = 50

# Generation parameters
DEFAULT_GEN_COUNT = 5
NUM_OF_CR = 20
NUM_OF_ELITES = 5
NUM_OF_RANDOM = 5
MIN_LEN = 2
MAX_LEN = 7
MAX_GROWTH_RT = 1.2
MUTATION_FREQ = 0.15
MUTATION_AMNT = 0.15

class SimulationRunTest(unittest.TestCase):
    
    def testDeterministicNatureForDifferentGenerations(self):
        pop = population.Population(NUM_OF_CR, DEFAULT_GEN_COUNT)
        sim = simulator.MultiSimulator(NUM_OF_PROCESSES)
        sim.eval_population(pop, MAX_SIM_FRAMES)
        
        for _ in range(NUM_OF_GENERATION):
            pop.new_generation(NUM_OF_ELITES,
                               NUM_OF_RANDOM,
                               MIN_LEN,
                               MAX_LEN,
                               MAX_GROWTH_RT,
                               MUTATION_FREQ,
                               MUTATION_AMNT)
            sim.eval_population(pop, MAX_SIM_FRAMES)
            pop.to_csvs(f"{BASE_DIR}/data", "dna")

            old_creatures = []
            old_distances = []
            for cr in pop.creatures:
                old_creatures.append(copy.copy(cr))
                old_distances.append(cr.get_distance())
                del cr
            del pop

            pop = population.Population(1)
            pop.from_csvs(f"{BASE_DIR}/data", "dna")
            
            sim.eval_population(pop, MAX_SIM_FRAMES)
            equal_distances = []
            for i, cr in enumerate(pop.creatures):
                equal_distances.append(cr.get_distance() == old_distances[i])
                
                self.assertEqual(cr.dna.shape, old_creatures[i].dna.shape)
                self.assertTrue((cr.dna == old_creatures[i].dna).all())
                self.assertEqual(cr.get_xml().toprettyxml(), old_creatures[i].get_xml().toprettyxml())
                self.assertEqual(cr.get_distance(), old_creatures[i].get_distance())
            
            self.assertGreaterEqual(np.mean(equal_distances), 1)
            self.assertGreaterEqual(np.min(old_distances), 0)
            
            # print(f"Generation {_}:", end = "\t")
            # print(f"{np.min(old_distances):.2f}", end = " ")
            # print(f"{np.mean(old_distances):.2f}", end = " ")
            # print(f"{np.max(old_distances):.2f}", end = " ")
            # print(f"{np.mean(equal_distances):.2f}", end = "\n")
            
            for cr in old_creatures:
                del cr
    
    def testDeterministicNatureForDifferentSimulators(self):
        pop1 = population.Population(NUM_OF_CR, DEFAULT_GEN_COUNT)
        sim1 = simulator.MultiSimulator(NUM_OF_PROCESSES)
        sim2 = simulator.MultiSimulator(NUM_OF_PROCESSES)

        for _ in range(5):
            sim1.eval_population(pop1, MAX_SIM_FRAMES)
            pop1.new_generation(NUM_OF_ELITES,
                                NUM_OF_RANDOM,
                                MIN_LEN,
                                MAX_LEN,
                                MAX_GROWTH_RT,
                                MUTATION_FREQ,
                                MUTATION_AMNT)

        pop1.to_csvs(f"{BASE_DIR}/data", "dna")

        pop2 = population.Population(1)
        pop2.from_csvs(f"{BASE_DIR}/data", "dna")
        
        sim1.eval_population(pop1, MAX_SIM_FRAMES)
        sim2.eval_population(pop2, MAX_SIM_FRAMES)
        
        equal_distances = []
        for i in range(NUM_OF_CR):
            equal_distances.append(pop1.creatures[i].get_distance() == pop2.creatures[i].get_distance())
        
            self.assertEqual(pop1.creatures[i].dna.shape, pop2.creatures[i].dna.shape)
            self.assertTrue((pop1.creatures[i].dna == pop2.creatures[i].dna).all())
            self.assertEqual(pop1.creatures[i].get_xml().toprettyxml(), pop2.creatures[i].get_xml().toprettyxml())
            self.assertEqual(pop1.creatures[i].get_distance(), pop2.creatures[i].get_distance())
        
        # dists1 = [cr.get_distance() for cr in pop1.creatures]
        # dists2 = [cr.get_distance() for cr in pop2.creatures]
        
        # print(f"Original Population\t:", end = "\t")
        # print(f"{np.min(dists1):.2f}", end = " ")
        # print(f"{np.mean(dists1):.2f}", end = " ")
        # print(f"{np.max(dists1):.2f}")
        
        # print(f"Copied Population\t:", end = "\t")
        # print(f"{np.min(dists2):.2f}", end = " ")
        # print(f"{np.mean(dists2):.2f}", end = " ")
        # print(f"{np.max(dists2):.2f}")

        # print(f"Num of Identical Distances: {np.mean(equal_distances):.2f}")