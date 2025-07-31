import random
import pygame
import numpy as np
from sim_config import SimConfig
from organism import Organism
from environment import Environment
from trait_analyzer import TraitAnalyzer
from weather_system import WeatherSystem

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
        
        # phase 5: weather system
        self.weather_system = WeatherSystem(config)
        
        # camera offset for world scrolling (future feature)
        self.camera_x = 0
        self.camera_y = 0
        
        # phase 4: species and lineage tracking
        self.species_count = 0
        self.species_history = []
        self.lineage_tree = {}
        self.next_species_id = 1
        
        # statistics and trait tracking
        self.stats = {
            'total_organisms': 0,
            'alive_organisms': 0,
            'predators': 0,
            'prey': 0,
            'total_food': 0,
            'available_food': 0,
            'generation': 0,
            'total_births': 0,
            'total_deaths': 0,
            'predator_kills': 0,
            'average_fitness': 0.0,
            'food_density': 0.0,
            # phase 4: speciation stats
            'species_count': 0,
            'speciation_events': 0,
            'average_genetic_distance': 0.0,
            'lineage_depth': 0,
            # phase 6: behavioral evolution stats
            'behavioral_states': {},
            'average_intelligence': 0.0,
            'average_social_behavior': 0.0,
            'average_exploration_rate': 0.0,
            'average_memory_capacity': 0.0,
            'prey_protective_traits': {},
            'predator_hunting_traits': {},
            'group_formation_count': 0,
            'cooperative_hunting_events': 0,
            'warning_signal_events': 0,
            'camouflage_effectiveness': 0.0,
            'toxicity_effectiveness': 0.0,
            'armor_effectiveness': 0.0,
            # new: enhanced evolution stats
            'average_adaptation_score': 0.0,
            'average_energy_efficiency': 0.0,
            'evolutionary_pressure': 0.0,
            'trait_synergy_count': 0,
            'trait_conflict_count': 0,
            'population_diversity': 0.0,
            'extinction_events': 0,
            'speciation_rate': 0.0,
            'average_generation_depth': 0,
            'environmental_stress': 0.0,
            'resource_competition_level': 0.0,
            'territorial_conflicts': 0,
            'learning_effectiveness': 0.0,
            'behavioral_innovation_rate': 0.0
        }
        
        self._generate_initial_organisms()
        
        # trait history tracking
        self.trait_history = []
        self.trait_snapshots = []
        
        # trait analyzer for advanced analysis
        self.trait_analyzer = TraitAnalyzer(config)
        
        # new: enhanced evolution tracking
        self.evolutionary_pressure_history = []
        self.adaptation_history = []
        self.diversity_history = []
        self.extinction_history = []
        
        # new: environmental tracking
        self.environmental_stress_history = []
        self.resource_competition_history = []
        self.territorial_conflict_history = []
        
        # new: learning and innovation tracking
        self.learning_effectiveness_history = []
        self.innovation_history = []
        self.behavioral_adaptation_history = []
    
    def _generate_initial_organisms(self):
        # generate predators
        for _ in range(self.config.initial_predators):
            x = random.uniform(0, self.config.world_width)
            y = random.uniform(0, self.config.world_height)
            self.organisms.append(Organism(x, y, self.config, species_type='predator'))
        
        # generate prey
        for _ in range(self.config.initial_prey):
            x = random.uniform(0, self.config.world_width)
            y = random.uniform(0, self.config.world_height)
            self.organisms.append(Organism(x, y, self.config, species_type='prey'))
        
        # phase 4: initialize species tracking
        self._update_species_tracking()
    
    def _update_species_tracking(self):
        """update species count and tracking"""
        species_ids = set()
        for org in self.organisms:
            if org.alive and hasattr(org, 'species_id'):
                species_ids.add(org.species_id)
        
        self.stats['species_count'] = len(species_ids)
        
        # track species history
        if self.time_step % 100 == 0:  # every 100 frames
            self.species_history.append({
                'time_step': self.time_step,
                'species_count': len(species_ids),
                'species_ids': list(species_ids)
            })
    
    def update(self):
        if self.paused:
            return
        
        self.time_step += 1
        
        # update weather system
        self.weather_system.update()
        
        # update environment
        self.environment.update(self.weather_system)
        
        # get environment data
        available_food = self.environment.get_available_food()
        obstacles = self.environment.get_obstacles()
        
        # update organisms
        new_organisms = []
        deaths_this_frame = 0
        predator_kills_this_frame = 0
        speciation_events_this_frame = 0
        
        for organism in self.organisms:
            was_alive = organism.alive
            old_species_id = getattr(organism, 'species_id', None)
            
            organism.update(available_food, self.organisms, obstacles, self.weather_system)
            
            # track speciation events
            if (was_alive and organism.alive and 
                hasattr(organism, 'species_id') and 
                old_species_id != organism.species_id):
                speciation_events_this_frame += 1
                self.stats['speciation_events'] += 1
            
            # track deaths
            if was_alive and not organism.alive:
                deaths_this_frame += 1
                self.stats['total_deaths'] += 1
                
                # track predator kills
                if organism.species_type == 'prey':
                    predator_kills_this_frame += 1
                    self.stats['predator_kills'] += 1
            
            # check for reproduction with carrying capacity
            if organism.can_reproduce() and self._can_reproduce_with_capacity():
                # improved reproduction chance based on energy and population
                reproduction_chance = 0.015  # reduced base chance
                
                # increase chance if energy is high
                if organism.energy > organism.reproduction_threshold * 1.5:
                    reproduction_chance *= 2
                
                # increase chance if population is low
                if len(self.organisms) < self.config.carrying_capacity * 0.3:
                    reproduction_chance *= 3
                
                # new: consider adaptation score for reproduction
                if hasattr(organism, 'adaptation_score'):
                    reproduction_chance *= organism.adaptation_score
                
                if random.random() < reproduction_chance:
                    child = organism.reproduce()
                    if child:
                        new_organisms.append(child)
                        self.stats['total_births'] += 1
                        
                        # phase 4: track lineage
                        if self.config.track_lineages:
                            self._track_lineage(organism.id, child.id)
        
        # add new organisms
        self.organisms.extend(new_organisms)
        
        # remove dead organisms
        self.organisms = [org for org in self.organisms if org.alive]
        
        # emergency population recovery
        self._emergency_population_recovery()
        
        # phase 4: update species tracking
        self._update_species_tracking()
        
        # new: update enhanced evolution tracking
        self._update_enhanced_evolution_stats()
        
        # update statistics
        self._update_stats()
        
        # log trait data periodically
        if self.time_step % self.config.trait_log_interval == 0:
            self._log_trait_snapshot()
    
    def _update_enhanced_evolution_stats(self):
        """update enhanced evolution statistics"""
        if not self.organisms:
            return
        
        # calculate adaptation scores
        adaptation_scores = []
        energy_efficiencies = []
        evolutionary_pressures = []
        
        # calculate trait synergies and conflicts
        total_synergies = 0
        total_conflicts = 0
        
        # calculate population diversity
        genetic_distances = []
        
        for org in self.organisms:
            if org.alive:
                if hasattr(org, 'adaptation_score'):
                    adaptation_scores.append(org.adaptation_score)
                if hasattr(org, 'energy_efficiency'):
                    energy_efficiencies.append(org.energy_efficiency)
                if hasattr(org, 'evolutionary_pressure'):
                    evolutionary_pressures.append(org.evolutionary_pressure)
                
                # count trait interactions
                if hasattr(org, 'trait_synergies'):
                    total_synergies += len(org.trait_synergies)
                if hasattr(org, 'trait_conflicts'):
                    total_conflicts += len(org.trait_conflicts)
                
                # calculate genetic diversity
                for other_org in self.organisms:
                    if other_org.alive and other_org.id != org.id:
                        distance = org.calculate_genetic_distance(other_org)
                        if distance != float('inf'):
                            genetic_distances.append(distance)
        
        # update enhanced stats
        if adaptation_scores:
            self.stats['average_adaptation_score'] = sum(adaptation_scores) / len(adaptation_scores)
        if energy_efficiencies:
            self.stats['average_energy_efficiency'] = sum(energy_efficiencies) / len(energy_efficiencies)
        if evolutionary_pressures:
            self.stats['evolutionary_pressure'] = sum(evolutionary_pressures) / len(evolutionary_pressures)
        
        self.stats['trait_synergy_count'] = total_synergies
        self.stats['trait_conflict_count'] = total_conflicts
        
        if genetic_distances:
            self.stats['population_diversity'] = sum(genetic_distances) / len(genetic_distances)
        
        # calculate environmental stress
        if hasattr(self.weather_system, 'get_light_level'):
            light_level = self.weather_system.get_light_level()
            temperature_modifier = self.weather_system.get_temperature_modifier()
            self.stats['environmental_stress'] = (1.0 - light_level) + abs(temperature_modifier) * 0.1
        
        # calculate resource competition
        food_density = self.environment.get_food_density()
        population_density = len(self.organisms) / (self.config.world_width * self.config.world_height)
        self.stats['resource_competition_level'] = max(0, population_density - food_density * 1000)
        
        # track history
        self.evolutionary_pressure_history.append(self.stats['evolutionary_pressure'])
        self.adaptation_history.append(self.stats['average_adaptation_score'])
        self.diversity_history.append(self.stats['population_diversity'])
        self.environmental_stress_history.append(self.stats['environmental_stress'])
        self.resource_competition_history.append(self.stats['resource_competition_level'])
        
        # limit history size
        max_history = 1000
        for history_list in [self.evolutionary_pressure_history, self.adaptation_history, 
                           self.diversity_history, self.environmental_stress_history, 
                           self.resource_competition_history]:
            if len(history_list) > max_history:
                history_list.pop(0)
    
    def _track_lineage(self, parent_id, child_id):
        """track parent-child relationships"""
        if parent_id not in self.lineage_tree:
            self.lineage_tree[parent_id] = []
        self.lineage_tree[parent_id].append(child_id)
    
    def _can_reproduce_with_capacity(self):
        """check if reproduction is allowed based on carrying capacity"""
        current_population = len(self.organisms)
        food_density = self.environment.get_food_density()
        
        # improved reproduction logic with adaptive thresholds
        base_capacity = self.config.carrying_capacity
        
        # adjust capacity based on food availability
        if food_density > 0.001:  # good food availability
            effective_capacity = base_capacity * 1.1
        elif food_density > 0.0005:  # moderate food availability
            effective_capacity = base_capacity
        else:  # low food availability
            effective_capacity = base_capacity * 0.6
        
        # if population is near carrying capacity, reduce reproduction chance
        if current_population >= effective_capacity * 0.9:
            return random.random() < 0.05  # 5% chance
        elif current_population >= effective_capacity * 0.7:
            return random.random() < 0.2  # 20% chance
        elif current_population >= effective_capacity * 0.5:
            return random.random() < 0.5  # 50% chance
        else:
            return random.random() < 0.8  # 80% chance for low population
    
    def _update_stats(self):
        self.stats['total_organisms'] = len(self.organisms)
        self.stats['alive_organisms'] = len([org for org in self.organisms if org.alive])
        self.stats['predators'] = len([org for org in self.organisms if org.species_type == 'predator' and org.alive])
        self.stats['prey'] = len([org for org in self.organisms if org.species_type == 'prey' and org.alive])
        self.stats['total_food'] = len(self.environment.food_list)
        self.stats['available_food'] = len(self.environment.get_available_food())
        self.stats['food_density'] = self.environment.get_food_density()
        
        # estimate generation based on births
        self.stats['generation'] = max(1, self.stats['total_births'] // max(1, self.config.initial_organisms))
        
        # calculate average fitness
        if self.organisms:
            total_fitness = sum(org.fitness_score for org in self.organisms)
            self.stats['average_fitness'] = total_fitness / len(self.organisms)
        
        # phase 4: calculate average genetic distance
        if len(self.organisms) > 1:
            total_distance = 0
            distance_count = 0
            
            for i, org1 in enumerate(self.organisms):
                for org2 in self.organisms[i+1:]:
                    if org1.alive and org2.alive:
                        distance = org1.calculate_genetic_distance(org2)
                        if distance != float('inf'):
                            total_distance += distance
                            distance_count += 1
            
            if distance_count > 0:
                self.stats['average_genetic_distance'] = total_distance / distance_count
        
        # calculate lineage depth
        if self.lineage_tree:
            max_depth = 0
            for parent_id, children in self.lineage_tree.items():
                max_depth = max(max_depth, len(children))
            self.stats['lineage_depth'] = max_depth
        
        # phase 6: update behavioral evolution statistics
        self._update_behavioral_stats()
    
    def _update_behavioral_stats(self):
        """phase 6: update behavioral evolution statistics"""
        if not self.organisms:
            return
        
        # track behavioral states
        state_counts = {}
        intelligence_values = []
        social_behavior_values = []
        exploration_rate_values = []
        memory_capacity_values = []
        
        # prey protective traits
        camouflage_values = []
        toxicity_values = []
        armor_values = []
        warning_signals_values = []
        group_cohesion_values = []
        
        # predator hunting traits
        hunting_strategy_values = []
        patience_values = []
        cooperation_values = []
        learning_rate_values = []
        
        for org in self.organisms:
            if org.alive:
                # track behavioral states
                state = getattr(org, 'current_state', 'unknown')
                state_counts[state] = state_counts.get(state, 0) + 1
                
                # track behavioral traits
                if hasattr(org, 'intelligence'):
                    intelligence_values.append(org.intelligence)
                if hasattr(org, 'social_behavior'):
                    social_behavior_values.append(org.social_behavior)
                if hasattr(org, 'exploration_rate'):
                    exploration_rate_values.append(org.exploration_rate)
                if hasattr(org, 'memory_capacity'):
                    memory_capacity_values.append(org.memory_capacity)
                
                # track prey protective traits
                if org.species_type == 'prey':
                    if hasattr(org, 'camouflage'):
                        camouflage_values.append(org.camouflage)
                    if hasattr(org, 'toxicity'):
                        toxicity_values.append(org.toxicity)
                    if hasattr(org, 'armor'):
                        armor_values.append(org.armor)
                    if hasattr(org, 'warning_signals'):
                        warning_signals_values.append(org.warning_signals)
                    if hasattr(org, 'group_cohesion'):
                        group_cohesion_values.append(org.group_cohesion)
                
                # track predator hunting traits
                if org.species_type == 'predator':
                    if hasattr(org, 'hunting_strategy'):
                        hunting_strategy_values.append(org.hunting_strategy)
                    if hasattr(org, 'patience'):
                        patience_values.append(org.patience)
                    if hasattr(org, 'cooperation'):
                        cooperation_values.append(org.cooperation)
                    if hasattr(org, 'learning_rate'):
                        learning_rate_values.append(org.learning_rate)
        
        # update behavioral state statistics
        self.stats['behavioral_states'] = state_counts
        
        # update average trait values
        if intelligence_values:
            self.stats['average_intelligence'] = sum(intelligence_values) / len(intelligence_values)
        if social_behavior_values:
            self.stats['average_social_behavior'] = sum(social_behavior_values) / len(social_behavior_values)
        if exploration_rate_values:
            self.stats['average_exploration_rate'] = sum(exploration_rate_values) / len(exploration_rate_values)
        if memory_capacity_values:
            self.stats['average_memory_capacity'] = sum(memory_capacity_values) / len(memory_capacity_values)
        
        # update prey protective trait statistics
        if camouflage_values:
            self.stats['prey_protective_traits']['camouflage'] = {
                'mean': sum(camouflage_values) / len(camouflage_values),
                'count': len(camouflage_values)
            }
        if toxicity_values:
            self.stats['prey_protective_traits']['toxicity'] = {
                'mean': sum(toxicity_values) / len(toxicity_values),
                'count': len(toxicity_values)
            }
        if armor_values:
            self.stats['prey_protective_traits']['armor'] = {
                'mean': sum(armor_values) / len(armor_values),
                'count': len(armor_values)
            }
        if warning_signals_values:
            self.stats['prey_protective_traits']['warning_signals'] = {
                'mean': sum(warning_signals_values) / len(warning_signals_values),
                'count': len(warning_signals_values)
            }
        if group_cohesion_values:
            self.stats['prey_protective_traits']['group_cohesion'] = {
                'mean': sum(group_cohesion_values) / len(group_cohesion_values),
                'count': len(group_cohesion_values)
            }
        
        # update predator hunting trait statistics
        if hunting_strategy_values:
            self.stats['predator_hunting_traits']['hunting_strategy'] = {
                'mean': sum(hunting_strategy_values) / len(hunting_strategy_values),
                'count': len(hunting_strategy_values)
            }
        if patience_values:
            self.stats['predator_hunting_traits']['patience'] = {
                'mean': sum(patience_values) / len(patience_values),
                'count': len(patience_values)
            }
        if cooperation_values:
            self.stats['predator_hunting_traits']['cooperation'] = {
                'mean': sum(cooperation_values) / len(cooperation_values),
                'count': len(cooperation_values)
            }
        if learning_rate_values:
            self.stats['predator_hunting_traits']['learning_rate'] = {
                'mean': sum(learning_rate_values) / len(learning_rate_values),
                'count': len(learning_rate_values)
            }
    
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
            'max_age': [],
            'aggression': [],
            'caution': [],
            'stamina': [],
            # phase 5: weather adaptation traits
            'cold_resistance': [],
            'heat_resistance': [],
            'night_vision': [],
            # phase 6: behavioral evolution traits
            'intelligence': [],
            'social_behavior': [],
            'exploration_rate': [],
            'memory_capacity': [],
            # phase 6: prey protective traits
            'camouflage': [],
            'toxicity': [],
            'armor': [],
            'warning_signals': [],
            'group_cohesion': [],
            # phase 6: predator hunting traits
            'hunting_strategy': [],
            'patience': [],
            'cooperation': [],
            'learning_rate': [],
            # new: enhanced traits
            'efficiency': [],
            'adaptability': [],
            'resilience': [],
            'specialization': [],
            'innovation': []
        }
        
        for organism in self.organisms:
            for trait_name in trait_data.keys():
                trait_data[trait_name].append(organism.dna.traits[trait_name])
        
        # calculate statistics
        snapshot = {
            'time_step': self.time_step,
            'population': len(self.organisms),
            'predators': self.stats['predators'],
            'prey': self.stats['prey'],
            'generation': self.stats['generation'],
            'average_fitness': self.stats['average_fitness'],
            'food_density': self.stats['food_density'],
            # phase 4: speciation data
            'species_count': self.stats['species_count'],
            'speciation_events': self.stats['speciation_events'],
            'average_genetic_distance': self.stats['average_genetic_distance'],
            'lineage_depth': self.stats['lineage_depth'],
            # phase 6: behavioral evolution data
            'behavioral_states': self.stats['behavioral_states'],
            'average_intelligence': self.stats['average_intelligence'],
            'average_social_behavior': self.stats['average_social_behavior'],
            'average_exploration_rate': self.stats['average_exploration_rate'],
            'average_memory_capacity': self.stats['average_memory_capacity'],
            'prey_protective_traits': self.stats['prey_protective_traits'],
            'predator_hunting_traits': self.stats['predator_hunting_traits'],
            # new: enhanced evolution data
            'average_adaptation_score': self.stats['average_adaptation_score'],
            'average_energy_efficiency': self.stats['average_energy_efficiency'],
            'evolutionary_pressure': self.stats['evolutionary_pressure'],
            'population_diversity': self.stats['population_diversity'],
            'environmental_stress': self.stats['environmental_stress'],
            'resource_competition_level': self.stats['resource_competition_level'],
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
        
        # phase 5: render weather effects
        self.weather_system.render_weather_effects(self.screen)
        
        # render organisms with species-based colors
        for organism in self.organisms:
            if organism.alive:
                screen_x = int(organism.x - self.camera_x)
                screen_y = int(organism.y - self.camera_y)
                
                # only render if on screen
                if (0 <= screen_x <= self.config.width and 
                    0 <= screen_y <= self.config.height):
                    
                    # use species-based color for phase 4
                    if self.config.show_species_colors:
                        color = organism.get_color()
                    else:
                        # fallback to original species colors
                        color = organism.get_color()
                    
                    # phase 6: modify color based on behavioral state and protective features
                    if self.config.behavioral_evolution_enabled:
                        color = self._get_behavioral_color(organism, color)
                    
                    # new: modify color based on enhanced traits
                    if self.config.show_trait_indicators:
                        color = self._get_enhanced_trait_color(organism, color)
                    
                    size = int(organism.size)
                    
                    pygame.draw.circle(
                        self.screen,
                        color,
                        (screen_x, screen_y),
                        size
                    )
                    
                    # new: render energy bars
                    if self.config.show_energy_bars:
                        self._render_energy_bar(screen_x, screen_y, organism)
                    
                    # phase 6: draw behavioral state indicators
                    if self.config.show_behavior_states and hasattr(organism, 'current_state'):
                        self._draw_behavioral_indicator(screen_x, screen_y, organism)
                    
                    # new: draw trait indicators
                    if self.config.show_trait_indicators:
                        self._draw_trait_indicators(screen_x, screen_y, organism)
                    
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
        
        # phase 5: render weather ui
        self.weather_system.render_weather_ui(self.screen)
        
        # new: render enhanced evolution indicators
        if self.config.show_evolutionary_pressure:
            self._render_evolutionary_indicators()
        
        # update display
        pygame.display.flip()
    
    def _get_enhanced_trait_color(self, organism, base_color):
        """new: modify organism color based on enhanced traits"""
        color = list(base_color)
        
        # modify based on adaptation score
        if hasattr(organism, 'adaptation_score'):
            adaptation = organism.adaptation_score
            if adaptation > 1.2:
                # well adapted - add green tint
                color[1] = min(255, color[1] + 30)
            elif adaptation < 0.8:
                # poorly adapted - add red tint
                color[0] = min(255, color[0] + 30)
        
        # modify based on energy efficiency
        if hasattr(organism, 'energy_efficiency'):
            efficiency = organism.energy_efficiency
            if efficiency > 0.8:
                # efficient - add blue tint
                color[2] = min(255, color[2] + 20)
            elif efficiency < 0.4:
                # inefficient - add yellow tint
                color[0] = min(255, color[0] + 20)
                color[1] = min(255, color[1] + 20)
        
        return tuple(color)
    
    def _render_energy_bar(self, x, y, organism):
        """new: render energy bar above organism"""
        if not self.config.show_energy_bars:
            return
        
        bar_width = 20
        bar_height = 3
        energy_ratio = organism.energy / self.config.initial_energy
        
        # energy bar background
        pygame.draw.rect(
            self.screen,
            (50, 50, 50),
            (x - bar_width//2, y - organism.size - 10, bar_width, bar_height)
        )
        
        # energy bar fill
        fill_width = int(bar_width * energy_ratio)
        if fill_width > 0:
            energy_color = (0, 255, 0) if energy_ratio > 0.5 else (255, 255, 0) if energy_ratio > 0.2 else (255, 0, 0)
            pygame.draw.rect(
                self.screen,
                energy_color,
                (x - bar_width//2, y - organism.size - 10, fill_width, bar_height)
            )
    
    def _draw_trait_indicators(self, x, y, organism):
        """new: draw trait-based visual indicators"""
        if not self.config.show_trait_indicators:
            return
        
        # draw small indicators for key traits
        indicator_size = 2
        y_offset = -organism.size - 15
        
        # intelligence indicator
        if hasattr(organism, 'intelligence') and organism.intelligence > 0.7:
            pygame.draw.circle(self.screen, (255, 255, 0), (x - 8, y + y_offset), indicator_size)
        
        # efficiency indicator
        if hasattr(organism, 'efficiency') and organism.efficiency > 0.8:
            pygame.draw.circle(self.screen, (0, 255, 255), (x, y + y_offset), indicator_size)
        
        # adaptation indicator
        if hasattr(organism, 'adaptation_score') and organism.adaptation_score > 1.1:
            pygame.draw.circle(self.screen, (0, 255, 0), (x + 8, y + y_offset), indicator_size)
    
    def _render_evolutionary_indicators(self):
        """new: render evolutionary pressure indicators"""
        if not self.config.show_evolutionary_pressure:
            return
        
        # render pressure level indicator
        pressure = self.stats['evolutionary_pressure']
        if pressure > 0.5:
            # high pressure - render warning indicator
            font = pygame.font.Font(None, 20)
            warning_text = f"High Evolutionary Pressure: {pressure:.2f}"
            warning_surface = font.render(warning_text, True, (255, 100, 100))
            self.screen.blit(warning_surface, (10, self.config.height - 60))
    
    def _get_behavioral_color(self, organism, base_color):
        """phase 6: modify organism color based on behavioral state and traits"""
        color = list(base_color)
        
        # modify color based on behavioral state
        if hasattr(organism, 'current_state'):
            if organism.current_state == 'evade':
                # add blue tint for evading organisms
                color[2] = min(255, color[2] + 50)
            elif organism.current_state == 'hunt':
                # add red tint for hunting predators
                color[0] = min(255, color[0] + 30)
            elif organism.current_state == 'rest':
                # add gray tint for resting organisms
                for i in range(3):
                    color[i] = max(0, color[i] - 30)
            elif organism.current_state == 'group_behavior':
                # add yellow tint for group behavior
                color[1] = min(255, color[1] + 30)
        
        # modify color based on protective traits (for prey)
        if organism.species_type == 'prey':
            if hasattr(organism, 'camouflage') and organism.camouflage > 0.7:
                # darker color for camouflaged prey
                for i in range(3):
                    color[i] = max(0, color[i] - 40)
            if hasattr(organism, 'toxicity') and organism.toxicity > 0.7:
                # bright purple for toxic prey
                color = [200, 0, 200]
            if hasattr(organism, 'armor') and organism.armor > 0.7:
                # metallic gray for armored prey
                color = [150, 150, 150]
        
        return tuple(color)
    
    def _draw_behavioral_indicator(self, x, y, organism):
        """phase 6: draw behavioral state indicators"""
        if not hasattr(organism, 'current_state'):
            return
        
        # draw small indicator based on behavioral state
        indicator_size = 3
        indicator_color = (255, 255, 255)  # white
        
        if organism.current_state == 'evade':
            indicator_color = (0, 0, 255)  # blue
        elif organism.current_state == 'hunt':
            indicator_color = (255, 0, 0)  # red
        elif organism.current_state == 'rest':
            indicator_color = (128, 128, 128)  # gray
        elif organism.current_state == 'group_behavior':
            indicator_color = (255, 255, 0)  # yellow
        elif organism.current_state == 'seek_food':
            indicator_color = (0, 255, 0)  # green
        elif organism.current_state == 'explore':
            indicator_color = (255, 165, 0)  # orange
        
        # draw indicator above organism
        pygame.draw.circle(
            self.screen,
            indicator_color,
            (x, y - int(organism.size) - 5),
            indicator_size
        )
    
    def _render_stats(self):
        font = pygame.font.Font(None, 24)
        
        # calculate population health indicators
        population_health = "Healthy"
        if self.stats['alive_organisms'] < 5:
            population_health = "Critical"
        elif self.stats['alive_organisms'] < 10:
            population_health = "Low"
        elif self.stats['alive_organisms'] < 20:
            population_health = "Moderate"
        
        # calculate food availability indicator
        food_availability = "Good"
        if self.stats['food_density'] < 0.0003:
            food_availability = "Critical"
        elif self.stats['food_density'] < 0.0006:
            food_availability = "Low"
        elif self.stats['food_density'] < 0.001:
            food_availability = "Moderate"
        
        stats_text = [
            f"Organisms: {self.stats['alive_organisms']} ({population_health})",
            f"Predators: {self.stats['predators']}",
            f"Prey: {self.stats['prey']}",
            f"Food: {self.stats['available_food']} ({food_availability})",
            f"Time: {self.time_step}",
            f"Generation: {self.stats['generation']}",
            f"Births: {self.stats['total_births']}",
            f"Deaths: {self.stats['total_deaths']}",
            f"Kills: {self.stats['predator_kills']}",
            f"Avg Fitness: {self.stats['average_fitness']:.1f}",
            f"Food Density: {self.stats['food_density']:.4f}",
            # phase 4: speciation stats
            f"Species: {self.stats['species_count']}",
            f"Speciation Events: {self.stats['speciation_events']}",
            f"Avg Genetic Distance: {self.stats['average_genetic_distance']:.3f}",
            f"Lineage Depth: {self.stats['lineage_depth']}",
            # phase 6: behavioral evolution stats
            f"Avg Intelligence: {self.stats['average_intelligence']:.2f}",
            f"Avg Social Behavior: {self.stats['average_social_behavior']:.2f}",
            f"Avg Exploration: {self.stats['average_exploration_rate']:.2f}",
            f"Avg Memory: {self.stats['average_memory_capacity']:.2f}",
            # new: enhanced evolution stats
            f"Avg Adaptation: {self.stats['average_adaptation_score']:.2f}",
            f"Avg Efficiency: {self.stats['average_energy_efficiency']:.2f}",
            f"Evolutionary Pressure: {self.stats['evolutionary_pressure']:.2f}",
            f"Population Diversity: {self.stats['population_diversity']:.3f}",
            f"Environmental Stress: {self.stats['environmental_stress']:.2f}",
            f"Resource Competition: {self.stats['resource_competition_level']:.3f}",
            f"Paused: {'Yes' if self.paused else 'No'}"
        ]
        
        # add trait statistics if available
        if self.trait_snapshots:
            latest = self.trait_snapshots[-1]
            if 'traits' in latest and 'speed' in latest['traits']:
                speed_mean = latest['traits']['speed']['mean']
                vision_mean = latest['traits']['vision']['mean']
                stats_text.append(f"Avg Speed: {speed_mean:.2f}")
                stats_text.append(f"Avg Vision: {vision_mean:.1f}")
        
        # render with color coding for health indicators
        for i, text in enumerate(stats_text):
            color = self.config.text_color
            
            # color code health indicators
            if "Critical" in text:
                color = (255, 100, 100)  # red
            elif "Low" in text:
                color = (255, 200, 100)  # orange
            elif "Moderate" in text:
                color = (200, 255, 100)  # yellow-green
            elif "Healthy" in text or "Good" in text:
                color = (100, 255, 100)  # green
            
            surface = font.render(text, True, color)
            self.screen.blit(surface, (10, 10 + i * 25))
    
    def toggle_pause(self):
        self.paused = not self.paused
    
    def reset(self):
        self.paused = False
        self.time_step = 0
        self.organisms = []
        self.environment = Environment(self.config)
        # phase 5: reset weather system
        self.weather_system = WeatherSystem(self.config)
        self._generate_initial_organisms()
        self._update_stats()
        self.trait_snapshots = []
        self.trait_analyzer = TraitAnalyzer(self.config)
        self.stats['total_births'] = 0
        self.stats['total_deaths'] = 0
        self.stats['predator_kills'] = 0
        # phase 4: reset speciation tracking
        self.species_count = 0
        self.species_history = []
        self.lineage_tree = {}
        self.next_species_id = 1
        self.stats['speciation_events'] = 0
        self.stats['species_count'] = 0
        self.stats['average_genetic_distance'] = 0.0
        self.stats['lineage_depth'] = 0
        
        # phase 6: reset behavioral evolution tracking
        self.stats['behavioral_states'] = {}
        self.stats['average_intelligence'] = 0.0
        self.stats['average_social_behavior'] = 0.0
        self.stats['average_exploration_rate'] = 0.0
        self.stats['average_memory_capacity'] = 0.0
        self.stats['prey_protective_traits'] = {}
        self.stats['predator_hunting_traits'] = {}
        self.stats['group_formation_count'] = 0
        self.stats['cooperative_hunting_events'] = 0
        self.stats['warning_signal_events'] = 0
        self.stats['camouflage_effectiveness'] = 0.0
        self.stats['toxicity_effectiveness'] = 0.0
        self.stats['armor_effectiveness'] = 0.0
        
        # new: reset enhanced evolution tracking
        self.evolutionary_pressure_history = []
        self.adaptation_history = []
        self.diversity_history = []
        self.extinction_history = []
        self.environmental_stress_history = []
        self.resource_competition_history = []
        self.territorial_conflict_history = []
        self.learning_effectiveness_history = []
        self.innovation_history = []
        self.behavioral_adaptation_history = []
    
    def get_trait_analyzer(self):
        """get the trait analyzer for external analysis"""
        return self.trait_analyzer

    def _emergency_population_recovery(self):
        """emergency population recovery to prevent complete extinction"""
        current_population = len(self.organisms)
        
        # if population is critically low, add new organisms
        if current_population < 3:
            # add emergency organisms
            for _ in range(min(5, self.config.initial_organisms - current_population)):
                x = random.uniform(0, self.config.world_width)
                y = random.uniform(0, self.config.world_height)
                
                # add both predators and prey to maintain balance
                if random.random() < 0.7:  # 70% chance for prey
                    self.organisms.append(Organism(x, y, self.config, species_type='prey'))
                else:
                    self.organisms.append(Organism(x, y, self.config, species_type='predator'))
        
        # if only one species type remains, add the other
        predators = [org for org in self.organisms if org.species_type == 'predator']
        prey = [org for org in self.organisms if org.species_type == 'prey']
        
        if len(predators) == 0 and len(prey) > 0:
            # add predators if none exist
            for _ in range(min(3, len(prey) // 3)):
                x = random.uniform(0, self.config.world_width)
                y = random.uniform(0, self.config.world_height)
                self.organisms.append(Organism(x, y, self.config, species_type='predator'))
        
        elif len(prey) == 0 and len(predators) > 0:
            # add prey if none exist
            for _ in range(min(5, len(predators) * 2)):
                x = random.uniform(0, self.config.world_width)
                y = random.uniform(0, self.config.world_height)
                self.organisms.append(Organism(x, y, self.config, species_type='prey')) 