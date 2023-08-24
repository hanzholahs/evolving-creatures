import os
import unittest
from creatures import creature, genome
from xml.dom.minidom import Element

class CreatureLinksTest(unittest.TestCase):
         
    def testCreatureFlatLinks(self):
        self.assertIsNotNone(creature.Creature.genome_to_links)
        self.assertIsNotNone(creature.Creature.get_flat_links)

        cr = creature.Creature(5)
        self.assertIsNotNone(cr)
        
        flat_links = cr.get_flat_links()
        link_names = [link.name for link in flat_links]
        self.assertEqual(len(flat_links), 5)
        self.assertEqual(type(flat_links[0]), creature.CreatureLink)
        self.assertEqual(flat_links[0].parent_name, "None")
        self.assertEqual(flat_links[0].recur, 1)
        self.assertIn(flat_links[0].name, link_names)
        self.assertIn(flat_links[-2].name, link_names)
        
    def testCreatureExpandedLinks(self):
        cr = creature.Creature(5)
        
        flat_links = [
            creature.CreatureLink("Link_0", None, "None", 1),
            creature.CreatureLink("Link_1", None, "Link_0", 3),
            creature.CreatureLink("Link_2", None, "Link_0", 1),
            creature.CreatureLink("Link_3", None, "Link_1", 1),
            creature.CreatureLink("Link_4", None, "Link_1", 2),
        ]
        
        # flat_links = cr.get_flat_links()
        exp_links = cr.expand_links(flat_links)
        self.assertEqual(len(exp_links), 14)
        self.assertEqual(exp_links[0].parent_name, "None")
        self.assertEqual(exp_links[-1].parent_name, "Link_1_2__ID_3")
        self.assertEqual(exp_links[5].parent_name, "Link_1_0__ID_1")
        
        for i, link in enumerate(exp_links):
            self.assertTrue(link.name.endswith(str(i)))
        
    def testCreatureExpandedLinksExtensive(self):
        self.assertIsNotNone(creature.Creature.expand_links)
        self.assertIsNotNone(creature.Creature.get_expanded_links)
        
        for _ in range(10):
            cr = creature.Creature(5)
            flat_links = cr.get_flat_links()
            exp_links = creature.Creature.expand_links(flat_links)

            # manually count the number of links in expanded link list
            parent_recur = 1
            exp_links_count = 0
            for link in flat_links:
                if link.parent_name != "None":
                    parents = [l for l in flat_links if l.name == link.parent_name]
                    parent_recur = parents[0].recur
                exp_links_count += link.recur * parent_recur
            # link_count = 1
            # last_count = 1
            # for i in range(1, len(flat_links)):
            #     last_count = last_count * flat_links[i].recur
            #     link_count += last_count

            self.assertIsNotNone(exp_links)
            self.assertEqual(type(exp_links), list)
            self.assertEqual(type(flat_links[0]), creature.CreatureLink)
            self.assertEqual(type(flat_links[-1]), creature.CreatureLink)
            self.assertEqual(type(exp_links[0]), creature.CreatureLink)
            self.assertEqual(type(exp_links[-1]), creature.CreatureLink)
            self.assertEqual(exp_links_count, len(exp_links))
            self.assertGreaterEqual(len(exp_links), len(flat_links))
    
        for _ in range(10):
            cr = creature.Creature(5)
            flat_links = cr.get_flat_links()
            exp_links = cr.get_expanded_links()

            # manually count the number of links in expanded link list
            parent_recur = 1
            exp_links_count = 0
            for link in flat_links:
                if link.parent_name != "None":
                    parents = [l for l in flat_links if l.name == link.parent_name]
                    parent_recur = parents[0].recur
                exp_links_count += link.recur * parent_recur
                
            self.assertIsNotNone(exp_links)
            self.assertEqual(type(exp_links), list)
            self.assertEqual(type(flat_links[0]), creature.CreatureLink)
            self.assertEqual(type(flat_links[-1]), creature.CreatureLink)
            self.assertEqual(type(exp_links[0]), creature.CreatureLink)
            self.assertEqual(type(exp_links[-1]), creature.CreatureLink)
            self.assertEqual(exp_links_count, len(exp_links))
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