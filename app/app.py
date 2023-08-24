import os
import datetime
import numpy as np

from app import simulator
from creatures import population
from creatures.evolution import Selection

eval_fitness = Selection.eval_fitness 
now = datetime.datetime.now

class MainApp:
    def __init__(self,
                 base_dir:str,
                 load_progress:bool = False,
                 multiprocess:bool = True,
                 pool_size:int = 5,
                 max_frame:int = 1200,
                 population_size:int = 5,
                 current_generation:int = 0,
                 num_of_generation:int = 10,
                 default_gene_count:int = 5,
                 num_of_elites:int = 1,
                 num_of_random:int = 1,
                 min_length:int = 2,
                 max_length:int = 5,
                 max_growth_rt:float = 1.1,
                 mutation_freq:float = 0.1,
                 mutation_amnt:float = 0.1,
                 dist_limit_rt:float = 1.025) -> None:
        if base_dir is None:
            raise Exception("`base_dir` cannot be empty.")
        
        # Set app specification
        self.base_dir = base_dir
        self.multiprocess = multiprocess
        self.pool_size = pool_size
        self.max_frame = max_frame
        self.population_size = population_size
        self.current_generation = current_generation
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
        self.build_simulator()
        self.reset_population()
        
        self.save_population()
        self.sim.eval_population(self.pop, self.max_frame)
        self.generate_report()
        
        if load_progress and os.path.exists(os.path.join(self.base_dir, "pop"))
            self.load_population()
        
    def build_simulator(self, 
                        multiprocess:bool = None, 
                        pool_size:int = None) -> None:
        
        # Change sim specification
        if multiprocess is not None:
            self.multiprocess = multiprocess
        if pool_size is not None:
            self.pool_size = pool_size
        if ((self.multiprocess == False and self.pool_size > 1) or
            (self.multiprocess == True and self.pool_size < 2)):         
            raise Exception(f"Multiprocess cannot {self.multiprocess} " +
                            f"while pool size is {self.pool_size}")

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
                         population_size:int = None, 
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
            base_dir:str = None,
            save_after:bool = True,
            save_each:int = None,
            report_after:bool = True,
            report_each:int = None,
            log_after:bool = True,
            log_each:int = None,
            log_console:bool = False,
            num_of_generation:int = None,
            num_of_elites:int = None,
            num_of_random:int = None,
            min_length:int = None,
            max_length:int = None,
            max_growth_rt:float = None,
            mutation_freq:float = None,
            mutation_amnt:float = None,
            dist_limit_rt:float = None) -> None:
        
        # change sim run specification
        if base_dir is not None:
            self.base_dir = base_dir
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
            
        self.print_setting(save_after, save_each, report_after, report_each, \
                           log_after, log_each, log_console)
            
        for cr in self.pop.creatures:
            cr.reset_motors()
            
        # run simulation for some generations
        while self.current_generation <= self.num_of_generation:
            self.sim.eval_population(self.pop, self.max_frame)
            
            if save_each is not None and self.current_generation % save_each == 0:
                self.save_population()
            if report_each is not None and self.current_generation % report_each == 0:
                self.generate_report()
            if log_each is not None and self.current_generation % log_each == 0:
                self.print_log(log_console)

            self.current_generation += 1
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
        
        self.sim.eval_population(self.pop, self.max_frame)
            
        if log_after:
            self.print_log(log_console = True)

        # generate report after simulation
        if report_after: 
            self.generate_report()
            
        # save csvs after simulation
        if save_after:
            self.save_population()
        
    def save_population(self, base_dir = None) -> None:
        if base_dir is not None:
            self.base_dir = base_dir
        
        save_path = os.path.join(self.base_dir, "pop", str(self.current_generation))
        
        if not os.path.exists(save_path):
            os.makedirs(save_path, exist_ok = True)
        
        self.pop.to_csvs(base_folder = save_path, identifier = "cr")
    
    def load_population(self, 
                        base_dir = None, 
                        current_generation:int = None) -> None:
        if base_dir is not None:
            self.base_dir = base_dir
        if current_generation is None:
            self.current_generation = max([int(d) for d in os.listdir(self.base_dir + "/pop")])
            
        load_path = os.path.join(self.base_dir, "pop", str(self.current_generation))
        
        self.pop.from_csvs(base_folder = load_path, identifier = "cr")
        
    def generate_report(self, base_dir = None) -> None:
        if base_dir is not None:
            self.base_dir = base_dir
        
        report_path = os.path.join(self.base_dir, "report", str(self.current_generation))
        
        self.pop.generate_report(self.current_generation, report_path)
        
    def print_log(self, log_console = False):
        log_path = os.path.join(self.base_dir, "log.txt")
        
        n_ex_link = np.mean([len(cr.get_expanded_links()) for cr in self.pop.creatures])
        n_fl_link = np.mean([len(cr.get_flat_links()) for cr in self.pop.creatures])
        max_ex_link = max([len(cr.get_expanded_links()) for cr in self.pop.creatures])
        max_fl_link = max([len(cr.get_flat_links()) for cr in self.pop.creatures])
        dists = np.mean([cr.get_distance() for cr in self.pop.creatures])
        fits  = np.mean(eval_fitness(self.pop.creatures))
                
        text = "".join([
            f"{now()},",
            f"{str(self.current_generation)},".rjust(10, " "),
            f"{round(n_ex_link, 2):.2f},".rjust(10, " "),
            f"{round(n_fl_link, 2):.2f},".rjust(10, " "),
            f"{round(max_ex_link, 2):.2f},".rjust(10, " "),
            f"{round(max_fl_link, 2):.2f},".rjust(10, " "),
            f"{round(dists, 2):.2f},".rjust(10, " "),
            f"{round(fits, 2):.2f}".rjust(10, " ")
        ])
        
        if log_console: print(text)
        
        with open(log_path, "a") as f:
            f.write(text + "\n")
            
    def print_setting(self,
                      save_after,
                      save_each,
                      report_after,
                      report_each,
                      log_after,
                      log_each,
                      log_console):
        setting_path = os.path.join(self.base_dir, "settings.txt")
        
        text = "\n".join([
            f"Multiprocess: {self.multiprocess}",
            f"Pool Size: {self.pool_size}",
            f"Max Frame: {self.max_frame}",
            f"Directory: {self.base_dir}",
            f"Save After: {save_after}",
            f"Save Each: {save_each}",
            f"Report After: {report_after}",
            f"Report Each: {report_each}",
            f"Log After: {log_after}",
            f"Log Each: {log_each}",
            f"Log Console: {log_console}",
            f"Population Size: {self.population_size}",
            f"Starting Generation: {self.current_generation}",
            f"Total Generation: {self.num_of_generation}",
            f"Default Gene Count: {self.default_gene_count}",
            f"Number of Elites: {self.num_of_elites}",
            f"Number of Random: {self.num_of_random}",
            f"Min Length: {self.min_length}",
            f"Max Length: {self.max_length}",
            f"Max Growth Rate: {self.max_growth_rt}",
            f"Distance Limit Rate: {self.dist_limit_rt}",
            f"Mutation Frequency: {self.mutation_freq}",
            f"Mutation Amount: {self.mutation_amnt}",
        ])
        
        with open(setting_path, "a") as f:
            f.write(text + "\n")