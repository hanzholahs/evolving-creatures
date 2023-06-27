import unittest
import numpy as np
from app import app, simulator
from creatures import population

class AppTest(unittest.TestCase):
    def testClassExists(self):
        self.assertIsNotNone(app.MainApp)
        self.assertIsNotNone(app.MainApp.reset_population)
        self.assertIsNotNone(app.MainApp.build_simulator)
        self.assertIsNotNone(app.MainApp.run)
        
        main = app.MainApp()
        self.assertIsNotNone(main)
        self.assertIsNotNone(main.sim)
        self.assertIsNotNone(main.pop)
        self.assertEqual(type(main.sim), simulator.MultiSimulator)
        self.assertEqual(type(main.pop), population.Population)
        self.assertEqual(len(main.sim.sims), 5)
        self.assertEqual(len(main.pop.creatures), 5)
        
        sim_type_1 = type(main.sim)
        main.multiprocess = False
        main.build_simulator()
        sim_type_2 = type(main.sim)
        
        main.run()
        dists_1 = [cr.get_distance() for cr in main.pop.creatures]
        main.reset_population()
        dists_2 = [cr.get_distance() for cr in main.pop.creatures]

        self.assertEqual(sim_type_1, simulator.MultiSimulator)
        self.assertEqual(sim_type_2, simulator.Simulator)
        self.assertGreater(np.sum(dists_1), 0)
        self.assertEqual(np.sum(dists_2), 0)