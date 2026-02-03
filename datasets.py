from random import random, shuffle
from math import pi, sqrt, cos, sin
import cmath


def rotate(point, pivot, angle):
    z = complex(*point)
    w = complex(*pivot)
    z_r = cmath.exp(1j * angle) * (z - w) + w
    return z_r.real, z_r.imag


def dataset_A(n):
    if n < 4:
        raise ValueError('n should be greater than or equal to 4.')

    A = dataset_B(n - 4)
    for corner in ((0, 0), (0, 1), (1, 0), (1, 1)):
        A.append(corner)

    pivot = (0.5, 0.5)
    angle = 2 * pi * random()
    A = [rotate(p, pivot, angle) for p in A]
    shuffle(A)
    return A


def dataset_B(n):
    return [(random(), random()) for _ in range(n)]


def dataset_C(n):
    C = []
    for _ in range(n):
        r = sqrt(random())
        a = random() * 2 * pi
        C.append((r * cos(a), r * sin(a)))
    return C


def dataset_D(n):
    D = []
    for _ in range(n):
        a = random() * 2 * pi
        D.append((cos(a), sin(a)))
    return D
