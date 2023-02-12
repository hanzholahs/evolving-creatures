import unittest
import copy
import numpy as np
from creatures import creature, population, genome, evolution

class SelectionTest(unittest.TestCase):
    def testSelectionClass(self):
        self.assertIsNotNone(evolution.Selection)
    
    def testFitnessFunction(self):
        pop_size = 50
        pop = population.Population(pop_size)
        
        for cr in pop.creatures:
            cr.last_position = (np.random.randint(-10, 10),
                                np.random.randint(-10, 10),
                                np.random.randint(-10, 10))
        
        fits = evolution.Selection.eval_fitness(pop.creatures)

        self.assertEqual(len(fits), pop_size)
        self.assertIsInstance(fits, np.ndarray)
        self.assertEqual(np.mean(fits >= 0), 1)

    def testFitnessEvaluationScenarioDiffLength(self):
        cr_1 = creature.Creature(10)
        cr_1.start_position = (0, 0, 0)
        cr_1.last_position  = (10, 100, 0)
        
        cr_2 = creature.Creature(5)
        cr_2.start_position = (0, 0, 0)
        cr_2.last_position  = (10, 100, 0)

        fits = evolution.Selection.eval_fitness([cr_1, cr_2])
        self.assertLess(fits[0], fits[1])
    
    def testFitnessEvaluationScenarioDiffDist(self):
        cr_1 = creature.Creature(5)
        cr_1.last_position  = (100, 100, 0)
        cr_2 = copy.copy(cr_1) 
        cr_2.last_position  = (100, 120, 0)
        cr_3 = copy.copy(cr_1) 
        cr_3.last_position  = (120, 100, 0)
        cr_4 = copy.copy(cr_1) 
        cr_4.last_position  = (120, 120, 0)

        fits = evolution.Selection.eval_fitness([cr_1, cr_2, cr_3, cr_4])
        self.assertLess(fits[0], fits[1])
        self.assertLess(fits[0], fits[2])
        self.assertLess(fits[1], fits[2])

    def testParentSelection(self):
        self.assertIsNotNone(evolution.Selection.select_parents)
        fits = [1, 1, 1, 2, 5]
        parents = ["A", "B", "C", "D", "E"]

        for _ in range(5):            
            p1, p2 = evolution.Selection.select_parents(parents, fits)
            self.assertIn(p1, parents)
            self.assertIn(p2, parents)
            self.assertNotEqual(p1, p2)

class MatingTest(unittest.TestCase):
    def testMatingClass(self):
        self.assertIsNotNone(evolution.Mating)
        self.assertIsNotNone(evolution.Mating.mate_crossover)
        self.assertIsNotNone(evolution.Mating.mate_grafting)

    def testGraftingGenes(self):
        gene_1 = genome.Genome.init_genome(10)
        gene_2 = genome.Genome.init_genome(10)
        for _ in range(15):
            child_gene = evolution.Mating.mate_grafting(gene_1, gene_2)
            self.assertIsNotNone(child_gene)
            self.assertGreater(len(child_gene), 1)
            self.assertLess(len(child_gene), len(gene_1) + len(gene_2))
        
        genome_1 = genome.Genome.init_genome(10, 10)
        genome_2 = genome.Genome.init_genome(10, 10)
        for _ in range(15):
            child_genome = evolution.Mating.mate_grafting(genome_1, genome_2)
            self.assertIsNotNone(child_genome)
            self.assertGreater(len(child_genome), 1)
            self.assertLess(len(child_genome), len(genome_1) + len(genome_2))

    def testCrossoverGenes(self):
        gene_1 = genome.Genome.init_genome(10)
        gene_2 = genome.Genome.init_genome(10)
        for _ in range(15):
            child_gene = evolution.Mating.mate_crossover(gene_1, gene_2)
            self.assertIsNotNone(child_gene)
            self.assertGreater(len(child_gene), 1)
            self.assertLess(len(child_gene), len(gene_1) + len(gene_2))
        
        genome_1 = genome.Genome.init_genome(10, 10)
        genome_2 = genome.Genome.init_genome(10, 10)
        for _ in range(15):
            child_genome = evolution.Mating.mate_crossover(genome_1, genome_2)
            self.assertIsNotNone(child_genome)
            self.assertGreater(len(child_genome), 1)
            self.assertLess(len(child_genome), len(genome_1) + len(genome_2))
        
