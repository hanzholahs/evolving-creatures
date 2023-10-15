from app.app import MainApp

# simulation parameters
BASE_DIR = ".sim-final-04"
NUM_OF_PROCESSES = 10
MAX_SIM_FRAMES = 2400 * 2 # for 20 secs
SAVE_EACH = 250
REPORT_EACH = 2
LOG_EACH = 25

# generation parameters
NUM_OF_GENERATION = 25_000
DEFAULT_GEN_COUNT = 2
NUM_OF_CR = 50
NUM_OF_ELITES = 7
NUM_OF_RANDOM = 0
MIN_LEN = 2
MAX_LEN = 20
MUTATION_FREQ = 0.30
MUTATION_AMNT = 0.30
MAX_GROWTH_RT = 1.30
DIST_LIMIT_RT = 1.10
INCREMENTAL = True

# instantiate simulator app
main = MainApp(
    base_dir  = BASE_DIR,
    pool_size = NUM_OF_PROCESSES,
    max_frame = MAX_SIM_FRAMES,
    incremental = INCREMENTAL,
    population_size = NUM_OF_CR,
    num_of_generation = NUM_OF_GENERATION,
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

# run app
main.run(
    save_each    = SAVE_EACH,
    save_after   = True,
    report_each  = REPORT_EACH,
    report_after = True,
    log_each     = LOG_EACH,
    log_after    = True,
    log_console  = True
)