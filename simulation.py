import random
import pygame
import numpy as np
from sim_config import SimConfig
from organism import Organism
from environment import Environment
from trait_analyzer import TraitAnalyzer

class Simulation:
    def __init__(self, config: SimConfig):
        self.config = config
        self.paused = False
        self.time_step = 0
        
        # initialize pygame display
        self.screen = pygame.display.set_mode((config.width, config.height))
        pygame.display.set_caption(config.title)
        
        # initialize components
        self.environment = Environment(config)
        self.organisms = []
        self._generate_initial_organisms()
        
        # camera offset for world scrolling (future feature)
        self.camera_x = 0
        self.camera_y = 0
        
        # statistics and trait tracking
        self.stats = {
            'total_organisms': 0,
            'alive_organisms': 0,
            'total_food': 0,
            'available_food': 0,
            'generation': 0,
            'total_births': 0,
            'total_deaths': 0
        }
        
        # trait history tracking
        self.trait_history = []
        self.trait_snapshots = []
        
        # trait analyzer for advanced analysis
        self.trait_analyzer = TraitAnalyzer(config)
    
    def _generate_initial_organisms(self):
        for _ in range(self.config.initial_organisms):
            x = random.uniform(0, self.config.world_width)
            y = random.uniform(0, self.config.world_height)
            self.organisms.append(Organism(x, y, self.config))
    
    def update(self):
        if self.paused:
            return
        
        self.time_step += 1
        
        # update environment
        self.environment.update()
        
        # update organisms
        available_food = self.environment.get_available_food()
        new_organisms = []
        deaths_this_frame = 0
        
        for organism in self.organisms:
            was_alive = organism.alive
            organism.update(available_food)
            
            # track deaths
            if was_alive and not organism.alive:
                deaths_this_frame += 1
                self.stats['total_deaths'] += 1
            
            # check for reproduction
            if organism.can_reproduce() and random.random() < 0.01:  # 1% chance per frame
                child = organism.reproduce()
                if child:
                    new_organisms.append(child)
                    self.stats['total_births'] += 1
        
        # add new organisms
        self.organisms.extend(new_organisms)
        
        # remove dead organisms
        self.organisms = [org for org in self.organisms if org.alive]
        
        # update statistics
        self._update_stats()
        
        # log trait data periodically
        if self.time_step % self.config.trait_log_interval == 0:
            self._log_trait_snapshot()
    
    def _update_stats(self):
        self.stats['total_organisms'] = len(self.organisms)
        self.stats['alive_organisms'] = len([org for org in self.organisms if org.alive])
        self.stats['total_food'] = len(self.environment.food_list)
        self.stats['available_food'] = len(self.environment.get_available_food())
        
        # estimate generation based on births
        self.stats['generation'] = max(1, self.stats['total_births'] // max(1, self.config.initial_organisms))
    
    def _log_trait_snapshot(self):
        if not self.organisms:
            return
        
        # collect all trait values
        trait_data = {
            'speed': [],
            'vision': [],
            'size': [],
            'metabolism': [],
            'reproduction_threshold': [],
            'max_age': []
        }
        
        for organism in self.organisms:
            for trait_name in trait_data.keys():
                trait_data[trait_name].append(organism.dna.traits[trait_name])
        
        # calculate statistics
        snapshot = {
            'time_step': self.time_step,
            'population': len(self.organisms),
            'generation': self.stats['generation'],
            'traits': {}
        }
        
        for trait_name, values in trait_data.items():
            if values:
                snapshot['traits'][trait_name] = {
                    'mean': np.mean(values),
                    'std': np.std(values),
                    'min': np.min(values),
                    'max': np.max(values)
                }
        
        self.trait_snapshots.append(snapshot)
        
        # also add to trait analyzer
        self.trait_analyzer.add_snapshot(snapshot)
        
        # limit history size
        if len(self.trait_snapshots) > self.config.max_trait_history:
            self.trait_snapshots.pop(0)
    
    def render(self):
        # clear screen
        self.screen.fill(self.config.background_color)
        
        # render environment
        self.environment.render(self.screen, (self.camera_x, self.camera_y))
        
        # render organisms with trait-based colors
        for organism in self.organisms:
            if organism.alive:
                screen_x = int(organism.x - self.camera_x)
                screen_y = int(organism.y - self.camera_y)
                
                # only render if on screen
                if (0 <= screen_x <= self.config.width and 
                    0 <= screen_y <= self.config.height):
                    
                    # use trait-based color
                    color = organism.get_color()
                    size = int(organism.size)
                    
                    pygame.draw.circle(
                        self.screen,
                        color,
                        (screen_x, screen_y),
                        size
                    )
                    
                    # draw vision radius for debugging (optional)
                    if self.config.show_vision_radius:
                        pygame.draw.circle(
                            self.screen,
                            (100, 100, 100),
                            (screen_x, screen_y),
                            int(organism.vision_radius),
                            1
                        )
        
        # render statistics
        self._render_stats()
        
        # update display
        pygame.display.flip()
    
    def _render_stats(self):
        font = pygame.font.Font(None, 24)
        
        stats_text = [
            f"Organisms: {self.stats['alive_organisms']}",
            f"Food: {self.stats['available_food']}",
            f"Time: {self.time_step}",
            f"Generation: {self.stats['generation']}",
            f"Births: {self.stats['total_births']}",
            f"Deaths: {self.stats['total_deaths']}",
            f"Paused: {'Yes' if self.paused else 'No'}"
        ]
        
        # add trait statistics if available
        if self.trait_snapshots:
            latest = self.trait_snapshots[-1]
            if 'traits' in latest and 'speed' in latest['traits']:
                speed_mean = latest['traits']['speed']['mean']
                stats_text.append(f"Avg Speed: {speed_mean:.2f}")
        
        for i, text in enumerate(stats_text):
            surface = font.render(text, True, self.config.text_color)
            self.screen.blit(surface, (10, 10 + i * 25))
    
    def toggle_pause(self):
        self.paused = not self.paused
    
    def reset(self):
        self.paused = False
        self.time_step = 0
        self.organisms = []
        self.environment = Environment(self.config)
        self._generate_initial_organisms()
        self._update_stats()
        self.trait_snapshots = []
        self.trait_analyzer = TraitAnalyzer(self.config)
        self.stats['total_births'] = 0
        self.stats['total_deaths'] = 0
    
    def get_trait_analyzer(self):
        """get the trait analyzer for external analysis"""
        return self.trait_analyzer 