# -------------------------------------------------------------------
# Wall following maze solver.
# -------------------------------------------------------------------


from typing import List, Optional

from maze.maze3D import Maze3D
from solving.mazeSolver import MazeSolver
from maze.util import Coordinates3D


# Movement directions as (level, row, col) offsets.  Row increases "north" (upwards in the visualisation).
NORTH = Coordinates3D(0, 1, 0)
EAST = Coordinates3D(0, 0, 1)
SOUTH = Coordinates3D(0, -1, 0)
WEST = Coordinates3D(0, 0, -1)
UP = Coordinates3D(1, 0, 0)
DOWN = Coordinates3D(-1, 0, 0)

# Fixed cyclic order of directions used by the left-hand rule.  Arriving from direction d (i.e. d points back to the
# cell we came from), the solver tries the directions that follow d in this cycle, in order, and d itself last.
# For planar moves this is exactly "left, forward, right, back" (e.g. heading north: back = SOUTH, then WEST = left,
# NORTH = forward, EAST = right); the two vertical directions are slotted into the same cycle.
# Because every cell uses the same cyclic order, the walk is an Euler tour of the passage tree in a perfect maze,
# so it is guaranteed to reach every cell, including the exit.
DIRECTION_CYCLE: List[Coordinates3D] = [SOUTH, WEST, NORTH, EAST, UP, DOWN]

PLANAR_CLOCKWISE: List[Coordinates3D] = [NORTH, EAST, SOUTH, WEST]


def opposite(direction: Coordinates3D)->Coordinates3D:
    return Coordinates3D(-direction.getLevel(), -direction.getRow(), -direction.getCol())



class WallFollowingMazeSolver(MazeSolver):
    """
    Wall following (left-hand rule) solver implementation, extended to 3D mazes.
    """

    def __init__(self):
        super().__init__()
        self.m_name = "wall"



    def canMove(self, maze: Maze3D, cell: Coordinates3D, direction: Coordinates3D)->bool:
        """
        @returns True if there is an open passage from cell in the given direction.
        """
        target = cell + direction
        return target in maze.neighbours(cell) and not maze.hasWall(cell, target)



    def nextDirection(self, maze: Maze3D, cell: Coordinates3D, backDirection: Coordinates3D)->Optional[Coordinates3D]:
        """
        Left-hand rule: the first open direction following backDirection in DIRECTION_CYCLE (backDirection itself
        is tried last, which corresponds to turning around at a dead end).

        @returns Direction to move in, or None if the cell has no open passage.
        """
        start = DIRECTION_CYCLE.index(backDirection)
        for i in range(1, len(DIRECTION_CYCLE) + 1):
            direction = DIRECTION_CYCLE[(start + i) % len(DIRECTION_CYCLE)]
            if self.canMove(maze, cell, direction):
                return direction
        return None



    def inwardDirection(self, maze: Maze3D, entrance: Coordinates3D)->Coordinates3D:
        """
        @returns Direction that leads from the (boundary) entrance into the maze.
        """
        (rowNum, colNum) = maze.m_levelDims[entrance.getLevel()]
        if entrance.getRow() == -1:
            return NORTH
        elif entrance.getRow() == rowNum:
            return SOUTH
        elif entrance.getCol() == -1:
            return EAST
        else:
            return WEST



    def moveTo(self, cell: Coordinates3D, visited: set):
        """
        Records a step of the solver.  Cells already visited are recorded as backtracking, so they are not counted
        as explored again.
        """
        self.solverPathAppend(cell, cell in visited)
        visited.add(cell)



    def maxSteps(self, maze: Maze3D)->int:
        """
        Upper bound on the number of steps of a full Euler tour of the maze (each passage is walked at most twice),
        used as a safety stop if the maze has no reachable exit.
        """
        return 2 * len(maze.allCells()) + 1



    def solveMaze(self, maze: Maze3D, entrance: Coordinates3D):
        self.m_solved = False
        exits = set(maze.getExits())

        visited: set[Coordinates3D] = set()
        currCell: Coordinates3D = entrance
        self.moveTo(currCell, visited)

        # pretend we arrived at the entrance from outside the maze
        backDirection = opposite(self.inwardDirection(maze, entrance))

        for _ in range(self.maxSteps(maze)):
            if currCell in exits:
                self.solved(entrance, currCell)
                return

            direction = self.nextDirection(maze, currCell, backDirection)
            if direction is None:
                return

            currCell = currCell + direction
            backDirection = opposite(direction)
            self.moveTo(currCell, visited)

        if currCell in exits:
            self.solved(entrance, currCell)
