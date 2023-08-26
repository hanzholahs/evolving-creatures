import os
import copy
import shutil
import unittest
import numpy as np
from app import app, simulator
from creatures import population

class AppTest(unittest.TestCase):
    def testClassExists(self):
        self.assertIsNotNone(app.MainApp)
        
        
    def testAppCanRun(self):
        self.assertIsNotNone(app.MainApp.reset_population)
        self.assertIsNotNone(app.MainApp.build_simulator)
        self.assertIsNotNone(app.MainApp.run)
        
        main = app.MainApp(".tmp/simulation-test-consistency")
        self.assertIsNotNone(main)
        self.assertIsNotNone(main.sim)
        self.assertIsNotNone(main.pop)
        self.assertEqual(type(main.sim), simulator.MultiSimulator)
        self.assertEqual(type(main.pop), population.Population)
        self.assertEqual(len(main.sim.sims), 5)
        self.assertEqual(len(main.pop.creatures), 5)
        
        sim_type_1 = type(main.sim)
        main.multiprocess = False
        main.pool_size = 1
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
    
    
    def testMultiprocessAndPoolSizeConsistency(self):
        main = app.MainApp(".tmp/simulation-test-consistency")
        
        with self.assertRaises(Exception) as context:
            main.build_simulator(multiprocess = True, pool_size = 1)
        with self.assertRaises(Exception) as context:
            main.build_simulator(multiprocess = True, pool_size = 1)
        
        
    def testAppSavePopulation(self):
        self.assertIsNotNone(app.MainApp.save_population)
        
        base_dir  = ".tmp/simulation-test-save"
        pop_size  = 10
        num_gens  = 5
        save_each = 1
        
        if os.path.exists(base_dir): shutil.rmtree(base_dir)
        
        main = app.MainApp(base_dir = base_dir, population_size = pop_size, num_of_generation = num_gens)
        self.assertTrue(os.path.exists(base_dir))
        self.assertEqual(len(os.listdir(base_dir + "/pop/0")), pop_size)
        
        main.run(save_after = True,
                 save_each = save_each)
        self.assertEqual(len(os.listdir(base_dir + "/pop")), num_gens + 1) # +1 for initialization and after simulation
        
        for i in range(num_gens + 1): # +1 for initialization and after simulation
            self.assertEqual(len(os.listdir(f"{base_dir}/pop/{i}")), pop_size)
        
        
    def testAppLoadPopulation(self):
        self.assertIsNotNone(app.MainApp.load_population)
        
        old_creatures = []
        base_dir = ".tmp/simulation-test-load"
        pop_size = 5
        num_gens = 5
        
        if os.path.exists(base_dir): shutil.rmtree(base_dir)
        
        main = app.MainApp(base_dir = base_dir, population_size = pop_size, num_of_generation = num_gens)
        main.run(save_after = True)
        
        main.multiprocess = False
        main.pool_size = 1
        main.build_simulator()
        
        for cr in main.pop.creatures:
            old_creatures.append(cr)
            del cr
        del main.sim
        del main.pop
        del main
        
        new = app.MainApp(base_dir = base_dir, population_size = pop_size)
        new.load_population()
        for i, cr in enumerate(new.pop.creatures):
            self.assertTrue((cr.dna == old_creatures[i].dna).all())
        
            
    def testAppGenerateReports(self):
        self.assertIsNotNone(app.MainApp.generate_report)
        base_dir  = ".tmp/simulation-test-run"
        pop_size  = 5
        num_gens  = 5
        
        if os.path.exists(base_dir): shutil.rmtree(base_dir)
        
        main = app.MainApp(base_dir = base_dir, num_of_generation=num_gens, population_size = pop_size)
        main.run(save_after = True, report_after = True, save_each = 1, report_each = 1, log_each = 1)
    
        self.assertTrue(os.path.exists(os.path.join(base_dir, "report")))
        self.assertEqual(len(os.listdir(os.path.join(base_dir, "report"))), num_gens + 1) # +1 for initialization and after simulation
    
    
    def testContinousRun(self):
        base_dir  = ".tmp/simulation-test-run"
        pop_size  = 5
        
        if os.path.exists(base_dir): shutil.rmtree(base_dir)
        
        for i in range(5):
            num_gens = i + 1
        
            main1 = app.MainApp(base_dir = base_dir, population_size = pop_size,  num_of_generation = num_gens, pool_size = 8)
            main1.run(save_after = True, save_each = 1, log_each = 1)
            
            main2 = app.MainApp(base_dir = base_dir, population_size = pop_size, num_of_generation = num_gens, pool_size = 8,
                                load_progress = True)
            main2.run(save_after = True, save_each = 1, log_each = 1)
            
            main3 = app.MainApp(base_dir = base_dir, population_size = pop_size, num_of_generation = num_gens, pool_size = 1,
                                multiprocess = False, load_progress = True)
            main3.run(save_after = True, report_after = True, save_each = 1, report_each = 1, log_each = 1)
            
            for i in range(pop_size):
                self.assertEqual(main1.pop.creatures[i].dna.shape, main2.pop.creatures[i].dna.shape)
                self.assertTrue((main1.pop.creatures[i].dna == main2.pop.creatures[i].dna).all())
                self.assertEqual(main2.pop.creatures[i].dna.shape, main3.pop.creatures[i].dna.shape)
                self.assertTrue((main2.pop.creatures[i].dna == main3.pop.creatures[i].dna).all())
        
            pop_dir = os.path.join(base_dir, "pop", str(num_gens))
            self.assertTrue(os.path.exists(pop_dir))
            self.assertEqual(len(os.listdir(pop_dir)), pop_size)
            
            report_dir = os.path.join(base_dir, "report")
            self.assertTrue(os.path.exists(report_dir))
            self.assertEqual(len(os.listdir(report_dir)), (num_gens) + 1)