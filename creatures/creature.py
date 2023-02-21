import copy
import numpy as np
from creatures import genome, phenotype
from xml.dom.minidom import getDOMImplementation


class CreatureLink:

    def __init__(self, name:str, g_dict:dict, parent_name:str, recur:str):
        self.name = name
        self.parent_name = parent_name
        self.g_dict = g_dict
        self.recur = recur
    
    def __repr__(self):
        return f"URDF Link\nName\t: {self.name}\nParent\t: {self.parent_name}\nRecur\t: {self.recur}\n"
    
class Creature:
    
    __counter = 0

    def __init__(self, gene_count):
        self.dna = genome.Genome.init_genome(gene_count, len(genome.Genome.get_spec()))
        self.start_position = (0, 0, 0)
        self.last_position = (0, 0, 0)
        self.motors = None
        self.__flat_links = None
        self.__expanded_links = None

    def update_dna(self, new_dna):
        assert len(genome.Genome.get_spec()) == new_dna.shape[-1]
        self.dna = new_dna
        self.start_position = (0, 0, 0)
        self.last_position = (0, 0, 0)
        self.motors = None
        self.__flat_links = None
        self.__expanded_links = None

    def reset_start_position(self, start_position):
        self.start_position = start_position
        return self.start_position

    def update_position(self, new_position):
        self.last_position = new_position
        return self.last_position

    def get_distance(self):
        dist = np.linalg.norm(np.asarray(self.last_position) - np.asarray(self.start_position))
        return np.nan_to_num(dist)

    def get_flat_links(self):
        if self.__flat_links == None:
            g_dicts = genome.Genome.to_dict(self.dna)
            self.__flat_links = Creature.genome_to_links(g_dicts)
        return self.__flat_links

    def get_expanded_links(self):
        if self.__expanded_links == None:
            self.__expanded_links = Creature.expand_links(self.get_flat_links())
        return self.__expanded_links

    def get_xml(self, robot_name = "robot"):
        adom = getDOMImplementation().createDocument(None, "start", None)
        robot_tag = adom.createElement("robot")
        robot_tag.setAttribute("name", robot_name)

        for i, link in enumerate(self.get_expanded_links()):
            link_tag, joint_tag = phenotype.BodyPart.body_part_xml(link.name, link.parent_name, link.g_dict, adom)
            robot_tag.appendChild(link_tag)
            if i != 0:
                robot_tag.appendChild(joint_tag)

        return robot_tag  

    def write_xml(self, path):
        with open(path, "w") as f:
            xml_str = self.get_xml().toprettyxml()
            f.write(xml_str)
    
    def get_motors(self):
        if self.motors == None:
            motors = []
            for i, link in enumerate(self.get_expanded_links()):
                if i == 0: continue
                motors.append(phenotype.Motor(
                    link.g_dict["control_motor_type"],
                    link.g_dict["control_amplitude"],
                    link.g_dict["control_step"],
                    link.g_dict["control_param1"]
                ))
            self.motors = motors
        return self.motors
    
    @staticmethod
    def genome_to_links(g_dicts):
        link_names = ["Link_" + str(i) for i in range(len(g_dicts))]
        flat_links = []
        for i, gene_dict in enumerate(g_dicts):
            if i == 0:
                parent_name, recur = "None", 1
            else:
                parent_name, recur = link_names[i-1], int(np.ceil(gene_dict["link_recurrence"]))
            flat_links.append(CreatureLink(link_names[i], gene_dict, parent_name, recur))
        return flat_links
    
    @staticmethod
    def expand_links(flat_links):       
        flat_links[0].recur == 1 
        assert flat_links[0].recur == 1
        exp_links = Creature.__expand_links_recursive(flat_links[0], flat_links[1:])
        Creature.__counter = 0
        return exp_links

    @staticmethod
    def __expand_links_recursive(parent, child_links, child_id = "0"):
        p_copy = copy.copy(parent)
        p_copy.name += ("_" + str(child_id) + "_" + str(Creature.__counter))
        Creature.__counter += 1
        exp_links = [p_copy]
        if len(child_links) > 0:
            for i in range(child_links[0].recur):
                child = Creature.__expand_links_recursive(child_links[0], child_links[1:], i)
                c_copy = copy.copy(child)
                c_copy[0].parent_name = p_copy.name
                exp_links.extend(c_copy)
        return exp_links