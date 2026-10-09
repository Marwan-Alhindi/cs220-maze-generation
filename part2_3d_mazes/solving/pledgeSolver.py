# -------------------------------------------------------------------
# Pledge maze solver.
# -------------------------------------------------------------------


from maze.maze3D import Maze3D
from maze.util import Coordinates3D
from solving.wallFollowingSolver import WallFollowingMazeSolver, PLANAR_CLOCKWISE, opposite


class PledgeMazeSolver(WallFollowingMazeSolver):
    """
    Pledge solver implementation, extended to 3D mazes.

    The solver keeps a preferred direction (into the maze from the entrance) and walks straight in it until blocked.
    It then follows the wall (left-hand rule, see WallFollowingMazeSolver) while keeping a turn counter: +1 for each
    90 degree right turn and -1 for each left turn.  Once the counter returns to 0 the solver is facing the preferred
    direction again and resumes walking straight.  Moving between levels doesn't change the heading or counter.

    Pledge's guarantee only holds for planar mazes, so as a safety net, if the walk exceeds a step budget the solver
    falls back to plain wall following, which is guaranteed to reach an exit in a perfect maze.
    """

    def __init__(self):
        super().__init__()
        self.m_name = "pledge"



    def turnAmount(self, heading: Coordinates3D, direction: Coordinates3D)->int:
        """
        @returns Number of 90 degree turns (right positive, left negative) to go from heading to direction.
        """
        delta = (PLANAR_CLOCKWISE.index(direction) - PLANAR_CLOCKWISE.index(heading)) % 4
        return {0: 0, 1: 1, 2: 2, 3: -1}[delta]



    def solveMaze(self, maze: Maze3D, entrance: Coordinates3D):
        self.m_solved = False
        exits = set(maze.getExits())

        visited: set[Coordinates3D] = set()
        currCell: Coordinates3D = entrance
        self.moveTo(currCell, visited)

        preferred = self.inwardDirection(maze, entrance)
        heading = preferred
        backDirection = opposite(preferred)
        turnCounter = 0
        followingWall = False

        pledgeBudget = 2 * self.maxSteps(maze)
        steps = 0

        while currCell not in exits:
            if steps >= pledgeBudget + self.maxSteps(maze):
                # no exit reachable
                return

            if steps < pledgeBudget and not followingWall and self.canMove(maze, currCell, preferred):
                direction = preferred
            else:
                # blocked (or past the Pledge budget): follow the wall
                followingWall = True
                direction = self.nextDirection(maze, currCell, backDirection)
                if direction is None:
                    return

            if direction in PLANAR_CLOCKWISE:
                turnCounter += self.turnAmount(heading, direction)
                heading = direction

            currCell = currCell + direction
            backDirection = opposite(direction)
            self.moveTo(currCell, visited)
            steps += 1

            # facing the preferred direction with no net rotation, so stop following the wall
            if followingWall and turnCounter == 0 and steps < pledgeBudget:
                followingWall = False

        self.solved(entrance, currCell)
