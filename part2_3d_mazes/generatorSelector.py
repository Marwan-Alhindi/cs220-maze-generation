# -------------------------------------------------------------------
# Class to select appropriate maze generator.
# -------------------------------------------------------------------


from generation.mazeGenerator import MazeGenerator
from generation.recurBackGenerator import RecurBackMazeGenerator
from generation.primGenerator import PrimMazeGenerator
from generation.wilsonGenerator import WilsonMazeGenerator
from generation.taskDMazeGenerator import TaskDMazeGenerator
from solving.mazeSolver import MazeSolver


class GeneratorSelector:
    """
    Class used to select and construct appropriate maze generator.
    """


    def construct(self, genApproach: str)->MazeGenerator:
        """
        Tasks A, B and C, with a specified maze generator.
        If genApproach is unknown, None will be returned.

        @param genApproach: Name of generator to use.
        
        @return: Instance of a maze generator.
        """
        generator: MazeGenerator = None

        if genApproach == 'recur':
            generator = RecurBackMazeGenerator()
        elif genApproach == 'prim':
            generator = PrimMazeGenerator()
        elif genApproach == 'wilson':
            generator = WilsonMazeGenerator()

        return generator



    def match(self, solver: MazeSolver)->MazeGenerator:
        """
        Task D, select a generator that maximises the number of cells the given solver explores.
        Only the solver's name is used; the solver is not run before the maze is generated.

        @param solver: Instance of the maze solver that will solve the generated maze.

        @return: Instance of a maze generator.
        """

        # the Task D generator tailors how it scores candidate mazes to the solver
        return TaskDMazeGenerator(solver.name())
