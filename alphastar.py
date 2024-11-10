"""
Implementing A* Algorithm to solve the maze.

Classes
-------
    AlphaStar
"""

import heapq
from maze import Maze

class AlphaStar:
    """
    Class that represents the A* (AlphaStar) algorithm.

    Attributes
    ----------
    maze : Maze
        The maze to be solved.
    visited : set
        A set to keep track of visited positions in the maze.
    open_set : list
        A priority queue (min-heap) to store the positions to be visited next.
    g_costs : dict
        A dictionary to store the cost from the start to each position.
    f_costs : dict
        A dictionary to store the estimated total cost (g + h) to the goal.
    """

    def __init__(self, maze: Maze) -> None:
        self.maze = maze
        self.visited = set()
        self.open_set = []
        self.g_costs = {}
        self.f_costs = {}

    def heuristic(self, position: tuple) -> int:
        """
        Heuristic function (Manhattan distance).

        Parameters
        ----------
        position : tuple
            The (x, y) coordinates of the current position.

        Returns
        -------
        int
            The Manhattan distance from the current position to the goal.
        """
        x, y = position
        end_x, end_y = self.maze.end
        return abs(x - end_x) + abs(y - end_y)

    def solve(self) -> list:
        """
        Solves the maze using the A* (AlphaStar) algorithm.

        Returns
        -------
        path : list of tuples
            A list of positions representing the path from the start to the end of the maze.
        """
        start = self.maze.start
        end = self.maze.end

        # Initialize the priority queue, g_costs, and f_costs
        heapq.heappush(self.open_set, (0, start))
        self.g_costs[start] = 0
        self.f_costs[start] = self.heuristic(start)
        parent = {start: None}

        while self.open_set:
            _, current = heapq.heappop(self.open_set)

            if current == end:
                # Reconstruct the path
                path = []
                while current is not None:
                    path.append(current)
                    current = parent[current]
                return path[::-1]

            self.visited.add(current)

            for neighbor in self.maze.get_neighbors(current):
                if neighbor in self.visited:
                    continue

                tentative_g_cost = self.g_costs[current] + 1  # Assume uniform cost for all edges

                if neighbor not in self.g_costs or tentative_g_cost < self.g_costs[neighbor]:
                    parent[neighbor] = current
                    self.g_costs[neighbor] = tentative_g_cost
                    self.f_costs[neighbor] = tentative_g_cost + self.heuristic(neighbor)
                    heapq.heappush(self.open_set, (self.f_costs[neighbor], neighbor))

        return []  # Return an empty list if no path is found
