"""
Main script to visualize the maze using Pygame.
"""

import sys
import pygame
from maze import Maze
from bfs import BFS
from constants import COLORS, SCREEN_WIDTH, SCREEN_HEIGHT

def main() -> None:
    """
    Main function to visualize the maze using Pygame.
    """
    # Create the Maze instance
    maze_file = 'maze11.txt'
    try:
        maze = Maze(maze_file)
    except Exception as e:
        print(f"Failed to load maze: {e}")
        sys.exit(1)

    # Create the BFS instance
    bfs = BFS(maze)
    solution = bfs.solve()

    if not solution:
        print("No solution found.")
        sys.exit(1)

    # Mark the path on the maze grid (except for the start and end positions)
    for position in solution[1:-1]:
        x, y = position
        maze.grid[y][x] = 4

    # Mark the visited positions on the maze grid
    for position in bfs.visited:
        x, y = position
        if maze.grid[y][x] == 0:
            maze.grid[y][x] = 5

    # Calculate the dimensions of the maze display
    grid_width = len(maze.grid[0])
    grid_height = len(maze.grid)
    cell_size = min(SCREEN_WIDTH // grid_width, SCREEN_HEIGHT // grid_height)

    # Initialize Pygame
    pygame.init()

    # Set up the display
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Maze Visualization')

    # Main loop
    running = True
    clock = pygame.time.Clock()

    while running:
        # Limit frame rate to 60 FPS
        clock.tick(60)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Draw the maze
        for y, row in enumerate(maze.grid):
            for x, cell in enumerate(row):
                color = COLORS.get(cell, (200, 200, 200))  # Default color for unknown cells
                rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
                pygame.draw.rect(screen, color, rect)

        # Update the display
        pygame.display.flip()

    # Quit Pygame
    pygame.quit()

if __name__ == '__main__':
    main()
