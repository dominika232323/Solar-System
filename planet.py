from simulation_consts import *
import pygame

class Planet:
    def __init__(self, mass, radius, starting_x, starting_y, rgb_color):
        self.m = mass
        self.r = radius
        self.x = starting_x
        self.y = starting_y
        self.color = rgb_color

        self.v_x = 0 # horizontal velocity component
        self.v_y = 0 # verticular velocity component

        self.orbit = [] # points on the orbit
    
    def draw(self, window):
        # position relative to the center of the window
        x = self.x * SCALE + WINDOW_WIDTH / 2
        y = self.y * SCALE + WINDOW_HEIGHT / 2

        pygame.draw.circle(window, self.color, (x, y), self.r * RADIUS_SCALE)
    
    def compute_gravitational_forces(self, other):
        pass
    
    def update_position(self):
        pass
    