import pygame
import sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from simulation import Simulation
from sim_config import SimConfig
from trait_analyzer import TraitAnalyzer

def run_enhanced_simulation():
    """run the enhanced simulation with comprehensive analysis"""
    print("Starting Enhanced Natural Selection Simulation...")
    print("=" * 60)
    print("Major Improvements:")
    print("- 30+ traits with realistic interactions")
    print("- Trait synergies and conflicts")
    print("- Enhanced evolutionary pressure")
    print("- Realistic energy costs and efficiency")
    print("- Territorial behavior and resource competition")
    print("- Advanced learning and memory systems")
    print("- Environmental adaptation tracking")
    print("- Population diversity monitoring")
    print("=" * 60)
    
    # initialize pygame
    pygame.init()
    
    # load enhanced configuration
    config = SimConfig()
    
    # create enhanced simulation
    sim = Simulation(config)
    
    # main game loop
    running = True
    clock = pygame.time.Clock()
    
    print("Controls:")
    print("- Space: Pause/Resume")
    print("- R: Reset")
    print("- Escape: Quit")
    print("- 1-9: Toggle visualization features")
    print()
    
    while running:
        # handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    sim.toggle_pause()
                    print(f"Simulation {'Paused' if sim.paused else 'Resumed'}")
                elif event.key == pygame.K_r:
                    sim.reset()
                    print("Simulation Reset")
                elif event.key == pygame.K_1:
                    config.show_energy_bars = not config.show_energy_bars
                    print(f"Energy Bars: {'On' if config.show_energy_bars else 'Off'}")
                elif event.key == pygame.K_2:
                    config.show_trait_indicators = not config.show_trait_indicators
                    print(f"Trait Indicators: {'On' if config.show_trait_indicators else 'Off'}")
                elif event.key == pygame.K_3:
                    config.show_behavior_states = not config.show_behavior_states
                    print(f"Behavior States: {'On' if config.show_behavior_states else 'Off'}")
                elif event.key == pygame.K_4:
                    config.show_evolutionary_pressure = not config.show_evolutionary_pressure
                    print(f"Evolutionary Pressure: {'On' if config.show_evolutionary_pressure else 'Off'}")
                elif event.key == pygame.K_5:
                    config.show_vision_radius = not config.show_vision_radius
                    print(f"Vision Radius: {'On' if config.show_vision_radius else 'Off'}")
                elif event.key == pygame.K_6:
                    config.show_species_colors = not config.show_species_colors
                    print(f"Species Colors: {'On' if config.show_species_colors else 'Off'}")
                elif event.key == pygame.K_7:
                    config.show_day_night_cycle = not config.show_day_night_cycle
                    print(f"Day/Night Cycle: {'On' if config.show_day_night_cycle else 'Off'}")
                elif event.key == pygame.K_8:
                    config.show_temperature_zones = not config.show_temperature_zones
                    print(f"Temperature Zones: {'On' if config.show_temperature_zones else 'Off'}")
                elif event.key == pygame.K_9:
                    config.show_season_indicator = not config.show_season_indicator
                    print(f"Season Indicator: {'On' if config.show_season_indicator else 'Off'}")
        
        # update simulation
        sim.update()
        
        # render
        sim.render()
        
        # control frame rate
        clock.tick(config.fps)
        
        # print periodic status updates
        if sim.time_step % 1000 == 0:
            print(f"Time: {sim.time_step}, Organisms: {sim.stats['alive_organisms']}, "
                  f"Species: {sim.stats['species_count']}, "
                  f"Adaptation: {sim.stats['average_adaptation_score']:.2f}, "
                  f"Pressure: {sim.stats['evolutionary_pressure']:.2f}")
    
    pygame.quit()
    
    # comprehensive analysis
    print("\n" + "=" * 60)
    print("SIMULATION ANALYSIS")
    print("=" * 60)
    
    analyzer = sim.get_trait_analyzer()
    
    # analyze trait evolution
    print("\nTrait Evolution Analysis:")
    trait_trends = analyzer.get_population_trends()
    for trait_name, trend_data in trait_trends.items():
        if isinstance(trend_data, dict) and 'trend' in trend_data:
            print(f"  {trait_name}: {trend_data['trend']} (current: {trend_data.get('current', 'N/A')})")
    
    # enhanced evolution analysis
    print("\nEnhanced Evolution Analysis:")
    print(f"  Average Adaptation Score: {sim.stats['average_adaptation_score']:.3f}")
    print(f"  Average Energy Efficiency: {sim.stats['average_energy_efficiency']:.3f}")
    print(f"  Population Diversity: {sim.stats['population_diversity']:.3f}")
    print(f"  Evolutionary Pressure: {sim.stats['evolutionary_pressure']:.3f}")
    print(f"  Environmental Stress: {sim.stats['environmental_stress']:.3f}")
    print(f"  Resource Competition: {sim.stats['resource_competition_level']:.3f}")
    
    # speciation analysis
    print(f"\nSpeciation Analysis:")
    print(f"  Total Species: {sim.stats['species_count']}")
    print(f"  Speciation Events: {sim.stats['speciation_events']}")
    print(f"  Average Genetic Distance: {sim.stats['average_genetic_distance']:.3f}")
    print(f"  Lineage Depth: {sim.stats['lineage_depth']}")
    
    # behavioral evolution analysis
    print(f"\nBehavioral Evolution Analysis:")
    print(f"  Average Intelligence: {sim.stats['average_intelligence']:.3f}")
    print(f"  Average Social Behavior: {sim.stats['average_social_behavior']:.3f}")
    print(f"  Average Exploration Rate: {sim.stats['average_exploration_rate']:.3f}")
    print(f"  Average Memory Capacity: {sim.stats['average_memory_capacity']:.3f}")
    
    # trait interaction analysis
    print(f"\nTrait Interaction Analysis:")
    print(f"  Trait Synergies: {sim.stats['trait_synergy_count']}")
    print(f"  Trait Conflicts: {sim.stats['trait_conflict_count']}")
    
    # population dynamics
    print(f"\nPopulation Dynamics:")
    print(f"  Total Births: {sim.stats['total_births']}")
    print(f"  Total Deaths: {sim.stats['total_deaths']}")
    print(f"  Predator Kills: {sim.stats['predator_kills']}")
    print(f"  Generation: {sim.stats['generation']}")
    
    # create comprehensive plots
    create_enhanced_analysis_plots(sim, analyzer)
    
    print("\nAnalysis complete! Check the generated plots for detailed insights.")
    print("=" * 60)

