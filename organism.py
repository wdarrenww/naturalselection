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
            'speed': random.uniform(0.5, 2.0),
            'vision': random.uniform(20, 100),
            'size': random.uniform(0.5, 1.5),
            'metabolism': random.uniform(0.3, 1.2),
            'reproduction_threshold': random.uniform(60, 100),
            'max_age': random.randint(200, 800),
            'aggression': random.uniform(0.1, 1.0),  # for predators
            'caution': random.uniform(0.1, 1.0),     # for prey
            'stamina': random.uniform(0.5, 1.5)      # affects sustained movement
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
            'stamina': (0.2, 2.0)
        }
        
        min_val, max_val = bounds.get(trait_name, (0, float('inf')))
        return max(min_val, min(max_val, value))

class Organism:
    def __init__(self, x, y, config: SimConfig, parent_dna=None, species_type='prey'):
        self.x = x
        self.y = y
        self.config = config
        self.dna = DNA(config, parent_dna)
        self.energy = config.initial_energy
        self.alive = True
        self.age = 0
        self.id = self._generate_id()
        self.species_type = species_type  # 'predator' or 'prey'
        
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
        
    def _generate_id(self):
        # simple id generation for tracking
        return random.randint(1000000, 9999999)
    
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
    
    def _normalize_direction(self):
        # normalize direction vector
        length = math.sqrt(self.dx**2 + self.dy**2)
        if length > 0:
            self.dx /= length
            self.dy /= length
    
    def update(self, food_list, other_organisms, obstacles):
        if not self.alive:
            return
        
        self.age += 1
        self.survival_time += 1
        
        # update behavior based on species type
        if self.species_type == 'predator':
            self._predator_behavior(food_list, other_organisms, obstacles)
        else:
            self._prey_behavior(food_list, other_organisms, obstacles)
        
        self._consume_energy()
        self._check_death()
    
    def _predator_behavior(self, food_list, other_organisms, obstacles):
        # find nearest prey
        nearest_prey = self._find_nearest_prey(other_organisms)
        
        if nearest_prey and self._distance_to(nearest_prey) < self.vision_radius:
            # chase prey
            self._move_towards(nearest_prey.x, nearest_prey.y, obstacles)
            
            # attack if close enough
            if (self._distance_to(nearest_prey) < self.config.predator_attack_range and 
                self.age - self.last_attack_time > self.config.predator_attack_cooldown):
                self._attack_prey(nearest_prey)
        else:
            # random movement or seek food
            self._move_randomly(obstacles)
            self._eat_food(food_list)
    
    def _prey_behavior(self, food_list, other_organisms, obstacles):
        # check for nearby predators
        nearest_predator = self._find_nearest_predator(other_organisms)
        
        if nearest_predator and self._distance_to(nearest_predator) < self.vision_radius * self.caution:
            # flee from predator
            self._flee_from(nearest_predator, obstacles)
            self.flee_timer = 10  # flee for 10 frames
        elif self.flee_timer > 0:
            # continue fleeing
            self._flee_from(nearest_predator, obstacles)
            self.flee_timer -= 1
        else:
            # normal behavior: seek food and move randomly
            self._move_randomly(obstacles)
            self._eat_food(food_list)
    
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
        # predator attacks prey
        if prey.alive:
            prey.alive = False
            self.energy += self.config.predator_energy_gain_from_prey
            self.last_attack_time = self.age
    
    def _consume_energy(self):
        # energy consumption based on metabolism trait
        self.energy -= self.metabolism_rate
    
    def _eat_food(self, food_list):
        # use vision trait to determine detection range
        for food in food_list:
            distance = self._distance_to(food)
            if distance < self.vision_radius and food.available:
                # check if close enough to eat (based on size)
                if distance < self.size + self.config.food_size:
                    food.consume()
                    self.energy += self.config.energy_gain_from_food
                    break
    
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
        child = Organism(child_x, child_y, self.config, self.dna, self.species_type)
        
        # parent loses energy for reproduction
        self.energy -= self.reproduction_threshold * 0.5
        self.reproduction_count += 1
        
        return child
    
    def get_color(self):
        # color based on species type
        if self.species_type == 'predator':
            return self.config.predator_color
        else:
            return self.config.prey_color 