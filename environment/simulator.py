import os
import pybullet as p
from multiprocessing import Pool
from creatures import population, creature

class Simulator:
    def __init__(self, sim_id:int = 0):
        self.client_id = p.connect(p.DIRECT)
        self.sim_id = sim_id

    def run_creature(self, cr:creature.Creature, filename:str = "robot.urdf", max_frame:int = 2400):
        if not os.path.exists(".tmp/urdf"):
            os.makedirs(".tmp/urdf")

        cr_xml_path = ".tmp/urdf/sim_" + str(self.sim_id) + "_" + filename
        cr.write_xml(cr_xml_path)

        client_id = self.client_id

        p.resetSimulation(physicsClientId = client_id)
        p.setPhysicsEngineParameter(enableFileCaching = 0, physicsClientId = client_id)
        p.setGravity(0, 0, -10, physicsClientId = client_id)

        plane_shape = p.createCollisionShape(p.GEOM_PLANE, physicsClientId = client_id)
        plane = p.createMultiBody(plane_shape, plane_shape, physicsClientId = client_id)
        robot = p.loadURDF(cr_xml_path, physicsClientId = client_id)

        p.resetBasePositionAndOrientation(robot, (0, 0, 3), (0, 0, 0, 1), physicsClientId = client_id)

        for i in range(max_frame):
            if i % 240 == 0:
                for joint_id, joint_motor in enumerate(cr.get_motors()):
                    p.setJointMotorControl2(
                        robot, 
                        joint_id, 
                        controlMode = p.VELOCITY_CONTROL, 
                        targetVelocity = joint_motor(),
                        force = 5, 
                        physicsClientId = client_id
                    )
            p.stepSimulation(physicsClientId = client_id)

            # Sometimes PyBullet gives an error loading cratures with too many parts
            try:
                last_position, _ = p.getBasePositionAndOrientation(robot, physicsClientId = client_id)
            except:
                last_position = (0, 0, 0)
                break
            finally:
                # if the creature jump, then the result is invalid. limit is defined arbitrarily
                if last_position[2] > 12.5:
                    last_position = (0, 0, 0)
                    break
                # if the creature fall below the ground, then the result is invalid
                if last_position[2] < 0:
                    last_position = (0, 0, 0)
                    break

        cr.update_position(last_position)

    def eval_population(self, pop:population.Population, max_frame:int = 2400):
        for cr in pop.creatures:
            self.run_creature(cr, max_frame = max_frame)
        
class MultiSimulator():
    def __init__(self, pool_size:int = 5):
        self.sims = [Simulator(i) for i in range(pool_size)]

    def eval_population(self, pop:population.Population, max_frame:int = 2400):
        sim_id = 0
        pool_size = len(self.sims)
        population_size = len(pop.creatures)
        pool_argset = []
        new_creatures = []

        for i, cr in enumerate(pop.creatures):
            pool_argset.append([self.sims[sim_id], cr, max_frame])
            sim_id += 1
            if sim_id >= pool_size or (i + 1) == population_size:
                with Pool(pool_size) as pool:
                    creatures = pool.starmap(MultiSimulator.static_run_creature, pool_argset)
                    new_creatures.extend(creatures)
                pool.close()
                pool_argset = []
                sim_id = 0

        pop.reset_population(new_creatures)

    @staticmethod
    def static_run_creature(sim:Simulator, cr:creature.Creature, max_frame:int = 2400):
        sim.run_creature(cr, max_frame = max_frame)
        return cr