class MutationTest(unittest.TestCase):
    def testMutationClass(self):
        self.assertIsNotNone(evolution.Mutation)
        self.assertIsNotNone(evolution.Mutation.mutate_point)
        self.assertIsNotNone(evolution.Mutation.mutate_shrink)
        self.assertIsNotNone(evolution.Mutation.mutate_grow)
    
    def testPointMutation(self):
        dna = genome.Genome.init_genome(10, 25)
        rate = 0.25
        for _ in range(15):
            mutated_dna = evolution.Mutation.mutate_point(dna, mutation_freq = rate)
            self.assertEqual(np.mean(mutated_dna <= 1), 1)
            self.assertEqual(np.mean(mutated_dna >= 0), 1)
            self.assertEqual(dna.shape, mutated_dna.shape)
            self.assertTrue(np.mean(dna == mutated_dna) < (1 - rate + 3 * rate))
            self.assertTrue(np.mean(dna == mutated_dna) > (1 - rate - 3 * rate))

        mutated_dna = evolution.Mutation.mutate_point(dna, 0)
        self.assertTrue(np.mean(dna == mutated_dna) == 1)

        mutated_dna = evolution.Mutation.mutate_point(dna, 1)
        self.assertTrue(np.mean(dna != mutated_dna) > .95)
        
    def testShrinkMutation(self):
        dna = genome.Genome.init_genome(25, 5)
        rate = 0.25
        for _ in range(15):
            mutated_dna = evolution.Mutation.mutate_shrink(dna, mutation_freq = rate)
            self.assertLessEqual(len(mutated_dna), len(dna))
            self.assertEqual(mutated_dna.shape[1], dna.shape[1])
            self.assertTrue(len(mutated_dna) / len(dna) < (1 - rate + 3 * rate))
            self.assertTrue(len(mutated_dna) / len(dna) > (1 - rate - 3 * rate))

        mutated_dna = evolution.Mutation.mutate_shrink(dna, mutation_freq = 1)
        self.assertTrue(len(mutated_dna) == 2)
        
        mutated_dna = evolution.Mutation.mutate_shrink(dna, mutation_freq = 0)
        self.assertTrue(len(mutated_dna) == len(dna))
        self.assertTrue(np.mean(dna == mutated_dna) == 1)
                    
    def testGrowMutation(self):
        dna = genome.Genome.init_genome(5, 5)
        rate = 0.25
        for _ in range(15):
            mutated_dna = evolution.Mutation.mutate_grow(dna, mutation_freq = rate)
            self.assertGreaterEqual(len(mutated_dna), len(dna))
            self.assertEqual(mutated_dna.shape[1], dna.shape[1])
            self.assertTrue(len(mutated_dna) / len(dna) < (1 + rate + 3 * rate))
            self.assertTrue(len(mutated_dna) / len(dna) > (1 + rate - 3 * rate))

        mutated_dna = evolution.Mutation.mutate_grow(dna, mutation_freq = 1)
        self.assertTrue(len(mutated_dna) == 2 * len(dna))
        self.assertEqual(mutated_dna.shape[1], dna.shape[1])
        self.assertEqual(np.mean(mutated_dna[0] == mutated_dna[len(dna)]), 1)
        
        mutated_dna = evolution.Mutation.mutate_grow(dna, mutation_freq = 0)
        self.assertTrue(len(mutated_dna) == len(dna))
        self.assertEqual(mutated_dna.shape[1], dna.shape[1])
        self.assertTrue(np.mean(dna == mutated_dna) == 1)