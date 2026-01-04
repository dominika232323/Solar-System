import math
from simulation_consts import SimulationConsts
from physical_consts import G
import pygame


class Planet:
    def __init__(self, mass, radius, starting_x, starting_y, rgb_color, is_sun=False):
        self.m = mass
        self.r = radius
        self.x = starting_x
        self.y = starting_y
        self.color = rgb_color

        self.is_sun = is_sun
        self.distance_to_sun = 0

        self.v_x = 0  # horizontal velocity component
        self.v_y = 0  # vertical velocity component
        self.a_x = 0.0 # horizontal acceleration component
        self.a_y = 0.0 # vertical acceleration component

        self.orbit = []  # points on the orbit

    def draw(self, window, font):
        # position relative to the center of the window
        x = (self.x - SimulationConsts.CAMERA_X) * SimulationConsts.SCALE + SimulationConsts.WINDOW_WIDTH / 2
        y = (self.y - SimulationConsts.CAMERA_Y) * SimulationConsts.SCALE + SimulationConsts.WINDOW_HEIGHT / 2

        if SimulationConsts.DRAW_ORBIT and len(self.orbit) > 2:
            updated_points = []

            for point in self.orbit:
                x, y = point
                x = (x - SimulationConsts.CAMERA_X) * SimulationConsts.SCALE + SimulationConsts.WINDOW_WIDTH / 2
                y = (y - SimulationConsts.CAMERA_Y) * SimulationConsts.SCALE + SimulationConsts.WINDOW_HEIGHT / 2
                updated_points.append((x, y))

            pygame.draw.lines(window, self.color, False, updated_points, 2)

        screen_radius = max(2, self.r * SimulationConsts.RADIUS_SCALE)
        pygame.draw.circle(window, self.color, (x, y), screen_radius)

        if SimulationConsts.SHOW_DISTANCE and not self.is_sun:
            distance_text = font.render(f"{round(self.distance_to_sun / 1000, 1)}km", 1, SimulationConsts.WHITE)
            window.blit(
                distance_text,
                (x - distance_text.get_width() / 2, y - distance_text.get_height() / 2),
            )

    def compute_gravitational_forces(self, other):
        distance_x = other.x - self.x
        distance_y = other.y - self.y

        distance = math.sqrt(distance_x**2 + distance_y**2)

        if other.is_sun:
            self.distance_to_sun = distance

        force = G * self.m * other.m / distance**2
        theta = math.atan2(distance_y, distance_x)

        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force

        return force_x, force_y

    def update_position(self, planets): # euler method
        if self.is_sun:
            return

        total_fx = 0
        total_fy = 0

        for planet in planets:
            if self == planet:
                continue

            fx, fy = self.compute_gravitational_forces(planet)
            total_fx += fx
            total_fy += fy

        self.v_x += total_fx / self.m * SimulationConsts.TIMESTEP
        self.v_y += total_fy / self.m * SimulationConsts.TIMESTEP

        self.x += self.v_x * SimulationConsts.TIMESTEP
        self.y += self.v_y * SimulationConsts.TIMESTEP

        self.orbit.append((self.x, self.y))

    def update_position_prim(self, planets): # verlet method
        if self.is_sun:
            return
        
        self.v_x += 0.5 * self.a_x * SimulationConsts.TIMESTEP
        self.v_y += 0.5 * self.a_y * SimulationConsts.TIMESTEP
          
        self.x += self.v_x * SimulationConsts.TIMESTEP
        self.y += self.v_y * SimulationConsts.TIMESTEP
          
        self.a_x, self.a_y = self.get_total_accel(planets)
        
        self.v_x += 0.5 * self.a_x * SimulationConsts.TIMESTEP
        self.v_y += 0.5 * self.a_y * SimulationConsts.TIMESTEP
          
        self.orbit.append((self.x, self.y))

    def get_total_accel(self, planets):
        ax, ay = 0, 0
        for p in planets:
            if p == self: continue
            fx, fy = self.compute_gravitational_forces(p)
            ax += fx / self.m
            ay += fy / self.m
        return ax, ay