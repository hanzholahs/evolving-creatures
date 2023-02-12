import unittest
import numpy as np
from creatures import genome, phenotype
from xml.dom.minidom import getDOMImplementation, Element

class BodyPartTest(unittest.TestCase):
    def testBodyPartDefault(self):
        self.assertIsNotNone(phenotype.BodyPart.get_link_shapes)
        self.assertIsNotNone(phenotype.BodyPart.get_joint_types)
        self.assertIsNotNone(phenotype.BodyPart.get_joint_axes)
        self.assertEqual(len(phenotype.BodyPart.get_link_shapes()), 12)
        self.assertEqual(len(phenotype.BodyPart.get_joint_types()), 2)
        self.assertEqual(len(phenotype.BodyPart.get_joint_axes()), 3)

    def testBodyPartXML(self):
        self.assertIsNotNone(phenotype.BodyPart.body_part_xml)

        dna = genome.Genome.init_genome(1)
        g_dicts = genome.Genome.to_dict(dna)
        adom = getDOMImplementation().createDocument(None, "start", None)
        name = "Test"
        parent_name = "NA"
        link_tag, joint_tag = phenotype.BodyPart.body_part_xml(name, parent_name, g_dicts[0], adom)
        self.assertIsNotNone(joint_tag)
        self.assertIsNotNone(link_tag)
        self.assertIsInstance(joint_tag, Element)
        self.assertIsInstance(link_tag, Element)
        
class MotorTest(unittest.TestCase):
    def testMotorOutput(self):
        m = phenotype.Motor(0,  1.57, 0.25, 0.4)
        self.assertEqual(m.motor_type, 0)
        self.assertEqual(m(), 0.25)
        self.assertEqual(m(), 0.25)
        self.assertEqual(m(), -0.25)
        self.assertEqual(m(), -0.25)

        m = phenotype.Motor(1, 1.57, 0.25, 0.4)
        self.assertEqual(m.motor_type, 1)
        self.assertLessEqual(m(), 0)
        self.assertLessEqual(m(), 0)
        self.assertGreaterEqual(m(), 0)
        self.assertGreaterEqual(m(), 0)
        self.assertLessEqual(m(), 0)
        self.assertLessEqual(m(), 0)
        self.assertGreaterEqual(m(), 0)
        self.assertGreaterEqual(m(), 0)

        m = phenotype.Motor(2, 1.57, 0.25, 0.4)
        self.assertEqual(m.motor_type, 2)
        self.assertGreaterEqual(m(), 0)
        self.assertGreaterEqual(m(), 0)
        self.assertLessEqual(m(), 0)
        self.assertLessEqual(m(), 0)