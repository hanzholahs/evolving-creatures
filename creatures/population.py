from creatures import creature


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



