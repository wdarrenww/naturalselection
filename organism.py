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
            'max_age': random.randint(200, 800)
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
            'max_age': (100, 1000)
        }
        
        min_val, max_val = bounds.get(trait_name, (0, float('inf')))
        return max(min_val, min(max_val, value))

class Organism:
    def __init__(self, x, y, config: SimConfig, parent_dna=None):
        self.x = x
        self.y = y
        self.config = config
        self.dna = DNA(config, parent_dna)
        self.energy = config.initial_energy
        self.alive = True
        self.age = 0
        self.id = self._generate_id()
        
        # movement direction (random initial direction)
        self.dx = random.uniform(-1, 1)
        self.dy = random.uniform(-1, 1)
        self._normalize_direction()
        
        # phenotype mapping - convert dna traits to actual behavior
        self._update_phenotype()
    
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
    
    def _normalize_direction(self):
        # normalize direction vector
        length = math.sqrt(self.dx**2 + self.dy**2)
        if length > 0:
            self.dx /= length
            self.dy /= length
    
    def update(self, food_list):
        if not self.alive:
            return
        
        self.age += 1
        self._move()
        self._consume_energy()
        self._eat_food(food_list)
        self._check_death()
    
    def _move(self):
        # random walk with slight direction changes
        if random.random() < 0.1:  # 10% chance to change direction
            self.dx += random.uniform(-0.5, 0.5)
            self.dy += random.uniform(-0.5, 0.5)
            self._normalize_direction()
        
        # move organism using trait-based speed
        self.x += self.dx * self.speed
        self.y += self.dy * self.speed
        
        # wrap around world boundaries
        self.x = self.x % self.config.world_width
        self.y = self.y % self.config.world_height
    
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
        child = Organism(child_x, child_y, self.config, self.dna)
        
        # parent loses energy for reproduction
        self.energy -= self.reproduction_threshold * 0.5
        
        return child
    
    def get_color(self):
        # color based on speed trait for visualization
        speed_ratio = (self.dna.traits['speed'] - 0.1) / (3.0 - 0.1)  # normalize to 0-1
        speed_ratio = max(0, min(1, speed_ratio))
        
        # green to red based on speed (faster = more red)
        red = int(255 * speed_ratio)
        green = int(255 * (1 - speed_ratio))
        blue = 0
        
        return (red, green, blue) 