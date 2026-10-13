# The Computer Language Benchmarks Game
# https://salsa.debian.org/benchmarksgame-team/benchmarksgame/
#
# originally by Kevin Carson
# modified by Tupteq, Fredrik Johansson, and Daniel Nanz
# modified by Maciej Fijalkowski
# modified by Abhinav Saini
# 2to3

from itertools import combinations
from math import sqrt
from time import perf_counter

import numpy as np
from numba import njit

PI = 3.14159265358979323
SOLAR_MASS = 4 * PI * PI
DAYS_PER_YEAR = 365.24

planets_idx = {"sun": 0, "jupiter": 1, "saturn": 2, "uranus": 3, "neptune": 4}

BODIES = np.array(
    [
        # Sun
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, SOLAR_MASS],
        # Jupiter
        [
            4.84143144246472090e00,
            -1.16032004402742839e00,
            -1.03622044471123109e-01,
            1.66007664274403694e-03 * DAYS_PER_YEAR,
            7.69901118419740425e-03 * DAYS_PER_YEAR,
            -6.90460016972063023e-05 * DAYS_PER_YEAR,
            9.54791938424326609e-04 * SOLAR_MASS,
        ],
        # Saturn
        [
            8.34336671824457987e00,
            4.12479856412430479e00,
            -4.03523417114321381e-01,
            -2.76742510726862411e-03 * DAYS_PER_YEAR,
            4.99852801234917238e-03 * DAYS_PER_YEAR,
            2.30417297573763929e-05 * DAYS_PER_YEAR,
            2.85885980666130812e-04 * SOLAR_MASS,
        ],
        # Uranus
        [
            1.28943695621391310e01,
            -1.51111514016986312e01,
            -2.23307578892655734e-01,
            2.96460137564761618e-03 * DAYS_PER_YEAR,
            2.37847173959480950e-03 * DAYS_PER_YEAR,
            -2.96589568540237556e-05 * DAYS_PER_YEAR,
            4.36624404335156298e-05 * SOLAR_MASS,
        ],
        # Neptune
        [
            1.53796971148509165e01,
            -2.59193146099879641e01,
            1.79258772950371181e-01,
            2.68067772490389322e-03 * DAYS_PER_YEAR,
            1.62824170038242295e-03 * DAYS_PER_YEAR,
            -9.51592254519715870e-05 * DAYS_PER_YEAR,
            5.15138902046611451e-05 * SOLAR_MASS,
        ],
    ]
)

PAIRS = np.array(list(combinations(planets_idx.values(), 2)))


@njit(cache=True, fastmath=True)
def advance(dt, n, bodies, pairs):

    for _ in range(n):
        for p in pairs:
            x1, y1, z1 = bodies[p[0], 0], bodies[p[0], 1], bodies[p[0], 2]
            x2, y2, z2 = bodies[p[1], 0], bodies[p[1], 1], bodies[p[1], 2]

            dx = x1 - x2
            dy = y1 - y2
            dz = z1 - z2
            dist_squared = dx * dx + dy * dy + dz * dz
            mag = dt / (dist_squared * sqrt(dist_squared))
            b1m = bodies[p[0], 6] * mag
            b2m = bodies[p[1], 6] * mag
            bodies[p[0], 3] -= dx * b2m
            bodies[p[0], 4] -= dy * b2m
            bodies[p[0], 5] -= dz * b2m
            bodies[p[1], 3] += dx * b1m
            bodies[p[1], 4] += dy * b1m
            bodies[p[1], 5] += dz * b1m
        for i in range(len(bodies)):
            bodies[i, 0] += dt * bodies[i, 3]
            bodies[i, 1] += dt * bodies[i, 4]
            bodies[i, 2] += dt * bodies[i, 5]


def report_energy(bodies=BODIES, pairs=PAIRS, e=0.0):

    for p in pairs:
        x1, y1, z1 = bodies[p[0], 0], bodies[p[0], 1], bodies[p[0], 2]
        x2, y2, z2 = bodies[p[1], 0], bodies[p[1], 1], bodies[p[1], 2]
        dx = x1 - x2
        dy = y1 - y2
        dz = z1 - z2
        e -= (bodies[p[0], 6] * bodies[p[1], 6]) / (
            (dx * dx + dy * dy + dz * dz) ** 0.5
        )
    for i in range(len(bodies)):
        e += (
            bodies[i, 6]
            * (
                bodies[i, 3] * bodies[i, 3]
                + bodies[i, 4] * bodies[i, 4]
                + bodies[i, 5] * bodies[i, 5]
            )
            / 2.0
        )
    print(f"{e:.9f}")


def offset_momentum(ref, bodies=BODIES, px=0.0, py=0.0, pz=0.0):

    for i in range(len(bodies)):
        px -= bodies[i, 3] * bodies[i, 6]
        py -= bodies[i, 4] * bodies[i, 6]
        pz -= bodies[i, 5] * bodies[i, 6]
    bodies[ref, 3] = px / bodies[ref, 6]
    bodies[ref, 4] = py / bodies[ref, 6]
    bodies[ref, 5] = pz / bodies[ref, 6]


def main(n, ref=0):
    offset_momentum(ref=ref)
    report_energy()
    advance(0.01, n, bodies=BODIES, pairs=PAIRS)
    report_energy()


if __name__ == "__main__":
    start_time = perf_counter()
    N = 50000000
    main(N)
    end_time = perf_counter()
    print(f"Execution time: {end_time - start_time:.6f} seconds")
