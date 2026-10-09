import matplotlib.pyplot as plt
    
from maze.maze import Maze
from maze.util import Coordinates
import pdb

class Visualizer(object):
    """Class that handles all aspects of visualization.


    Attributes:
        maze: The maze that will be visualized
        cell_size (int): How large the cells will be in the plots
        height (int): The height of the maze
        width (int): The width of the maze
        ax: The axes for the plot
    """

    def __init__(self, maze :Maze, cellSize):
        self.m_maze = maze
        self.m_cellSize = cellSize
        self.m_height = (maze.rowNum()+2) * cellSize
        self.m_width = (maze.colNum()+2) * cellSize
        self.m_ax = None


    def show_maze(self):
        """Displays a plot of the maze without the solution path"""

        # create the plot figure and style the axes
        fig = self.configure_plot()

        # plot the walls on the figure
        self.plot_walls()

        # plot the entrances and exits on the figure
        self.plotEntExit()

        # display the plot to the user
        plt.show()


    def plot_walls(self):
        """ 
        Plots the walls of a maze. This is used when generating the maze image.
        """
        for r in range(0, self.m_maze.rowNum()):
            for c in range(0, self.m_maze.colNum()):
                # if self.maze.initial_grid[i][j].is_entry_exit == "entry":
                #     self.ax.text(j*self.cell_size, i*self.cell_size, "START", fontsize=7, weight="bold")
                # elif self.maze.initial_grid[i][j].is_entry_exit == "exit":
                #     self.ax.text(j*self.cell_size, i*self.cell_size, "END", fontsize=7, weight="bold")

                #      row plot
                    if self.m_maze.hasWall(Coordinates(r-1,c), Coordinates(r,c)): # -1|0,1,2,3,4 - 0|0,1,2,3,4
                        self.m_ax.plot([(c+1)*self.m_cellSize, (c+1+1)*self.m_cellSize],
                                    [(r+1)*self.m_cellSize, (r+1)*self.m_cellSize], color="k")    
        #             # column plot
                    if self.m_maze.hasWall(Coordinates(r,c-1), Coordinates(r,c)):
                        self.m_ax.plot([(c+1)*self.m_cellSize, (c+1)*self.m_cellSize],
                                    [(r+1)*self.m_cellSize, (r+1+1)*self.m_cellSize], color="k")  


        # # top boundary
        for c in range(0, self.m_maze.colNum()):
        #     # top
            if self.m_maze.hasWall(Coordinates(self.m_maze.rowNum()-1,c), Coordinates(self.m_maze.rowNum(),c)):
                self.m_ax.plot([(c+1)*self.m_cellSize, (c+1+1)*self.m_cellSize],
                                [(self.m_maze.rowNum()+1)*self.m_cellSize, (self.m_maze.rowNum()+1)*self.m_cellSize], color="k")    

        # right boundary
        for r in range(0, self.m_maze.rowNum()):
            if self.m_maze.hasWall(Coordinates(r,self.m_maze.colNum()-1), Coordinates(r,self.m_maze.colNum())):
                self.m_ax.plot([(self.m_maze.colNum()+1)*self.m_cellSize, (self.m_maze.colNum()+1)*self.m_cellSize],
                                [(r+1)*self.m_cellSize, (r+1+1)*self.m_cellSize], color="k")  

    def plotEntExit(self):
        """
        Plots the entrances and exits in the displayed maze.
        """

        for ent in self.m_maze.getEntrances():
            # check direction of arrow
            # upwards arrow
            if ent.getRow() == -1:
                self.m_ax.arrow((ent.getCol()+1.5)*self.m_cellSize, (ent.getRow()+1)*self.m_cellSize, 0, self.m_cellSize*0.6, head_width=0.1)
            # downwards arrow
            elif ent.getRow() == self.m_maze.rowNum():
                self.m_ax.arrow((ent.getCol()+1.5)*self.m_cellSize, (ent.getRow()+2)*self.m_cellSize, 0, -self.m_cellSize*0.6, head_width=0.1)
            # rightward arrow
            elif ent.getCol() == -1:
                self.m_ax.arrow((ent.getCol()+1)*self.m_cellSize, (ent.getRow()+1.5)*self.m_cellSize, self.m_cellSize*0.6, 0, head_width=0.1)
            # leftward arrow
            elif ent.getCol() == self.m_maze.colNum():
                self.m_ax.arrow((ent.getCol()+2)*self.m_cellSize, (ent.getRow()+1.5)*self.m_cellSize, -self.m_cellSize*0.6, 0, head_width=0.1)

        for ext in self.m_maze.getExits():
            # downwards arrow
            if ext.getRow() == -1:
                self.m_ax.arrow((ext.getCol()+1.5)*self.m_cellSize, (ext.getRow()+1.8)*self.m_cellSize, 0, -self.m_cellSize*0.6, head_width=0.1)
            # upwards arrow
            elif ext.getRow() == self.m_maze.rowNum():
                self.m_ax.arrow((ext.getCol()+1.5)*self.m_cellSize, (ext.getRow()+1.2)*self.m_cellSize, 0, self.m_cellSize*0.6, head_width=0.1)
            # leftward arrow
            elif ext.getCol() == -1:
                self.m_ax.arrow((ext.getCol())*self.m_cellSize, (ext.getRow()+1.5)*self.m_cellSize, -self.m_cellSize*0.6, 0, head_width=0.1)
            # leftward arrow
            elif ext.getCol() == self.m_maze.colNum():
                self.m_ax.arrow((ext.getCol()+1.2)*self.m_cellSize, (ext.getRow()+1.5)*self.m_cellSize, self.m_cellSize*0.6, 0, head_width=0.1)



    def configure_plot(self):
        """Sets the initial properties of the maze plot. Also creates the plot and axes"""

        # Create the plot figure
        fig = plt.figure(figsize = (7, 7*self.m_maze.rowNum() / self.m_maze.colNum()))

        # Create the axes
        self.m_ax = plt.axes()

        # Set an equal aspect ratio
        self.m_ax.set_aspect("equal")

        # Remove the axes from the figure
        self.m_ax.axes.get_xaxis().set_visible(False)
        self.m_ax.axes.get_yaxis().set_visible(False)

        # title_box = self.m_ax.text(0, self.m_maze.rowNum() + self.m_cellSize + 0.1,
        #                     r"{}$\times${}".format(self.m_maze.rowNum(), self.m_maze.colNum()),
        #                     bbox={"facecolor": "gray", "alpha": 0.5, "pad": 4}, fontname="serif", fontsize=15)

        return fig

