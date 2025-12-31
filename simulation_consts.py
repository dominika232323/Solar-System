from physical_consts import AU


class SimulationConsts:
    WINDOW_WIDTH, WINDOW_HEIGHT =  800, 800

    SCALE = 390 / (30 * AU)
    RADIUS_SCALE = 3e-7
    TIMESTEP = 3600*24 # 1 day in seconds

    SUN_COLOR = (255, 255, 153)
    MERCURY_COLOR = (128, 128, 128)
    VENUS_COLOR = (255, 200, 150)
    EARTH_COLOR = (0, 100, 200)
    MARS_COLOR = (200, 80, 40)
    JUPITER_COLOR = (216, 202, 157)
    SATURN_COLOR = (250, 213, 165)
    URANUS_COLOR = (173, 216, 230)
    NEPTUN_COLOR = (0, 50, 150)

    WHITE = (255, 255, 255)