def create_enhanced_analysis_plots(sim, analyzer):
    """create comprehensive analysis plots"""
    print("\nGenerating analysis plots...")
    
    # create figure with subplots
    fig = plt.figure(figsize=(20, 16))
    
    # 1. Population and Species Dynamics
    ax1 = plt.subplot(3, 3, 1)
    times = [s['time_step'] for s in sim.trait_snapshots]
    populations = [s['population'] for s in sim.trait_snapshots]
    predators = [s['predators'] for s in sim.trait_snapshots]
    prey = [s['prey'] for s in sim.trait_snapshots]
    species_counts = [s['species_count'] for s in sim.trait_snapshots]
    
    ax1.plot(times, populations, 'b-', linewidth=2, label='Total Population')
    ax1.plot(times, predators, 'r-', linewidth=2, label='Predators')
    ax1.plot(times, prey, 'g-', linewidth=2, label='Prey')
    ax1_twin = ax1.twinx()
    ax1_twin.plot(times, species_counts, 'm--', linewidth=2, label='Species Count')
    ax1.set_title('Population and Species Dynamics')
    ax1.set_xlabel('Time Step')
    ax1.set_ylabel('Population')
    ax1_twin.set_ylabel('Species Count')
    ax1.legend(loc='upper left')
    ax1_twin.legend(loc='upper right')
    ax1.grid(True, alpha=0.3)
    
    # 2. Enhanced Evolution Metrics
    ax2 = plt.subplot(3, 3, 2)
    adaptation_scores = [s['average_adaptation_score'] for s in sim.trait_snapshots]
    energy_efficiencies = [s['average_energy_efficiency'] for s in sim.trait_snapshots]
    evolutionary_pressures = [s['evolutionary_pressure'] for s in sim.trait_snapshots]
    
    ax2.plot(times, adaptation_scores, 'g-', linewidth=2, label='Adaptation Score')
    ax2.plot(times, energy_efficiencies, 'b-', linewidth=2, label='Energy Efficiency')
    ax2_twin = ax2.twinx()
    ax2_twin.plot(times, evolutionary_pressures, 'r--', linewidth=2, label='Evolutionary Pressure')
    ax2.set_title('Enhanced Evolution Metrics')
    ax2.set_xlabel('Time Step')
    ax2.set_ylabel('Score')
    ax2_twin.set_ylabel('Pressure')
    ax2.legend(loc='upper left')
    ax2_twin.legend(loc='upper right')
    ax2.grid(True, alpha=0.3)
    
    # 3. Environmental and Competition Analysis
    ax3 = plt.subplot(3, 3, 3)
    environmental_stress = [s['environmental_stress'] for s in sim.trait_snapshots]
    resource_competition = [s['resource_competition_level'] for s in sim.trait_snapshots]
    population_diversity = [s['population_diversity'] for s in sim.trait_snapshots]
    
    ax3.plot(times, environmental_stress, 'r-', linewidth=2, label='Environmental Stress')
    ax3.plot(times, resource_competition, 'orange', linewidth=2, label='Resource Competition')
    ax3_twin = ax3.twinx()
    ax3_twin.plot(times, population_diversity, 'g--', linewidth=2, label='Population Diversity')
    ax3.set_title('Environmental and Competition Analysis')
    ax3.set_xlabel('Time Step')
    ax3.set_ylabel('Stress/Competition Level')
    ax3_twin.set_ylabel('Diversity')
    ax3.legend(loc='upper left')
    ax3_twin.legend(loc='upper right')
    ax3.grid(True, alpha=0.3)
    
    # 4. Trait Evolution - Speed and Vision
    ax4 = plt.subplot(3, 3, 4)
    speed_means = []
    vision_means = []
    for snapshot in sim.trait_snapshots:
        if 'traits' in snapshot and 'speed' in snapshot['traits']:
            speed_means.append(snapshot['traits']['speed']['mean'])
            vision_means.append(snapshot['traits']['vision']['mean'])
        else:
            speed_means.append(0)
            vision_means.append(0)
    
    ax4.plot(times, speed_means, 'b-', linewidth=2, label='Speed')
    ax4.plot(times, vision_means, 'g-', linewidth=2, label='Vision')
    ax4.set_title('Movement Trait Evolution')
    ax4.set_xlabel('Time Step')
    ax4.set_ylabel('Trait Value')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    
    # 5. Behavioral Trait Evolution
    ax5 = plt.subplot(3, 3, 5)
    intelligence_means = []
    social_behavior_means = []
    for snapshot in sim.trait_snapshots:
        if 'traits' in snapshot and 'intelligence' in snapshot['traits']:
            intelligence_means.append(snapshot['traits']['intelligence']['mean'])
            social_behavior_means.append(snapshot['traits']['social_behavior']['mean'])
        else:
            intelligence_means.append(0)
            social_behavior_means.append(0)
    
    ax5.plot(times, intelligence_means, 'purple', linewidth=2, label='Intelligence')
    ax5.plot(times, social_behavior_means, 'orange', linewidth=2, label='Social Behavior')
    ax5.set_title('Behavioral Trait Evolution')
    ax5.set_xlabel('Time Step')
    ax5.set_ylabel('Trait Value')
    ax5.legend()
    ax5.grid(True, alpha=0.3)
    
    # 6. Enhanced Trait Evolution
    ax6 = plt.subplot(3, 3, 6)
    efficiency_means = []
    adaptability_means = []
    for snapshot in sim.trait_snapshots:
        if 'traits' in snapshot and 'efficiency' in snapshot['traits']:
            efficiency_means.append(snapshot['traits']['efficiency']['mean'])
            adaptability_means.append(snapshot['traits']['adaptability']['mean'])
        else:
            efficiency_means.append(0)
            adaptability_means.append(0)
    
    ax6.plot(times, efficiency_means, 'cyan', linewidth=2, label='Efficiency')
    ax6.plot(times, adaptability_means, 'magenta', linewidth=2, label='Adaptability')
    ax6.set_title('Enhanced Trait Evolution')
    ax6.set_xlabel('Time Step')
    ax6.set_ylabel('Trait Value')
    ax6.legend()
    ax6.grid(True, alpha=0.3)
    
    # 7. Predator-Prey Dynamics
    ax7 = plt.subplot(3, 3, 7)
    aggression_means = []
    caution_means = []
    for snapshot in sim.trait_snapshots:
        if 'traits' in snapshot and 'aggression' in snapshot['traits']:
            aggression_means.append(snapshot['traits']['aggression']['mean'])
            caution_means.append(snapshot['traits']['caution']['mean'])
        else:
            aggression_means.append(0)
            caution_means.append(0)
    
    ax7.plot(times, aggression_means, 'red', linewidth=2, label='Aggression (Predators)')
    ax7.plot(times, caution_means, 'green', linewidth=2, label='Caution (Prey)')
    ax7.set_title('Predator-Prey Trait Evolution')
    ax7.set_xlabel('Time Step')
    ax7.set_ylabel('Trait Value')
    ax7.legend()
    ax7.grid(True, alpha=0.3)
    
    # 8. Protective Features Evolution
    ax8 = plt.subplot(3, 3, 8)
    camouflage_means = []
    toxicity_means = []
    armor_means = []
    for snapshot in sim.trait_snapshots:
        if 'traits' in snapshot and 'camouflage' in snapshot['traits']:
            camouflage_means.append(snapshot['traits']['camouflage']['mean'])
            toxicity_means.append(snapshot['traits']['toxicity']['mean'])
            armor_means.append(snapshot['traits']['armor']['mean'])
        else:
            camouflage_means.append(0)
            toxicity_means.append(0)
            armor_means.append(0)
    
    ax8.plot(times, camouflage_means, 'brown', linewidth=2, label='Camouflage')
    ax8.plot(times, toxicity_means, 'purple', linewidth=2, label='Toxicity')
    ax8.plot(times, armor_means, 'gray', linewidth=2, label='Armor')
    ax8.set_title('Protective Features Evolution')
    ax8.set_xlabel('Time Step')
    ax8.set_ylabel('Trait Value')
    ax8.legend()
    ax8.grid(True, alpha=0.3)
    
    # 9. Fitness and Survival Analysis
    ax9 = plt.subplot(3, 3, 9)
    fitness_scores = [s['average_fitness'] for s in sim.trait_snapshots]
    food_density = [s['food_density'] for s in sim.trait_snapshots]
    
    ax9.plot(times, fitness_scores, 'gold', linewidth=2, label='Average Fitness')
    ax9_twin = ax9.twinx()
    ax9_twin.plot(times, food_density, 'brown', linewidth=2, label='Food Density')
    ax9.set_title('Fitness and Resource Analysis')
    ax9.set_xlabel('Time Step')
    ax9.set_ylabel('Fitness Score')
    ax9_twin.set_ylabel('Food Density')
    ax9.legend(loc='upper left')
    ax9_twin.legend(loc='upper right')
    ax9.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('enhanced_evolution_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # create trait interaction heatmap
    create_trait_interaction_heatmap(sim)
    
    # create speciation timeline
    create_speciation_timeline(sim)
    
    print("Analysis plots saved as:")
    print("- enhanced_evolution_analysis.png")
    print("- trait_interaction_heatmap.png")
    print("- speciation_timeline.png")

def create_trait_interaction_heatmap(sim):
    """create heatmap showing trait interactions"""
    if not sim.trait_snapshots:
        return
    
    # get latest snapshot for trait interactions
    latest = sim.trait_snapshots[-1]
    
    # define trait categories
    movement_traits = ['speed', 'vision', 'stamina']
    behavioral_traits = ['intelligence', 'social_behavior', 'exploration_rate', 'memory_capacity']
    protective_traits = ['camouflage', 'toxicity', 'armor', 'warning_signals', 'group_cohesion']
    hunting_traits = ['hunting_strategy', 'patience', 'cooperation', 'learning_rate']
    enhanced_traits = ['efficiency', 'adaptability', 'resilience', 'specialization', 'innovation']
    
    all_traits = movement_traits + behavioral_traits + protective_traits + hunting_traits + enhanced_traits
    
    # create correlation matrix
    trait_data = {}
    for trait in all_traits:
        if trait in latest['traits']:
            trait_data[trait] = latest['traits'][trait]['mean']
    
    # create simple interaction matrix (simplified)
    n_traits = len(trait_data)
    interaction_matrix = np.zeros((n_traits, n_traits))
    
    trait_names = list(trait_data.keys())
    for i, trait1 in enumerate(trait_names):
        for j, trait2 in enumerate(trait_names):
            if i == j:
                interaction_matrix[i, j] = 1.0  # self-correlation
            else:
                # simple interaction based on trait values
                val1 = trait_data[trait1]
                val2 = trait_data[trait2]
                interaction_matrix[i, j] = (val1 + val2) / 2.0
    
    # create heatmap
    plt.figure(figsize=(12, 10))
    plt.imshow(interaction_matrix, cmap='viridis', aspect='auto')
    plt.colorbar(label='Interaction Strength')
    plt.title('Trait Interaction Matrix')
    plt.xlabel('Traits')
    plt.ylabel('Traits')
    plt.xticks(range(len(trait_names)), trait_names, rotation=45, ha='right')
    plt.yticks(range(len(trait_names)), trait_names)
    plt.tight_layout()
    plt.savefig('trait_interaction_heatmap.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_speciation_timeline(sim):
    """create speciation timeline plot"""
    if not sim.species_history:
        return
    
    # extract speciation data
    times = [entry['time_step'] for entry in sim.species_history]
    species_counts = [entry['species_count'] for entry in sim.species_history]
    
    plt.figure(figsize=(12, 6))
    plt.plot(times, species_counts, 'b-', linewidth=2, marker='o', markersize=4)
    plt.title('Speciation Timeline')
    plt.xlabel('Time Step')
    plt.ylabel('Number of Species')
    plt.grid(True, alpha=0.3)
    
    # highlight speciation events
    speciation_events = []
    for i in range(1, len(species_counts)):
        if species_counts[i] > species_counts[i-1]:
            speciation_events.append(times[i])
    
    if speciation_events:
        plt.scatter(speciation_events, [species_counts[times.index(t)] for t in speciation_events], 
                   color='red', s=100, zorder=5, label='Speciation Events')
        plt.legend()
    
    plt.tight_layout()
    plt.savefig('speciation_timeline.png', dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    run_enhanced_simulation() 