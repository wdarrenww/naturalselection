import math
import pygame
from sim_config import SimConfig

class WeatherSystem:
    def __init__(self, config: SimConfig):
        self.config = config
        self.time_step = 0
        
        # day/night cycle
        self.day_night_progress = 0.0  # 0.0 = day, 1.0 = night
        self.is_night = False
        self.light_level = 1.0  # 1.0 = full light, 0.0 = no light
        
        # temperature zones
        self.temperature_map = {}
        self._generate_temperature_map()
        
        # seasons
        self.season_progress = 0.0  # 0.0 = start of season, 1.0 = end of season
        self.current_season = 'spring'
        self.seasons = ['spring', 'summer', 'autumn', 'winter']
        self.season_index = 0
        
        # weather effects
        self.current_temperature_modifier = 0
        self.current_food_multiplier = 1.0
    
    def _generate_temperature_map(self):
        """generate temperature map for the world"""
        self.temperature_map = {}
        
        for y in range(0, self.config.world_height, 10):  # sample every 10 pixels
            for x in range(0, self.config.world_width, 10):
                # determine temperature based on y position
                if y <= self.config.cold_zone_y_range[1]:
                    # cold zone
                    temperature = self.config.cold_temperature
                elif y >= self.config.hot_zone_y_range[0]:
                    # hot zone
                    temperature = self.config.hot_temperature
                else:
                    # moderate zone - interpolate between cold and hot
                    cold_y = self.config.cold_zone_y_range[1]
                    hot_y = self.config.hot_zone_y_range[0]
                    progress = (y - cold_y) / (hot_y - cold_y)
                    temperature = self.config.cold_temperature + progress * (self.config.hot_temperature - self.config.cold_temperature)
                
                self.temperature_map[(x, y)] = temperature
    
    def update(self):
        """update weather system for current frame"""
        self.time_step += 1
        
        # update day/night cycle
        self._update_day_night_cycle()
        
        # update seasons
        self._update_seasons()
        
        # update temperature effects
        self._update_temperature_effects()
    
    def _update_day_night_cycle(self):
        """update day/night cycle"""
        if not self.config.day_night_cycle_enabled:
            return
        
        # calculate progress through cycle (0.0 to 1.0)
        self.day_night_progress = (self.time_step % self.config.day_night_cycle_duration) / self.config.day_night_cycle_duration
        
        # determine if it's night (0.5 to 1.0 = night)
        self.is_night = self.day_night_progress > 0.5
        
        # calculate light level (smooth transition)
        if self.is_night:
            # night phase: light decreases from 1.0 to 0.0
            night_progress = (self.day_night_progress - 0.5) * 2  # 0.0 to 1.0
            self.light_level = 1.0 - night_progress
        else:
            # day phase: light increases from 0.0 to 1.0
            day_progress = self.day_night_progress * 2  # 0.0 to 1.0
            self.light_level = day_progress
    
    def _update_seasons(self):
        """update seasonal changes"""
        if not self.config.seasons_enabled:
            return
        
        # calculate season progress
        season_frame = self.time_step % self.config.season_duration
        self.season_progress = season_frame / self.config.season_duration
        
        # determine current season
        season_index = (self.time_step // self.config.season_duration) % len(self.seasons)
        self.current_season = self.seasons[season_index]
        self.season_index = season_index
        
        # update seasonal modifiers
        self.current_food_multiplier = self.config.season_food_multiplier.get(self.current_season, 1.0)
        self.current_temperature_modifier = self.config.season_temperature_modifier.get(self.current_season, 0)
    
    def _update_temperature_effects(self):
        """update temperature effects on the environment"""
        # temperature effects are applied per-organism in the organism update
        pass
    
    def get_temperature_at_position(self, x, y):
        """get temperature at a specific position"""
        if not self.config.temperature_zones_enabled:
            return self.config.moderate_temperature
        
        # find nearest temperature sample
        sample_x = (x // 10) * 10
        sample_y = (y // 10) * 10
        
        # clamp to world boundaries
        sample_x = max(0, min(sample_x, self.config.world_width - 10))
        sample_y = max(0, min(sample_y, self.config.world_height - 10))
        
        base_temperature = self.temperature_map.get((sample_x, sample_y), self.config.moderate_temperature)
        
        # apply seasonal modifier
        return base_temperature + self.current_temperature_modifier
    
    def get_light_level(self):
        """get current light level (0.0 to 1.0)"""
        if not self.config.day_night_cycle_enabled:
            return 1.0
        return self.light_level
    
    def is_night_time(self):
        """check if it's currently night"""
        if not self.config.day_night_cycle_enabled:
            return False
        return self.is_night
    
    def get_current_season(self):
        """get current season name"""
        if not self.config.seasons_enabled:
            return 'none'
        return self.current_season
    
    def get_food_multiplier(self):
        """get current food availability multiplier"""
        if not self.config.seasons_enabled:
            return 1.0
        return self.current_food_multiplier
    
    def get_temperature_modifier(self):
        """get current temperature modifier"""
        if not self.config.seasons_enabled:
            return 0
        return self.current_temperature_modifier
    
    def render_weather_effects(self, screen):
        """render weather effects on the screen"""
        if not self.config.show_day_night_cycle and not self.config.show_temperature_zones:
            return
        
        # create a surface for weather effects
        weather_surface = pygame.Surface((self.config.width, self.config.height))
        weather_surface.set_alpha(50)  # semi-transparent
        
        # apply day/night cycle overlay
        if self.config.show_day_night_cycle and self.config.day_night_cycle_enabled:
            if self.is_night:
                weather_surface.fill(self.config.night_color)
                screen.blit(weather_surface, (0, 0))
        
        # apply temperature zone overlays
        if self.config.show_temperature_zones and self.config.temperature_zones_enabled:
            self._render_temperature_zones(screen)
    
    def _render_temperature_zones(self, screen):
        """render temperature zone indicators"""
        # render cold zone (top)
        cold_rect = pygame.Rect(0, 0, self.config.width, self.config.cold_zone_y_range[1])
        cold_surface = pygame.Surface((self.config.width, self.config.cold_zone_y_range[1]))
        cold_surface.set_alpha(30)
        cold_surface.fill(self.config.cold_zone_color)
        screen.blit(cold_surface, (0, 0))
        
        # render hot zone (bottom)
        hot_height = self.config.world_height - self.config.hot_zone_y_range[0]
        hot_rect = pygame.Rect(0, self.config.hot_zone_y_range[0], self.config.width, hot_height)
        hot_surface = pygame.Surface((self.config.width, hot_height))
        hot_surface.set_alpha(30)
        hot_surface.fill(self.config.hot_zone_color)
        screen.blit(hot_surface, (0, self.config.hot_zone_y_range[0]))
    
    def render_weather_ui(self, screen):
        """render weather information in the ui"""
        if not self.config.show_season_indicator:
            return
        
        font = pygame.font.Font(None, 24)
        
        # render day/night indicator
        if self.config.show_day_night_cycle and self.config.day_night_cycle_enabled:
            time_text = "Night" if self.is_night else "Day"
            time_color = (100, 100, 255) if self.is_night else (255, 255, 100)
            time_surface = font.render(f"Time: {time_text}", True, time_color)
            screen.blit(time_surface, (self.config.width - 150, 10))
        
        # render season indicator
        if self.config.seasons_enabled:
            season_text = f"Season: {self.current_season.capitalize()}"
            season_surface = font.render(season_text, True, self.config.text_color)
            screen.blit(season_surface, (self.config.width - 150, 35))
            
            # render food multiplier
            food_text = f"Food: {self.current_food_multiplier:.1f}x"
            food_surface = font.render(food_text, True, self.config.text_color)
            screen.blit(food_surface, (self.config.width - 150, 60))
            
            # render temperature modifier
            temp_text = f"Temp: {self.current_temperature_modifier:+d}°C"
            temp_surface = font.render(temp_text, True, self.config.text_color)
            screen.blit(temp_surface, (self.config.width - 150, 85)) 