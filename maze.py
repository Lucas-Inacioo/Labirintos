"""
Module that contains the Maze class, which is used to represent a maze.

Classes
-------
    Maze
"""

class Maze:
    """
    Class that represents a maze.

    Attributes
    ----------
    grid : list of lists
        A 2D grid representing the maze layout.
    start : tuple
        Coordinates (x, y) of the start position in the maze.
    end : tuple
        Coordinates (x, y) of the end position in the maze.

    Methods
    -------
    read_maze(maze_file)
        Reads the maze from a file and initializes the grid, start, and end attributes.
    get_neighbors(position)
        Returns a list of accessible neighboring positions from the given position.
    is_valid_position(position)
        Checks if a position is within the maze bounds and not a barrier.
    """

    def __init__(self, maze_file: str) -> None:
        """
        Initializes the Maze class by reading the maze from a file.

        Parameters
        ----------
        maze_file : str
            The name of the file that contains the maze.
        """
        self.grid = []
        self.start = None
        self.end = None
        self.read_maze(maze_file)

    def read_maze(self, maze_file: str) -> None:
        """
        Reads the maze from a file and initializes the grid, start, and end attributes.

        Parameters
        ----------
        maze_file : str
            The name of the file that contains the maze.
        """
        try:
            with open(maze_file, 'r', encoding='utf-8') as f:
                for y, line in enumerate(f):
                    row = []
                    # Remove whitespace and split the line into characters
                    elements = line.strip().split()
                    if not elements:
                        continue
                    for x, value in enumerate(elements[0]):
                        value = int(value)
                        if value not in [0, 1, 2, 3]:
                            raise ValueError(
                                "Invalid value in maze file. Allowed values are 0, 1, 2, 3."
                            )
                        row.append(value)
                        if value == 2:
                            if self.start is not None:
                                raise ValueError("Maze can only have one start position.")
                            self.start = (x, y)
                        elif value == 3 and self.end is None:
                            if self.end is not None:
                                raise ValueError("Maze can only have one end position.")
                            self.end = (x, y)
                    self.grid.append(row)
            if self.start is None or self.end is None:
                raise ValueError("Maze must have start (2) and end (3) positions.")
        except FileNotFoundError:
            print(f"Error: File '{maze_file}' not found.")
            raise
        except ValueError as ve:
            print(f"Error: {ve}")
            raise

    def get_neighbors(self, position: tuple) -> list:
        """
        Returns a list of accessible neighboring positions from the given position.

        Parameters
        ----------
        position : tuple
            The (x, y) coordinates of the current position.

        Returns
        -------
        neighbors : list of tuples
            A list of (x, y) coordinates that are accessible from the current position.
        """
        x, y = position
        neighbors = []
        # Define possible movements: up, down, left, right
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # (dx, dy)
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if self.is_valid_position((nx, ny)):
                neighbors.append((nx, ny))
        return neighbors

    def is_valid_position(self, position: tuple) -> bool:
        """
        Checks if a position is within the maze bounds and not a barrier.

        Parameters
        ----------
        position : tuple
            The (x, y) coordinates to check.

        Returns
        -------
        bool
            True if the position is valid (within bounds and not a barrier), False otherwise.
        """
        x, y = position
        if 0 <= y < len(self.grid) and 0 <= x < len(self.grid[0]):
            # Check if the position is not a barrier (1)
            return self.grid[y][x] != 1
        return False

    def print_maze(self):
        """
        Prints the maze grid to the console for debugging purposes.
        """
        for y, row in enumerate(self.grid):
            row_str = ''
            for x, cell in enumerate(row):
                if (x, y) == self.start:
                    row_str += 'S '  # Start position
                elif (x, y) == self.end:
                    row_str += 'E '  # End position
                elif cell == 1:
                    row_str += '# '  # Barrier
                elif cell == 0:
                    row_str += '. '  # Empty space
                else:
                    row_str += '? '  # Unknown cell type
            print(row_str)
