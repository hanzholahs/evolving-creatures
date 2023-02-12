import unittest
from creatures import population, creature

class PopulationTest(unittest.TestCase):
    def testPopulationCreatures(self):
        pop = population.Population(10, 3)
        self.assertIsNotNone(pop)
        self.assertEqual(len(pop.creatures), 10)
        
        pop.reset_population([creature.Creature(10), creature.Creature(10)])
        self.assertEqual(len(pop.creatures), 2)
        with self.assertRaises(AssertionError):
            pop.reset_population(creature.Creature(10)) # requires a list of crs
        
        pop.add_creature(creature.Creature(20))
        self.assertEqual(len(pop.creatures), 3)
        
        pop.add_creatures([creature.Creature(10), creature.Creature(10)])
        self.assertEqual(len(pop.creatures), 5)

        pop.population_size = 10
        pop.reset_population()
        self.assertEqual(len(pop.creatures), 10)