import os
import re
import numpy as np
from creatures import creature, evolution


class Population:
    def __init__(self, population_size:int, default_gene_count:int = 5):
        self.default_gene_count = default_gene_count
        self.population_size = population_size
        self.creatures = []
        self.max_dist = 1
        self.min_dist = 0
        self.avg_dist = 0
        self.reset_population()

    def reset_population(self, creatures:list[creature.Creature] = None):
        if creatures == None:
            self.creatures = [creature.Creature(self.default_gene_count) for _ in range(self.population_size)]
        else:
            assert type(creatures) == list and len(creatures) > 0
            assert type(creatures[0]) == creature.Creature
            for old_creature in self.creatures:
                del old_creature
            self.creatures = creatures
            self.population_size = len(self.creatures)

    def add_creature(self, cr:creature.Creature):
        self.creatures.append(cr)
        self.population_size = len(self.creatures)

    def add_creatures(self, creatures:list[creature.Creature]):
        self.creatures.extend(creatures)
        self.population_size = len(self.creatures)

    def new_generation(self,
                       num_of_elites:int,
                       num_of_random:int,
                       min_length:int,
                       max_length:int,
                       max_growth_rt:float,
                       mutation_freq:float,
                       mutation_amnt:float,
                       dist_limit_rt:float = 1.025):
        assert num_of_elites < self.population_size
        assert num_of_random < self.population_size
        assert num_of_elites + num_of_random < self.population_size
        assert 0 < min_length and min_length <= max_length
        assert 0 <= max_growth_rt
        assert 0 <= mutation_freq and mutation_freq <= 1
        assert 0 <= mutation_amnt and mutation_amnt <= 1

        # eliminate cheating creatures manually by incremental fit increase
        for cr in self.creatures:
            if cr.get_distance() > self.max_dist * dist_limit_rt:
                cr.update_position((0, 0, 0))

        # update max dist
        dists = np.array([cr.get_distance() for cr in self.creatures])
        self.n_invalid = np.sum(dists == 0.0)
        self.min_dist = np.min(dists)
        self.max_dist = np.max(dists)
        self.avg_dist = np.mean(dists)

        # genetic algo
        fits = evolution.Selection.eval_fitness(self.creatures)
        fittest_indices = np.array(fits).argsort()[-1:-(num_of_elites+1):-1]

        new_creatures = []
        for index in fittest_indices:
            fittest_cr = self.creatures[index]
            new_creatures.append(fittest_cr)
        for _ in range(self.population_size - num_of_elites - num_of_random):
            fits = evolution.Selection.eval_fitness(self.creatures)
            p1, p2 = evolution.Selection.select_parents(self.creatures, fits)
            child_cr = creature.Creature(1)
            child_cr.update_dna(evolution.Mating.mate(
                p1.dna,
                p2.dna,
                min_length,
                max_length,
                max_growth_rt,
                mutation_freq,
                mutation_amnt
            ))
            new_creatures.append(child_cr)
        for _ in range(num_of_random):
            random_cr = creature.Creature(self.default_gene_count)
            new_creatures.append(random_cr)

        self.reset_population(new_creatures)

    def generate_report(self, generation, base_folder = ".tmp"):
        n_exp_link  = [len(cr.get_expanded_links()) for cr in self.creatures]
        n_flat_link = [len(cr.get_flat_links()) for cr in self.creatures]
        dists = [cr.get_distance() for cr in self.creatures]
        fits  = list(evolution.Selection.eval_fitness(self.creatures))

        file_names = [
            f"{generation}_n_exp_links.csv",
            f"{generation}_n_flat_links.csv",
            f"{generation}_distances.csv",
            f"{generation}_fitness.csv",
        ]

        Population.__generate_report_csv(file_names[0], n_exp_link, base_folder)
        Population.__generate_report_csv(file_names[1], n_flat_link, base_folder)
        Population.__generate_report_csv(file_names[2], dists, base_folder)
        Population.__generate_report_csv(file_names[3], fits, base_folder)

    @staticmethod
    def __generate_report_csv(csv_file_name, csv_rows, base_folder = ".tmp"):
        if not os.path.exists(base_folder):
            os.makedirs(base_folder, exist_ok=True)
        with open(os.path.join(base_folder, csv_file_name), "w") as f:
            f.write(','.join(map(str, csv_rows)) + "\n")

    def to_csvs(self, base_folder = ".", identifier = "dna"):
        Population.__to_csvs(self.creatures, base_folder = base_folder, identifier = identifier)

    def from_csvs(self, base_folder = ".", identifier = "dna"):
        new_creatures = Population.__from_csvs(base_folder = base_folder, identifier = identifier)
        self.reset_population(new_creatures)

    def fittest_to_csvs(self, n_fittest = 3, base_folder = ".", identifier = "dna"):
        fits = evolution.Selection.eval_fitness(self.creatures)
        fittest_ids = fits.argsort()[-n_fittest:][::-1] 
        fittest_crs = [self.creatures[id] for id in fittest_ids]
        Population.__to_csvs(fittest_crs, base_folder = base_folder, identifier = identifier)

    @staticmethod
    def __to_csvs(creatures, base_folder = ".tmp", identifier = "dna"):
        if not os.path.exists(base_folder):
            os.makedirs(base_folder, exist_ok=True)
        for i, cr in enumerate(creatures):
            np.savetxt(f"{base_folder}/{identifier}_cr_{i:04}.csv", cr.dna, delimiter = ",")

    @staticmethod
    def __from_csvs(base_folder = ".tmp", identifier = "dna"):
        assert os.path.exists(base_folder)
        files = [f for f in os.listdir(base_folder) if re.match(f"^({identifier}).*\\.csv$", f)]
        files.sort()
        new_creatures = []
        for file in files:
            path = os.path.join(base_folder, file)
            dna = np.genfromtxt(path, delimiter = ",")
            cr = creature.Creature(1)
            cr.update_dna(dna)
            new_creatures.append(cr)
        return new_creatures