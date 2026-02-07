# Convex Hulls

Implementations and experiments for computing 2D convex hulls, plus dataset generators,
visualization helpers, and benchmarking utilities.

## Purpose
This repository contains the solution for the assignment described in `project.pdf`, with the
analysis, experiments, and results presented in `notebook.ipynb`. The notebook is the intended
entry point for evaluation.

## Requirements
Core modules only use the Python standard library. Visualization and benchmarking require:
- `matplotlib`
- `tqdm`

The notebook additionally expects Jupyter.

## File Map
- [`notebook.ipynb`](./notebook.ipynb): full analysis, experiments, and results (primary entry point)
- [`datasets.py`](./datasets.py): dataset generators
- [`geometry.py`](./geometry.py): geometric utilities (orientation tests, median selection, etc.)
- [`sweeping_algorithm.py`](./sweeping_algorithm.py): sweeping convex hull
- [`output_sensitive_algorithm.py`](./output_sensitive_algorithm.py): output‑sensitive convex hull
- [`windmill_algorithm.py`](./windmill_algorithm.py): windmill / gift‑wrapping approaches
- [`visualization.py`](./visualization.py): plotting + correctness checks
- [`benchmarking.py`](./benchmarking.py): timing and plotting benchmarks

## Module Details
### `datasets.py`
Point generators used in experiments and benchmarks.
- `dataset_A(n)`: random points + the 4 corners of a unit square, rotated.
- `dataset_B(n)`: uniform random points in the unit square.
- `dataset_C(n)`: uniform random points in the unit disk.
- `dataset_D(n)`: points on the unit circle.

### `geometry.py`
Core geometric helpers used by the algorithms.
- `is_clockwise(A, B, C)`: orientation test for turn direction.
- `are_collinear(A, B, C)`: checks if three points are collinear.
- `sort_points(points)`: lexicographic sort of points.
- `select(arr, k)`: deterministic linear-time selection (median of medians).
- `separator_x(points)`: x-coordinate of the vertical separator such that half the points (rounded down) are strictly to the left and half the points (rounded up) are strictly to the right.
- `is_above(p1, p2, target)`: relative position test for upper hull routines.
- `find_upper_basis(x_m, points)`: finds a supporting upper line (basis) around the separator.
- `get_rotation_angle(vec1, vec2)`: positive rotation from `vec1` to `vec2` in `[0, 2π)`.

### `sweeping_algorithm.py`
Monotonic chain (sweeping) hull construction.
- `compute_convex_hull_1(points)`: full convex hull (uses upper/lower chain helpers internally).

### `output_sensitive_algorithm.py`
Output‑sensitive upper hull construction with recursion.
- `compute_convex_hull_2(points)`: full convex hull (recursive upper hull + symmetric lower hull).

### `windmill_algorithm.py`
Gift‑wrapping / windmill process implementations.
- `compute_convex_hull_3(points)`: classic orientation‑based gift wrapping.
- `compute_convex_hull_4(points)`: angle‑based windmill variant.

### `visualization.py`
Helpers to plot datasets, hulls, and windmill steps for explanation and checks.

### `benchmarking.py`
Helpers to time algorithms and plot performance curves.
