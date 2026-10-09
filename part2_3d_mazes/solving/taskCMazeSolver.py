# -------------------------------------------------------------------
# Task C solver.
# -------------------------------------------------------------------


from collections import deque
from typing import Dict, List, Optional

from maze.maze3D import Maze3D
from solving.mazeSolver import MazeSolver
from maze.util import Coordinates3D


class TaskCMazeSolver(MazeSolver):
    """
    Task C solver: finds the entrance-exit pair with the shortest path, while keeping the number of explored cells low.

    Uses a multi-source breadth-first search started from all entrances simultaneously.  The search expands in
    order of distance from the nearest entrance, so the first exit it discovers is the closest exit to any entrance,
    and the search stops right there.  Compared to searching from each entrance separately (and having to explore
    until every exit is found), each cell is explored at most once and only cells closer than the best pair are
    explored.  Every edge has the same cost, so BFS gives the same result as Dijkstra without the priority queue.
    """

    def __init__(self):
        super().__init__()
        self.m_name = "taskC"
        # shortest entrance-to-exit path found (entrance and exit included)
        self.m_bestPath: List[Coordinates3D] = []



    def solveMaze(self, maze: Maze3D):
        # we call the solve maze call without the entrance.
        self.solveMazeTaskC(maze)



    def solveMazeTaskC(self, maze: Maze3D):
        self.m_solved = False
        self.m_bestPath = []

        exits = set(maze.getExits())
        queue: deque = deque()
        # parent of each discovered cell in the search tree (entrances have no parent)
        parent: Dict[Coordinates3D, Optional[Coordinates3D]] = {}

        for entrance in maze.getEntrances():
            if entrance not in parent:
                parent[entrance] = None
                queue.append(entrance)
                self.solverPathAppend(entrance, False)

        while queue:
            cell = queue.popleft()
            for neigh in maze.neighbours(cell):
                if neigh in parent or maze.hasWall(cell, neigh):
                    continue

                parent[neigh] = cell
                self.solverPathAppend(neigh, False)

                if neigh in exits:
                    self.m_bestPath = self.reconstructPath(parent, neigh)
                    self.solved(self.m_bestPath[0], neigh)
                    return

                queue.append(neigh)



    def reconstructPath(self, parent: Dict[Coordinates3D, Optional[Coordinates3D]], end: Coordinates3D)->List[Coordinates3D]:
        """
        @returns Path from the entrance the search reached end from, to end.
        """
        path: List[Coordinates3D] = []
        cell: Optional[Coordinates3D] = end
        while cell is not None:
            path.append(cell)
            cell = parent[cell]
        path.reverse()
        return path



    def getBestPath(self)->List[Coordinates3D]:
        """
        @returns The shortest entrance-to-exit path found.
        """
        return self.m_bestPath
