import math
from simulation_consts import SimulationConsts
from physical_consts import G


def compute_accelerations_at(positions, masses, sun):
    n = len(masses)
    ax = [0] * n
    ay = [0] * n

    for i in range(n):  # sun's gravity
        distance_x = sun.x - positions[i][0]
        distance_y = sun.y - positions[i][1]
        r2 = distance_x**2 + distance_y**2
        r = math.sqrt(r2)

        a = G * sun.m / r2
        ax[i] += a * distance_x / r
        ay[i] += a * distance_y / r

        for j in range(n):  # planets' gravity
            if i == j:
                continue
            distance_x = positions[j][0] - positions[i][0]
            distance_y = positions[j][1] - positions[i][1]
            r2 = distance_x**2 + distance_y**2
            r = math.sqrt(r2)

            a = G * masses[j] / r2
            ax[i] += a * distance_x / r
            ay[i] += a * distance_y / r

    return ax, ay


def compute_derivatives(state, masses, sun):
    n = len(masses)
    positions = []
    velocities = []

    for i in range(n):
        x, y, vx, vy = state[4 * i : 4 * i + 4]
        positions.append((x, y))
        velocities.append((vx, vy))

    ax, ay = compute_accelerations_at(positions, masses, sun)

    state_derivatives = []
    for i in range(n):
        state_derivatives.extend([velocities[i][0], velocities[i][1], ax[i], ay[i]])
    return state_derivatives


def compute_state_rk4(state, masses, sun):
    k1 = compute_derivatives(state, masses, sun)
    s2 = [state[i] + 0.5 * SimulationConsts.TIMESTEP * k1[i] for i in range(len(state))]
    k2 = compute_derivatives(s2, masses, sun)
    s3 = [state[i] + 0.5 * SimulationConsts.TIMESTEP * k2[i] for i in range(len(state))]
    k3 = compute_derivatives(s3, masses, sun)
    s4 = [state[i] + SimulationConsts.TIMESTEP * k3[i] for i in range(len(state))]
    k4 = compute_derivatives(s4, masses, sun)

    return [
        state[i] + ((SimulationConsts.TIMESTEP / 6) * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]))
        for i in range(len(state))
    ]


def compute_total_energy(planets):
    E_k = 0  # kinetic energy
    E_p = 0  # potential energy
    n = len(planets)

    for i, p in enumerate(planets):
        E_k += 0.5 * p.m * (p.v_x**2 + p.v_y**2)
        for j in range(i + 1, n):
            other = planets[j]
            distance_x = p.x - other.x
            distance_y = p.y - other.y
            r = math.sqrt(distance_x**2 + distance_y**2)
            E_p += -G * p.m * other.m / r

    return E_k + E_p
