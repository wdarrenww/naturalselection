import random
import math
import numpy as np
from sim_config import SimConfig

class DNA:
    def __init__(self, config: SimConfig, parent_dna=None):
        self.config = config
        
        if parent_dna:
            # inherit from parent with mutation
            self.traits = self._inherit_with_mutation(parent_dna.traits)
        else:
            # generate random initial traits
            self.traits = self._generate_random_traits()
    
    def _generate_random_traits(self):
        return {
            'speed': random.uniform(1.0, 3.0),  # increased minimum speed
            'vision': random.uniform(30, 120),   # increased minimum vision
            'size': random.uniform(0.5, 1.5),
            'metabolism': random.uniform(0.2, 0.8),  # reduced metabolism range
            'reproduction_threshold': random.uniform(40, 80),  # reduced threshold
            'max_age': random.randint(300, 1000),  # increased minimum age
            'aggression': random.uniform(0.1, 1.0),  # for predators
            'caution': random.uniform(0.1, 1.0),     # for prey
            'stamina': random.uniform(0.8, 2.0),     # increased stamina
            # phase 5: weather adaptation traits
            'cold_resistance': random.uniform(0.1, 1.0),  # resistance to cold temperatures
            'heat_resistance': random.uniform(0.1, 1.0),  # resistance to hot temperatures
            'night_vision': random.uniform(0.1, 1.0),     # ability to see in low light
            # phase 6: behavioral evolution traits
            'intelligence': random.uniform(0.1, 1.0),     # decision making ability
            'social_behavior': random.uniform(0.1, 1.0),  # group behavior tendency
            'exploration_rate': random.uniform(0.1, 1.0), # tendency to explore new areas
            'memory_capacity': random.uniform(0.1, 1.0),  # ability to remember past events
            # phase 6: prey protective traits
            'camouflage': random.uniform(0.1, 1.0),       # ability to hide from predators
            'toxicity': random.uniform(0.1, 1.0),         # poisonous/repellent to predators
            'armor': random.uniform(0.1, 1.0),            # physical protection
            'warning_signals': random.uniform(0.1, 1.0),  # ability to signal danger to others
            'group_cohesion': random.uniform(0.1, 1.0),   # tendency to stay in groups
            # phase 6: predator hunting traits
            'hunting_strategy': random.uniform(0.1, 1.0), # different hunting approaches
            'patience': random.uniform(0.1, 1.0),         # willingness to wait for prey
            'cooperation': random.uniform(0.1, 1.0),      # ability to hunt in groups
            'learning_rate': random.uniform(0.1, 1.0),     # ability to adapt hunting strategies
            # new: enhanced trait interactions
            'efficiency': random.uniform(0.1, 1.0),  # energy efficiency
            'adaptability': random.uniform(0.1, 1.0),  # ability to adapt to changes
            'resilience': random.uniform(0.1, 1.0),  # ability to recover from damage
            'specialization': random.uniform(0.1, 1.0),  # specialization vs generalization
            'innovation': random.uniform(0.1, 1.0)  # ability to develop new strategies
        }
    
    def _inherit_with_mutation(self, parent_traits):
        traits = {}
        for trait_name, parent_value in parent_traits.items():
            # gaussian mutation with configurable rate and magnitude
            mutation_rate = self.config.mutation_rate
            mutation_magnitude = self.config.mutation_magnitude
            
            if random.random() < mutation_rate:
                # apply gaussian mutation
                mutation = random.gauss(0, mutation_magnitude)
                traits[trait_name] = parent_value + mutation
            else:
                traits[trait_name] = parent_value
            
            # ensure traits stay within reasonable bounds
            traits[trait_name] = self._clamp_trait(trait_name, traits[trait_name])
        
        return traits
    
    def _clamp_trait(self, trait_name, value):
        # define bounds for each trait
        bounds = {
            'speed': (0.1, 3.0),
            'vision': (10, 150),
            'size': (0.3, 2.0),
            'metabolism': (0.1, 2.0),
            'reproduction_threshold': (40, 120),
            'max_age': (100, 1000),
            'aggression': (0.05, 1.5),
            'caution': (0.05, 1.5),
            'stamina': (0.2, 2.0),
            # phase 5: weather adaptation trait bounds
            'cold_resistance': (0.05, 1.5),
            'heat_resistance': (0.05, 1.5),
            'night_vision': (0.05, 1.5),
            # phase 6: behavioral evolution trait bounds
            'intelligence': (0.05, 1.5),
            'social_behavior': (0.05, 1.5),
            'exploration_rate': (0.05, 1.5),
            'memory_capacity': (0.05, 1.5),
            # phase 6: prey protective trait bounds
            'camouflage': (0.05, 1.5),
            'toxicity': (0.05, 1.5),
            'armor': (0.05, 1.5),
            'warning_signals': (0.05, 1.5),
            'group_cohesion': (0.05, 1.5),
            # phase 6: predator hunting trait bounds
            'hunting_strategy': (0.05, 1.5),
            'patience': (0.05, 1.5),
            'cooperation': (0.05, 1.5),
            'learning_rate': (0.05, 1.5),
            # new: enhanced trait bounds
            'efficiency': (0.05, 1.5),
            'adaptability': (0.05, 1.5),
            'resilience': (0.05, 1.5),
            'specialization': (0.05, 1.5),
            'innovation': (0.05, 1.5)
        }
        
        min_val, max_val = bounds.get(trait_name, (0, float('inf')))
        return max(min_val, min(max_val, value))
    
    def calculate_genetic_distance(self, other_dna):
        """calculate genetic distance between two dna sequences"""
        if not other_dna:
            return float('inf')
        
        total_distance = 0
        trait_count = 0
        
        for trait_name in self.traits.keys():
            if trait_name in other_dna.traits:
                # normalize trait values to 0-1 range for comparison
                my_value = self.traits[trait_name]
                other_value = other_dna.traits[trait_name]
                
                # calculate normalized difference
                # use trait-specific normalization based on typical ranges
                normalization_factors = {
                    'speed': 3.0,
                    'vision': 150.0,
                    'size': 2.0,
                    'metabolism': 2.0,
                    'reproduction_threshold': 120.0,
                    'max_age': 1000.0,
                    'aggression': 1.5,
                    'caution': 1.5,
                    'stamina': 2.0,
                    # phase 5: weather adaptation normalization
                    'cold_resistance': 1.5,
                    'heat_resistance': 1.5,
                    'night_vision': 1.5,
                    # phase 6: behavioral evolution normalization
                    'intelligence': 1.5,
                    'social_behavior': 1.5,
                    'exploration_rate': 1.5,
                    'memory_capacity': 1.5,
                    # phase 6: prey protective trait normalization
                    'camouflage': 1.5,
                    'toxicity': 1.5,
                    'armor': 1.5,
                    'warning_signals': 1.5,
                    'group_cohesion': 1.5,
                    # phase 6: predator hunting trait normalization
                    'hunting_strategy': 1.5,
                    'patience': 1.5,
                    'cooperation': 1.5,
                    'learning_rate': 1.5,
                    # new: enhanced trait normalization
                    'efficiency': 1.5,
                    'adaptability': 1.5,
                    'resilience': 1.5,
                    'specialization': 1.5,
                    'innovation': 1.5
                }
                
                norm_factor = normalization_factors.get(trait_name, 1.0)
                normalized_diff = abs(my_value - other_value) / norm_factor
                total_distance += normalized_diff
                trait_count += 1
        
        # return average distance across all traits
        return total_distance / max(1, trait_count)
    
    def calculate_trait_synergies(self):
        """calculate trait synergies and conflicts"""
        synergies = []
        conflicts = []
        
        # define trait synergies (complementary traits)
        synergy_pairs = [
            ('speed', 'stamina'),  # speed + stamina = better movement
            ('vision', 'intelligence'),  # vision + intelligence = better perception
            ('aggression', 'hunting_strategy'),  # aggression + hunting = better hunting
            ('caution', 'camouflage'),  # caution + camouflage = better survival
            ('social_behavior', 'cooperation'),  # social + cooperation = better groups
            ('memory_capacity', 'learning_rate'),  # memory + learning = better adaptation
            ('efficiency', 'metabolism'),  # efficiency + metabolism = better energy use
            ('adaptability', 'innovation'),  # adaptability + innovation = better evolution
            ('resilience', 'armor'),  # resilience + armor = better protection
            ('exploration_rate', 'innovation')  # exploration + innovation = better discovery
        ]
        
        # define trait conflicts (opposing traits)
        conflict_pairs = [
            ('aggression', 'caution'),  # aggression vs caution
            ('speed', 'size'),  # speed vs size (trade-off)
            ('specialization', 'adaptability'),  # specialization vs adaptability
            ('efficiency', 'innovation'),  # efficiency vs innovation
            ('social_behavior', 'exploration_rate')  # social vs exploration
        ]
        
        # calculate synergy scores
        for trait1, trait2 in synergy_pairs:
            if trait1 in self.traits and trait2 in self.traits:
                value1 = self.traits[trait1]
                value2 = self.traits[trait2]
                synergy_score = (value1 + value2) / 2.0
                synergies.append((trait1, trait2, synergy_score))
        
        # calculate conflict scores
        for trait1, trait2 in conflict_pairs:
            if trait1 in self.traits and trait2 in self.traits:
                value1 = self.traits[trait1]
                value2 = self.traits[trait2]
                conflict_score = abs(value1 - value2)
                conflicts.append((trait1, trait2, conflict_score))
        
        return synergies, conflicts

