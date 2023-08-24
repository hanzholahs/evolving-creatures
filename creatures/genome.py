import numpy as np


class Genome:
    __spec = None

    @staticmethod
    def init_genome(gene_count:int):
        gene_size = len(Genome.get_spec())
        return np.random.rand(gene_count, gene_size)
    
    @staticmethod
    def to_dict(dna:np.ndarray):
        assert dna.shape[1] == len(Genome.get_spec())
        g_dicts = []
        spec = Genome.get_spec()
        for i in range(dna.shape[0]):
            g_dict = {}
            for key in spec.keys():
                value = dna[i][spec[key]["index"]] * spec[key]["scale"]
                if spec[key]["type"] == "discrete":
                    value = int(value) + 1
                elif spec[key]["type"] == "categorical":
                    value = int(value)
                g_dict[key] = value
            g_dicts.append(g_dict)
        return g_dicts

    @staticmethod
    def get_spec():
        if Genome.__spec == None:
            spec = {
                "parent_link": {"scale":1},
                "link_shape": {"scale":12, "type":"categorical"},
                "link_length_1": {"scale":2.5},
                "link_length_2": {"scale":2.5},
                "link_length_3": {"scale":2.5},
                "link_radius": {"scale":2.5},
                "link_recurrence": {"scale":3, "type":"discrete"},
                "link_mass_density": {"scale":5},
                "joint_type": {"scale":2, "type":"categorical"},
                "joint_axis_xyz": {"scale":3, "type": "categorical"},
                "joint_origin_rpy_1": {"scale":np.pi * 2},
                "joint_origin_rpy_2": {"scale":np.pi * 2},
                "joint_origin_rpy_3": {"scale":np.pi * 2},
                "joint_origin_xyz_1": {"scale":1},
                "joint_origin_xyz_2": {"scale":1},
                "joint_origin_xyz_3": {"scale":1},
                "control_motor_type": {"scale":3, "type":"categorical"},
                "control_amplitude": {"scale":0.25},
                "control_step": {"scale":1},
                "control_param1": {"scale":0.5}
            }
            ind = 0
            for key in spec.keys():
                if "type" not in spec[key].keys():
                    spec[key]["type"] = "continuous"
                spec[key]["index"] = ind
                ind += 1
            Genome.__spec = spec
        return Genome.__spec