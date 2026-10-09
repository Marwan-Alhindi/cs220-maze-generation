# -------------------------------------------------------------------
# Implementation of Task D maze generator.
# -------------------------------------------------------------------

from collections import deque
from typing import Dict, List, Optional, Tuple
import random

from maze.maze3D import Maze3D
from maze.util import Coordinates3D
from generation.mazeGenerator import MazeGenerator


Edge = Tuple[Coordinates3D, Coordinates3D]


class TaskDMazeGenerator(MazeGenerator):
    """
    Generates a perfect maze that makes the given solver explore as many cells as possible.

    Every solver has to walk at least the path from its entrance to the exit it finds, and in a perfect maze that path
    is unique.  So the generator builds many candidate perfect mazes (spanning trees grown by randomised DFS, which
    produces long winding corridors with few branches) and keeps the one where the entrances are furthest from the
    exits, measured along the maze's passages:
        - 'taskC' (searches from all entrances at once and stops at the nearest exit): maximise the shortest
          distance over all entrance-exit pairs, since that is the distance the search has to cover.
        - other solvers (single entrance, unknown in advance): maximise the average over entrances of the distance
          to the nearest exit.
    Candidates are built and scored as plain edge lists; only the best one is carved into the maze.
    The solver is never run during generation.
    """

    # upper bound on (candidates x cells), keeps generation time roughly constant across maze sizes
    WORK_BUDGET = 200000
    MAX_CANDIDATES = 100


    def __init__(self, solverName: str = ""):
        super().__init__()
        self.m_solverName = solverName



    def generateMaze(self, maze: Maze3D):
        maze.initCells(True)

        cells = [cell for cell in maze.allCells() if self.isInside(maze, cell)]
        if len(cells) == 0:
            self.m_mazeGenerated = True
            return

        adjacency: Dict[Coordinates3D, List[Coordinates3D]] = {
            cell: [neigh for neigh in maze.neighbours(cell) if self.isInside(maze, neigh)] for cell in cells
        }
        entranceCells = [self.innerCell(maze, ent) for ent in maze.getEntrances()]
        exitCells = set(self.innerCell(maze, ext) for ext in maze.getExits())

        candidateNum = max(1, min(self.MAX_CANDIDATES, self.WORK_BUDGET // len(cells)))
        bestEdges: List[Edge] = []
        bestScore: Optional[float] = None
        for _ in range(candidateNum):
            edges = self.randomSpanningTree(cells, adjacency)
            score = self.score(cells, edges, entranceCells, exitCells)
            if bestScore is None or score > bestScore:
                bestScore = score
                bestEdges = edges

        for (cell1, cell2) in bestEdges:
            maze.removeWall(cell1, cell2)

        self.m_mazeGenerated = True



    def isInside(self, maze: Maze3D, cell: Coordinates3D)->bool:
        """
        @returns True if cell is a cell of the maze (not a boundary cell).
        """
        level = cell.getLevel()
        return 0 <= level < maze.levelNum() and 0 <= cell.getRow() < maze.rowNum(level) and 0 <= cell.getCol() < maze.colNum(level)



    def innerCell(self, maze: Maze3D, boundary: Coordinates3D)->Coordinates3D:
        """
        @returns The maze cell that an entrance/exit on the boundary opens into.
        """
        level = boundary.getLevel()
        rowNum = maze.rowNum(level)
        colNum = maze.colNum(level)
        if boundary.getRow() == -1:
            return Coordinates3D(level, 0, boundary.getCol())
        elif boundary.getRow() == rowNum:
            return Coordinates3D(level, rowNum - 1, boundary.getCol())
        elif boundary.getCol() == -1:
            return Coordinates3D(level, boundary.getRow(), 0)
        else:
            return Coordinates3D(level, boundary.getRow(), colNum - 1)



    def randomSpanningTree(self, cells: List[Coordinates3D], adjacency: Dict[Coordinates3D, List[Coordinates3D]])->List[Edge]:
        """
        Randomised depth-first search (recursive backtracking) spanning tree over the maze cells.

        @returns List of passages (pairs of cells whose wall is removed).
        """
        start = random.choice(cells)
        visited = {start}
        stack = [start]
        edges: List[Edge] = []

        while stack:
            current = stack[-1]
            unvisited = [neigh for neigh in adjacency[current] if neigh not in visited]
            if unvisited:
                neigh = random.choice(unvisited)
                visited.add(neigh)
                edges.append((current, neigh))
                stack.append(neigh)
            else:
                stack.pop()

        return edges



    def score(self, cells: List[Coordinates3D], edges: List[Edge], entranceCells: List[Coordinates3D], exitCells: set)->float:
        """
        @returns How hard the candidate maze is for the solver (higher is harder).
        """
        if len(entranceCells) == 0 or len(exitCells) == 0:
            return 0

        tree: Dict[Coordinates3D, List[Coordinates3D]] = {cell: [] for cell in cells}
        for (cell1, cell2) in edges:
            tree[cell1].append(cell2)
            tree[cell2].append(cell1)

        distances = [self.distanceToNearestExit(tree, ent, exitCells) for ent in entranceCells]
        if self.m_solverName == 'taskC':
            return min(distances)
        return sum(distances) / len(distances)



    def distanceToNearestExit(self, tree: Dict[Coordinates3D, List[Coordinates3D]], start: Coordinates3D, exitCells: set)->int:
        """
        @returns Number of passages between start and the closest exit cell (BFS over the tree).
        """
        distance = {start: 0}
        queue = deque([start])
        while queue:
            cell = queue.popleft()
            if cell in exitCells:
                return distance[cell]
            for neigh in tree[cell]:
                if neigh not in distance:
                    distance[neigh] = distance[cell] + 1
                    queue.append(neigh)
        return 0
