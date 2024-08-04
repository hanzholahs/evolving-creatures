from app.app import MainApp

# simulation parameters
BASE_DIR = ".sim"
NUM_OF_PROCESSES = 8
MAX_SIM_FRAMES = 2400
SAVE_EACH = 2500
REPORT_EACH = 50
LOG_EACH = 250

# generation parameters
NUM_OF_GENERATION = 10_000
DEFAULT_GEN_COUNT = 5
NUM_OF_CR = 120
NUM_OF_ELITES = 10
NUM_OF_RANDOM = 0
MIN_LEN = 2
MAX_LEN = 20
MUTATION_FREQ = 0.25
MUTATION_AMNT = 0.25
MAX_GROWTH_RT = 1.25
DIST_LIMIT_RT = 1.25
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