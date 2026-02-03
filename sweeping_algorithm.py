from geometry import is_clockwise, sort_points


def compute_upper_hull_1(sorted_points):
    chain = [sorted_points[0], sorted_points[1]]

    for point in sorted_points[2:]:
        while len(chain) > 1 and not is_clockwise(chain[-2], chain[-1], point):
            chain.pop()
        chain.append(point)

    chain.reverse()
    return chain


def compute_lower_hull_1(sorted_points):
    inverted_points = [(p[0], -p[1]) for p in sorted_points]
    lower_hull = compute_upper_hull_1(inverted_points)
    lower_hull = [(p[0], -p[1]) for p in lower_hull]
    lower_hull.reverse()
    return lower_hull


def compute_convex_hull_1(points):
    sorted_points = sort_points(points)
    convex_hull = compute_upper_hull_1(sorted_points)
    lower_hull = compute_lower_hull_1(sorted_points)[1:-1]
    convex_hull.extend(lower_hull)
    return convex_hull
