import random
import pygame
from sim_config import SimConfig

class Food:
    def __init__(self, x, y, config: SimConfig):
        self.x = x
        self.y = y
        self.config = config
        self.available = True
        self.regen_timer = 0
    
    def consume(self):
        self.available = False
        self.regen_timer = 0
    
    def update(self):
        if not self.available:
            self.regen_timer += 1
            if self.regen_timer >= 1 / self.config.food_regen_rate:
                self.available = True
                self.regen_timer = 0

class Obstacle:
    def __init__(self, x, y, size, config: SimConfig):
        self.x = x
        self.y = y
        self.size = size
        self.config = config

class Environment:
    def __init__(self, config: SimConfig):
        self.config = config
        self.food_list = []
        self.obstacles = []
        self._generate_initial_food()
        if config.terrain_enabled:
            self._generate_obstacles()
    
    def _generate_initial_food(self):
        for _ in range(self.config.initial_food_count):
            x = random.uniform(0, self.config.world_width)
            y = random.uniform(0, self.config.world_height)
            self.food_list.append(Food(x, y, self.config))
    
    def _generate_obstacles(self):
        for _ in range(self.config.obstacle_count):
            x = random.uniform(0, self.config.world_width)
            y = random.uniform(0, self.config.world_height)
            size = random.uniform(*self.config.obstacle_size_range)
            self.obstacles.append(Obstacle(x, y, size, self.config))
    
    def update(self, weather_system=None):
        # update all food
        for food in self.food_list:
            food.update()
        
        # phase 5: apply seasonal food multipliers
        food_multiplier = 1.0
        if weather_system:
            food_multiplier = weather_system.get_food_multiplier()
        
        # improved food generation: more frequent and adaptive
        current_food_count = len(self.get_available_food())
        target_food_count = int(self.config.initial_food_count * food_multiplier)
        
        # if food is scarce, increase generation rate
        if current_food_count < target_food_count * 0.5:
            # high food scarcity - generate more food
            if random.random() < 0.05:  # 5% chance per frame
                self._add_random_food()
        elif current_food_count < target_food_count * 0.8:
            # moderate food scarcity
            if random.random() < 0.02:  # 2% chance per frame
                self._add_random_food()
        else:
            # normal food levels
            if random.random() < 0.01:  # 1% chance per frame
                self._add_random_food()
    
    def _add_random_food(self):
        x = random.uniform(0, self.config.world_width)
        y = random.uniform(0, self.config.world_height)
        self.food_list.append(Food(x, y, self.config))
    
    def get_available_food(self):
        return [food for food in self.food_list if food.available]
    
    def get_obstacles(self):
        return self.obstacles
    
    def get_food_density(self):
        """calculate food density for competition mechanics"""
        available_food = len(self.get_available_food())
        total_area = self.config.world_width * self.config.world_height
        return available_food / total_area
    
    def render(self, screen, camera_offset=(0, 0)):
        # render obstacles
        for obstacle in self.obstacles:
            screen_x = int(obstacle.x - camera_offset[0])
            screen_y = int(obstacle.y - camera_offset[1])
            
            # only render if on screen
            if (0 <= screen_x <= self.config.width and 
                0 <= screen_y <= self.config.height):
                pygame.draw.circle(
                    screen, 
                    self.config.obstacle_color, 
                    (screen_x, screen_y), 
                    int(obstacle.size)
                )
        
        # render food
        for food in self.food_list:
            if food.available:
                screen_x = int(food.x - camera_offset[0])
                screen_y = int(food.y - camera_offset[1])
                
                # only render if on screen
                if (0 <= screen_x <= self.config.width and 
                    0 <= screen_y <= self.config.height):
                    pygame.draw.circle(
                        screen, 
                        self.config.food_color, 
                        (screen_x, screen_y), 
                        self.config.food_size
                    ) 