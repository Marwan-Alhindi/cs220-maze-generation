# -------------------------------------------------------------------
# Prim's maze generator.
# -------------------------------------------------------------------

from maze.maze3D import Maze3D
from maze.util import Coordinates3D
from generation.mazeGenerator import MazeGenerator
import random

class PrimMazeGenerator(MazeGenerator):
    """
    A maze generator that implements Prim's algorithm to generate mazes.
    This generator works by starting from a random cell, and then iteratively
    adding cells to a growing 'maze' by knocking down walls between adjacent cells,
    prioritizing those with the least 'weight' or cost to move to (in this case, randomly),
    until all cells are visited.
    
    Attributes:
        m_mazeGenerated (bool): Flag to check if the maze was generated successfully.
    """
    
    def generateMaze(self, maze: Maze3D):
        """
        Generates a maze using Prim's algorithm.
        
        Starts with a full grid of walls and iteratively removes walls until
        all cells are accessible from one another without breaking the maze rules.

        Args:
            maze (Maze3D): The 3D maze object to be generated.

        Returns:
            None
        """
        # Initialize all cells in the maze as having walls between them.
        maze.initCells(True)
        
        # Select a random starting cell and add it to the visited set.
        startLevel = random.randint(0, maze.levelNum()-1)
        startCoord = Coordinates3D(startLevel, random.randint(0, maze.rowNum(startLevel)-1), random.randint(0, maze.colNum(startLevel)-1))
        visited = set([startCoord])
        
        # Initialize the frontier with all neighbours of the starting cell.
        # The frontier is kept as a list (for O(1) random selection with a deterministic order, so a fixed random
        # seed reproduces the same maze) plus a set for O(1) membership checks.
        frontier = []
        inFrontier = set()
        neighbours = maze.neighbours(startCoord)
        for neighbour in neighbours:
            if (0 <= neighbour.getRow() < maze.rowNum(neighbour.getLevel())) and (0 <= neighbour.getCol() < maze.colNum(neighbour.getLevel())):
                frontier.append(neighbour)
                inFrontier.add(neighbour)
        
        # Calculate the total number of cells in the maze across all levels.
        totalCells = sum([maze.rowNum(l) * maze.colNum(l) for l in range(maze.levelNum())])

        # Continue the algorithm until all cells are visited.
        while len(visited) < totalCells:
            # Randomly select a cell from the frontier, removing it by swapping with the last element.
            index = random.randrange(len(frontier))
            frontier[index], frontier[-1] = frontier[-1], frontier[index]
            selected_cell = frontier.pop()
            inFrontier.remove(selected_cell)

            # Find all visited neighbours of the selected cell.
            visitedNeighbours = [neigh for neigh in maze.neighbours(selected_cell) if neigh in visited and
                                     (0 <= neigh.getRow() < maze.rowNum(neigh.getLevel())) and (0 <= neigh.getCol() < maze.colNum(neigh.getLevel()))]
            
            if visitedNeighbours:
                # Randomly choose a visited neighbour and remove the wall between.
                neigh = random.choice(visitedNeighbours)
                maze.removeWall(selected_cell, neigh)

            # Mark the selected cell as visited.
            visited.add(selected_cell)

            # Add new unvisited neighbours of the selected cell to the frontier.
            neighbours = maze.neighbours(selected_cell)
            for neighbour in neighbours:
                if neighbour not in visited and neighbour not in inFrontier and (0 <= neighbour.getRow() < maze.rowNum(neighbour.getLevel())) and \
                    (0 <= neighbour.getCol() < maze.colNum(neighbour.getLevel())):
                    frontier.append(neighbour)
                    inFrontier.add(neighbour)

        # Verification of maze generation.
        self.m_mazeGenerated = True


# NOTES:

# 1: We have MST/Visisted Nodes and this store the cells that have been visisted
# 2: We have PQ/Frontier set and this store all the neighbours of the MST/Visisted Nodes
# 2 (Continued): Whenever we visit a cell, we remove it and add it to the MST/Visisted Nodes 
# 3: The difference between depth-first search and Prims is that we don't necessarily have to visit cells from the current cell
# 4: This process continue until all cells have been visited