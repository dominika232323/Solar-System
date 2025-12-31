from pygame_gui import UIManager
from pygame_gui.elements import UIButton, UIHorizontalSlider, UILabel

from simulation_consts import SimulationConsts
from planet import Planet
from physical_consts import *

import pygame
import pygame_gui


def initialize_planets():
    sun = Planet(SUN_MASS, SUN_RADIUS / 50, 0, 0, SimulationConsts.SUN_COLOR, True)
    mercury = Planet(MERCURY_MASS, MERCURY_RADIUS, MERCURY_DISTANCE, 0, SimulationConsts.MERCURY_COLOR)
    venus = Planet(VENUS_MASS, VENUS_RADIUS, VENUS_DISTANCE, 0, SimulationConsts.VENUS_COLOR)
    earth = Planet(EARTH_MASS, EARTH_RADIUS, EARTH_DISTANCE, 0, SimulationConsts.EARTH_COLOR)
    mars = Planet(MARS_MASS, MARS_RADIUS, MARS_DISTANCE, 0, SimulationConsts.MARS_COLOR)
    jupiter = Planet(JUPITER_MASS, JUPITER_RADIUS, JUPITER_DISTANCE, 0, SimulationConsts.JUPITER_COLOR)
    saturn = Planet(SATURN_MASS, SATURN_RADIUS, SATURN_DISTANCE, 0, SimulationConsts.SATURN_COLOR)
    uranus = Planet(URANUS_MASS, URANUS_RADIUS, URANUS_DISTANCE, 0, SimulationConsts.URANUS_COLOR)
    neptun = Planet(NEPTUN_MASS, NEPTUN_RADIUS, NEPTUN_DISTANCE, 0, SimulationConsts.NEPTUN_COLOR)
    
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
    pygame.init()
    WINDOW = pygame.display.set_mode((SimulationConsts.WINDOW_WIDTH, SimulationConsts.WINDOW_HEIGHT))
    pygame.display.set_caption("Solar System Simulation")
    FONT = pygame.font.SysFont("comicsans", 16)

    manager = pygame_gui.UIManager((SimulationConsts.WINDOW_WIDTH, SimulationConsts.WINDOW_HEIGHT))

    draw_orbit_checkbox, radius_label, radius_slider, scale_label, scale_slider, show_distance_checkbox, timestep_label, timestep_slider, reset_button = initialize_panel(manager)

    run_simulation = True
    clock = pygame.time.Clock() 
    
    planets = initialize_planets()
    
    while run_simulation:
        time_delta = clock.tick(60) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_simulation = False

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == draw_orbit_checkbox:
                    SimulationConsts.DRAW_ORBIT = not SimulationConsts.DRAW_ORBIT
                    draw_orbit_checkbox.set_text(
                        "Draw Orbit: ON" if SimulationConsts.DRAW_ORBIT else "Draw Orbit: OFF"
                    )
                elif event.ui_element == show_distance_checkbox:
                    SimulationConsts.SHOW_DISTANCE = not SimulationConsts.SHOW_DISTANCE
                    show_distance_checkbox.set_text(
                        "Show distance: ON" if SimulationConsts.DRAW_ORBIT else "Show distance: OFF"
                    )
                elif event.ui_element == reset_button:
                    SimulationConsts.SCALE = SimulationConsts.DEFAULT_SCALE
                    scale_slider.set_current_value(SimulationConsts.SCALE)

                    SimulationConsts.TIMESTEP = SimulationConsts.DEFAULT_TIMESTEP
                    timestep_slider.set_current_value(SimulationConsts.TIMESTEP)

                    SimulationConsts.RADIUS_SCALE = SimulationConsts.DEFAULT_RADIUS_SCALE
                    radius_slider.set_current_value(SimulationConsts.RADIUS_SCALE)

                    SimulationConsts.DRAW_ORBIT = True
                    draw_orbit_checkbox.set_text("Draw Orbit: ON")

                    SimulationConsts.SHOW_DISTANCE = True
                    show_distance_checkbox.set_text("Show distance: ON")

                    planets = initialize_planets()

            manager.process_events(event)

        SimulationConsts.SCALE = scale_slider.get_current_value()
        scale_label.set_text(f"SCALE: {SimulationConsts.SCALE:.2e}")

        SimulationConsts.TIMESTEP = timestep_slider.get_current_value()
        timestep_label.set_text(f"TIMESTEP: {SimulationConsts.TIMESTEP:.2e}")

        SimulationConsts.RADIUS_SCALE = radius_slider.get_current_value()
        radius_label.set_text(f"RADIUS_SCALE: {SimulationConsts.RADIUS_SCALE:.2e}")

        manager.update(time_delta)

        WINDOW.fill((0, 0, 0))

        for planet in planets:
            planet.update_position(planets)
            planet.draw(WINDOW, FONT)

        manager.draw_ui(WINDOW)
        pygame.display.update()

    pygame.quit()


