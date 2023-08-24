import unittest
import numpy as np
from app import simulator
from creatures import creature, population

class SimulatorTest(unittest.TestCase):
    def testSimulatorForCreature(self):
        self.assertIsNotNone(simulator.Simulator)
        self.assertIsNotNone(simulator.Simulator.run_creature)
        self.assertIsNotNone(simulator.Simulator.eval_population)

        for _ in range(5):
            cr = creature.Creature(5) 
            pos1 = cr.last_position
            dis1 = cr.get_distance()

            sim = simulator.Simulator()
            self.assertIsNotNone(sim)

            sim.run_creature(cr)
            pos2 = cr.last_position
            dis2 = cr.get_distance()
            self.assertNotEqual(pos1, pos2)
            self.assertNotEqual(dis1, dis2)
            self.assertLessEqual(dis1, dis2)

    def testSimulatorForPopulation(self):
        pop = population.Population(5)
        sim = simulator.Simulator()

        for cr in pop.creatures:
            sim.run_creature(cr)        
        dists1 = np.array([cr.get_distance() for cr in pop.creatures])

        sim.eval_population(pop)
        dists2 = np.array([cr.get_distance() for cr in pop.creatures])

        self.assertEqual(np.mean(0 <= dists1), 1)
        self.assertEqual(np.mean(0 <= dists2), 1)

    def testMultiSimulator(self):
        self.assertIsNotNone(simulator.MultiSimulator)
        
        pop = population.Population(5)
        sim = simulator.MultiSimulator(5)
        self.assertIsNotNone(sim)
        
        sim.eval_population(pop)
        dists2 = np.array([cr.get_distance() for cr in pop.creatures])
        self.assertEqual(np.mean(0 <= dists2), 1)        

    def testExtremeLengthPopulation(self):
        pop_size = 15
    
        pop = population.Population(pop_size, 5)
        sim = simulator.Simulator(5)
        
        for _ in range(10):
            sim.eval_population(pop)
            pop.new_generation()