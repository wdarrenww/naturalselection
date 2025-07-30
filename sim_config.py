class SimConfig:
    def __init__(self):
        # display settings
        self.width = 1200
        self.height = 800
        self.fps = 60
        self.title = "Natural Selection Simulator"
        
        # world settings
        self.world_width = 1000
        self.world_height = 600
        
        # organism settings
        self.initial_organisms = 20
        self.organism_size = 8
        self.organism_speed = 2.0
        self.initial_energy = 100
        self.energy_decay_rate = 0.5
        self.energy_gain_from_food = 50
        self.min_energy_to_reproduce = 80
        
        # dna and mutation settings
        self.mutation_rate = 0.3  # 30% chance of mutation per trait
        self.mutation_magnitude = 0.1  # standard deviation for gaussian mutation
        
        # food settings
        self.initial_food_count = 50
        self.food_size = 6
        self.food_regen_rate = 0.02
        self.max_food_per_cell = 3
        
        # simulation settings
        self.time_step = 1.0
        self.paused = False
        
        # trait tracking settings
        self.trait_log_interval = 100  # log traits every N frames
        self.max_trait_history = 1000  # max number of trait snapshots to keep
        
        # visualization settings
        self.show_vision_radius = False  # show vision radius circles for debugging
        
        # colors
        self.background_color = (50, 50, 50)
        self.organism_color = (0, 255, 0)
        self.food_color = (255, 255, 0)
        self.text_color = (255, 255, 255)
        
        # phase 3: predator-prey settings
        self.initial_predators = 5
        self.initial_prey = 15
        self.predator_energy_gain_from_prey = 80
        self.predator_attack_range = 15
        self.predator_attack_cooldown = 30  # frames between attacks
        self.prey_flee_distance = 50
        self.prey_flee_speed_multiplier = 1.5
        
        # fitness tracking
        self.fitness_survival_weight = 0.7
        self.fitness_reproduction_weight = 0.3
        
        # carrying capacity and competition
        self.carrying_capacity = 100
        self.competition_intensity = 0.1
        self.resource_scarcity_threshold = 0.3  # when food is scarce, increase competition
        
        # terrain settings
        self.terrain_enabled = True
        self.obstacle_count = 20
        self.obstacle_size_range = (20, 60)
        self.obstacle_color = (100, 100, 100)
        
        # species colors
        self.predator_color = (255, 0, 0)  # red
        self.prey_color = (0, 255, 0)      # green 