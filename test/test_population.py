import os
import shutil
import unittest
import numpy as np
from creatures import population, evolution, genome, creature

class PopulationTest(unittest.TestCase):

    def testPopulationCreatures(self):
        self.assertIsNotNone(population.Population)
        self.assertIsNotNone(population.Population.add_creature)
        self.assertIsNotNone(population.Population.add_creatures)

        pop = population.Population(10, 3)
        self.assertIsNotNone(pop)
        self.assertEqual(len(pop.creatures), 10)
        
        pop.reset_population([creature.Creature(10), creature.Creature(10)])
        self.assertEqual(len(pop.creatures), 2)
        with self.assertRaises(AssertionError):
            # `reset_population` method requires a list of crs
            pop.reset_population(creature.Creature(10)) 
        
        pop.add_creature(creature.Creature(20))
        self.assertEqual(len(pop.creatures), 3)
        
        pop.add_creatures([creature.Creature(10), creature.Creature(10)])
        self.assertEqual(len(pop.creatures), 5)

    def testResetPopulation(self):
        self.assertIsNotNone(population.Population.reset_population)

        pop = population.Population(5, 3)
        dna1 = pop.creatures[0].dna

        for pop_size in range(1, 20):
            pop.population_size = pop_size
            pop.reset_population()
            dna2 = pop.creatures[0].dna
            self.assertEqual(len(pop.creatures), pop_size)
            self.assertTrue((dna1 != dna2).all())

    def testReadWritePopulation(self):
        num_cr = 10
        base_dir = ".tmp/test_population"
        
        pop1 = population.Population(num_cr, 5)
        pop1.to_csvs(f"{base_dir}/data", "dna")
        pop2 = population.Population(1)
        pop2.from_csvs(f"{base_dir}/data", "dna")
        self.assertEqual(len(pop1.creatures), len(pop2.creatures))
        
        for i in range(num_cr):
            # creatures have identical dna
            dna1 = pop1.creatures[i].dna
            dna2 = pop2.creatures[i].dna
            self.assertTrue(np.all(dna1 == dna2))
            
            # creatures have identical xml string
            xml1 = pop1.creatures[i].get_xml().toprettyxml()
            xml2 = pop2.creatures[i].get_xml().toprettyxml()
            self.assertEqual(xml1, xml2)
            
            # creatures have identical motors
            motors1 = pop1.creatures[i].get_motors()
            motors2 = pop2.creatures[i].get_motors()
            self.assertEqual(len(motors1), len(motors2))
            for j in range(len(motors1)):
                self.assertEqual(motors2[j].motor_type, motors1[j].motor_type)
                self.assertEqual(motors2[j].step_size, motors1[j].step_size)
                self.assertEqual(motors2[j].amplitude, motors1[j].amplitude)
                self.assertEqual(motors2[j].param1, motors1[j].param1)
                self.assertEqual(motors2[j].param2, motors1[j].param2)
                self.assertEqual(motors2[j].phase, motors1[j].phase)
        
        shutil.rmtree(base_dir)

    def testNewGeneration(self):
        self.assertIsNotNone(population.Population.new_generation)

        pop_size = 50
        num_of_elites = 5
        num_of_random = 5
        min_length = 2
        max_length = 10
        max_growth_rt = 1.5
        mutation_freq = 0.15
        mutation_amnt = 0.15
        rand = np.random.normal
    
        pop = population.Population(pop_size, 3)
        for cr in pop.creatures:
            cr.last_position = (rand(), rand(), rand())
            
        for _ in range(15):
            pop.new_generation(
                num_of_elites = num_of_elites,
                num_of_random = num_of_random,
                min_length = min_length,
                max_length = max_length,
                max_growth_rt = max_growth_rt,
                mutation_freq = mutation_freq,
                mutation_amnt = mutation_amnt,
            )
            self.assertEqual(len(pop.creatures), pop_size)
            for cr in pop.creatures:
                self.assertEqual(cr.dna.shape[1], len(genome.Genome.get_spec()))
            
        with self.assertRaises(AssertionError):
            pop.new_generation(
                num_of_elites = num_of_elites,
                num_of_random = num_of_random,
                min_length = 100,
                max_length = max_length,
                max_growth_rt = max_growth_rt,
                mutation_freq = mutation_freq,
                mutation_amnt = mutation_amnt,
            )
                        
        with self.assertRaises(AssertionError):
            pop.new_generation(
                num_of_elites = num_of_elites,
                num_of_random = num_of_random,
                min_length = min_length,
                max_length = max_length,
                max_growth_rt = -1,
                mutation_freq = mutation_freq,
                mutation_amnt = mutation_amnt,
            )
                        
        with self.assertRaises(AssertionError):
            pop.new_generation(
                num_of_elites = num_of_elites,
                num_of_random = num_of_random,
                min_length = min_length,
                max_length = max_length,
                max_growth_rt = max_growth_rt,
                mutation_freq = 2,
                mutation_amnt = mutation_amnt,
            )
                        
        with self.assertRaises(AssertionError):
            pop.new_generation(
                num_of_elites = 100,
                num_of_random = num_of_random,
                min_length = min_length,
                max_length = max_length,
                max_growth_rt = max_growth_rt,
                mutation_freq = mutation_freq,
                mutation_amnt = mutation_amnt,
            )