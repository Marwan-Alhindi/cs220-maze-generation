# -------------------------------------------------------------------
# Wilson's algorithm maze generator.
# -------------------------------------------------------------------


from maze.maze3D import Maze3D
from maze.util import Coordinates3D
from generation.mazeGenerator import MazeGenerator
import random


class WilsonMazeGenerator(MazeGenerator):
    """
    Wilson's algorithm maze generator. This algorithm generates a uniform spanning tree maze,
    which ensures that the generated maze has no loops and that all parts of the maze are reachable from
    any other part. It uses a random walk that erases its own loops until it connects to the growing tree.

    Attributes:
        m_mazeGenerated (bool): Flag to indicate whether the maze has been successfully generated.
    """
    

    def generateMaze(self, maze: Maze3D):
        """
        Generates a maze using Wilson's algorithm.

        Args:
            maze (Maze3D): The 3D maze object that will be modified in place.

        The algorithm:
        1. Initializes all cells with walls between them.
        2. Begins with a randomly chosen cell, marking it as part of the maze.
        3. Performs random walks from random cells until they connect to the part of the maze already built,
           erasing loops in the walk and adding the path to the maze.
        4. Continues until all cells are included in the maze.
        """

        # The algorithm, like the previous two, starts with a maze with walls between all pair of adjacent cells. 
        maze.initCells(True)
        # Also initially every cell in the maze is considered as not finalised.
        finalized = set()

        # select starting cell 
        # random floor
        startLevel = random.randint(0, maze.levelNum() - 1)
        startCoord: Coordinates3D = Coordinates3D(startLevel, random.randint(0, maze.rowNum(startLevel) - 1), random.randint(0, maze.colNum(startLevel) - 1))

        # It then starts by randomly selecting a starting cell, that is the first cell to be considered as finalised.
        finalized.add(startCoord)

        # total number of cells in maze including all levels
        totalCells = sum([maze.rowNum(l) * maze.colNum(l) for l in range(maze.levelNum())])
        
        while len(finalized) < totalCells:
            
            # Select another cell, at random, that isn’t finalised yet. 
            while True:
                randomLevel = random.randint(0, maze.levelNum() - 1)
                randomRow = random.randint(0, maze.rowNum(randomLevel) - 1)
                randomCol = random.randint(0, maze.colNum(randomLevel) - 1)
                moving_cell: Coordinates3D = Coordinates3D(randomLevel, randomRow, randomCol)
                if moving_cell not in finalized:
                    break

            # Store the path
            path = [moving_cell]
            while moving_cell not in finalized:
                neighbours = [neigh for neigh in maze.neighbours(moving_cell) if
                              (0 <= neigh.getRow() < maze.rowNum(neigh.getLevel())) and
                              (0 <= neigh.getCol() < maze.colNum(neigh.getLevel()))]
                moving_cell = random.choice(neighbours)
                if moving_cell in path:
                    # Erase loop
                    loop_start = path.index(moving_cell)
                    path = path[:loop_start + 1]
                else:
                    path.append(moving_cell)
            
            # We then add all the cells visited during the random walk to the finalised set.
            for cell in path:
                finalized.add(cell)
            
            # We then remove the walls between the cells visited during the random walk.
            for i in range(len(path) - 1):
                maze.removeWall(path[i], path[i + 1])
    
        # Update maze generated
        self.m_mazeGenerated = True
