from random import shuffle, choice
from math import pi, atan2


def is_clockwise(A, B, C):
    AB = B[0] - A[0], B[1] - A[1]
    AC = C[0] - A[0], C[1] - A[1]
    cross_prod = AB[0]*AC[1] - AB[1]*AC[0]
    return cross_prod < 0


def sort_points(points):
    return sorted(points)


def select(arr, k):
        if len(arr) <= 5:
            return sorted(arr)[k]

        groups = [arr[i:i+5] for i in range(0, len(arr), 5)]
        medians = []
        for group in groups:
            sorted_group = sorted(group)
            medians.append(sorted_group[len(sorted_group) // 2])

        pivot = select(medians, len(medians) // 2)
        lows = [p for p in arr if p < pivot]
        highs = [p for p in arr if p > pivot]

        if k < len(lows):
            return select(lows, k)
        elif k == len(lows):
            return pivot
        else:
            return select(highs, k - len(lows) - 1)


def separator_x(points):
    x_coords = list(map(lambda x: x[0], points))

    upper_median = select(x_coords, len(x_coords) // 2)

    if len(x_coords) % 2 == 0:
        lower_median = select(x_coords, (len(x_coords) - 1) // 2)
    else:
        lower_median = select(x_coords, len(x_coords) // 2 - 1)

    return (upper_median + lower_median) / 2


def is_above(p1, p2, target):
    if p1[0] > p2[0]:
        return is_clockwise(p2, target, p1)
    return is_clockwise(p1, target, p2)


def find_upper_basis(x_m, points):
    left = [p for p in points if p[0] < x_m]
    right = [p for p in points if p[0] > x_m]

    p1 = choice(left)
    p2 = choice(right)
    basis = (p1, p2)

    remaining_points = [p for p in points if p != p1 and p != p2]
    shuffle(remaining_points)

    P_k_left = [p1]
    P_k_right = [p2]

    for p_k in remaining_points:
        if is_above(basis[0], basis[1], p_k):
            look_in = P_k_right if p_k[0] < x_m else P_k_left
            best_partner = look_in[0]

            for candidate in look_in:
                if candidate == p_k:
                    continue
                if is_above(p_k, best_partner, candidate):
                    best_partner = candidate
            
            basis = (p_k, best_partner)

        if p_k[0] < x_m:
            P_k_left.append(p_k)
        else:
            P_k_right.append(p_k)

    return sorted(basis)


def get_rotation_angle(vec1, vec2):
    source_angle = atan2(vec1[1], vec1[0])
    dest_angle = atan2(vec2[1], vec2[0])
    angle_diff = dest_angle - source_angle

    if angle_diff < 0:
        angle_diff += 2 * pi
    
    return angle_diff