from time import perf_counter_ns
from tqdm.auto import tqdm
import gc
import matplotlib.pyplot as plt


def get_benchmarks(dataset_sizes, convex_hull_algorithm, dataset_generation_functions):
    ratios = [[] for _ in range(len(dataset_generation_functions))]
    times = [[] for _ in range(len(dataset_generation_functions))]
    gc.collect()

    for n in tqdm(dataset_sizes, desc="Benchmarking"):
        for j, gen_func in enumerate(dataset_generation_functions):
            data = gen_func(n)
            gc.collect()

            start = perf_counter_ns()
            convex_hull_algorithm(data)
            duration = perf_counter_ns() - start
            
            times[j].append(duration)
            ratios[j].append(duration / n)

    return ratios, times


def smooth_curve(curve, window_len=10):
    smooth = []
    for i in range(len(curve)):
        window = curve[max(0, i - window_len // 2):min(i + 1 + window_len // 2, len(curve))]
        med = sorted(window)[len(window) // 2]
        smooth.append(med)
    return smooth


def smooth_benchmarks(benchmarks, window_len=10, strip=0):
    return [smooth_curve(benchmark[strip:], window_len) for benchmark in benchmarks]


def plot_benchmarks(dataset_sizes, benchmarks, y_labels):
    num_plots = len(benchmarks)
    fig, axes = plt.subplots(num_plots, 1, figsize=(10, 4 * num_plots))

    if num_plots == 1:
        axes = [axes]

    for i, (data, label) in enumerate(zip(benchmarks, y_labels)):
        axes[i].plot(dataset_sizes, data)
        axes[i].set_xlabel("Dataset size (n)")
        axes[i].set_ylabel(label)
        axes[i].set_title(f"Benchmark: {label}")
        axes[i].grid(True, linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.show()


def plot_smooth_benchmarks(dataset_sizes, benchmarks, y_labels, window_len=10, strip=0):
    plot_benchmarks(
        dataset_sizes[strip:], 
        smooth_benchmarks(benchmarks, window_len, strip), 
        y_labels
    )
