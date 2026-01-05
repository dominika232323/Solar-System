from physical_consts import AU


class SimulationConsts:
    WINDOW_WIDTH, WINDOW_HEIGHT = 800, 800

    DEFAULT_SCALE = 390 / (30 * AU)
    DEFAULT_RADIUS_SCALE = 3e-7
    DEFAULT_TIMESTEP = 3600 * 24  # 1 day in seconds

    SCALE = 390 / (30 * AU)
    MIN_SCALE = SCALE * 0.1
    MAX_SCALE = SCALE * 10
    RADIUS_SCALE = 3e-7
    TIMESTEP = 3600 * 24  # 1 day in seconds

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

    DRAW_ORBIT = True
    SHOW_DISTANCE = True

    CAMERA_X = 0.0
    CAMERA_Y = 0.0

    CAMERA_SPEED = 5e9
    ZOOM_FACTOR = 1.1

    INTEGRATION_METHOD = "euler"