class BehaviorState:
    """phase 6: behavioral state machine states"""
    IDLE = "idle"
    SEEK_FOOD = "seek_food"
    EVADE = "evade"
    SEEK_MATE = "seek_mate"
    REST = "rest"
    HUNT = "hunt"
    EXPLORE = "explore"
    GROUP_BEHAVIOR = "group_behavior"

class Organism:
    def __init__(self, x, y, config: SimConfig, parent_dna=None, species_type='prey', parent_id=None):
        self.x = x
        self.y = y
        self.config = config
        self.dna = DNA(config, parent_dna)
        self.energy = config.initial_energy
        self.alive = True
        self.age = 0
        self.id = self._generate_id()
        self.species_type = species_type  # 'predator' or 'prey'
        
        # phase 4: lineage tracking
        self.parent_id = parent_id
        self.ancestors = self._initialize_ancestors(parent_id)
        self.species_id = self._assign_initial_species_id()
        self.generation = self._calculate_generation()
        
        # movement direction (random initial direction)
        self.dx = random.uniform(-1, 1)
        self.dy = random.uniform(-1, 1)
        self._normalize_direction()
        
        # phenotype mapping - convert dna traits to actual behavior
        self._update_phenotype()
        
        # fitness tracking
        self.fitness_score = 0
        self.survival_time = 0
        self.reproduction_count = 0
        self.last_attack_time = 0  # for predators
        self.flee_target = None     # for prey
        self.flee_timer = 0
        
        # phase 4: speciation tracking
        self.last_speciation_check = 0
        self.speciation_cooldown = 1000  # frames between speciation checks
        
        # phase 5: weather adaptation tracking
        self.current_temperature = 20  # default moderate temperature
        self.temperature_stress = 0.0  # accumulated temperature stress
        self.weather_adaptation_score = 0.0  # how well adapted to current weather
        
        # phase 6: behavioral evolution system
        self.current_state = BehaviorState.IDLE
        self.state_timer = 0
        self.state_duration = 0
        self.perception_memory = []  # remember recent perceptions
        self.behavior_weights = self._initialize_behavior_weights()
        self.last_decision_time = 0
        self.decision_cooldown = 30  # frames between decisions
        
        # phase 6: prey protective features
        self.camouflage_active = False
        self.toxicity_damage = 0
        self.armor_protection = 0
        self.warning_signal_cooldown = 0
        self.group_members = []  # nearby organisms of same type
        
        # phase 6: predator hunting features
        self.hunting_target = None
        self.hunting_strategy_cooldown = 0
        self.learned_behaviors = {}  # remember successful strategies
        
        # phase 6: social behavior tracking
        self.social_connections = []
        self.group_center = None
        self.is_group_leader = False
        
        # new: enhanced trait interaction tracking
        self.trait_synergies = []
        self.trait_conflicts = []
        self.evolutionary_pressure = 0.0
        self.adaptation_score = 0.0
        self.energy_efficiency = 1.0
        
        # new: realistic physics tracking
        self.momentum_x = 0.0
        self.momentum_y = 0.0
        self.velocity_x = 0.0
        self.velocity_y = 0.0
        
        # new: learning and memory tracking
        self.experience_memory = []
        self.learned_strategies = {}
        self.behavioral_adaptations = {}
        
        # new: environmental interaction tracking
        self.territory_center = None
        self.territory_radius = 0
        self.resource_claims = []
        
        # calculate initial trait interactions
        self._calculate_trait_interactions()
    
    def _calculate_trait_interactions(self):
        """calculate trait synergies and conflicts"""
        self.trait_synergies, self.trait_conflicts = self.dna.calculate_trait_synergies()
        
        # calculate overall adaptation score
        synergy_bonus = sum(synergy[2] for synergy in self.trait_synergies) * self.config.trait_synergy_bonus
        conflict_penalty = sum(conflict[2] for conflict in self.trait_conflicts) * self.config.trait_conflict_penalty
        
        self.adaptation_score = max(0.1, 1.0 + synergy_bonus - conflict_penalty)
        
        # calculate energy efficiency based on traits
        efficiency_trait = self.dna.traits.get('efficiency', 0.5)
        metabolism_trait = self.dna.traits.get('metabolism', 0.5)
        
        # efficiency reduces energy costs, metabolism increases them
        self.energy_efficiency = efficiency_trait / (1.0 + metabolism_trait)
    
    def _generate_id(self):
        # simple id generation for tracking
        return random.randint(1000000, 9999999)
    
    def _initialize_ancestors(self, parent_id):
        """initialize ancestry tracking"""
        if parent_id is None:
            # founder organism
            return [self.id]
        else:
            # inherit parent's ancestors and add parent
            return [parent_id]  # simplified for now
    
    def _assign_initial_species_id(self):
        """assign initial species id based on type and traits"""
        if self.species_type == 'predator':
            return f"predator_{self.id}"
        else:
            return f"prey_{self.id}"
    
    def _calculate_generation(self):
        """calculate generation number based on ancestry"""
        if self.parent_id is None:
            return 1
        else:
            # simplified generation calculation
            return 2  # will be updated by simulation
    
    def _initialize_behavior_weights(self):
        """phase 6: initialize behavior decision weights"""
        return {
            'seek_food_weight': self.dna.traits['intelligence'] * 0.5 + 0.5,
            'evade_weight': self.dna.traits['caution'] * 0.8 + 0.2,
            'rest_weight': (1.0 - self.dna.traits['stamina']) * 0.6 + 0.4,
            'explore_weight': self.dna.traits['exploration_rate'] * 0.7 + 0.3,
            'social_weight': self.dna.traits['social_behavior'] * 0.8 + 0.2,
            'hunt_weight': self.dna.traits['aggression'] * 0.8 + 0.2,
            'patience_weight': self.dna.traits['patience'] * 0.6 + 0.4,
            'cooperation_weight': self.dna.traits['cooperation'] * 0.7 + 0.3
        }
    
    def _update_phenotype(self):
        # convert dna traits to actual organism properties
        self.speed = self.dna.traits['speed']
        self.vision_radius = self.dna.traits['vision']
        self.size = self.config.organism_size * self.dna.traits['size']
        self.metabolism_rate = self.config.energy_decay_rate * self.dna.traits['metabolism']
        self.reproduction_threshold = self.dna.traits['reproduction_threshold']
        self.max_age = self.dna.traits['max_age']
        self.aggression = self.dna.traits['aggression']
        self.caution = self.dna.traits['caution']
        self.stamina = self.dna.traits['stamina']
        
        # phase 5: weather adaptation traits
        self.cold_resistance = self.dna.traits['cold_resistance']
        self.heat_resistance = self.dna.traits['heat_resistance']
        self.night_vision = self.dna.traits['night_vision']
        
        # phase 6: behavioral evolution traits
        self.intelligence = self.dna.traits['intelligence']
        self.social_behavior = self.dna.traits['social_behavior']
        self.exploration_rate = self.dna.traits['exploration_rate']
        self.memory_capacity = self.dna.traits['memory_capacity']
        
        # phase 6: prey protective traits
        self.camouflage = self.dna.traits['camouflage']
        self.toxicity = self.dna.traits['toxicity']
        self.armor = self.dna.traits['armor']
        self.warning_signals = self.dna.traits['warning_signals']
        self.group_cohesion = self.dna.traits['group_cohesion']
        
        # phase 6: predator hunting traits
        self.hunting_strategy = self.dna.traits['hunting_strategy']
        self.patience = self.dna.traits['patience']
        self.cooperation = self.dna.traits['cooperation']
        self.learning_rate = self.dna.traits['learning_rate']
        
        # new: enhanced traits
        self.efficiency = self.dna.traits['efficiency']
        self.adaptability = self.dna.traits['adaptability']
        self.resilience = self.dna.traits['resilience']
        self.specialization = self.dna.traits['specialization']
        self.innovation = self.dna.traits['innovation']
    
    def _normalize_direction(self):
        # normalize direction vector
        length = math.sqrt(self.dx**2 + self.dy**2)
        if length > 0:
            self.dx /= length
            self.dy /= length
    
    def update(self, food_list, other_organisms, obstacles, weather_system=None):
        if not self.alive:
            return
        
        self.age += 1
        self.survival_time += 1
        
        # phase 5: update weather effects
        if weather_system:
            self._update_weather_effects(weather_system)
        
        # phase 4: check for speciation periodically
        if self.age - self.last_speciation_check > self.speciation_cooldown:
            self._check_speciation(other_organisms)
            self.last_speciation_check = self.age
        
        # phase 6: update behavioral state machine
        self._update_behavioral_state(food_list, other_organisms, obstacles, weather_system)
        
        # execute behavior based on current state
        self._execute_behavior(food_list, other_organisms, obstacles, weather_system)
        
        # phase 6: update protective features
        self._update_protective_features(other_organisms)
        
        # phase 6: update hunting strategies
        if self.species_type == 'predator':
            self._update_hunting_strategies(other_organisms)
        
        # phase 6: update social behavior
        self._update_social_behavior(other_organisms)
        
        # new: update enhanced systems
        self._update_physics()
        self._update_learning()
        self._update_territorial_behavior(other_organisms)
        self._update_evolutionary_pressure(other_organisms)
        
        self._consume_energy()
        self._check_death()
    
    def _update_behavioral_state(self, food_list, other_organisms, obstacles, weather_system=None):
        """phase 6: update behavioral state machine"""
        # update state timer
        self.state_timer += 1
        
        # check if it's time to make a new decision
        if (self.age - self.last_decision_time > self.decision_cooldown or 
            self.state_timer > self.state_duration):
            self._make_behavioral_decision(food_list, other_organisms, weather_system)
            self.last_decision_time = self.age
            self.state_timer = 0
    
    def _make_behavioral_decision(self, food_list, other_organisms, weather_system=None):
        """phase 6: make behavioral decision based on current situation and traits"""
        # gather perception data
        perception = self._gather_perception_data(food_list, other_organisms, weather_system)
        
        # store in memory
        self._update_perception_memory(perception)
        
        # calculate state probabilities based on situation and traits
        state_scores = self._calculate_state_scores(perception)
        
        # select new state based on scores and randomness
        self._select_new_state(state_scores)
    
    def _gather_perception_data(self, food_list, other_organisms, weather_system):
        """phase 6: gather perception data from environment"""
        perception = {
            'nearby_food': [],
            'nearby_predators': [],
            'nearby_prey': [],
            'nearby_allies': [],
            'energy_level': self.energy / self.config.initial_energy,
            'temperature_stress': getattr(self, 'temperature_stress', 0.0),
            'light_level': weather_system.get_light_level() if weather_system else 1.0,
            'group_size': len(self.group_members),
            'threat_level': 0.0,
            'food_availability': 0.0
        }
        
        # scan for nearby entities
        for food in food_list:
            if food.available:
                distance = self._distance_to(food)
                if distance < self.vision_radius:
                    perception['nearby_food'].append((food, distance))
                    perception['food_availability'] += 1.0 / max(1, distance)
        
        for org in other_organisms:
            if org.alive and org.id != self.id:
                distance = self._distance_to(org)
                if distance < self.vision_radius:
                    if org.species_type == 'predator' and self.species_type == 'prey':
                        perception['nearby_predators'].append((org, distance))
                        perception['threat_level'] += 1.0 / max(1, distance)
                    elif org.species_type == 'prey' and self.species_type == 'predator':
                        perception['nearby_prey'].append((org, distance))
                    elif org.species_type == self.species_type:
                        perception['nearby_allies'].append((org, distance))
        
        return perception
    
    def _update_perception_memory(self, perception):
        """phase 6: update perception memory with recent data"""
        self.perception_memory.append(perception)
        
        # limit memory size based on memory capacity trait
        max_memory = int(self.memory_capacity * 10) + 5
        if len(self.perception_memory) > max_memory:
            self.perception_memory.pop(0)
    
    def _calculate_state_scores(self, perception):
        """phase 6: calculate scores for different behavioral states"""
        scores = {}
        
        # base scores from behavior weights
        scores[BehaviorState.SEEK_FOOD] = self.behavior_weights['seek_food_weight']
        scores[BehaviorState.EVADE] = self.behavior_weights['evade_weight']
        scores[BehaviorState.REST] = self.behavior_weights['rest_weight']
        scores[BehaviorState.EXPLORE] = self.behavior_weights['explore_weight']
        scores[BehaviorState.GROUP_BEHAVIOR] = self.behavior_weights['social_weight']
        
        if self.species_type == 'predator':
            scores[BehaviorState.HUNT] = self.behavior_weights['hunt_weight']
        
        # modify scores based on current situation
        self._modify_scores_by_situation(scores, perception)
        
        return scores
    
    def _modify_scores_by_situation(self, scores, perception):
        """phase 6: modify state scores based on current situation"""
        # energy-based modifications
        if perception['energy_level'] < 0.3:
            scores[BehaviorState.SEEK_FOOD] *= 2.0
            scores[BehaviorState.REST] *= 1.5
        elif perception['energy_level'] < 0.6:
            scores[BehaviorState.SEEK_FOOD] *= 1.5
        
        # threat-based modifications
        if perception['threat_level'] > 0.5:
            scores[BehaviorState.EVADE] *= 2.0
            scores[BehaviorState.REST] *= 0.5
        elif perception['threat_level'] > 0.2:
            scores[BehaviorState.EVADE] *= 1.5
        
        # food availability modifications
        if perception['food_availability'] > 0.5:
            scores[BehaviorState.SEEK_FOOD] *= 1.5
        elif perception['food_availability'] < 0.1:
            scores[BehaviorState.EXPLORE] *= 1.5
        
        # social behavior modifications
        if perception['group_size'] > 3:
            scores[BehaviorState.GROUP_BEHAVIOR] *= 1.5
        elif perception['group_size'] == 0 and self.social_behavior > 0.7:
            scores[BehaviorState.GROUP_BEHAVIOR] *= 1.3
        
        # predator-specific modifications
        if self.species_type == 'predator':
            if perception['nearby_prey']:
                scores[BehaviorState.HUNT] *= 1.8
            else:
                scores[BehaviorState.HUNT] *= 0.7
                scores[BehaviorState.EXPLORE] *= 1.3
        
        # weather-based modifications
        if hasattr(self, 'current_temperature'):
            if self.current_temperature < 10 or self.current_temperature > 30:
                scores[BehaviorState.REST] *= 1.3  # rest more in extreme temperatures
        
        # intelligence-based modifications
        if self.intelligence > 0.7:
            # intelligent organisms make better decisions
            for state in scores:
                if scores[state] > 1.0:
                    scores[state] *= 1.2
    
    def _select_new_state(self, state_scores):
        """phase 6: select new behavioral state based on scores"""
        # convert scores to probabilities
        total_score = sum(state_scores.values())
        if total_score == 0:
            # fallback to idle
            self.current_state = BehaviorState.IDLE
            self.state_duration = random.randint(30, 120)
            return
        
        probabilities = {state: score / total_score for state, score in state_scores.items()}
        
        # select state using weighted random choice
        states = list(probabilities.keys())
        weights = list(probabilities.values())
        
        self.current_state = random.choices(states, weights=weights)[0]
        
        # set state duration based on state type and traits
        self.state_duration = self._calculate_state_duration()
    
    def _calculate_state_duration(self):
        """phase 6: calculate how long to stay in current state"""
        base_duration = 60  # 1 second at 60fps
        
        if self.current_state == BehaviorState.REST:
            return random.randint(30, 90)  # shorter rest periods
        elif self.current_state == BehaviorState.EVADE:
            return random.randint(20, 60)  # short evade periods
        elif self.current_state == BehaviorState.SEEK_FOOD:
            return random.randint(60, 180)  # longer food seeking
        elif self.current_state == BehaviorState.EXPLORE:
            return random.randint(120, 300)  # longer exploration
        elif self.current_state == BehaviorState.HUNT:
            return random.randint(60, 150)  # moderate hunting periods
        elif self.current_state == BehaviorState.GROUP_BEHAVIOR:
            return random.randint(90, 240)  # longer group behavior
        else:
            return random.randint(30, 120)  # default duration
    
    def _execute_behavior(self, food_list, other_organisms, obstacles, weather_system=None):
        """phase 6: execute behavior based on current state"""
        if self.current_state == BehaviorState.IDLE:
            self._execute_idle_behavior(obstacles)
        elif self.current_state == BehaviorState.SEEK_FOOD:
            self._execute_seek_food_behavior(food_list, obstacles)
        elif self.current_state == BehaviorState.EVADE:
            self._execute_evade_behavior(other_organisms, obstacles)
        elif self.current_state == BehaviorState.REST:
            self._execute_rest_behavior(obstacles)
        elif self.current_state == BehaviorState.EXPLORE:
            self._execute_explore_behavior(obstacles)
        elif self.current_state == BehaviorState.HUNT:
            self._execute_hunt_behavior(other_organisms, obstacles)
        elif self.current_state == BehaviorState.GROUP_BEHAVIOR:
            self._execute_group_behavior(other_organisms, obstacles)
        elif self.current_state == BehaviorState.SEEK_MATE:
            self._execute_seek_mate_behavior(other_organisms, obstacles)
    
    def _execute_idle_behavior(self, obstacles):
        """phase 6: execute idle behavior"""
        # minimal movement, conserve energy
        if random.random() < 0.1:  # 10% chance to move
            self._move_randomly_improved(obstacles)
    
    def _execute_seek_food_behavior(self, food_list, obstacles):
        """phase 6: execute food seeking behavior"""
        # actively seek food
        if not self._eat_food(food_list):
            # move towards nearest food or explore
            nearest_food = self._find_nearest_food(food_list)
            if nearest_food:
                self._move_towards(nearest_food.x, nearest_food.y, obstacles)
            else:
                self._move_randomly_improved(obstacles)
    
    def _execute_evade_behavior(self, other_organisms, obstacles):
        """phase 6: execute evasion behavior"""
        # find nearest threat
        nearest_threat = None
        if self.species_type == 'prey':
            nearest_threat = self._find_nearest_predator(other_organisms)
        elif self.species_type == 'predator':
            # predators might evade larger predators or dangerous prey
            nearest_threat = self._find_nearest_larger_predator(other_organisms)
        
        if nearest_threat:
            self._flee_from(nearest_threat, obstacles)
        else:
            # no immediate threat, return to normal behavior
            self.current_state = BehaviorState.IDLE
    
    def _execute_rest_behavior(self, obstacles):
        """phase 6: execute rest behavior"""
        # minimal movement, focus on energy recovery
        if random.random() < 0.05:  # 5% chance to move
            self._move_randomly_improved(obstacles)
    
    def _execute_explore_behavior(self, obstacles):
        """phase 6: execute exploration behavior"""
        # move in a more exploratory pattern
        if random.random() < 0.15:  # 15% chance to change direction
            self.dx += random.uniform(-0.5, 0.5)
            self.dy += random.uniform(-0.5, 0.5)
            self._normalize_direction()
        
        self._move_randomly_improved(obstacles)
    
    def _execute_hunt_behavior(self, other_organisms, obstacles):
        """phase 6: execute hunting behavior for predators"""
        if self.species_type != 'predator':
            return
        
        # use different hunting strategies based on traits
        if self.hunting_strategy > 0.7:
            # ambush hunting
            self._execute_ambush_hunting(other_organisms, obstacles)
        elif self.cooperation > 0.6:
            # cooperative hunting
            self._execute_cooperative_hunting(other_organisms, obstacles)
        else:
            # standard pursuit hunting
            self._execute_pursuit_hunting(other_organisms, obstacles)
    
    def _execute_ambush_hunting(self, other_organisms, obstacles):
        """phase 6: execute ambush hunting strategy"""
        # find good ambush position near prey
        nearest_prey = self._find_nearest_prey(other_organisms)
        if nearest_prey and self._distance_to(nearest_prey) < self.vision_radius * 0.5:
            # stay still and wait for prey to come closer
            if self._distance_to(nearest_prey) < self.config.predator_attack_range:
                self._attack_prey(nearest_prey)
        else:
            # move towards prey while staying hidden
            if nearest_prey:
                self._move_towards(nearest_prey.x, nearest_prey.y, obstacles)
    
    def _execute_cooperative_hunting(self, other_organisms, obstacles):
        """phase 6: execute cooperative hunting strategy"""
        # find nearby predators to hunt with
        nearby_predators = [org for org in other_organisms 
                          if org.species_type == 'predator' and org.id != self.id 
                          and self._distance_to(org) < self.vision_radius * 0.8]
        
        nearest_prey = self._find_nearest_prey(other_organisms)
        if nearest_prey and nearby_predators:
            # coordinate attack with other predators
            if self._distance_to(nearest_prey) < self.config.predator_attack_range:
                self._attack_prey(nearest_prey)
                # signal other predators
                for predator in nearby_predators:
                    if self._distance_to(predator) < self.vision_radius * 0.5:
                        predator.hunting_target = nearest_prey
        else:
            # fall back to standard hunting
            self._execute_pursuit_hunting(other_organisms, obstacles)
    
    def _execute_pursuit_hunting(self, other_organisms, obstacles):
        """phase 6: execute standard pursuit hunting"""
        nearest_prey = self._find_nearest_prey(other_organisms)
        if nearest_prey:
            self._move_towards(nearest_prey.x, nearest_prey.y, obstacles)
            if self._distance_to(nearest_prey) < self.config.predator_attack_range:
                self._attack_prey(nearest_prey)
    
    def _execute_group_behavior(self, other_organisms, obstacles):
        """phase 6: execute group behavior"""
        # find nearby allies
        nearby_allies = [org for org in other_organisms 
                        if org.species_type == self.species_type and org.id != self.id 
                        and self._distance_to(org) < self.vision_radius * 0.8]
        
        if nearby_allies:
            # move towards group center
            group_center_x = sum(org.x for org in nearby_allies) / len(nearby_allies)
            group_center_y = sum(org.y for org in nearby_allies) / len(nearby_allies)
            self._move_towards(group_center_x, group_center_y, obstacles)
            
            # share information with group members
            self._share_information_with_group(nearby_allies)
        else:
            # no group nearby, return to normal behavior
            self.current_state = BehaviorState.IDLE
    
    def _execute_seek_mate_behavior(self, other_organisms, obstacles):
        """phase 6: execute mate seeking behavior"""
        # find potential mates
        potential_mates = [org for org in other_organisms 
                         if org.species_type == self.species_type and org.id != self.id 
                         and org.alive and org.can_reproduce()
                         and self._distance_to(org) < self.vision_radius]
        
        if potential_mates:
            # move towards nearest potential mate
            nearest_mate = min(potential_mates, key=lambda org: self._distance_to(org))
            self._move_towards(nearest_mate.x, nearest_mate.y, obstacles)
        else:
            # no mates nearby, return to normal behavior
            self.current_state = BehaviorState.IDLE
    
    def _update_protective_features(self, other_organisms):
        """phase 6: update prey protective features"""
        if self.species_type != 'prey':
            return
        
        # update camouflage
        self._update_camouflage(other_organisms)
        
        # update toxicity
        self._update_toxicity(other_organisms)
        
        # update armor protection
        self._update_armor_protection()
        
        # update warning signals
        self._update_warning_signals(other_organisms)
        
        # update group cohesion
        self._update_group_cohesion(other_organisms)
    
    def _update_camouflage(self, other_organisms):
        """phase 6: update camouflage effectiveness"""
        # camouflage reduces detection by predators
        nearby_predators = [org for org in other_organisms 
                          if org.species_type == 'predator' and org.alive 
                          and self._distance_to(org) < self.vision_radius]
        
        if nearby_predators and self.camouflage > 0.5:
            # camouflage makes it harder for predators to detect this prey
            for predator in nearby_predators:
                # reduce predator's effective vision against this prey
                camouflage_factor = self.camouflage * 0.5
                if hasattr(predator, 'effective_vision'):
                    predator.effective_vision *= (1.0 - camouflage_factor)
    
    def _update_toxicity(self, other_organisms):
        """phase 6: update toxicity effects"""
        # toxicity can damage predators that attack this prey
        if self.toxicity > 0.3:
            # store toxicity damage for when attacked
            self.toxicity_damage = self.toxicity * 20  # damage to predator
    
    def _update_armor_protection(self):
        """phase 6: update armor protection"""
        # armor reduces damage from attacks
        self.armor_protection = self.armor * 0.5  # 50% damage reduction
    
    def _update_warning_signals(self, other_organisms):
        """phase 6: update warning signal behavior"""
        if self.warning_signals > 0.4 and self.warning_signal_cooldown <= 0:
            # check for nearby threats
            nearby_threats = [org for org in other_organisms 
                            if org.species_type == 'predator' and org.alive 
                            and self._distance_to(org) < self.vision_radius * 0.8]
            
            if nearby_threats:
                # send warning signal to nearby prey
                nearby_prey = [org for org in other_organisms 
                             if org.species_type == 'prey' and org.id != self.id 
                             and self._distance_to(org) < self.vision_radius * 1.2]
                
                for prey in nearby_prey:
                    # trigger evade behavior in nearby prey
                    if hasattr(prey, 'current_state'):
                        prey.current_state = BehaviorState.EVADE
                        prey.state_timer = 0
                        prey.state_duration = 30
                
                self.warning_signal_cooldown = 60  # cooldown between signals
    
        if self.warning_signal_cooldown > 0:
            self.warning_signal_cooldown -= 1
    
    def _update_group_cohesion(self, other_organisms):
        """phase 6: update group cohesion behavior"""
        if self.group_cohesion > 0.5:
            # find nearby prey of same species
            nearby_prey = [org for org in other_organisms 
                          if org.species_type == 'prey' and org.id != self.id 
                          and self._distance_to(org) < self.vision_radius * 0.8]
            
            self.group_members = nearby_prey
            
            # move towards group center if group exists
            if self.group_members:
                group_center_x = sum(org.x for org in self.group_members) / len(self.group_members)
                group_center_y = sum(org.y for org in self.group_members) / len(self.group_members)
                
                # move towards group center
                dx = group_center_x - self.x
                dy = group_center_y - self.y
                distance = math.sqrt(dx*dx + dy*dy)
                
                if distance > 20:  # if not too close to center
                    self.dx = (dx / distance) * self.speed * 0.5
                    self.dy = (dy / distance) * self.speed * 0.5
                    self._normalize_direction()
    
    def _update_hunting_strategies(self, other_organisms):
        """phase 6: update predator hunting strategies"""
        if self.species_type != 'predator':
            return
        
        # learn from successful hunts
        if self.learning_rate > 0.5:
            self._learn_hunting_strategies(other_organisms)
        
        # update hunting target
        if not self.hunting_target or not self.hunting_target.alive:
            self.hunting_target = self._find_nearest_prey(other_organisms)
    
    def _learn_hunting_strategies(self, other_organisms):
        """phase 6: learn from hunting experiences"""
        # track successful hunting strategies
        if self.hunting_target and self._distance_to(self.hunting_target) < self.config.predator_attack_range:
            # record successful approach
            strategy_key = f"hunt_{self.hunting_target.id}"
            if strategy_key not in self.learned_behaviors:
                self.learned_behaviors[strategy_key] = {
                    'success_count': 0,
                    'approach_pattern': (self.dx, self.dy),
                    'distance_threshold': self._distance_to(self.hunting_target)
                }
            
            self.learned_behaviors[strategy_key]['success_count'] += 1
    
    def _update_social_behavior(self, other_organisms):
        """phase 6: update social behavior"""
        if self.social_behavior > 0.4:
            # find social connections
            nearby_same_type = [org for org in other_organisms 
                              if org.species_type == self.species_type and org.id != self.id 
                              and self._distance_to(org) < self.vision_radius * 0.6]
            
            self.social_connections = nearby_same_type
            
            # share information with social connections
            if self.social_connections:
                self._share_information_with_group(self.social_connections)
    
    def _share_information_with_group(self, group_members):
        """phase 6: share information with group members"""
        # share perception data with group members
        if self.perception_memory:
            latest_perception = self.perception_memory[-1]
            
            for member in group_members:
                if hasattr(member, 'perception_memory'):
                    # share threat information
                    if latest_perception['threat_level'] > 0.3:
                        member.current_state = BehaviorState.EVADE
                        member.state_timer = 0
                        member.state_duration = 30
                    
                    # share food information
                    if latest_perception['food_availability'] > 0.5:
                        member.current_state = BehaviorState.SEEK_FOOD
                        member.state_timer = 0
                        member.state_duration = 60
    
    def _find_nearest_larger_predator(self, other_organisms):
        """phase 6: find nearest larger predator (for predator-predator interactions)"""
        nearest_larger = None
        min_distance = float('inf')
        
        for org in other_organisms:
            if (org.alive and org.species_type == 'predator' and org.id != self.id and
                org.size > self.size * 1.2):  # 20% larger
                distance = self._distance_to(org)
                if distance < min_distance:
                    min_distance = distance
                    nearest_larger = org
        
        return nearest_larger
    
    def _find_nearest_food(self, food_list):
        """phase 6: find nearest available food"""
        nearest_food = None
        min_distance = float('inf')
        
        for food in food_list:
            if food.available:
                distance = self._distance_to(food)
                if distance < min_distance:
                    min_distance = distance
                    nearest_food = food
        
        return nearest_food
    
    def _move_randomly_improved(self, obstacles):
        """phase 6: improved random movement with better exploration"""
        # improved random movement with better exploration
        if random.random() < 0.05:  # 5% chance to change direction (reduced from 10%)
            # more gradual direction changes
            self.dx += random.uniform(-0.3, 0.3)
            self.dy += random.uniform(-0.3, 0.3)
            self._normalize_direction()
        
        # avoid obstacles
        self._avoid_obstacles(obstacles)
        
        # move organism using trait-based speed with stamina consideration
        effective_speed = self.speed * min(1.0, self.energy / self.config.initial_energy)
        self.x += self.dx * effective_speed
        self.y += self.dy * effective_speed
        
        # wrap around world boundaries
        self.x = self.x % self.config.world_width
        self.y = self.y % self.config.world_height
    
    def _check_speciation(self, other_organisms):
        """check if this organism should form a new species"""
        if not self.alive:
            return
        
        # find nearby organisms of the same type
        nearby_organisms = []
        for org in other_organisms:
            if (org.alive and org.species_type == self.species_type and 
                org.id != self.id and self._distance_to(org) < self.config.speciation_spatial_threshold):
                nearby_organisms.append(org)
        
        if not nearby_organisms:
            return
        
        # calculate average genetic distance to nearby organisms
        total_distance = 0
        count = 0
        
        for org in nearby_organisms:
            genetic_distance = self.dna.calculate_genetic_distance(org.dna)
            total_distance += genetic_distance
            count += 1
        
        if count > 0:
            avg_genetic_distance = total_distance / count
            
            # if genetic distance is high enough, form new species
            if avg_genetic_distance > self.config.speciation_genetic_threshold:
                self._form_new_species()
    
    def _form_new_species(self):
        """form a new species for this organism"""
        new_species_id = f"{self.species_type}_{self.id}_{self.age}"
        self.species_id = new_species_id
        
        # update generation based on speciation event
        self.generation += 1
    
    def calculate_genetic_distance(self, other_organism):
        """calculate genetic distance to another organism"""
        if not other_organism or not other_organism.alive:
            return float('inf')
        
        return self.dna.calculate_genetic_distance(other_organism.dna)
    
    def _find_nearest_prey(self, other_organisms):
        nearest_prey = None
        min_distance = float('inf')
        
        for org in other_organisms:
            if org.alive and org.species_type == 'prey':
                distance = self._distance_to(org)
                if distance < min_distance:
                    min_distance = distance
                    nearest_prey = org
        
        return nearest_prey
    
    def _find_nearest_predator(self, other_organisms):
        nearest_predator = None
        min_distance = float('inf')
        
        for org in other_organisms:
            if org.alive and org.species_type == 'predator':
                distance = self._distance_to(org)
                if distance < min_distance:
                    min_distance = distance
                    nearest_predator = org
        
        return nearest_predator
    
    def _move_towards(self, target_x, target_y, obstacles):
        # calculate direction to target
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance > 0:
            # normalize and apply speed
            self.dx = (dx / distance) * self.speed
            self.dy = (dy / distance) * self.speed
            
            # avoid obstacles
            self._avoid_obstacles(obstacles)
            
            # move
            self.x += self.dx
            self.y += self.dy
            
            # wrap around world boundaries
            self.x = self.x % self.config.world_width
            self.y = self.y % self.config.world_height
    
    def _flee_from(self, predator, obstacles):
        # calculate direction away from predator
        dx = self.x - predator.x
        dy = self.y - predator.y
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance > 0:
            # normalize and apply enhanced speed
            flee_speed = self.speed * self.config.prey_flee_speed_multiplier
            self.dx = (dx / distance) * flee_speed
            self.dy = (dy / distance) * flee_speed
            
            # avoid obstacles
            self._avoid_obstacles(obstacles)
            
            # move
            self.x += self.dx
            self.y += self.dy
            
            # wrap around world boundaries
            self.x = self.x % self.config.world_width
            self.y = self.y % self.config.world_height
    
    def _move_randomly(self, obstacles):
        # random walk with slight direction changes
        if random.random() < 0.1:  # 10% chance to change direction
            self.dx += random.uniform(-0.5, 0.5)
            self.dy += random.uniform(-0.5, 0.5)
            self._normalize_direction()
        
        # avoid obstacles
        self._avoid_obstacles(obstacles)
        
        # move organism using trait-based speed
        self.x += self.dx * self.speed
        self.y += self.dy * self.speed
        
        # wrap around world boundaries
        self.x = self.x % self.config.world_width
        self.y = self.y % self.config.world_height
    
    def _avoid_obstacles(self, obstacles):
        # simple obstacle avoidance
        for obstacle in obstacles:
            distance = self._distance_to(obstacle)
            if distance < obstacle.size + self.size:
                # calculate avoidance direction
                dx = self.x - obstacle.x
                dy = self.y - obstacle.y
                if dx != 0 or dy != 0:
                    # normalize and apply avoidance
                    length = math.sqrt(dx*dx + dy*dy)
                    self.dx += (dx / length) * 2.0
                    self.dy += (dy / length) * 2.0
                    self._normalize_direction()
    
    def _attack_prey(self, prey):
        """phase 6: predator attacks prey with protective feature handling"""
        if not prey.alive:
            return
        
        # phase 6: check for protective features
        attack_success = True
        damage_to_predator = 0
        
        # check armor protection
        if hasattr(prey, 'armor_protection') and prey.armor_protection > 0:
            armor_reduction = prey.armor_protection
            if random.random() < armor_reduction:
                # armor blocks the attack
                attack_success = False
        
        # check camouflage effectiveness
        if hasattr(prey, 'camouflage') and prey.camouflage > 0.7:
            camouflage_chance = prey.camouflage * 0.3
            if random.random() < camouflage_chance:
                # camouflage prevents detection/attack
                attack_success = False
        
        if attack_success:
            # successful attack
            prey.alive = False
            self.energy += self.config.predator_energy_gain_from_prey
            self.last_attack_time = self.age
            
            # phase 6: handle toxicity damage to predator
            if hasattr(prey, 'toxicity_damage') and prey.toxicity_damage > 0:
                damage_to_predator = prey.toxicity_damage
                self.energy -= damage_to_predator
                
                # if predator dies from toxicity, mark prey as also dead (mutual destruction)
                if self.energy <= 0:
                    self.alive = False
        else:
            # failed attack - predator loses some energy for the attempt
            self.energy -= 5
            self.last_attack_time = self.age
    
    def _consume_energy(self):
        # improved energy consumption based on metabolism trait and activity
        base_consumption = self.metabolism_rate
        
        # reduce consumption when energy is low (survival mode)
        if self.energy < self.config.initial_energy * 0.3:
            base_consumption *= 0.5
        
        # increase consumption when moving fast
        current_speed = math.sqrt(self.dx**2 + self.dy**2)
        if current_speed > self.speed * 0.8:
            base_consumption *= 1.2
        
        # phase 5: temperature effects on metabolism
        if hasattr(self, 'current_temperature'):
            temp_effect = self.config.temperature_effect_on_metabolism
            if self.current_temperature < 20:  # cold
                # cold increases metabolism (need more energy to stay warm)
                cold_factor = (20 - self.current_temperature) * temp_effect * (1.0 - self.cold_resistance)
                base_consumption *= (1.0 + cold_factor)
            elif self.current_temperature > 20:  # hot
                # heat can also increase metabolism (cooling down)
                heat_factor = (self.current_temperature - 20) * temp_effect * (1.0 - self.heat_resistance)
                base_consumption *= (1.0 + heat_factor)
        
        # phase 5: temperature stress increases energy consumption
        if hasattr(self, 'temperature_stress'):
            base_consumption *= (1.0 + self.temperature_stress)
        
        self.energy -= base_consumption
    
    def _eat_food(self, food_list):
        # improved food detection and consumption
        nearest_food = None
        min_distance = float('inf')
        
        # find nearest available food within vision range
        for food in food_list:
            if food.available:
                distance = self._distance_to(food)
                if distance < self.vision_radius and distance < min_distance:
                    min_distance = distance
                    nearest_food = food
        
        # if food is found, move towards it and eat if close enough
        if nearest_food:
            if min_distance < self.size + self.config.food_size + 5:  # slightly larger eating range
                nearest_food.consume()
                self.energy += self.config.energy_gain_from_food
                return True
            else:
                # move towards the nearest food
                self._move_towards(nearest_food.x, nearest_food.y, [])
                return False
        
        return False
    
    def _distance_to(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        return math.sqrt(dx*dx + dy*dy)
    
    def _check_death(self):
        # death by energy or age
        if self.energy <= 0 or self.age >= self.max_age:
            self.alive = False
            self._calculate_fitness()
    
    def _calculate_fitness(self):
        # calculate fitness based on survival time and reproduction
        survival_fitness = self.survival_time * self.config.fitness_survival_weight
        reproduction_fitness = self.reproduction_count * self.config.fitness_reproduction_weight
        self.fitness_score = survival_fitness + reproduction_fitness
    
    def can_reproduce(self):
        return self.alive and self.energy >= self.reproduction_threshold
    
    def reproduce(self):
        if not self.can_reproduce():
            return None
        
        # create child with slight position offset
        child_x = self.x + random.uniform(-20, 20)
        child_y = self.y + random.uniform(-20, 20)
        
        # wrap around boundaries
        child_x = child_x % self.config.world_width
        child_y = child_y % self.config.world_height
        
        # pass dna to child (will be mutated in dna constructor)
        child = Organism(child_x, child_y, self.config, self.dna, self.species_type, self.id)
        
        # parent loses energy for reproduction
        self.energy -= self.reproduction_threshold * 0.5
        self.reproduction_count += 1
        
        return child
    
    def get_color(self):
        """get color based on species type and species id for phase 4"""
        if self.species_type == 'predator':
            # use species id to generate consistent color for predators
            if hasattr(self, 'species_id') and self.species_id:
                # hash the species id to get a consistent color
                color_hash = hash(self.species_id) % 256
                return (255, color_hash % 128, color_hash % 128)  # red variants
            else:
                return self.config.predator_color
        else:
            # use species id to generate consistent color for prey
            if hasattr(self, 'species_id') and self.species_id:
                # hash the species id to get a consistent color
                color_hash = hash(self.species_id) % 256
                return (color_hash % 128, 255, color_hash % 128)  # green variants
            else:
                return self.config.prey_color
    
    def _update_weather_effects(self, weather_system):
        """update organism based on weather conditions"""
        # get current temperature at organism's position
        self.current_temperature = weather_system.get_temperature_at_position(self.x, self.y)
        
        # calculate temperature stress
        self._calculate_temperature_stress()
        
        # update weather adaptation score
        self._update_weather_adaptation_score(weather_system)
    
    def _calculate_temperature_stress(self):
        """calculate temperature stress based on organism's resistance traits"""
        optimal_temp = 20  # moderate temperature is optimal
        
        if self.current_temperature < optimal_temp:
            # cold stress
            cold_difference = optimal_temp - self.current_temperature
            stress_factor = cold_difference * (1.0 - self.cold_resistance)
            self.temperature_stress = max(0, stress_factor * 0.1)
        elif self.current_temperature > optimal_temp:
            # heat stress
            heat_difference = self.current_temperature - optimal_temp
            stress_factor = heat_difference * (1.0 - self.heat_resistance)
            self.temperature_stress = max(0, stress_factor * 0.1)
        else:
            # optimal temperature - reduce stress
            self.temperature_stress = max(0, self.temperature_stress - 0.05)
    
    def _update_weather_adaptation_score(self, weather_system):
        """update how well adapted the organism is to current weather"""
        # base adaptation score
        adaptation = 1.0
        
        # temperature adaptation
        if self.current_temperature < 20:
            adaptation *= self.cold_resistance
        elif self.current_temperature > 20:
            adaptation *= self.heat_resistance
        
        # light adaptation (night vision)
        light_level = weather_system.get_light_level()
        if light_level < 0.5:  # low light conditions
            adaptation *= self.night_vision
        
        self.weather_adaptation_score = adaptation 

    def _update_physics(self):
        """update realistic physics simulation"""
        if not self.config.collision_detection_enabled:
            return
        
        # apply friction
        self.velocity_x *= self.config.friction_factor
        self.velocity_y *= self.config.friction_factor
        
        # apply momentum conservation
        self.momentum_x *= self.config.momentum_conservation
        self.momentum_y *= self.config.momentum_conservation
        
        # apply slight gravity effect
        self.velocity_y += self.config.gravity_effect
    
    def _update_learning(self):
        """update learning and memory systems"""
        if not self.config.learning_enabled:
            return
        
        # decay old memories
        if len(self.experience_memory) > int(self.memory_capacity * 5):
            self.experience_memory.pop(0)
        
        # update learned strategies
        for strategy_key in list(self.learned_strategies.keys()):
            if random.random() < self.config.memory_decay_rate:
                del self.learned_strategies[strategy_key]
    
    def _update_territorial_behavior(self, other_organisms):
        """update territorial behavior"""
        if not self.config.territorial_behavior_enabled:
            return
        
        # establish territory if none exists
        if self.territory_center is None:
            self.territory_center = (self.x, self.y)
            self.territory_radius = self.vision_radius * 0.5
        
        # defend territory from intruders
        for org in other_organisms:
            if org.alive and org.id != self.id:
                distance = self._distance_to(org)
                if distance < self.territory_radius:
                    # territorial conflict
                    if org.species_type == self.species_type:
                        # same species - compete for territory
                        if self.aggression > org.aggression:
                            # drive away intruder
                            self._move_towards(org.x, org.y, [])
                        else:
                            # retreat
                            self._flee_from(org, [])
    
    def _update_evolutionary_pressure(self, other_organisms):
        """update evolutionary pressure based on environment"""
        # calculate pressure based on competition
        nearby_competitors = 0
        for org in other_organisms:
            if org.alive and org.species_type == self.species_type:
                distance = self._distance_to(org)
                if distance < self.vision_radius:
                    nearby_competitors += 1
        
        # pressure increases with competition
        self.evolutionary_pressure = min(1.0, nearby_competitors * 0.1)
        
        # pressure also increases with environmental stress
        if hasattr(self, 'temperature_stress'):
            self.evolutionary_pressure = max(self.evolutionary_pressure, self.temperature_stress)
    
    def _update_physics(self):
        """update realistic physics simulation"""
        if not self.config.collision_detection_enabled:
            return
        
        # apply friction
        self.velocity_x *= self.config.friction_factor
        self.velocity_y *= self.config.friction_factor
        
        # apply momentum conservation
        self.momentum_x *= self.config.momentum_conservation
        self.momentum_y *= self.config.momentum_conservation
        
        # apply slight gravity effect
        self.velocity_y += self.config.gravity_effect
    
    def _update_learning(self):
        """update learning and memory systems"""
        if not self.config.learning_enabled:
            return
        
        # decay old memories
        if len(self.experience_memory) > int(self.memory_capacity * 5):
            self.experience_memory.pop(0)
        
        # update learned strategies
        for strategy_key in list(self.learned_strategies.keys()):
            if random.random() < self.config.memory_decay_rate:
                del self.learned_strategies[strategy_key] 