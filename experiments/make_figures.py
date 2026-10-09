"""
Builds the report figures from experiments/results/*.csv into report/figures/.

Usage (from the repository root, needs matplotlib):  python3 experiments/make_figures.py
"""

import csv
import os
import statistics as st
from collections import defaultdict

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS = os.path.join(ROOT, 'experiments', 'results')
FIGURES = os.path.join(ROOT, 'report', 'figures')

# categorical slots in fixed order (validated palette)
SERIES = ['#2a78d6', '#eb6834', '#1baf7a', '#eda100']
INK = '#0b0b0b'
MUTED = '#52514e'
GRID = '#e4e3df'

plt.rcParams.update({
    'font.size': 8, 'axes.titlesize': 8.5, 'axes.labelsize': 8, 'legend.fontsize': 7,
    'xtick.labelsize': 7, 'ytick.labelsize': 7, 'axes.edgecolor': MUTED, 'axes.labelcolor': INK,
    'xtick.color': MUTED, 'ytick.color': MUTED, 'axes.spines.top': False, 'axes.spines.right': False,
    'axes.grid': True, 'grid.color': GRID, 'grid.linewidth': 0.6, 'axes.axisbelow': True,
    'legend.frameon': False, 'pdf.fonttype': 42,
})


def load(name):
    with open(os.path.join(RESULTS, name)) as f:
        return list(csv.DictReader(f))


def representations():
    rows = load('part1_representations.csv')
    groups = defaultdict(list)
    for row in rows:
        groups[(row['structure'], int(row['cells']))].append(row)

    def series(structure, column):
        keys = sorted(k for k in groups if k[0] == structure)
        return [k[1] for k in keys], [st.mean(float(r[column]) for r in groups[k]) for k in keys]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6.6, 2.9))
    names = {'array': 'Array', 'adjlist': 'Adjacency list', 'adjmat': 'Adjacency matrix'}
    short = {'adjlist': 'List', 'adjmat': 'Matrix'}
    colors = {'array': SERIES[2], 'adjlist': SERIES[0], 'adjmat': SERIES[1]}

    for structure in ['adjlist', 'adjmat']:
        x, y = series(structure, 'neighbours_us')
        ax1.plot(x, y, color=colors[structure], lw=2, marker='o', ms=4, label=f'{short[structure]}: neighbours()')
        x, y = series(structure, 'update_wall_us')
        ax1.plot(x, y, color=colors[structure], lw=2, ls='--', marker='s', ms=4, label=f'{short[structure]}: updateWall()')
    ax1.set(xscale='log', yscale='log', xlabel='Cells in maze', ylabel='Mean time per call (µs)',
            title='(a) Cost per graph operation')
    # legends sit below each panel so they never cover the data
    ax1.legend(loc='upper center', bbox_to_anchor=(0.5, -0.24), ncol=2, columnspacing=1.0, handlelength=2.2)

    for structure in ['array', 'adjlist', 'adjmat']:
        x, y = series(structure, 'memory_mb')
        ax2.plot(x, y, color=colors[structure], lw=2, marker='o', ms=4, label=names[structure])
    ax2.set(xscale='log', yscale='log', xlabel='Cells in maze', ylabel='Peak memory (MB)',
            title='(b) Memory of the initialised maze')
    ax2.legend(loc='upper center', bbox_to_anchor=(0.5, -0.24), ncol=3, columnspacing=1.0)

    fig.tight_layout(w_pad=3)
    fig.savefig(os.path.join(FIGURES, 'representations.pdf'), bbox_inches='tight', pad_inches=0.02)


def explored():
    rows = [r for r in load('part2_solvers.csv') if r['setting'] == 'uniform 4x20x20']
    generators = [('recur', 'Recursive backtracking'), ('prim', 'Prim'), ('wilson', 'Wilson'), ('taskD', 'Adversarial (ours)')]
    solvers = [('recur', 'Random DFS'), ('wall', 'Wall follower'), ('pledge', 'Pledge'), ('taskC', 'Multi-source BFS')]
    cells = int(rows[0]['cells'])

    fig, ax = plt.subplots(figsize=(6.6, 2.5))
    width = 0.19
    for i, (gen, label) in enumerate(generators):
        means, sds = [], []
        for (solver, _) in solvers:
            values = [int(r['explored']) for r in rows if r['generator'] == gen and r['solver'] == solver]
            means.append(st.mean(values))
            sds.append(st.stdev(values))
        xs = [j + (i - 1.5) * (width + 0.01) for j in range(len(solvers))]
        ax.bar(xs, means, width, color=SERIES[i], label=label, yerr=sds,
               error_kw=dict(ecolor=MUTED, elinewidth=0.8, capsize=1.5))
    ax.axhline(cells, color=MUTED, lw=0.8, ls=':')
    ax.text(len(solvers) - 0.5, cells, f'all {cells} cells', color=MUTED, fontsize=6.5, ha='right', va='bottom')
    ax.set_xticks(range(len(solvers)), [s[1] for s in solvers])
    ax.set_ylabel('Cells explored (mean ± sd)')
    ax.set_ylim(0, cells * 1.08)
    ax.legend(ncol=4, loc='upper center', bbox_to_anchor=(0.5, 1.16))
    fig.tight_layout()
    fig.savefig(os.path.join(FIGURES, 'explored.pdf'))


if __name__ == '__main__':
    os.makedirs(FIGURES, exist_ok=True)
    representations()
    explored()