def initialize_panel(manager: UIManager) -> tuple[
    UIButton, UILabel, UIHorizontalSlider, UILabel, UIHorizontalSlider, UIButton, UILabel, UIHorizontalSlider, UIButton]:

    panel_width = 260
    panel_height = 280
    panel = pygame_gui.elements.UIPanel(
        relative_rect=pygame.Rect((SimulationConsts.WINDOW_WIDTH - panel_width - 10, 10), (panel_width, panel_height)),
        starting_height=1,
        manager=manager
    )

    # SCALE slider
    scale_slider = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=pygame.Rect(10, 10, panel_width - 20, 20),
        start_value=SimulationConsts.SCALE,
        value_range=(SimulationConsts.SCALE * 0.1, SimulationConsts.SCALE * 10),
        manager=manager,
        container=panel
    )
    scale_label = pygame_gui.elements.UILabel(
        pygame.Rect(10, 30, panel_width - 20, 20),
        text=f"SCALE: {SimulationConsts.SCALE:.2e}",
        manager=manager, container=panel
    )

    # TIMESTEP slider
    timestep_slider = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=pygame.Rect(10, 70, panel_width - 20, 20),
        start_value=SimulationConsts.TIMESTEP,
        value_range=(1000, 3600 * 24 * 30),
        manager=manager,
        container=panel
    )
    timestep_label = pygame_gui.elements.UILabel(
        pygame.Rect(10, 90, panel_width - 20, 20),
        text=f"TIMESTEP: {SimulationConsts.TIMESTEP:.2e}",
        manager=manager,
        container=panel
    )

    # RADIUS_SCALE slider
    radius_slider = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=pygame.Rect(10, 130, panel_width - 20, 20),
        start_value=SimulationConsts.RADIUS_SCALE,
        value_range=(SimulationConsts.RADIUS_SCALE / 10, SimulationConsts.RADIUS_SCALE * 10),
        manager=manager,
        container=panel
    )
    radius_label = pygame_gui.elements.UILabel(
        pygame.Rect(10, 150, panel_width - 20, 20),
        text=f"RADIUS_SCALE: {SimulationConsts.RADIUS_SCALE:.2e}",
        manager=manager,
        container=panel
    )

    # DRAW_ORBIT checkbox
    draw_orbit_checkbox = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(10, 180, panel_width - 20, 30),
        text="DRAW_ORBIT",
        manager=manager,
        container=panel
    )

    # SHOW_DISTANCE checkbox
    show_distance_checkbox = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(10, 210, panel_width - 20, 30),
        text="SHOW_DISTANCE",
        manager=manager,
        container=panel
    )

    # RESET button
    reset_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(10, 240, panel_width - 20, 30),
        text="RESET",
        manager=manager,
        container=panel
    )

    return draw_orbit_checkbox, radius_label, radius_slider, scale_label, scale_slider, show_distance_checkbox, timestep_label, timestep_slider, reset_button


if __name__ == "__main__":
    main()
