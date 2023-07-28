import copy
import numpy as np
from creatures import creature

def normalize(data):
    return (data - np.min(data)) / (np.max(data) - np.min(data))

def relu(data):
    return np.maximum(0, data)

class Selection:
    @staticmethod
    def eval_fitness(creatures:list[creature.Creature], gamma = 0.25):
        start_points = np.array([cr.start_position for cr in creatures])
        finish_points = np.array([cr.last_position for cr in creatures])
        n_exp_links = np.array([len(cr.get_expanded_links()) for cr in creatures])
        fits = np.linalg.norm(finish_points - start_points, axis = 1)
        # handling condition of all invalid creatures or only one successful creature 
        if np.mean(fits == 0.0) == 1 or np.sum(fits != 0.) == 1:
            fits = np.ones(len(fits)) / len(fits)
        # add reward if based on the x positive direction
        fits = fits * (1 + gamma * normalize(relu(finish_points[:, 0] - start_points[:, 0])) - 0.5 * gamma)
        # add penalty if having less body parts
        fits = fits / (1 + gamma * normalize(n_exp_links) - 0.5 * gamma)
        # remove NaN, if any
        fits = np.nan_to_num(fits, nan = 0)
        return fits

    @staticmethod
    def select_parents(creatures:list[creature.Creature], fits:np.ndarray):
        probs = fits / np.sum(fits)
        probs = np.nan_to_num(probs, nan = 0)
        ind_parent1, ind_parent2 = np.random.choice(range(len(fits)), 2, False, probs)
        return creatures[ind_parent1], creatures[ind_parent2]

class Mutation:
    @staticmethod
    def mutate_point(dna:np.ndarray, mutation_freq:float, mutation_amnt: float = 0.1):
        mutated_dna = copy.copy(dna)
        mutated = np.random.choice((True, False), size = mutated_dna.shape, replace = True, p = (mutation_freq, 1-mutation_freq))
        mutated_dna[mutated] = np.maximum(
            0.0001 + np.random.random() / 1000,
            np.minimum(
                0.9999 - np.random.random() / 1000,
                mutated_dna[mutated] + (np.random.random() * mutation_amnt) - (mutation_amnt / 2)
            )
        )
        return mutated_dna
    
    @staticmethod
    def mutate_shrink(dna:np.ndarray, mutation_freq:float, min_length:int = 2):
        mutated_dna = copy.copy(dna)
        mutation = np.random.choice((True, False), size = len(mutated_dna), replace = True, p = (mutation_freq, 1-mutation_freq))
        mutated_dna = np.delete(mutated_dna, mutation, axis = 0)
        if len(mutated_dna) < min_length:
            mutated_dna = dna[:min_length]
        return mutated_dna
    
    @staticmethod
    def mutate_grow(dna:np.ndarray, mutation_freq:float, max_length:int = 15):
        mutated_dna = copy.copy(dna)
        mutation = np.random.choice((True, False), size = len(mutated_dna), replace = True, p = (mutation_freq, 1-mutation_freq))
        mutated_dna = np.append(mutated_dna, mutated_dna[mutation], axis = 0)
        return mutated_dna[:max_length]
    
class Mating:
    @staticmethod
    def mate_grafting(dna1:np.ndarray, dna2:np.ndarray, max_length:int = 15, max_growth_rt:float = 1.2):
        length_limit = np.minimum(max_length, int(np.maximum(len(dna1), len(dna2)) * max_growth_rt))
        ind_1 = np.random.randint(1, len(dna1)+1)
        ind_2 = np.random.randint(0, len(dna2))
        child_dna = np.concatenate((dna1[:ind_1], dna2[ind_2:]))
        return child_dna[:length_limit]

    @staticmethod
    def mate_crossover(dna1:np.ndarray, dna2:np.ndarray, max_length:int = 15, max_growth_rt = 1.2):
        length_limit = np.minimum(max_length, int(np.maximum(len(dna1), len(dna2)) * max_growth_rt))
        indices1 = np.sort(np.random.choice(range(len(dna1)), 2, replace = False))
        indices2 = np.sort(np.random.choice(range(len(dna2)), 2, replace = False))
        child_dna = np.concatenate((dna1[indices1[0]:], dna2[indices2[0]:indices2[1]], dna1[:indices1[1]]))
        return child_dna[:length_limit]
    
    @staticmethod
    def mate(dna1:np.ndarray, 
             dna2:np.ndarray,
             min_length:int,
             max_length:int,
             max_growth_rt:float,
             mutation_freq:float,
             mutation_amnt:float):
        # select the mating method
        if np.random.random() < 0.5:
            child_dna = Mating.mate_grafting(dna1, dna2, max_length, max_growth_rt)
        else:
            child_dna = Mating.mate_crossover(dna1, dna2, max_length, max_growth_rt)
            
        child_dna = Mutation.mutate_shrink(child_dna, mutation_freq, min_length)
        child_dna = Mutation.mutate_grow(child_dna, mutation_freq, max_length)
        child_dna = Mutation.mutate_point(child_dna, mutation_freq, mutation_amnt)
        return child_dna