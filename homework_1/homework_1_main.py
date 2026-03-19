import random
import bisect
import statistics
import os
from datetime import datetime
import matplotlib.pyplot as plt

M = 32
SIZE = 2 ** M
N = 10000


def in_range(x, a, b):
    """Check if x is in (a, b] on the ring."""
    if a < b:
        return a < x <= b
    return x > a or x <= b


def create_topology():
    ids = sorted(random.sample(range(SIZE), N))
    nodes = []
    for i, nid in enumerate(ids):
        nodes.append({
            'id': nid,
            'pred': ids[(i - 1) % N],
            'succ': ids[(i + 1) % N],
            'finger': [],
        })
    # build finger tables
    for node in nodes:
        ft = []
        for i in range(M):
            target = (node['id'] + (1 << i)) % SIZE
            idx = bisect.bisect_left(ids, target)
            ft.append(ids[idx % N])
        node['finger'] = ft
    return nodes, ids


def map_keys_to_peers(ids):
    results = {'min': [], 'max': [], 'median': []}
    for mult in range(10, 101, 10):
        num_keys = mult * N
        count = [0] * N
        for _ in range(num_keys):
            k = random.randint(0, SIZE - 1)
            idx = bisect.bisect_left(ids, k)
            count[idx % N] += 1
        results['min'].append(min(count))
        results['max'].append(max(count))
        results['median'].append(statistics.median(count))
    return results


def chord_lookup(start_idx, key, nodes, ids):
    node = nodes[start_idx]
    if key == node['id']:
        return 0
    hops = 0
    while True:
        if in_range(key, node['id'], node['succ']):
            return hops + 1
        # find closest preceding finger
        best = node['succ']
        for f in reversed(node['finger']):
            if in_range(f, node['id'], key):
                best = f
                break
        hops += 1
        idx = bisect.bisect_left(ids, best)
        node = nodes[idx % N]
        if hops >= M:
            return hops


def compute_search_hops(nodes, ids):
    hops_count = [0] * M
    for i in range(N):
        for _ in range(100):
            k = random.randint(0, SIZE - 1)
            h = chord_lookup(i, k, nodes, ids)
            if h < M:
                hops_count[h] += 1
    total = sum(hops_count)
    return [c / total for c in hops_count]


def save_results(key_stats, hop_pdf, out_dir):
    path = os.path.join(out_dir, 'data.txt')
    with open(path, 'w', encoding='utf-8') as f:
        f.write('=== Key Distribution Data ===\n')
        f.write(f'{"numK":>10} {"Min":>8} {"Median":>8} {"Max":>8}\n')
        for i, mult in enumerate(range(10, 101, 10)):
            f.write(f'{mult * N:>10} {key_stats["min"][i]:>8} {key_stats["median"][i]:>8.1f} {key_stats["max"][i]:>8}\n')
        f.write('\n=== Hop Distribution Data ===\n')
        f.write(f'{"Hops":>6} {"Proportion":>12}\n')
        for h, p in enumerate(hop_pdf):
            if p > 0:
                f.write(f'{h:>6} {p:>12.6f}\n')
    print(f'Saved {path}')


def plot_results(key_stats, hop_pdf):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    out_dir = os.path.join(base_dir, 'result', timestamp)
    os.makedirs(out_dir, exist_ok=True)

    save_results(key_stats, hop_pdf, out_dir)

    x_keys = [mult * N for mult in range(10, 101, 10)]

    # Figure 1: key distribution
    fig1, ax1 = plt.subplots()
    medians = key_stats['median']
    mins = key_stats['min']
    maxs = key_stats['max']
    yerr_low = [m - lo for m, lo in zip(medians, mins)]
    yerr_high = [hi - m for hi, m in zip(maxs, medians)]
    ax1.errorbar(x_keys, medians, yerr=[yerr_low, yerr_high],
                 fmt='o-', capsize=4, color='black')
    ax1.set_xlabel('Total number of keys')
    ax1.set_ylabel('Number of keys per node')
    ax1.set_title('Key Distribution per Node')
    path1 = os.path.join(out_dir, 'key_distribution.png')
    fig1.savefig(path1, dpi=150, bbox_inches='tight')
    print(f'Saved {path1}')

    # Figure 2: hop distribution
    fig2, ax2 = plt.subplots()
    ax2.plot(range(M), hop_pdf, '-o', color='black')
    ax2.set_xlabel('Path length')
    ax2.set_ylabel('PDF')
    ax2.set_title('Search Hop Distribution')
    path2 = os.path.join(out_dir, 'hop_distribution.png')
    fig2.savefig(path2, dpi=150, bbox_inches='tight')
    print(f'Saved {path2}')


def main():
    print('Creating topology...')
    nodes, ids = create_topology()

    print('Mapping keys to peers...')
    key_stats = map_keys_to_peers(ids)

    print('\n=== Key Distribution Data ===')
    print(f'{"numK":>10} {"Min":>8} {"Median":>8} {"Max":>8}')
    for i, mult in enumerate(range(10, 101, 10)):
        print(f'{mult * N:>10} {key_stats["min"][i]:>8} {key_stats["median"][i]:>8.1f} {key_stats["max"][i]:>8}')

    print('\nComputing search hops (1M lookups)...')
    hop_pdf = compute_search_hops(nodes, ids)

    print('\n=== Hop Distribution Data ===')
    print(f'{"Hops":>6} {"Proportion":>12}')
    for h, p in enumerate(hop_pdf):
        if p > 0:
            print(f'{h:>6} {p:>12.6f}')

    print('\nPlotting results...')
    plot_results(key_stats, hop_pdf)
    print('Done!')


if __name__ == '__main__':
    main()
