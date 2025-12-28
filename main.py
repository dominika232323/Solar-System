from simulation_consts import *
from planet import Planet
from physical_consts import *

import pygame

pygame.init()
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Solar System Simulation")

def main():
    run_simulation = True 
    
    sun = Planet(SUN_MASS, SUN_RADIUS / 50, 0, 0, SUN_COLOR)
    mercury = Planet(MERCURY_MASS, MERCURY_RADIUS, MERCURY_DISTANCE, 0, MERCURY_COLOR)
    venus = Planet(VENUS_MASS, VENUS_RADIUS, VENUS_DISTANCE, 0, VENUS_COLOR)
    earth = Planet(EARTH_MASS, EARTH_RADIUS, EARTH_DISTANCE, 0, EARTH_COLOR)
    mars = Planet(MARS_MASS, MARS_RADIUS, MARS_DISTANCE, 0, MARS_COLOR)
    jupiter = Planet(JUPITER_MASS, JUPITER_RADIUS, JUPITER_DISTANCE, 0, JUPITER_COLOR)
    saturn = Planet(SATURN_MASS, SATURN_RADIUS, SATURN_DISTANCE, 0, SATURN_COLOR)
    uranus = Planet(URANUS_MASS, URANUS_RADIUS, URANUS_DISTANCE, 0, URANUS_COLOR)
    neptun = Planet(NEPTUN_MASS, NEPTUN_RADIUS, NEPTUN_DISTANCE, 0, NEPTUN_COLOR)
    
    planets = [sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptun]
    
    while run_simulation:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_simulation = False
        
        WINDOW.fill((0, 0, 0))
        
        for planet in planets:
            planet.draw(WINDOW)
        
        pygame.display.update()
    pygame.quit()

if __name__ == "__main__":
    main()
