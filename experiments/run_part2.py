"""
Experiments 2-4: structure of the generated 3D mazes, cells explored by each solver, and the effect of the
adversarial (Task D) generator.

For every maze setting, generator and seed, a maze is generated and its structure measured; then every solver
solves it.  The Task D generator is matched to each solver, so it produces a separate maze per solver.

Usage (from the repository root):  python3 experiments/run_part2.py
"""

import csv
import os
import random
import sys
import time
from collections import deque

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'part2_3d_mazes'))

from maze.maze3D import Maze3D
from maze.util import Coordinates3D as C
from generatorSelector import GeneratorSelector
from solverSelector import SolverSelector


# (name, level dimensions, entrances, exits); boundary coordinates are (level, row, col)
SETTINGS = [
    ('uniform 3x12x12', [(12, 12)] * 3,
     [C(0, 0, -1), C(1, -1, 6)], [C(2, 11, 12), C(1, 12, 3)]),
    ('mixed 3 levels', [(10, 10), (14, 8), (8, 14)],
     [C(0, 0, -1), C(1, -1, 4)], [C(2, 7, 14), C(1, 14, 2)]),
    ('uniform 4x20x20', [(20, 20)] * 4,
     [C(0, 0, -1), C(2, -1, 10)], [C(3, 19, 20), C(1, 20, 5)]),
]
GENERATORS = ['recur', 'prim', 'wilson']
SOLVERS = ['recur', 'wall', 'pledge', 'taskC']
SEEDS = range(30)


def inside(maze, cell):
    level = cell.getLevel()
    return 0 <= level < maze.levelNum() and 0 <= cell.getRow() < maze.rowNum(level) and 0 <= cell.getCol() < maze.colNum(level)


def structure(maze):
    """Dead-end ratio, junction ratio, share of vertical passages and entrance-to-nearest-exit distance."""
    cells = [cell for cell in maze.allCells() if inside(maze, cell)]
    deadEnds = junctions = vertical = passages = 0
    for cell in cells:
        open_ = [n for n in maze.neighbours(cell) if inside(maze, n) and not maze.hasWall(cell, n)]
        deadEnds += len(open_) == 1
        junctions += len(open_) >= 3
        passages += len(open_)
        vertical += sum(1 for n in open_ if n.getLevel() != cell.getLevel())

    exits = set(maze.getExits())
    distances = []
    for entrance in maze.getEntrances():
        dist = {entrance: 0}
        queue = deque([entrance])
        found = None
        while queue and found is None:
            cell = queue.popleft()
            for n in maze.neighbours(cell):
                if n not in dist and not maze.hasWall(cell, n):
                    dist[n] = dist[cell] + 1
                    if n in exits:
                        found = dist[n]
                        break
                    queue.append(n)
        distances.append(found)

    return {
        'dead_end_ratio': deadEnds / len(cells),
        'junction_ratio': junctions / len(cells),
        'vertical_share': vertical / passages,
        'dist_entrance0': distances[0],
        'dist_min': min(distances),
    }


def buildMaze(levels, entrances, exits):
    maze = Maze3D(levels)
    for e in entrances:
        maze.storeEntrance(e)
    for x in exits:
        maze.storeExit(x)
    return maze


def solve(maze, solverName):
    solver = SolverSelector().construct(solverName)
    start = time.perf_counter()
    if solverName == 'taskC':
        solver.solveMaze(maze)
    else:
        solver.solveMaze(maze, maze.getEntrances()[0])
    elapsed = time.perf_counter() - start
    return solver, elapsed


def main():
    out = os.path.join(ROOT, 'experiments', 'results', 'part2_solvers.csv')
    fields = ['setting', 'cells', 'generator', 'target_solver', 'seed', 'gen_time_s', 'dead_end_ratio', 'junction_ratio',
              'vertical_share', 'dist_entrance0', 'dist_min', 'solver', 'solved', 'explored', 'steps', 'solve_time_s']
    with open(out, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for (setting, levels, entrances, exits) in SETTINGS:
            cellNum = sum(r * c for r, c in levels)
            for seed in SEEDS:
                jobs = [(g, None) for g in GENERATORS] + [('taskD', s) for s in SOLVERS]
                for (genName, target) in jobs:
                    random.seed(seed)
                    maze = buildMaze(levels, entrances, exits)
                    if genName == 'taskD':
                        generator = GeneratorSelector().match(SolverSelector().construct(target))
                    else:
                        generator = GeneratorSelector().construct(genName)
                    start = time.perf_counter()
                    generator.generateMaze(maze)
                    genTime = time.perf_counter() - start
                    maze.carveEntrances()
                    maze.carveExits()
                    stats = structure(maze)

                    for solverName in ([target] if target else SOLVERS):
                        random.seed(seed)
                        solver, solveTime = solve(maze, solverName)
                        writer.writerow(dict(setting=setting, cells=cellNum, generator=genName, target_solver=target or '',
                                             seed=seed, gen_time_s=genTime, solver=solverName, solved=solver.isSolved(),
                                             explored=solver.getCellsExplored(), steps=len(solver.getSolverPath()),
                                             solve_time_s=solveTime, **stats))
                print(setting, seed, flush=True)


if __name__ == '__main__':
    main()
