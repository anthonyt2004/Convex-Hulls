from geometry import separator_x, find_upper_basis


def compute_upper_hull_2(points):
    if len(points) <= 1:
        return points

    if len(points) == 2:
        return sorted(points)[::-1]

    x_m = separator_x(points)
    l, r = find_upper_basis(x_m, points)

    left_subproblem = [p for p in points if p[0] <= l[0]]
    right_subproblem = [p for p in points if p[0] >= r[0]]

    hull_left = compute_upper_hull_2(left_subproblem)
    upper_hull = compute_upper_hull_2(right_subproblem)
    upper_hull.extend(hull_left)

    return upper_hull


def compute_lower_hull_2(points):
    inverted_points = [(p[0], -p[1]) for p in points]
    lower_hull = compute_upper_hull_2(inverted_points)
    lower_hull = [(p[0], -p[1]) for p in lower_hull]
    lower_hull.reverse()
    return lower_hull


def compute_convex_hull_2(points):
    convex_hull = compute_upper_hull_2(points)
    lower_hull = compute_lower_hull_2(points)[1:-1]
    convex_hull.extend(lower_hull)
    return convex_hull