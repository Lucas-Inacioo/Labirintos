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

# Define button dimensions and colors
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50
BUTTON_COLOR = (100, 100, 255)
HOVER_COLOR = (150, 150, 255)

# Define font size and colors
FONT_SIZE = 24
BG_COLOR = (30, 30, 30)
TEXT_COLOR = (255, 255, 255)
