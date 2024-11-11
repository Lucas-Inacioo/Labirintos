"""
Main script to visualize the maze solver using Pygame.

This script provides a menu interface for selecting a maze, choosing an AI algorithm,
and running a simulation of the maze-solving process.

Modules:
    - sys: System-specific parameters and functions.
    - pygame: Library for creating graphical interfaces.
    - maze: Contains the Maze class.
    - bfs: Contains the BFS class.
    - alphastar: Contains the AlphaStar (A*) class.
    - constants: Contains color definitions and dimensions.
"""

from pathlib import Path
from typing import Optional
import sys
import pygame
from maze import Maze
from bfs import BFS
from alphastar import AlphaStar
import constants

# Initialize Pygame
pygame.init()
FONT = pygame.font.Font(None, constants.FONT_SIZE)

# Global variables
selected_maze: Optional[str] = None
selected_ai: Optional[str] = None

def draw_button(
    screen: pygame.Surface,
    text: str,
    x: int,
    y: int,
    width: int,
    height: int,
    hover: bool = False
) -> None:
    """
    Draws a button on the Pygame screen.

    Parameters
    ----------
    screen : pygame.Surface
        The Pygame surface to draw the button on.
    text : str
        The text to display on the button.
    x : int
        The x-coordinate of the button.
    y : int
        The y-coordinate of the button.
    width : int
        The width of the button.
    height : int
        The height of the button.
    hover : bool, optional
        Whether the button is being hovered over (default is False).
    """
    color = constants.HOVER_COLOR if hover else constants.BUTTON_COLOR
    pygame.draw.rect(screen, color, (x, y, width, height))
    label = FONT.render(text, True, constants.TEXT_COLOR)
    label_rect = label.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(label, label_rect)


def select_maze(screen: pygame.Surface) -> None:
    """
    Displays a menu for selecting a maze file.

    Parameters
    ----------
    screen : pygame.Surface
        The Pygame surface to display the menu on.
    """
    global selected_maze

    # Specify the directory containing your maze files
    # Here we get the actual directory path and joins the /mazes directory
    maze_dir = Path(__file__).resolve().parent / "mazes"

    # Retrieve all .txt files from the specified directory
    maze_files = [f.name for f in maze_dir.glob("*.txt")]

    while True:
        screen.fill(constants.BG_COLOR)
        mouse_pos = pygame.mouse.get_pos()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Check for mouse button click
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i, maze_file in enumerate(maze_files):
                    y = 100 + i * (constants.BUTTON_HEIGHT + 10)
                    button_rect = pygame.Rect(
                        100,
                        y,
                        constants.BUTTON_WIDTH,
                        constants.BUTTON_HEIGHT
                    )
                    if button_rect.collidepoint(event.pos):
                        selected_maze = maze_dir / maze_file  # Combine directory and file name
                        return

        # Draw buttons and handle hover effect
        for i, maze_file in enumerate(maze_files):
            y = 100 + i * (constants.BUTTON_HEIGHT + 10)
            button_rect = pygame.Rect(100, y, constants.BUTTON_WIDTH, constants.BUTTON_HEIGHT)
            hover = button_rect.collidepoint(mouse_pos)
            draw_button(
                screen,
                maze_file,
                button_rect.x,
                button_rect.y,
                button_rect.width,
                button_rect.height,
                hover
            )

        pygame.display.flip()


def select_ai(screen: pygame.Surface) -> None:
    """
    Displays a menu for selecting an AI algorithm.

    Parameters
    ----------
    screen : pygame.Surface
        The Pygame surface to display the menu on.
    """
    global selected_ai
    ai_algorithms = [("BFS", BFS), ("A*", AlphaStar)]

    while True:
        screen.fill(constants.BG_COLOR)
        for i, (name, _) in enumerate(ai_algorithms):
            y = 100 + i * (constants.BUTTON_HEIGHT + 10)
            hover = pygame.mouse.get_pos()[1] in range(y, y + constants.BUTTON_HEIGHT)
            draw_button(screen, name, 100, y, constants.BUTTON_WIDTH, constants.BUTTON_HEIGHT, hover)

            if hover and pygame.mouse.get_pressed()[0]:
                selected_ai = name
                return

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


