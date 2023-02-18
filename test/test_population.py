import unittest
import numpy as np
from creatures import population, creature, genome

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

        pop = population.Population(pop_size, 3)

        for cr in pop.creatures:
            cr.last_position = (np.random.normal(),
                                np.random.normal(),
                                np.random.normal())
            
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
        
        # fits = evolution.Selection.eval_fitness(pop.creatures)
        pass