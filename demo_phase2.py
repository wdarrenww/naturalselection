#!/usr/bin/env python3
"""
Phase 2 Demo - Heredity and Reproduction

This demo showcases the Phase 2 features:
- DNA/genome system with traits (speed, vision, size, metabolism)
- Trait-to-behavior mapping (phenotype mapping)
- Asexual reproduction with DNA inheritance and mutation
- Death by age/energy
- Visualization of trait differences
- Trait tracking and analysis
"""

import pygame
import sys
import time
from simulation import Simulation
from sim_config import SimConfig
from trait_analyzer import TraitAnalyzer

def run_phase2_demo():
    """run a demonstration of phase 2 features"""
    
    # initialize pygame
    pygame.init()
    
    # load configuration with phase 2 settings
    config = SimConfig()
    config.initial_organisms = 30
    config.mutation_rate = 0.4  # higher mutation rate for demo
    config.mutation_magnitude = 0.15
    config.trait_log_interval = 50  # log more frequently for demo
    
    # create simulation
    sim = Simulation(config)
    
    print("Phase 2 Demo - Heredity and Reproduction")
    print("=" * 50)
    print("Features:")
    print("- DNA system with 6 traits: speed, vision, size, metabolism, reproduction_threshold, max_age")
    print("- Trait-based behavior: speed affects movement, vision affects food detection")
    print("- Asexual reproduction with gaussian mutation")
    print("- Death by energy or age")
    print("- Color visualization: red = fast, green = slow")
    print("- Real-time trait tracking and statistics")
    print("\nControls:")
    print("- Space: Pause/Resume")
    print("- R: Reset")
    print("- Escape: Quit")
    print("- V: Toggle vision radius display")
    print("\nPress any key to start...")
    
    # wait for user input
    input()
    
    # main game loop
    running = True
    clock = pygame.time.Clock()
    start_time = time.time()
    
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
                elif event.key == pygame.K_r:
                    sim.reset()
                elif event.key == pygame.K_v:
                    config.show_vision_radius = not config.show_vision_radius
        
        # update simulation
        sim.update()
        
        # render
        sim.render()
        
        # control frame rate
        clock.tick(config.fps)
        
        # check if demo should end (after 30 seconds)
        if time.time() - start_time > 30:
            print("\nDemo completed! Generating analysis...")
            break
    
    # generate analysis
    analyzer = sim.get_trait_analyzer()
    if analyzer.trait_history:
        print("\nTrait Analysis:")
        print("-" * 30)
        
        trends = analyzer.get_population_trends()
        for trait, data in trends.items():
            if trait == 'population':
                print(f"Population: {data['current']} (trend: {data['trend']})")
            else:
                print(f"{trait.capitalize()}: mean={data['current_mean']:.2f}, trend={data['trend']}")
        
        # save plots
        print("\nGenerating plots...")
        analyzer.plot_population_and_traits("phase2_analysis.png")
        analyzer.export_trait_data("phase2_traits.csv")
        print("Analysis saved to phase2_analysis.png and phase2_traits.csv")
    
    pygame.quit()
    print("\nPhase 2 demo completed!")

if __name__ == "__main__":
    run_phase2_demo() 