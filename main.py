import pygame
import sys
from simulation import Simulation
from sim_config import SimConfig

def main():
    # initialize pygame
    pygame.init()
    
    # load configuration
    config = SimConfig()
    
    # create simulation
    sim = Simulation(config)
    
    # main game loop
    running = True
    clock = pygame.time.Clock()
    
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
        
        # update simulation
        sim.update()
        
        # render
        sim.render()
        
        # control frame rate
        clock.tick(config.fps)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main() 