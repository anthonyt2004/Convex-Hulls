from geometry import is_clockwise, are_collinear, get_rotation_angle


def _dist2(a, b):
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    return dx * dx + dy * dy


def compute_convex_hull_3(points):
    n = len(points)
    if n < 3:
        return points

    convex_hull = []
    pivot = min(points, key=lambda p: p[0])

    while True:
        convex_hull.append(pivot)
        candidate = points[0] if points[0] != pivot else points[1]

        for p in points:
            if p == pivot:
                continue

            if is_clockwise(pivot, candidate, p):
                candidate = p
            elif are_collinear(pivot, candidate, p) and _dist2(pivot, p) > _dist2(pivot, candidate):
                candidate = p

        pivot = candidate
        if pivot == convex_hull[0]:
            break

    return convex_hull


def compute_convex_hull_4(points):
    convex_hull = []
    pivot = min(points, key=lambda p: p[0])
    windmill_vector = (0, -1)

    while True:
        convex_hull.append(pivot)
        candidate = points[0] if points[0] != pivot else points[1]

        for p in points:
            if p == pivot:
                continue

            candidate_vector = (candidate[0] - pivot[0], candidate[1] - pivot[1])
            p_vector = (p[0] - pivot[0], p[1] - pivot[1])
            
            candidate_angle = get_rotation_angle(windmill_vector, candidate_vector)
            p_angle = get_rotation_angle(windmill_vector, p_vector)
            if p_angle < candidate_angle:
                candidate = p
            elif p_angle == candidate_angle and _dist2(pivot, p) > _dist2(pivot, candidate):
                candidate = p

        windmill_vector = (candidate[0] - pivot[0], candidate[1] - pivot[1])
        pivot = candidate
        if pivot == convex_hull[0]:
            break

    return convex_hull