def simulate(screen: pygame.Surface) -> None:
    """
    Runs the simulation of the maze-solving process using the selected algorithm.

    Parameters
    ----------
    screen : pygame.Surface
        The Pygame surface to display the simulation on.
    """
    if not selected_maze or not selected_ai:
        print("Error: Maze and AI algorithm must be selected before simulation.")
        return

    try:
        maze = Maze(selected_maze)
    except Exception as exc:
        print(f"Failed to load maze: {exc}")
        return

    solver = BFS(maze) if selected_ai == "BFS" else AlphaStar(maze)
    solution = solver.solve()

    if not solution:
        print("No solution found.")
        return

    grid_width = len(maze.grid[0])
    grid_height = len(maze.grid)
    cell_size = min(constants.SCREEN_WIDTH // grid_width, constants.SCREEN_HEIGHT // grid_height)
    clock = pygame.time.Clock()

    while True:
        screen.fill(constants.BG_COLOR)

        # Draw the maze
        for y, row in enumerate(maze.grid):
            for x, cell in enumerate(row):
                color = constants.COLORS.get(cell, (200, 200, 200))
                rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
                pygame.draw.rect(screen, color, rect)

        # Mark visited positions
        for position in solver.visited:
            x, y = position
            if maze.grid[y][x] == 0:
                pygame.draw.rect(
                    screen,
                    constants.COLORS[5],
                    (x * cell_size, y * cell_size, cell_size, cell_size)
                )
            pygame.display.flip()

        # Mark the solution path
        for position in solution[1:-1]:
            x, y = position
            pygame.draw.rect(
                screen,
                constants.COLORS[4],
                (x * cell_size, y * cell_size, cell_size, cell_size)
            )
            pygame.display.flip()

        clock.tick(60)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()


def main_menu(screen: pygame.Surface) -> None:
    """
    Displays the main menu for the maze solver application.

    Parameters
    ----------
    screen : pygame.Surface
        The Pygame surface to display the menu on.
    """
    while True:
        screen.fill(constants.BG_COLOR)
        mouse_pos = pygame.mouse.get_pos()

        # Define buttons
        select_maze_button = pygame.Rect(100, 100, constants.BUTTON_WIDTH, constants.BUTTON_HEIGHT)
        select_ai_button = pygame.Rect(100, 200, constants.BUTTON_WIDTH, constants.BUTTON_HEIGHT)
        simulate_button = pygame.Rect(100, 300, constants.BUTTON_WIDTH, constants.BUTTON_HEIGHT)

        # Draw buttons
        draw_button(
            screen,
            "Select Maze",
            select_maze_button.x,
            select_maze_button.y,
            constants.BUTTON_WIDTH,
            constants.BUTTON_HEIGHT,
            select_maze_button.collidepoint(mouse_pos)
        )
        draw_button(
            screen,
            "Select AI",
            select_ai_button.x,
            select_ai_button.y,
            constants.BUTTON_WIDTH,
            constants.BUTTON_HEIGHT,
            select_ai_button.collidepoint(mouse_pos)
        )
        draw_button(
            screen,
            "Simulate",
            simulate_button.x,
            simulate_button.y,
            constants.BUTTON_WIDTH,
            constants.BUTTON_HEIGHT,
            simulate_button.collidepoint(mouse_pos)
        )

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if select_maze_button.collidepoint(mouse_pos):
                    select_maze(screen)
                elif select_ai_button.collidepoint(mouse_pos):
                    select_ai(screen)
                elif simulate_button.collidepoint(mouse_pos):
                    simulate(screen)

if __name__ == "__main__":
    SCREEN = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
    pygame.display.set_caption("Maze Solver")
    main_menu(SCREEN)
    pygame.quit()
