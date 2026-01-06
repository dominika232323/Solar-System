from simulation_consts import SimulationConsts
from planet import Planet
from physical_consts import (
    SUN_MASS,
    SUN_RADIUS,
    MERCURY_MASS,
    MERCURY_RADIUS,
    MERCURY_DISTANCE,
    VENUS_MASS,
    VENUS_RADIUS,
    VENUS_DISTANCE,
    EARTH_MASS,
    EARTH_RADIUS,
    EARTH_DISTANCE,
    MARS_MASS,
    MARS_RADIUS,
    MARS_DISTANCE,
    JUPITER_MASS,
    JUPITER_RADIUS,
    JUPITER_DISTANCE,
    SATURN_MASS,
    SATURN_RADIUS,
    SATURN_DISTANCE,
    URANUS_DISTANCE,
    URANUS_RADIUS,
    URANUS_MASS,
    NEPTUN_MASS,
    NEPTUN_RADIUS,
    NEPTUN_DISTANCE,
    MERCURY_VELOCITY,
    VENUS_VELOCITY,
    EARTH_VELOCITY,
    MARS_VELOCITY,
    JUPITER_VELOCITY,
    SATURN_VELOCITY,
    URANUS_VELOCITY,
    NEPTUN_VELOCITY,
)
from nbody_physics import compute_state_rk4, compute_total_energy

