# ------------------------------------------------------------------------
# Adjacency matrix implementation.
#
# Every possible vertex of the maze (all cells plus the boundary cells around
# them) is given a fixed index.  The V x V matrix is stored as one flat
# bytearray, where each entry encodes the edge between two vertices:
#   NO_EDGE   - vertices are not adjacent
#   NO_WALL   - adjacent, no wall between them
#   WALL      - adjacent, wall between them
# Space is O(V^2), edge look-ups are O(1) and neighbours() is O(V) as it has to
# scan a full row of the matrix.
# ------------------------------------------------------------------------

import re
from typing import Dict, List

from maze.util import Coordinates
from maze.graph import Graph


NO_EDGE = 0
NO_WALL = 1
WALL = 2

# matches any matrix entry that represents an existing edge
_EDGE_PATTERN = re.compile(b'[\x01\x02]')


class AdjMatGraph(Graph):
    """
    Represents an undirected graph using an adjacency matrix.
    """

    def __init__(self, rowNum: int, colNum: int):
        self.m_rowNum = rowNum
        self.m_colNum = colNum

        # The maze occupies rows/cols -1..rowNum/colNum (cells plus boundary), which bounds the vertex set.
        self.m_capacity = (rowNum + 2) * (colNum + 2)
        self.m_matrix = bytearray(self.m_capacity * self.m_capacity)

        # vertex label <-> matrix index, only for vertices that have been added
        self.m_indexOf: Dict[Coordinates, int] = {}
        self.m_labelOf: List[Coordinates] = [None] * self.m_capacity


    def _slot(self, label: Coordinates) -> int:
        """
        @returns The fixed matrix index reserved for label, or -1 if it lies outside the maze area.
        """
        r = label.getRow() + 1
        c = label.getCol() + 1
        if 0 <= r < self.m_rowNum + 2 and 0 <= c < self.m_colNum + 2:
            return r * (self.m_colNum + 2) + c
        return -1


    def _entry(self, vert1: Coordinates, vert2: Coordinates) -> int:
        """
        @returns Flat position of the (vert1, vert2) entry, or -1 if either vertex doesn't exist.
        """
        i = self.m_indexOf.get(vert1, -1)
        j = self.m_indexOf.get(vert2, -1)
        if i < 0 or j < 0:
            return -1
        return i * self.m_capacity + j


    def _setEdge(self, vert1: Coordinates, vert2: Coordinates, value: int):
        i = self.m_indexOf[vert1]
        j = self.m_indexOf[vert2]
        self.m_matrix[i * self.m_capacity + j] = value
        self.m_matrix[j * self.m_capacity + i] = value


    def addVertex(self, label: Coordinates):
        if self.hasVertex(label):
            return
        idx = self._slot(label)
        if idx < 0:
            return
        self.m_indexOf[label] = idx
        self.m_labelOf[idx] = label


    def addVertices(self, vertLabels: List[Coordinates]):
        for label in vertLabels:
            self.addVertex(label)


    def addEdge(self, vert1: Coordinates, vert2: Coordinates, addWall: bool = False) -> bool:
        pos = self._entry(vert1, vert2)
        if pos < 0 or self.m_matrix[pos] != NO_EDGE:
            return False

        self._setEdge(vert1, vert2, WALL if addWall else NO_WALL)
        return True


    def updateWall(self, vert1: Coordinates, vert2: Coordinates, wallStatus: bool) -> bool:
        if not self.hasEdge(vert1, vert2):
            return False

        self._setEdge(vert1, vert2, WALL if wallStatus else NO_WALL)
        return True


    def removeEdge(self, vert1: Coordinates, vert2: Coordinates) -> bool:
        if not self.hasEdge(vert1, vert2):
            return False

        self._setEdge(vert1, vert2, NO_EDGE)
        return True


    def hasVertex(self, label: Coordinates) -> bool:
        return label in self.m_indexOf


    def hasEdge(self, vert1: Coordinates, vert2: Coordinates) -> bool:
        pos = self._entry(vert1, vert2)
        return pos >= 0 and self.m_matrix[pos] != NO_EDGE


    def getWallStatus(self, vert1: Coordinates, vert2: Coordinates) -> bool:
        pos = self._entry(vert1, vert2)
        return pos >= 0 and self.m_matrix[pos] == WALL


    def neighbours(self, label: Coordinates) -> List[Coordinates]:
        i = self.m_indexOf.get(label, -1)
        if i < 0:
            return []

        # scan the vertex's row of the matrix (regex scan runs in C rather than a Python loop)
        start = i * self.m_capacity
        row = self.m_matrix[start:start + self.m_capacity]
        return [self.m_labelOf[m.start()] for m in _EDGE_PATTERN.finditer(row)]
