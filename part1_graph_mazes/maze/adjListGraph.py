# ------------------------------------------------------------------------
# Adjacency list implementation.
#
# Each vertex (a Coordinates) maps to a dictionary of its neighbours, where the
# value is the wall status of the edge between them.  Using a dictionary for the
# neighbour "list" keeps edge look-ups O(1) while still storing only the edges
# that exist (O(V + E) space).
# ------------------------------------------------------------------------

from typing import Dict, List

from maze.util import Coordinates
from maze.graph import Graph


class AdjListGraph(Graph):
    """
    Represents an undirected graph using an adjacency list.
    """

    def __init__(self, rowNum: int, colNum: int):
        self.m_rowNum = rowNum
        self.m_colNum = colNum
        # vertex -> {neighbour: wallStatus}
        self.m_adjList: Dict[Coordinates, Dict[Coordinates, bool]] = {}


    def addVertex(self, label: Coordinates):
        if label not in self.m_adjList:
            self.m_adjList[label] = {}


    def addVertices(self, vertLabels: List[Coordinates]):
        for label in vertLabels:
            self.addVertex(label)


    def addEdge(self, vert1: Coordinates, vert2: Coordinates, addWall: bool = False) -> bool:
        if not (self.hasVertex(vert1) and self.hasVertex(vert2)) or self.hasEdge(vert1, vert2):
            return False

        self.m_adjList[vert1][vert2] = addWall
        self.m_adjList[vert2][vert1] = addWall
        return True


    def updateWall(self, vert1: Coordinates, vert2: Coordinates, wallStatus: bool) -> bool:
        if not self.hasEdge(vert1, vert2):
            return False

        self.m_adjList[vert1][vert2] = wallStatus
        self.m_adjList[vert2][vert1] = wallStatus
        return True


    def removeEdge(self, vert1: Coordinates, vert2: Coordinates) -> bool:
        if not self.hasEdge(vert1, vert2):
            return False

        del self.m_adjList[vert1][vert2]
        del self.m_adjList[vert2][vert1]
        return True


    def hasVertex(self, label: Coordinates) -> bool:
        return label in self.m_adjList


    def hasEdge(self, vert1: Coordinates, vert2: Coordinates) -> bool:
        return self.hasVertex(vert1) and vert2 in self.m_adjList[vert1]


    def getWallStatus(self, vert1: Coordinates, vert2: Coordinates) -> bool:
        if not self.hasEdge(vert1, vert2):
            return False
        return self.m_adjList[vert1][vert2]


    def neighbours(self, label: Coordinates) -> List[Coordinates]:
        if not self.hasVertex(label):
            return []
        return list(self.m_adjList[label].keys())