import pygame
import pygame_gui
import math
import argparse


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
    parser = argparse.ArgumentParser(description="Solar System Simulation")
    parser.add_argument(
        "--method", choices=["euler", "verlet", "rk4"], default="euler", help="Numerical integration method"
    )
    args = parser.parse_args()
    SimulationConsts.INTEGRATION_METHOD = args.method

    pygame.init()
    WINDOW = pygame.display.set_mode((SimulationConsts.WINDOW_WIDTH, SimulationConsts.WINDOW_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Solar System Simulation")
    FONT = pygame.font.SysFont("comicsans", 16)

    manager = pygame_gui.UIManager((SimulationConsts.WINDOW_WIDTH, SimulationConsts.WINDOW_HEIGHT))

    (
        panel,
        draw_orbit_checkbox,
        radius_label,
        radius_slider,
        scale_label,
        scale_slider,
        show_distance_checkbox,
        timestep_label,
        timestep_slider,
        reset_button,
    ) = initialize_panel(manager)

    panel.set_relative_position((SimulationConsts.WINDOW_WIDTH - panel.rect.width - 10, 10))
    run_simulation = True
    clock = pygame.time.Clock()

    planets = initialize_planets()

    if SimulationConsts.INTEGRATION_METHOD == "verlet":
        for p in planets:
            if not p.is_sun:
                p.a_x, p.a_y = p.compute_accelerations(planets)

    while run_simulation:
        time_delta = clock.tick(60) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_simulation = False

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == draw_orbit_checkbox:
                    SimulationConsts.DRAW_ORBIT = not SimulationConsts.DRAW_ORBIT
                    draw_orbit_checkbox.set_text("Draw Orbit: ON" if SimulationConsts.DRAW_ORBIT else "Draw Orbit: OFF")
                elif event.ui_element == show_distance_checkbox:
                    SimulationConsts.SHOW_DISTANCE = not SimulationConsts.SHOW_DISTANCE
                    show_distance_checkbox.set_text(
                        "Show distance: ON" if SimulationConsts.SHOW_DISTANCE else "Show distance: OFF"
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

                    SimulationConsts.CAMERA_X = 0
                    SimulationConsts.CAMERA_Y = 0

                    planets = initialize_planets()

            if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                if event.ui_element == scale_slider:
                    apply_zoom(event.value, (SimulationConsts.WINDOW_WIDTH // 2, SimulationConsts.WINDOW_HEIGHT // 2))

            if event.type == pygame.MOUSEWHEEL:
                factor = SimulationConsts.ZOOM_FACTOR if event.y > 0 else 1 / SimulationConsts.ZOOM_FACTOR
                apply_zoom(SimulationConsts.SCALE * factor, pygame.mouse.get_pos())

            if event.type == pygame.VIDEORESIZE:
                SimulationConsts.WINDOW_WIDTH = event.w
                SimulationConsts.WINDOW_HEIGHT = event.h

                WINDOW = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                manager.set_window_resolution((event.w, event.h))
                panel.set_relative_position((SimulationConsts.WINDOW_WIDTH - panel.rect.width - 10, 10))

            manager.process_events(event)

        keys = pygame.key.get_pressed()
        speed = SimulationConsts.CAMERA_SPEED * math.log10(SimulationConsts.SCALE * 1e9)

        if keys[pygame.K_LEFT]:
            SimulationConsts.CAMERA_X -= speed
        if keys[pygame.K_RIGHT]:
            SimulationConsts.CAMERA_X += speed
        if keys[pygame.K_UP]:
            SimulationConsts.CAMERA_Y -= speed
        if keys[pygame.K_DOWN]:
            SimulationConsts.CAMERA_Y += speed

        scale_slider.set_current_value(SimulationConsts.SCALE)
        scale_label.set_text(f"SCALE: {SimulationConsts.SCALE:.2e}")

        SimulationConsts.TIMESTEP = timestep_slider.get_current_value()
        timestep_label.set_text(f"TIMESTEP: {SimulationConsts.TIMESTEP:.2e}")

        SimulationConsts.RADIUS_SCALE = radius_slider.get_current_value()
        radius_label.set_text(f"RADIUS_SCALE: {SimulationConsts.RADIUS_SCALE:.2e}")

        manager.update(time_delta)

        WINDOW.fill((0, 0, 0))

        if SimulationConsts.INTEGRATION_METHOD == "rk4":
            sun = planets[0]
            state = []
            masses = []
            for p in planets[1:]:
                state.extend([p.x, p.y, p.v_x, p.v_y])
                masses.append(p.m)

            state = compute_state_rk4(state, masses, sun)

            for i, p in enumerate(planets[1:]):  # update positions runge-kutta 4th order
                p.x, p.y, p.v_x, p.v_y = state[4 * i : 4 * i + 4]
                p.orbit.append((p.x, p.y))

            sun.draw(WINDOW, FONT)
            for planet in planets[1:]:  # draw and update distance to sun
                planet.draw(WINDOW, FONT)
                distance_x = sun.x - planet.x
                distance_y = sun.y - planet.y
                planet.distance_to_sun = math.sqrt(distance_x**2 + distance_y**2)

        else:
            for planet in planets:
                if SimulationConsts.INTEGRATION_METHOD == "verlet":
                    planet.update_position_verlet(planets)
                else:
                    planet.update_position_euler(planets)
                planet.draw(WINDOW, FONT)

        total_energy = compute_total_energy(planets)
        energy_text = FONT.render(f"Total Energy: {total_energy:.3e} J", 1, SimulationConsts.WHITE)
        WINDOW.blit(energy_text, (10, SimulationConsts.WINDOW_HEIGHT - 30))

        manager.draw_ui(WINDOW)
        pygame.display.update()

    pygame.quit()


def initialize_panel(manager):
    panel_width = 260
    panel_height = 280
    panel = pygame_gui.elements.UIPanel(
        relative_rect=pygame.Rect(
            (SimulationConsts.WINDOW_WIDTH - panel_width - 10, 10),
            (panel_width, panel_height),
        ),
        starting_height=1,
        manager=manager,
    )

    # SCALE slider
    scale_slider = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=pygame.Rect(10, 10, panel_width - 20, 20),
        start_value=SimulationConsts.SCALE,
        value_range=(SimulationConsts.MIN_SCALE, SimulationConsts.MAX_SCALE),
        manager=manager,
        container=panel,
    )
    scale_label = pygame_gui.elements.UILabel(
        pygame.Rect(10, 30, panel_width - 20, 20),
        text=f"SCALE: {SimulationConsts.SCALE:.2e}",
        manager=manager,
        container=panel,
    )

    # TIMESTEP slider
    timestep_slider = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=pygame.Rect(10, 70, panel_width - 20, 20),
        start_value=SimulationConsts.TIMESTEP,
        value_range=(1000, 3600 * 24 * 30),
        manager=manager,
        container=panel,
    )
    timestep_label = pygame_gui.elements.UILabel(
        pygame.Rect(10, 90, panel_width - 20, 20),
        text=f"TIMESTEP: {SimulationConsts.TIMESTEP:.2e}",
        manager=manager,
        container=panel,
    )

    # RADIUS_SCALE slider
    radius_slider = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=pygame.Rect(10, 130, panel_width - 20, 20),
        start_value=SimulationConsts.RADIUS_SCALE,
        value_range=(
            SimulationConsts.RADIUS_SCALE / 10,
            SimulationConsts.RADIUS_SCALE * 10,
        ),
        manager=manager,
        container=panel,
    )
    radius_label = pygame_gui.elements.UILabel(
        pygame.Rect(10, 150, panel_width - 20, 20),
        text=f"RADIUS_SCALE: {SimulationConsts.RADIUS_SCALE:.2e}",
        manager=manager,
        container=panel,
    )

    # DRAW_ORBIT checkbox
    draw_orbit_checkbox = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(10, 180, panel_width - 20, 30),
        text="DRAW_ORBIT",
        manager=manager,
        container=panel,
    )

    # SHOW_DISTANCE checkbox
    show_distance_checkbox = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(10, 210, panel_width - 20, 30),
        text="SHOW_DISTANCE",
        manager=manager,
        container=panel,
    )

    # RESET button
    reset_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(10, 240, panel_width - 20, 30),
        text="RESET",
        manager=manager,
        container=panel,
    )

    return (
        panel,
        draw_orbit_checkbox,
        radius_label,
        radius_slider,
        scale_label,
        scale_slider,
        show_distance_checkbox,
        timestep_label,
        timestep_slider,
        reset_button,
    )


def apply_zoom(new_scale, mouse_pos):
    old_scale = SimulationConsts.SCALE
    new_scale = max(SimulationConsts.MIN_SCALE, min(new_scale, SimulationConsts.MAX_SCALE))

    mx, my = mouse_pos

    # getting real coordinates, opposite of drawing
    world_x = (mx - SimulationConsts.WINDOW_WIDTH / 2) / old_scale + SimulationConsts.CAMERA_X
    world_y = (my - SimulationConsts.WINDOW_HEIGHT / 2) / old_scale + SimulationConsts.CAMERA_Y

    SimulationConsts.SCALE = new_scale
    # maintaining point's position
    SimulationConsts.CAMERA_X += (world_x - SimulationConsts.CAMERA_X) * (1 - old_scale / new_scale)
    SimulationConsts.CAMERA_Y += (world_y - SimulationConsts.CAMERA_Y) * (1 - old_scale / new_scale)


if __name__ == "__main__":
    main()
