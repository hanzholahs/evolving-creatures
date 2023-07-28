from app.app import MainApp

# Simulation parameters
BASE_DIR = ".sim"
NUM_OF_PROCESSES = 10
MAX_SIM_FRAMES   = 2400
SAVE_EACH   = 100
REPORT_EACH = 5
LOG_EACH    = 1

# Generation parameters
NUM_OF_GENERATION = 500
DEFAULT_GEN_COUNT = 5
NUM_OF_CR = 30
NUM_OF_ELITES = 5
NUM_OF_RANDOM = 5
MIN_LEN = 2
MAX_LEN = 12
MUTATION_FREQ = 0.1
MUTATION_AMNT = 0.1
MAX_GROWTH_RT = 1.05
DIST_LIMIT_RT = 1.05

main = MainApp(
    pool_size = NUM_OF_PROCESSES,
    max_frame = MAX_SIM_FRAMES,
    population_size = NUM_OF_CR,
    num_of_elites = NUM_OF_ELITES,
    num_of_random = NUM_OF_RANDOM,
    min_length = MIN_LEN,
    max_length = MAX_LEN,
    mutation_freq = MUTATION_FREQ,
    mutation_amnt = MUTATION_AMNT,
    max_growth_rt = MAX_GROWTH_RT,
    dist_limit_rt = DIST_LIMIT_RT,
    load_progress = True
)

main.run(
    base_dir = BASE_DIR,
    num_of_generation = NUM_OF_GENERATION,
    save_each   = SAVE_EACH,
    report_each = REPORT_EACH,
    log_each    = LOG_EACH,
    log_console = True
)