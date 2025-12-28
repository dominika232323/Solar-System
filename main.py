from simulation_consts import *
from planet import Planet
from physical_consts import *

import pygame

pygame.init()
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Solar System Simulation")

FONT = pygame.font.SysFont("comicsans", 16)

def initialize_planets():
    sun = Planet(SUN_MASS, SUN_RADIUS / 50, 0, 0, SUN_COLOR, True)
    mercury = Planet(MERCURY_MASS, MERCURY_RADIUS, MERCURY_DISTANCE, 0, MERCURY_COLOR)
    venus = Planet(VENUS_MASS, VENUS_RADIUS, VENUS_DISTANCE, 0, VENUS_COLOR)
    earth = Planet(EARTH_MASS, EARTH_RADIUS, EARTH_DISTANCE, 0, EARTH_COLOR)
    mars = Planet(MARS_MASS, MARS_RADIUS, MARS_DISTANCE, 0, MARS_COLOR)
    jupiter = Planet(JUPITER_MASS, JUPITER_RADIUS, JUPITER_DISTANCE, 0, JUPITER_COLOR)
    saturn = Planet(SATURN_MASS, SATURN_RADIUS, SATURN_DISTANCE, 0, SATURN_COLOR)
    uranus = Planet(URANUS_MASS, URANUS_RADIUS, URANUS_DISTANCE, 0, URANUS_COLOR)
    neptun = Planet(NEPTUN_MASS, NEPTUN_RADIUS, NEPTUN_DISTANCE, 0, NEPTUN_COLOR)
    
    mercury.v_y = MERCURY_VELOCITY
    venus.v_y = VENUS_VELOCITY
    earth.v_y = EARTH_VELOCITY
    mars.v_y = MARS_VELOCITY
    jupiter.v_y = JUPITER_VELOCITY
    saturn.v_y = SATURN_VELOCITY
    uranus.v_y = URANUS_VELOCITY
    neptun.v_y = NEPTUN_VELOCITY

    return [sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptun]

def main():
    run_simulation = True
    clock = pygame.time.Clock() 
    
    planets = initialize_planets()
    
    while run_simulation:
        clock.tick(60)
        WINDOW.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_simulation = False
                
        for planet in planets:
            planet.update_position(planets)
            planet.draw(WINDOW, FONT)
        
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
