# Maze Generation and Solving

Two parts, each a self-contained Python program run from its own folder.

```
part1_graph_mazes/   2D maze generation, comparing graph representations
part2_3d_mazes/      3D (multi-level) maze generation and solving, Tasks A-D
experiments/         scripts reproducing the report's results (CSVs in experiments/results/)
report/              project report (shared body, NeurIPS and IEEE Computer Society builds)
```

Requirements: Python 3.9+, and `matplotlib` for visualisation (`pip install -r requirements.txt`).
Without matplotlib everything still runs, only the plots are skipped.

## Part 1: graph representations of 2D mazes

```
cd part1_graph_mazes
python3 main.py configs/sample.json
```

| Component | File |
|---|---|
| Array maze (baseline) | `maze/arrayMaze.py` |
| Adjacency list graph | `maze/adjListGraph.py` |
| Adjacency matrix graph | `maze/adjMatGraph.py` |
| Graph-backed maze, times `updateWall()` / `neighbours()` | `maze/graphMaze.py` |
| Recursive backtracking generator | `generation/recurBackGenerator.py` |

Config keys: `dataStructure` (`array`, `adjlist`, `adjmat`), `rowNum`, `colNum`, `entrances`, `exits`
(`[row, col]` on the boundary), `generator` (`recur`), `visualise`.
`configs/experiments/` holds the configurations used for the empirical comparison.
The adjacency matrix uses O(V^2) memory (V = (rows+2)(cols+2)), so the matrix runs larger than about 200x200 need several GB of RAM.

## Part 2: 3D mazes

```
cd part2_3d_mazes
python3 main.py configs/taskA_generation.json
```

| Task | What | Files | Config |
|---|---|---|---|
| A | Maze generators: recursive backtracking, Prim, Wilson | `generation/` | `configs/taskA_generation.json` |
| B | Solvers: recursive backtracking, wall following, Pledge | `solving/` | `configs/taskB_solving.json` |
| C | Find the closest entrance-exit pair with few cells explored | `solving/taskCMazeSolver.py` | `configs/taskC_best_entrance_exit.json` |
| D | Generator that maximises the cells a given solver explores | `generation/taskDMazeGenerator.py`, `generatorSelector.py` | `configs/taskD_adversarial_generation.json` |

Config keys: `levelSpecs` (`[rows, cols]` per level), `entrances` / `exits` (`[level, row, col]` on a level's boundary),
`generator` (`recur`, `prim`, `wilson`, `taskD`), `solver` (`recur`, `wall`, `pledge`, `taskC`),
`solverEntranceIndex` (not used by Task C), `visualise`, and optionally `randSeed` and `fileOutput` (save the plot instead of showing it).

## Experiments and report

```
python3 experiments/run_part1.py      # representations, ~1 min
python3 experiments/run_part2.py      # generators x solvers, ~4 min
python3 experiments/make_figures.py   # figures -> report/figures/ (needs matplotlib)
cd report/neurips && tectonic main.tex   # or report/ieee
```

The report text lives in `report/abstract.tex` and `report/body.tex`; `report/neurips/main.tex` and
`report/ieee/main.tex` only wrap it in each template.
