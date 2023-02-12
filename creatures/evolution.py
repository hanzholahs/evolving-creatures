import copy
import numpy as np
from creatures import creature

class Selection:
    @staticmethod
    def eval_fitness(creatures:list[creature.Creature]):
        start_points = np.array([cr.start_position for cr in creatures])
        finish_points = np.array([cr.last_position for cr in creatures])
        n_exp_links = np.array([len(cr.get_expanded_links()) for cr in creatures])
        fits = np.linalg.norm(finish_points - start_points, axis = 1)
        # add reward if taking more x direction
        fits = fits * (1 + (finish_points[:, 0] - start_points[:, 0]) / np.max(fits))
        # add penalty if having less body parts
        fits = fits / (1 + n_exp_links / np.max(n_exp_links))
        # remove NaN, if any
        fits = np.nan_to_num(fits, nan = 0)
        return fits

    @staticmethod
    def select_parents(creatures:list[creature.Creature], fits:np.ndarray):
        probs = fits / np.sum(fits)
        if np.mean(probs == 0.0) == 1 or np.sum(probs == 1.) == 1:
            probs = np.ones(len(fits)) / len(fits)
        ind_parent1, ind_parent2 = np.random.choice(range(len(fits)), 2, False, probs)
        return creatures[ind_parent1], creatures[ind_parent2]

class Mutation:
    @staticmethod
    def mutate_point(dna:np.ndarray, mutation_freq:float, mutation_amt: float = 0.1):
        mutated_dna = copy.copy(dna)
        mutated = np.random.choice((True, False), size = mutated_dna.shape, replace = True, p = (mutation_freq, 1-mutation_freq))
        mutated_dna[mutated] = np.maximum(
            0.0001 + np.random.random() / 1000,
            np.minimum(
                0.9999 - np.random.random() / 1000,
                mutated_dna[mutated] + (np.random.random() * mutation_amt) - (mutation_amt / 2)
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