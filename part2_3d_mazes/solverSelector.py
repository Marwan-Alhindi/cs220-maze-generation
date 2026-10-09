# -------------------------------------------------------------------
# Class to select appropriate solver.
# -------------------------------------------------------------------



from solving.recurBackMazeSolver import RecurBackMazeSolver
from solving.wallFollowingSolver import WallFollowingMazeSolver
from solving.pledgeSolver import PledgeMazeSolver
from solving.taskCMazeSolver import TaskCMazeSolver
from solving.mazeSolver import MazeSolver


class SolverSelector:
    """
    Class used to select and construct appropriate maze solver.
    """


    def construct(self, solverApproach: str)->MazeSolver:
        """
        Constructs the specified maze solver.
        If solverApproach is unknown, None will be returned.

        @param solverApproach: Name of solver to use.
        
        @return: Instance of a maze solver.
        """
        solver: MazeSolver = None

        if solverApproach == 'recur':
            solver = RecurBackMazeSolver()
        elif solverApproach == 'wall':
            solver = WallFollowingMazeSolver()
        elif solverApproach == 'pledge':
            solver = PledgeMazeSolver()
        elif solverApproach == 'taskC':
            solver = TaskCMazeSolver()

        return solver
    

 


