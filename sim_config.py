class SimConfig:
    def __init__(self):
        # display settings
        self.width = 1200
        self.height = 800
        self.fps = 60
        self.title = "Natural Selection Simulator - Enhanced"
        
        # world settings
        self.world_width = 1000
        self.world_height = 600
        
        # organism settings - completely rebalanced for realism
        self.initial_organisms = 30
        self.organism_size = 8
        self.organism_speed = 2.0
        self.initial_energy = 150  # reduced for more pressure
        self.energy_decay_rate = 0.15  # increased pressure
        self.energy_gain_from_food = 60  # reduced for more pressure
        self.min_energy_to_reproduce = 100  # increased threshold
        
        # dna and mutation settings - more realistic
        self.mutation_rate = 0.15  # reduced for more stable evolution
        self.mutation_magnitude = 0.08  # smaller mutations for gradual change
        
        # food settings - more realistic scarcity
        self.initial_food_count = 80  # reduced for more competition
        self.food_size = 6
        self.food_regen_rate = 0.08  # slower regeneration
        self.max_food_per_cell = 2  # reduced for more competition
        
        # simulation settings
        self.time_step = 1.0
        self.paused = False
        
        # trait tracking settings
        self.trait_log_interval = 100
        self.max_trait_history = 1000
        
        # visualization settings
        self.show_vision_radius = False
        self.show_trait_indicators = True  # new: show trait-based visual indicators
        
        # colors
        self.background_color = (50, 50, 50)
        self.organism_color = (0, 255, 0)
        self.food_color = (255, 255, 0)
        self.text_color = (255, 255, 255)
        
        # phase 3: predator-prey settings - completely rebalanced
        self.initial_predators = 8
        self.initial_prey = 22
        self.predator_energy_gain_from_prey = 80  # reduced for balance
        self.predator_attack_range = 12  # reduced for more skill requirement
        self.predator_attack_cooldown = 45  # increased cooldown
        self.prey_flee_distance = 60
        self.prey_flee_speed_multiplier = 1.3  # reduced for balance
        
        # fitness tracking - more realistic
        self.fitness_survival_weight = 0.6
        self.fitness_reproduction_weight = 0.4
        
        # carrying capacity and competition - more realistic
        self.carrying_capacity = 120  # reduced for more pressure
        self.competition_intensity = 0.08  # increased competition
        self.resource_scarcity_threshold = 0.15  # more sensitive
        
        # terrain settings
        self.terrain_enabled = True
        self.obstacle_count = 12  # reduced for better movement
        self.obstacle_size_range = (25, 50)
        self.obstacle_color = (100, 100, 100)
        
        # species colors
        self.predator_color = (255, 0, 0)
        self.prey_color = (0, 255, 0)
        
        # phase 4: speciation settings - more realistic
        self.speciation_genetic_threshold = 0.25  # reduced for easier speciation
        self.speciation_spatial_threshold = 80   # reduced spatial requirement
        self.speciation_cooldown = 800          # reduced cooldown
        self.show_species_colors = True
        self.track_lineages = True
        
        # phase 5: environment and weather settings - more impactful
        self.day_night_cycle_enabled = True
        self.day_night_cycle_duration = 900  # faster cycles
        self.night_vision_penalty = 0.6  # stronger night penalty
        
        self.temperature_zones_enabled = True
        self.temperature_zones_count = 3
        self.cold_zone_y_range = (0, 180)  # larger cold zone
        self.hot_zone_y_range = (420, 600)  # larger hot zone
        self.cold_temperature = -15  # more extreme
        self.moderate_temperature = 20
        self.hot_temperature = 55  # more extreme
        self.temperature_effect_on_metabolism = 0.15  # stronger effect
        
        self.seasons_enabled = True
        self.season_duration = 3600  # faster seasons
        self.season_food_multiplier = {
            'spring': 1.1,  # more moderate
            'summer': 0.9,  # summer scarcity
            'autumn': 0.7,  # autumn scarcity
            'winter': 0.4   # severe winter scarcity
        }
        self.season_temperature_modifier = {
            'spring': 3,   # more moderate
            'summer': 12,  # more moderate
            'autumn': 3,   # more moderate
            'winter': -8   # more moderate
        }
        
        # weather visualization
        self.show_temperature_zones = True
        self.show_day_night_cycle = True
        self.show_season_indicator = True
        
        # weather colors
        self.night_color = (15, 15, 35)
        self.day_color = (50, 50, 50)
        self.cold_zone_color = (80, 120, 255)
        self.hot_zone_color = (255, 120, 80)
        
        # phase 6: behavioral evolution settings - more impactful
        self.behavioral_evolution_enabled = True
        self.decision_cooldown = 25  # faster decisions
        self.state_duration_multiplier = 0.8  # shorter states for more dynamic behavior
        self.perception_memory_size = 8  # reduced for performance
        self.behavior_learning_rate = 0.15  # faster learning
        
        # phase 6: prey protective feature settings - more impactful
        self.camouflage_effectiveness = 0.7  # stronger camouflage
        self.toxicity_damage_multiplier = 25  # stronger toxicity
        self.armor_protection_factor = 0.6  # stronger armor
        self.warning_signal_range = 1.4  # longer warning range
        self.group_cohesion_range = 0.7  # tighter groups
        
        # phase 6: predator hunting strategy settings - more impactful
        self.ambush_hunting_threshold = 0.6  # easier ambush
        self.cooperative_hunting_threshold = 0.5  # easier cooperation
        self.hunting_learning_rate = 0.15  # faster learning
        self.patience_threshold = 0.5  # easier patience
        
        # phase 6: social behavior settings - more impactful
        self.social_behavior_threshold = 0.3  # easier social behavior
        self.group_formation_threshold = 2  # smaller groups
        self.information_sharing_range = 0.7  # longer sharing range
        
        # phase 6: intelligence and learning settings - more impactful
        self.intelligence_decision_bonus = 1.3  # stronger intelligence bonus
        self.memory_capacity_multiplier = 8  # more reasonable memory
        self.exploration_rate_multiplier = 0.8  # more exploration
        
        # phase 6: visualization settings
        self.show_behavior_states = True
        self.show_perception_range = False
        self.show_social_connections = False
        self.show_hunting_targets = False
        
        # new: trait interaction settings
        self.trait_interaction_enabled = True
        self.trait_synergy_bonus = 0.2  # bonus for complementary traits
        self.trait_conflict_penalty = 0.15  # penalty for conflicting traits
        
        # new: realistic energy costs
        self.movement_energy_cost = 0.02  # energy cost per movement unit
        self.attack_energy_cost = 15  # energy cost for attacking
        self.reproduction_energy_cost = 50  # energy cost for reproduction
        self.social_energy_cost = 0.01  # energy cost for social behavior
        
        # new: realistic trait effects
        self.speed_energy_multiplier = 1.5  # faster movement costs more energy
        self.vision_energy_cost = 0.005  # energy cost for vision
        self.size_energy_multiplier = 1.3  # larger organisms need more energy
        self.metabolism_energy_multiplier = 1.2  # higher metabolism costs more
        
        # new: environmental adaptation
        self.weather_adaptation_bonus = 0.3  # bonus for well-adapted organisms
        self.weather_maladaptation_penalty = 0.4  # penalty for poorly adapted organisms
        
        # new: evolutionary pressure settings
        self.selection_pressure_multiplier = 1.2  # stronger selection pressure
        self.fitness_threshold_for_reproduction = 0.6  # minimum fitness for reproduction
        self.genetic_drift_rate = 0.05  # random genetic changes
        
        # new: realistic population dynamics
        self.population_growth_rate = 0.02  # natural population growth
        self.population_decline_rate = 0.03  # natural population decline
        self.extinction_threshold = 3  # minimum population before extinction
        self.recovery_threshold = 5  # population needed for recovery
        
        # new: trait evolution settings
        self.trait_evolution_rate = 0.1  # rate of trait evolution
        self.trait_convergence_threshold = 0.1  # threshold for trait convergence
        self.trait_divergence_rate = 0.05  # rate of trait divergence
        
        # new: realistic interaction settings
        self.predator_prey_balance_factor = 1.1  # factor for predator-prey balance
        self.resource_competition_intensity = 0.12  # intensity of resource competition
        self.territorial_behavior_enabled = True  # enable territorial behavior
        self.mating_selection_enabled = True  # enable mate selection
        
        # new: advanced behavioral settings
        self.learning_enabled = True  # enable learning from experience
        self.memory_decay_rate = 0.02  # rate at which memories decay
        self.behavior_adaptation_rate = 0.1  # rate of behavioral adaptation
        self.social_learning_enabled = True  # enable learning from others
        
        # new: realistic physics settings
        self.collision_detection_enabled = True  # enable collision detection
        self.momentum_conservation = 0.8  # conservation of momentum
        self.friction_factor = 0.95  # friction in movement
        self.gravity_effect = 0.01  # slight gravity effect
        
        # new: advanced visualization settings
        self.show_energy_bars = True  # show energy bars on organisms
        self.show_trait_indicators = True  # show trait-based visual indicators
        self.show_behavior_indicators = True  # show behavioral state indicators
        self.show_environmental_effects = True  # show environmental effects
        self.show_evolutionary_pressure = True  # show evolutionary pressure indicators 