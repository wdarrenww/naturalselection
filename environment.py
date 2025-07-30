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

class Environment:
    def __init__(self, config: SimConfig):
        self.config = config
        self.food_list = []
        self._generate_initial_food()
    
    def _generate_initial_food(self):
        for _ in range(self.config.initial_food_count):
            x = random.uniform(0, self.config.world_width)
            y = random.uniform(0, self.config.world_height)
            self.food_list.append(Food(x, y, self.config))
    
    def update(self):
        # update all food
        for food in self.food_list:
            food.update()
        
        # add new food occasionally
        if random.random() < 0.01:  # 1% chance per frame
            self._add_random_food()
    
    def _add_random_food(self):
        x = random.uniform(0, self.config.world_width)
        y = random.uniform(0, self.config.world_height)
        self.food_list.append(Food(x, y, self.config))
    
    def get_available_food(self):
        return [food for food in self.food_list if food.available]
    
    def render(self, screen, camera_offset=(0, 0)):
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