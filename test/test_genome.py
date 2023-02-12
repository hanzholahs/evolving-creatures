import unittest
import numpy as np
from creatures import genome

class GenotypeTest(unittest.TestCase):
    def testGenotypeRandomInitializer(self):
        self.assertIsNotNone(genome.Genome.init_genome)
        
        dna = genome.Genome.init_genome(5, 10)
        self.assertEqual(dna.shape, (5, 10))
        self.assertIsInstance(dna, np.ndarray)

        for _ in range(10):
            gene_length = np.random.randint(5, 10)
            dna = genome.Genome.init_genome(gene_length)
            self.assertIsNotNone(dna)
            self.assertIsNotNone(dna[0])
            self.assertIsNotNone(dna[0][0])
            self.assertEqual(dna.shape[1], len(genome.Genome.get_spec()))

    def testGenotypeSpecification(self):
        self.assertIsNotNone(genome.Genome.set_spec)
        self.assertIsNotNone(genome.Genome.get_spec)
        self.assertIsInstance(genome.Genome.set_spec(), dict)
        self.assertIsInstance(genome.Genome.get_spec(), dict)

        spec = genome.Genome.get_spec()

        for key in spec.keys():
            self.assertEqual(type(spec[key]), dict)
            self.assertIn("scale", spec[key].keys())
            self.assertIn("type", spec[key].keys())
            self.assertIn("index", spec[key].keys())
            self.assertIn(spec[key]["type"], ["discrete", "continuous", "categorical"])

        self.assertEqual(spec["link_shape"]["type"], "categorical")
        self.assertEqual(spec["link_recurrence"]["type"], "discrete")
        self.assertEqual(spec["joint_origin_xyz_3"]["type"], "continuous")

    def testGenotypeToDictionary(self):
        self.assertIsNotNone(genome.Genome.to_dict)

        spec = genome.Genome.get_spec()
        dna = genome.Genome.init_genome(10)
        g_dicts = genome.Genome.to_dict(dna)
        self.assertEqual(dna.shape[0], len(g_dicts))
        self.assertEqual(dna.shape[1], len(spec))

        for d in g_dicts:
            self.assertIsInstance(d, dict)
            self.assertEqual(len(d), len(spec))
            self.assertIn("link_shape", d.keys())
            self.assertIn("link_recurrence", d.keys())
            self.assertIn("joint_axis_xyz", d.keys())
            self.assertIn("control_motor_type", d.keys())
            self.assertIsInstance(d["link_shape"], int)
            self.assertIsInstance(d["link_recurrence"], int)
            self.assertIsInstance(d["joint_type"], int)
            self.assertIsInstance(d["control_motor_type"], int)

