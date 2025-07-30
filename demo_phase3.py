import pygame
import sys
import time
import matplotlib.pyplot as plt
from simulation import Simulation
from sim_config import SimConfig

def run_phase3_demo():
    """run a comprehensive demo of phase 3 features"""
    print("=== Natural Selection Simulator - Phase 3 Demo ===")
    print("Features:")
    print("- Predator-prey dynamics")
    print("- Species distinction (red = predators, green = prey)")
    print("- Fitness tracking (survival time + reproduction)")
    print("- Carrying capacity and resource competition")
    print("- Terrain obstacles affecting movement")
    print("- Ecological interactions and coevolution")
    print()
    
    # initialize pygame
    pygame.init()
    
    # load configuration
    config = SimConfig()
    
    # create simulation
    sim = Simulation(config)
    
    # main demo loop
    running = True
    clock = pygame.time.Clock()
    demo_duration = 10000  # frames (about 2.8 minutes at 60fps)
    frame_count = 0
    
    print("Starting Phase 3 demo...")
    print("Controls:")
    print("- Space: Pause/Resume")
    print("- R: Reset")
    print("- Escape: Quit")
    print()
    
    while running and frame_count < demo_duration:
        # handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    sim.toggle_pause()
                elif event.key == pygame.K_r:
                    sim.reset()
                    frame_count = 0
        
        # update simulation
        sim.update()
        
        # render
        sim.render()
        
        # control frame rate
        clock.tick(config.fps)
        frame_count += 1
        
        # print periodic updates
        if frame_count % 1000 == 0:
            stats = sim.stats
            print(f"Time: {frame_count}, Predators: {stats['predators']}, Prey: {stats['prey']}, "
                  f"Fitness: {stats['average_fitness']:.1f}, Kills: {stats['predator_kills']}")
    
    pygame.quit()
    
    # analyze results
    print("\n=== Demo Complete ===")
    print("Analyzing results...")
    
    # get final statistics
    final_stats = sim.stats
    trait_analyzer = sim.get_trait_analyzer()
    
    print(f"\nFinal Statistics:")
    print(f"- Total Organisms: {final_stats['total_organisms']}")
    print(f"- Predators: {final_stats['predators']}")
    print(f"- Prey: {final_stats['prey']}")
    print(f"- Total Births: {final_stats['total_births']}")
    print(f"- Total Deaths: {final_stats['total_deaths']}")
    print(f"- Predator Kills: {final_stats['predator_kills']}")
    print(f"- Average Fitness: {final_stats['average_fitness']:.1f}")
    print(f"- Food Density: {final_stats['food_density']:.3f}")
    
    # analyze trait trends
    trends = trait_analyzer.get_population_trends()
    
    print(f"\nTrait Analysis:")
    for trait_name, trend_data in trends.items():
        if trait_name in ['speed', 'vision', 'aggression', 'caution']:
            print(f"- {trait_name.capitalize()}: {trend_data['current_mean']:.2f} ({trend_data['trend']})")
    
    # create analysis plots
    print(f"\nGenerating analysis plots...")
    
    # population dynamics
    trait_analyzer.plot_population_and_traits('phase3_population_analysis.png')
    print("- Population analysis saved as 'phase3_population_analysis.png'")
    
    # ecological dynamics
    trait_analyzer.plot_ecological_dynamics('phase3_ecological_dynamics.png')
    print("- Ecological dynamics saved as 'phase3_ecological_dynamics.png'")
    
    # export data
    trait_analyzer.export_trait_data('phase3_data.csv')
    print("- Trait data exported as 'phase3_data.csv'")
    
    print(f"\nPhase 3 demo complete!")
    print("Key observations:")
    print("- Predators (red) actively hunt prey (green)")
    print("- Prey flee from nearby predators")
    print("- Fitness is tracked based on survival and reproduction")
    print("- Carrying capacity limits population growth")
    print("- Terrain obstacles affect movement patterns")
    print("- Coevolution between predator and prey traits")

if __name__ == "__main__":
    run_phase3_demo() 