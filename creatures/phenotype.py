import copy
import numpy as np


class BodyPart:

    @staticmethod
    def get_link_shapes():
        return ("box", "box", "box", "box", "box",
                "cylinder", "cylinder", "cylinder", "cylinder", "cylinder",
                "sphere", "sphere") 

    @staticmethod
    def get_joint_types():
        return ("revolute", "continuous")
    
    @staticmethod
    def get_joint_axes():
        return ("1 0 0", "0 1 0", "0 0 1")

    @staticmethod
    def body_part_xml(name, parent_name, g_dict, adom, sib_ind = None):
        link_shape = BodyPart.get_link_shapes()[ g_dict["link_shape"] ]
        joint_type = BodyPart.get_joint_types()[ g_dict["joint_type"] ]
        joint_axis = BodyPart.get_joint_axes()[ g_dict["joint_axis_xyz"] ]
        
        if sib_ind == None:
            try:
                sib_ind = int(name.split("_")[2]) # ex: Link_1_2_4
            except:
                sib_ind = 0

        shape_tag = adom.createElement(link_shape)
        if link_shape == "box":
            link_size = " ".join([str(g_dict["link_length_1"]), str(g_dict["link_length_2"]), str(g_dict["link_length_3"])])
            shape_tag.setAttribute("size", str(link_size))
            link_volume    = g_dict["link_length_1"] * g_dict["link_length_2"] *  g_dict["link_length_3"]
        elif link_shape =="cylinder":
            link_length = np.mean([g_dict["link_length_1"], g_dict["link_length_2"], g_dict["link_length_3"]]) * 0.83 # rate to limit a maximum volume of 1
            link_radius = g_dict["link_radius"] * 0.62 # rate to limit a maximum volume of 1
            shape_tag.setAttribute("radius", str(link_radius))
            shape_tag.setAttribute("length", str(link_length))
            link_volume = np.pi * (g_dict["link_length_1"] ** 2) * np.mean([
                g_dict["link_length_1"],
                g_dict["link_length_2"],
                g_dict["link_length_3"]
            ])
        else:
            link_radius = g_dict["link_radius"] * 0.62 # rate to limit a maximum volume of 1
            shape_tag.setAttribute("radius", str(link_radius))
            link_volume = 4 / 3 * np.pi * (g_dict["link_radius"] ** 3)

        link_mass = link_volume * g_dict["link_mass_density"]

        # ----- LINK TAG -----
        mass_tag = adom.createElement("mass")
        mass_tag.setAttribute("value", str(link_mass))

        inertia_tag = adom.createElement("inertia")
        inertia_tag.setAttribute("ixx", "0.03")  
        inertia_tag.setAttribute("ixy", "0.03")  
        inertia_tag.setAttribute("ixz", "0.03") 
        inertia_tag.setAttribute("iyy", "0") 
        inertia_tag.setAttribute("iyz", "0") 
        inertia_tag.setAttribute("izz", "0")

        geometry_tag = adom.createElement("geometry")
        geometry_tag.appendChild(shape_tag)
        
        link_visual_tag = adom.createElement("visual")
        link_visual_tag.appendChild(copy.copy(geometry_tag))

        link_collision_tag = adom.createElement("collision")
        link_collision_tag.appendChild(geometry_tag)

        link_inertial_tag = adom.createElement("inertial")
        link_inertial_tag.appendChild(mass_tag)
        link_inertial_tag.appendChild(inertia_tag)

        link_tag = adom.createElement("link")
        link_tag.setAttribute("name", name)
        link_tag.appendChild(link_visual_tag)
        link_tag.appendChild(link_collision_tag)
        link_tag.appendChild(link_inertial_tag)
               
        # ----- JOINT TAG ----- 
        joint_parent_tag = adom.createElement("parent")
        joint_parent_tag.setAttribute("link", parent_name)

        joint_child_tag = adom.createElement("child")
        joint_child_tag.setAttribute("link", name)

        joint_origin_tag = adom.createElement("origin")
        joint_origin_tag.setAttribute("xyz", " ".join([
            str(g_dict["joint_origin_xyz_1"] * sib_ind),
            str(g_dict["joint_origin_xyz_2"]),
            str(g_dict["joint_origin_xyz_3"])
        ]))
        joint_origin_tag.setAttribute("rpy", " ".join([
            str(g_dict["joint_origin_rpy_1"]),
            str(g_dict["joint_origin_rpy_2"]),
            str(g_dict["joint_origin_rpy_3"])            
        ]))

        joint_axis_tag = adom.createElement("axis")
        joint_axis_tag.setAttribute("xyz", str(joint_axis))

        joint_limit_tag = adom.createElement("limit")
        joint_limit_tag.setAttribute("effort", "1")
        joint_limit_tag.setAttribute("upper", str(-np.pi))
        joint_limit_tag.setAttribute("lower", str(np.pi))
        joint_limit_tag.setAttribute("velocity", "1")

        joint_tag = adom.createElement("joint")
        joint_tag.setAttribute("name", "joint_" + name)
        joint_tag.setAttribute("type", joint_type)
        joint_tag.appendChild(joint_parent_tag)
        joint_tag.appendChild(joint_child_tag)
        joint_tag.appendChild(joint_axis_tag)
        joint_tag.appendChild(joint_origin_tag)
        joint_tag.appendChild(joint_limit_tag)

        return link_tag, joint_tag
    

class Motor:

    def __init__(self, motor_type:int, step_size:float, amplitude:float, param1:float):
        self.motor_type = motor_type
        self.step_size  = step_size
        self.amplitude  = amplitude
        self.param1     = param1
        self.param2     = 1 - param1
        self.phase      = 0

    def __call__(self):
        self.phase += self.step_size
        if self.motor_type == 0:
            velocity =  self.amplitude * ((-1) ** (np.ceil(self.phase % (np.pi * 2))))
        elif self.motor_type == 1:
            velocity =  self.amplitude * np.sin(np.pi * self.phase)
        elif self.motor_type == 2:
            velocity =  self.amplitude * np.sin(self.param1 * np.pi * self.phase) * np.sin(self.param2 * np.pi * self.phase)
        else:
            raise Exception("Invalid motor type")
        return velocity
    
    def __repr__(self):
        return f"Motor\nType\t: {self.motor_type}\nAmp\t: {self.amp}\nFreq\t: {self.freq}\n"