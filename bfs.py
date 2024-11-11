"""
Implementing Breadth First Search Algorithm to solve the maze.

Classes
-------
    BFS
"""

from collections import deque, OrderedDict
from maze import Maze

class BFS:
    """
    Class that represents the Breadth First Search algorithm.

    Attributes
    ----------
    maze : Maze
        The maze to be solved.
    visited : OrderedDict
        An OrderedDict to keep track of visited positions in the maze.
    queue : deque
        A deque to store the positions to be visited next.

    Methods
    -------
    solve()
        Solves the maze using Breadth First Search.
    """

    def __init__(self, maze: Maze) -> None:
        """
        Initializes the BFS class with the given maze.

        Parameters
        ----------
        maze : Maze
            The maze to be solved.
        """
        self.maze = maze
        self.visited = OrderedDict()
        self.queue = deque()

    def solve(self) -> list:
        """
        Solves the maze using Breadth First Search.

        Returns
        -------
        path : list of tuples
            A list of positions representing the path from the start to the end of the maze.
        """
        start = self.maze.start
        end = self.maze.end

        # Initialize the queue and visited OrderedDict
        self.queue.append(start)
        self.visited[start] = None

        # Keep track of the parent of each position
        parent = {start: None}

        while self.queue:
            current = self.queue.popleft()

            if current == end:
                # Reconstruct the path from end to start
                path = []
                while current is not None:
                    path.append(current)
                    current = parent[current]
                return path[::-1]

            # Get the neighboring positions
            neighbors = self.maze.get_neighbors(current)

            for neighbor in neighbors:
                if neighbor not in self.visited:
                    self.queue.append(neighbor)
                    self.visited[neighbor] = None
                    parent[neighbor] = current

        return []  # Return an empty list if no path is found
