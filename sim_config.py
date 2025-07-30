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