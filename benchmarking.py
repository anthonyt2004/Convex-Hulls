from time import perf_counter_ns
from geometry import rotate_hull
from tqdm.auto import tqdm
import gc



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
