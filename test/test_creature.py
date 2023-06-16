import os
import unittest
from creatures import creature, genome
from xml.dom.minidom import Element

class CreatureLinksTest(unittest.TestCase):
         
    def testCreatureGenomeToLinks(self):
        self.assertIsNotNone(creature.Creature.genome_to_links)

        dna = genome.Genome.init_genome(5)
        g_dicts = genome.Genome.to_dict(dna)

        links = creature.Creature.genome_to_links(g_dicts)
        self.assertIsNotNone(links)
        self.assertEqual(len(links), len(g_dicts))
        self.assertEqual(type(links[0]), creature.CreatureLink)
        self.assertEqual(links[0].parent_name, "None")
        self.assertEqual(links[0].recur, 1)
        self.assertEqual(links[0].name, links[1].parent_name)
        self.assertEqual(links[-2].name, links[-1].parent_name)

    def testCreatureFlatLinks(self):
        self.assertIsNotNone(creature.Creature.get_flat_links)

        cr = creature.Creature(5)
        self.assertIsNotNone(cr)
        
        flat_links = cr.get_flat_links()
        self.assertEqual(len(flat_links), 5)
        self.assertEqual(type(flat_links[0]), creature.CreatureLink)
        self.assertEqual(flat_links[0].parent_name, "None")
        self.assertEqual(flat_links[0].recur, 1)
        self.assertEqual(flat_links[0].name, flat_links[1].parent_name)
        self.assertEqual(flat_links[-2].name, flat_links[-1].parent_name)
        
    def testCreatureExpandedLinks(self):
        self.assertIsNotNone(creature.Creature.expand_links)
        self.assertIsNotNone(creature.Creature.get_expanded_links)
        
        for _ in range(10):
            cr = creature.Creature(5)
            flat_links = cr.get_flat_links()
            exp_links = creature.Creature.expand_links(flat_links)

            # manually count the number of links in expanded link list
            link_count = 1
            last_count = 1
            for i in range(1, len(flat_links)):
                last_count = last_count * flat_links[i].recur
                link_count += last_count

            self.assertIsNotNone(exp_links)
            self.assertEqual(type(exp_links), list)
            self.assertEqual(type(flat_links[0]), creature.CreatureLink)
            self.assertEqual(type(flat_links[-1]), creature.CreatureLink)
            self.assertEqual(type(exp_links[0]), creature.CreatureLink)
            self.assertEqual(type(exp_links[-1]), creature.CreatureLink)
            self.assertEqual(link_count, len(exp_links))
            self.assertGreaterEqual(len(exp_links), len(flat_links))
    
        for _ in range(10):
            cr = creature.Creature(5)
            flat_links = cr.get_flat_links()
            exp_links = cr.get_expanded_links()

            # manually count the number of links in expanded link list
            link_count = 1
            last_count = 1
            for i in range(1, len(flat_links)):
                last_count = last_count * flat_links[i].recur
                link_count += last_count

            self.assertIsNotNone(exp_links)
            self.assertEqual(type(exp_links), list)
            self.assertEqual(type(flat_links[0]), creature.CreatureLink)
            self.assertEqual(type(flat_links[-1]), creature.CreatureLink)
            self.assertEqual(type(exp_links[0]), creature.CreatureLink)
            self.assertEqual(type(exp_links[-1]), creature.CreatureLink)
            self.assertEqual(link_count, len(exp_links))
            self.assertGreaterEqual(len(exp_links), len(flat_links))

class CreatureXMLTest(unittest.TestCase):

    def testCreatureXML(self):
        cr = creature.Creature(5)
        robot_tag = cr.get_xml()

        self.assertIsNotNone(robot_tag)
        self.assertIsInstance(robot_tag, Element)

    def testCreatureWriteXML(self):
        file_path = ".tmp/test_motors.urdf"
        cr = creature.Creature(5)
        cr.write_xml(file_path)
        self.assertTrue(os.path.exists(file_path))

        with open(file_path) as f:
            f_str= f.read()

        self.assertEqual(f_str, cr.get_xml().toprettyxml())
        os.remove(file_path)

class CreatureMoveTest(unittest.TestCase):
    def testMovingDistance(self):
        self.assertIsNotNone(creature.Creature.update_position)
        self.assertIsNotNone(creature.Creature.get_distance)

        cr = creature.Creature(2)
        self.assertEqual(0, cr.get_distance())
        self.assertEqual(cr.start_position, (0, 0, 0))
        self.assertEqual(cr.last_position, (0, 0, 0))

        cr.update_position((0, 0, 1))
        self.assertGreater(cr.get_distance(), 0)
        self.assertEqual(cr.start_position, (0, 0, 0))
        self.assertEqual(cr.last_position, (0, 0, 1))