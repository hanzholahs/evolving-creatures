from app import simulator
from creatures import population

class MainApp:
    def __init__(
        self, 
        multiprocess:bool = True, 
        pool_size:int = 5,
        max_frame:int = 1200,
        population_size:int = 5,
        num_of_generation:int = 10,
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
        
        # Set app specification
        self.multiprocess = multiprocess
        self.pool_size = pool_size
        self.max_frame = max_frame
        self.population_size = population_size
        self.num_of_generation = num_of_generation
        self.default_gene_count = default_gene_count
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

        # instantiate pop and sim
        self.reset_population()
        self.build_simulator()
        
    def build_simulator(self, 
                        multiprocess: bool = None, 
                        pool_size: int = None) -> None:
        # Change sim specification
        if multiprocess is not None:
            self.multiprocess = multiprocess
        if pool_size is not None:
            self.pool_size = pool_size

        # delete simulator object(s)
        if self.sim is not None:
            if type(self.sim) == simulator.MultiSimulator:
                for sim in self.sim.sims:
                    del sim
            del self.sim

        # instantiate new simulator       
        if self.multiprocess:
            self.sim = simulator.MultiSimulator(self.pool_size)
        else:
            self.sim = simulator.Simulator()
            
    def reset_population(self, 
                         population_size: int = None, 
                         default_gene_count:int = None) -> None:
        # Change pop specification
        if population_size is not None:
            self.population_size = population_size
        if default_gene_count is not None:
            self.default_gene_count = default_gene_count        

        # Instatiate population
        if self.pop == None:
            self.pop = population.Population(
                population_size = self.population_size,
                default_gene_count = self.default_gene_count
            )
        else:
            self.pop.reset_population()
        
    def run(self,
            num_of_generation: int = None,
            num_of_elites: int = None,
            num_of_random: int = None,
            min_length: int = None,
            max_length: int = None,
            max_growth_rt: float = None,
            mutation_freq: float = None,
            mutation_amnt: float = None,
            dist_limit_rt: float = None) -> None:
        # change sim run specification
        if num_of_generation is not None:
            self.num_of_generation = num_of_generation
        if num_of_elites is not None:
            self.num_of_elites = num_of_elites
        if num_of_random is not None:
            self.num_of_random = num_of_random
        if min_length is not None:
            self.min_length = min_length
        if max_length is not None:
            self.max_length = max_length
        if max_growth_rt is not None:
            self.max_growth_rt = max_growth_rt
        if mutation_freq is not None:
            self.mutation_freq = mutation_freq
        if mutation_amnt is not None:
            self.mutation_amnt = mutation_amnt
        if dist_limit_rt is not None:
            self.dist_limit_rt = dist_limit_rt
        
        # run simulation for some generations
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
        