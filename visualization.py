import matplotlib.pyplot as plt
from random import randint
from geometry import is_clockwise
from datasets import dataset_A, dataset_B, dataset_C, dataset_D


def test_dataset(dataset_generation_function, dataset_sizes):
    num_plots = len(dataset_sizes)
    fig, axes = plt.subplots(1, num_plots, figsize=(5 * num_plots, 5), constrained_layout=True)
    
    if num_plots == 1:
        axes = [axes]

    for i, size in enumerate(dataset_sizes):
        data = dataset_generation_function(size)
        x, y = zip(*data)
            
        axes[i].scatter(x, y, color='blue', s=5)
        axes[i].set_title(f"Size: {size}")
        axes[i].set_aspect('equal') 

    plt.show()


def test_algorithm(convex_hull_algorithm):
    fig, axes = plt.subplots(2, 2, figsize=(12, 12))
    axes = axes.flatten()

    datasets = [generator(randint(4, 1_000)) for generator in (dataset_A, dataset_B, dataset_C, dataset_D)]
    titles = ["Dataset A", "Dataset B", "Dataset C", "Dataset D"]
    
    for idx, (points, title) in enumerate(zip(datasets, titles)):
        ax = axes[idx]
        hull = convex_hull_algorithm(points)

        if idx == 0:
            assert len(hull) == 4, f"Dataset A should have 4 hull vertices, got {len(hull)}"
        elif idx == 3:
            assert len(hull) == len(points), f"Dataset D should have all points on hull"

        for i in range(len(hull) - 2):
            assert not is_clockwise(hull[i], hull[i+1], hull[i+2]), \
                f"Hull vertices not in counter-clockwise order at index {i}"
        
        x_coords, y_coords = zip(*points)
        ax.scatter(x_coords, y_coords, color='blue', s=5, label='Points', zorder=1)
        
        hull_x, hull_y = zip(*hull)
        ax.scatter(hull_x, hull_y, color='green', s=15, label='Hull vertices', zorder=3)
        ax.plot(list(hull_x) + [hull_x[0]], list(hull_y) + [hull_y[0]], 
                color='red', linewidth=1, linestyle='-', label='Hull', zorder=2)
        
        ax.set_aspect('equal')
        ax.set_title(title)
        ax.legend()

    print("TESTS FOR DATASETS A & D AND COUNTERCLOCKWISE HULL ORIENTATION PASSED")
    plt.tight_layout()
    plt.show()


def visualize_windmill_steps(points, num_frames=None):
    n = len(points)
    if n < 3:
        print("Need at least 3 points")
        return
    
    hull_sequence = []
    pivot = min(points, key=lambda p: p[0])
    start_pivot = pivot
    
    while True:
        hull_sequence.append(pivot)
        candidate = points[0] if points[0] != pivot else points[1]
        for p in points:
            if p == pivot:
                continue
            if is_clockwise(pivot, candidate, p):
                candidate = p
        pivot = candidate
        if pivot == start_pivot:
            break
    
    frames_to_show = num_frames if num_frames else len(hull_sequence) + 1
    
    grid_size = int((len(hull_sequence) + 1) ** 0.5) + 1
    fig, axes = plt.subplots(grid_size, grid_size, figsize=(15, 15))
    axes = axes.flatten()
    
    x_coords, y_coords = zip(*points)
    x_range = max(x_coords) - min(x_coords)
    y_range = max(y_coords) - min(y_coords)
    margin = 0.2
    
    for frame in range(min(frames_to_show, len(hull_sequence) + 1)):
        ax = axes[frame]
        
        ax.scatter(x_coords, y_coords, color='blue', s=3, zorder=3)
        
        if frame == 0:
            current_pivot = hull_sequence[0]
            ax.axvline(current_pivot[0], color='red', linewidth=2, alpha=0.7)
            ax.scatter([current_pivot[0]], [current_pivot[1]], color='green', s=150, marker='*', zorder=4)
        else:
            current_pivot = hull_sequence[frame - 1]
            next_pivot = hull_sequence[frame % len(hull_sequence)]
            
            if abs(current_pivot[0] - next_pivot[0]) < 1e-10:
                ax.axvline(current_pivot[0], color='red', linewidth=2, alpha=0.7)
            else:
                slope = (next_pivot[1] - current_pivot[1]) / (next_pivot[0] - current_pivot[0])
                x_min, x_max = min(x_coords) - margin * x_range, max(x_coords) + margin * x_range
                y_vals = [current_pivot[1] + slope * (x - current_pivot[0]) for x in [x_min, x_max]]
                ax.plot([x_min, x_max], y_vals, 'r-', linewidth=2, alpha=0.7)
            
            ax.scatter([current_pivot[0]], [current_pivot[1]], color='green', s=150, marker='*', zorder=4)
            
            hull_so_far = hull_sequence[:frame]
            hull_x, hull_y = zip(*hull_so_far)
            ax.plot(hull_x, hull_y, 'orange', linewidth=2, linestyle='--', alpha=0.7)
        
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)
        ax.set_xlim(min(x_coords) - margin * x_range, max(x_coords) + margin * x_range)
        ax.set_ylim(min(y_coords) - margin * y_range, max(y_coords) + margin * y_range)
        ax.set_title(f'Step {frame}')
    
    for i in range(min(frames_to_show, len(hull_sequence) + 1), len(axes)):
        axes[i].axis('off')
    
    plt.tight_layout()
    plt.show()