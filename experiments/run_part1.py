"""
Experiment 1: cost of the maze representations (array, adjacency list, adjacency matrix).

For each representation and maze size, generates mazes with recursive backtracking and records the generation time,
the average time per updateWall() / neighbours() call and the memory used by the initialised maze.

Usage (from the repository root):  python3 experiments/run_part1.py
"""

import csv
import os
import random
import sys
import time
import tracemalloc

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'part1_graph_mazes'))

from maze.util import Coordinates
from maze.arrayMaze import ArrayMaze
from maze.graphMaze import GraphMaze
from generation.recurBackGenerator import RecurBackMazeGenerator


SIZES = {
    'array': [10, 20, 30, 50, 70, 100, 150, 200],
    'adjlist': [10, 20, 30, 50, 70, 100, 150, 200],
    # O(V^2) memory: 100x100 already needs ~108 MB
    'adjmat': [10, 20, 30, 50, 70, 100],
}
SEEDS = range(5)


def makeMaze(ds: str, n: int):
    maze = ArrayMaze(n, n) if ds == 'array' else GraphMaze(n, n, ds)
    maze.addEntrance(Coordinates(0, -1))
    maze.addExit(Coordinates(n - 1, n))
    return maze


def memoryOf(ds: str, n: int) -> int:
    """Peak bytes allocated while building and initialising (all walls) a maze."""
    tracemalloc.start()
    maze = makeMaze(ds, n)
    maze.initCells(True)
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    del maze
    return peak


def main():
    out = os.path.join(ROOT, 'experiments', 'results', 'part1_representations.csv')
    with open(out, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['structure', 'n', 'cells', 'seed', 'gen_time_s', 'update_wall_us', 'neighbours_us', 'memory_mb', 'perfect'])
        for ds, sizes in SIZES.items():
            for n in sizes:
                memory = memoryOf(ds, n) / 2**20
                for seed in SEEDS:
                    random.seed(seed)
                    maze = makeMaze(ds, n)
                    generator = RecurBackMazeGenerator()
                    start = time.perf_counter()
                    generator.generateMaze(maze)
                    genTime = time.perf_counter() - start
                    generator.addEntrances(maze)
                    generator.addExits(maze)

                    updateUs = neighUs = ''
                    if isinstance(maze, GraphMaze):
                        updateUs = 1e6 * maze.m_updateWallTime / maze.m_updateWallCalls
                        neighUs = 1e6 * maze.m_neighboursTime / maze.m_neighboursCalls
                    writer.writerow([ds, n, n * n, seed, genTime, updateUs, neighUs, memory, maze.isPerfect()])
                    print(ds, n, seed, f'{genTime:.3f}s', flush=True)


if __name__ == '__main__':
    main()
