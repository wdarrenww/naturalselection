import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict

class TraitAnalyzer:
    def __init__(self, config):
        self.config = config
        self.trait_history = []
        self.generation_data = defaultdict(list)
    
    def add_snapshot(self, snapshot):
        """add a trait snapshot from the simulation"""
        self.trait_history.append(snapshot)
        
        # also track by generation
        generation = snapshot.get('generation', 0)
        self.generation_data[generation].append(snapshot)
    
    def get_trait_statistics(self, trait_name, time_range=None):
        """get statistics for a specific trait over time"""
        if not self.trait_history:
            return None
        
        start_idx = 0
        end_idx = len(self.trait_history)
        
        if time_range:
            start_time, end_time = time_range
            start_idx = max(0, start_time // self.config.trait_log_interval)
            end_idx = min(len(self.trait_history), end_time // self.config.trait_log_interval)
        
        values = []
        for snapshot in self.trait_history[start_idx:end_idx]:
            if 'traits' in snapshot and trait_name in snapshot['traits']:
                values.append(snapshot['traits'][trait_name]['mean'])
        
        if not values:
            return None
        
        return {
            'mean': np.mean(values),
            'std': np.std(values),
            'min': np.min(values),
            'max': np.max(values),
            'trend': self._calculate_trend(values)
        }
    
    def _calculate_trend(self, values):
        """calculate if trait is increasing, decreasing, or stable"""
        if len(values) < 2:
            return 'stable'
        
        # simple linear regression slope
        x = np.arange(len(values))
        slope = np.polyfit(x, values, 1)[0]
        
        if abs(slope) < 0.01:
            return 'stable'
        elif slope > 0:
            return 'increasing'
        else:
            return 'decreasing'
    
    def get_population_trends(self):
        """analyze population and trait trends over time"""
        if not self.trait_history:
            return {}
        
        trends = {}
        for trait_name in ['speed', 'vision', 'size', 'metabolism', 'aggression', 'caution', 'stamina']:
            stats = self.get_trait_statistics(trait_name)
            if stats:
                trends[trait_name] = {
                    'current_mean': stats['mean'],
                    'trend': stats['trend'],
                    'volatility': stats['std']
                }
        
        # population trends
        populations = [s['population'] for s in self.trait_history]
        predators = [s.get('predators', 0) for s in self.trait_history]
        prey = [s.get('prey', 0) for s in self.trait_history]
        
        if populations:
            trends['population'] = {
                'current': populations[-1],
                'trend': self._calculate_trend(populations),
                'max': max(populations),
                'min': min(populations)
            }
        
        if predators:
            trends['predators'] = {
                'current': predators[-1],
                'trend': self._calculate_trend(predators),
                'max': max(predators),
                'min': min(predators)
            }
        
        if prey:
            trends['prey'] = {
                'current': prey[-1],
                'trend': self._calculate_trend(prey),
                'max': max(prey),
                'min': min(prey)
            }
        
        return trends
    
    def plot_trait_evolution(self, trait_name, save_path=None):
        """create a plot showing trait evolution over time"""
        if not self.trait_history:
            return
        
        times = [s['time_step'] for s in self.trait_history]
        means = []
        stds = []
        
        for snapshot in self.trait_history:
            if 'traits' in snapshot and trait_name in snapshot['traits']:
                means.append(snapshot['traits'][trait_name]['mean'])
                stds.append(snapshot['traits'][trait_name]['std'])
            else:
                means.append(0)
                stds.append(0)
        
        plt.figure(figsize=(10, 6))
        plt.plot(times, means, 'b-', linewidth=2, label=f'{trait_name} mean')
        plt.fill_between(times, 
                        [m - s for m, s in zip(means, stds)],
                        [m + s for m, s in zip(means, stds)],
                        alpha=0.3, color='blue', label='±1 std dev')
        
        plt.xlabel('Time Step')
        plt.ylabel(f'{trait_name.capitalize()} Value')
        plt.title(f'{trait_name.capitalize()} Evolution Over Time')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        if save_path:
            plt.savefig(save_path)
            plt.close()
        else:
            plt.show()
    
    def plot_population_and_traits(self, save_path=None):
        """create a comprehensive plot showing population and key traits"""
        if not self.trait_history:
            return
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
        
        times = [s['time_step'] for s in self.trait_history]
        
        # population by species
        predators = [s.get('predators', 0) for s in self.trait_history]
        prey = [s.get('prey', 0) for s in self.trait_history]
        
        ax1.plot(times, predators, 'r-', linewidth=2, label='Predators')
        ax1.plot(times, prey, 'g-', linewidth=2, label='Prey')
        ax1.set_title('Population by Species Over Time')
        ax1.set_ylabel('Population')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # speed
        speed_means = []
        for snapshot in self.trait_history:
            if 'traits' in snapshot and 'speed' in snapshot['traits']:
                speed_means.append(snapshot['traits']['speed']['mean'])
            else:
                speed_means.append(0)
        ax2.plot(times, speed_means, 'b-', linewidth=2)
        ax2.set_title('Average Speed Over Time')
        ax2.set_ylabel('Speed')
        ax2.grid(True, alpha=0.3)
        
        # aggression (predator trait)
        aggression_means = []
        for snapshot in self.trait_history:
            if 'traits' in snapshot and 'aggression' in snapshot['traits']:
                aggression_means.append(snapshot['traits']['aggression']['mean'])
            else:
                aggression_means.append(0)
        ax3.plot(times, aggression_means, 'r-', linewidth=2)
        ax3.set_title('Average Aggression Over Time')
        ax3.set_ylabel('Aggression')
        ax3.grid(True, alpha=0.3)
        
        # caution (prey trait)
        caution_means = []
        for snapshot in self.trait_history:
            if 'traits' in snapshot and 'caution' in snapshot['traits']:
                caution_means.append(snapshot['traits']['caution']['mean'])
            else:
                caution_means.append(0)
        ax4.plot(times, caution_means, 'g-', linewidth=2)
        ax4.set_title('Average Caution Over Time')
        ax4.set_ylabel('Caution')
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path)
            plt.close()
        else:
            plt.show()
    
    def plot_ecological_dynamics(self, save_path=None):
        """create a plot showing ecological dynamics"""
        if not self.trait_history:
            return
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
        
        times = [s['time_step'] for s in self.trait_history]
        
        # predator-prey dynamics
        predators = [s.get('predators', 0) for s in self.trait_history]
        prey = [s.get('prey', 0) for s in self.trait_history]
        
        ax1.plot(times, predators, 'r-', linewidth=2, label='Predators')
        ax1.plot(times, prey, 'g-', linewidth=2, label='Prey')
        ax1.set_title('Predator-Prey Dynamics')
        ax1.set_ylabel('Population')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # food density
        food_density = [s.get('food_density', 0) for s in self.trait_history]
        ax2.plot(times, food_density, 'y-', linewidth=2)
        ax2.set_title('Food Density Over Time')
        ax2.set_ylabel('Food Density')
        ax2.grid(True, alpha=0.3)
        
        # average fitness
        fitness = [s.get('average_fitness', 0) for s in self.trait_history]
        ax3.plot(times, fitness, 'm-', linewidth=2)
        ax3.set_title('Average Fitness Over Time')
        ax3.set_ylabel('Fitness Score')
        ax3.grid(True, alpha=0.3)
        
        # vision evolution
        vision_means = []
        for snapshot in self.trait_history:
            if 'traits' in snapshot and 'vision' in snapshot['traits']:
                vision_means.append(snapshot['traits']['vision']['mean'])
            else:
                vision_means.append(0)
        ax4.plot(times, vision_means, 'c-', linewidth=2)
        ax4.set_title('Average Vision Over Time')
        ax4.set_ylabel('Vision Radius')
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path)
            plt.close()
        else:
            plt.show()
    
    def export_trait_data(self, filename):
        """export trait data to csv for external analysis"""
        if not self.trait_history:
            return
        
        import csv
        
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['time_step', 'population', 'predators', 'prey', 'generation', 'average_fitness', 'food_density']
            trait_names = ['speed', 'vision', 'size', 'metabolism', 'reproduction_threshold', 'max_age', 'aggression', 'caution', 'stamina']
            
            for trait in trait_names:
                fieldnames.extend([f'{trait}_mean', f'{trait}_std', f'{trait}_min', f'{trait}_max'])
            
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for snapshot in self.trait_history:
                row = {
                    'time_step': snapshot['time_step'],
                    'population': snapshot['population'],
                    'predators': snapshot.get('predators', 0),
                    'prey': snapshot.get('prey', 0),
                    'generation': snapshot.get('generation', 0),
                    'average_fitness': snapshot.get('average_fitness', 0),
                    'food_density': snapshot.get('food_density', 0)
                }
                
                for trait in trait_names:
                    if 'traits' in snapshot and trait in snapshot['traits']:
                        trait_data = snapshot['traits'][trait]
                        row[f'{trait}_mean'] = trait_data['mean']
                        row[f'{trait}_std'] = trait_data['std']
                        row[f'{trait}_min'] = trait_data['min']
                        row[f'{trait}_max'] = trait_data['max']
                    else:
                        row[f'{trait}_mean'] = 0
                        row[f'{trait}_std'] = 0
                        row[f'{trait}_min'] = 0
                        row[f'{trait}_max'] = 0
                
                writer.writerow(row) 