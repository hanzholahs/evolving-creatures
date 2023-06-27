from app import simulator
from creatures import population

class MainApp:
    def __init__(
        self, 
        multiprocess:bool = True, 
        pool_size:int = 5,
        max_frame:int = 1200,
        num_of_generation:int = 10,
        population_size:int = 5,
        default_gene_count:int = 5,
        num_of_elites:int = 1,
        num_of_random:int = 1,
        min_length:int = 2,
        max_length:int = 5,
        max_growth_rt:float = 1.1,
        mutation_freq:float = 0.1,
        mutation_amnt:float = 0.1,
        dist_limit_rt:float = 1.025
    ) -> None:
        
        self.multiprocess = multiprocess
        self.pool_size = pool_size
        self.max_frame = max_frame
        self.population_size = population_size
        self.default_gene_count = default_gene_count
        self.num_of_generation = num_of_generation
        self.num_of_elites = num_of_elites
        self.num_of_random = num_of_random
        self.min_length = min_length
        self.max_length = max_length
        self.max_growth_rt = max_growth_rt
        self.mutation_freq = mutation_freq
        self.mutation_amnt = mutation_amnt
        self.dist_limit_rt = dist_limit_rt
        self.pop = None
        self.sim = None

        self.reset_population()
        self.build_simulator()
        
    def build_simulator(self):
        if self.sim is not None:
            if type(self.sim) == simulator.MultiSimulator:
                for sim in self.sim.sims:
                    del sim
            del self.sim
        
        if self.multiprocess:
            self.sim = simulator.MultiSimulator(self.pool_size)
        else:
            self.sim = simulator.Simulator()
            
    def reset_population(self):
        if self.pop == None:
            self.pop = population.Population(
                population_size = self.population_size,
                default_gene_count = self.default_gene_count
            )
        else:
            self.pop.reset_population()
        
    def run(self):
        for _ in range(self.num_of_generation - 1):
            self.sim.eval_population(self.pop, self.max_frame)
            self.pop.new_generation(
                self.num_of_elites,
                self.num_of_random,
                self.min_length,
                self.max_length,
                self.max_growth_rt,
                self.mutation_freq,
                self.mutation_amnt,
                self.dist_limit_rt
            )
        self.sim.eval_population(self.pop)