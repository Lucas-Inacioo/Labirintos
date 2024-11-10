"""
File that contains constants used in the maze solver.
"""
# Define colors for different cell types
COLORS = {
    0: (255, 255, 255),  # Empty space - white
    1: (0, 0, 0),        # Barrier - black
    2: (0, 255, 0),      # Start position - green
    3: (255, 0, 0),      # End position - red
    4: (0, 0, 255),      # Path - blue
    5: (255, 255, 0),    # Visited - yellow
}

# Define screen dimensions
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700
