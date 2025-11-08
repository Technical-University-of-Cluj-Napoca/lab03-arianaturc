import pygame

# some global constants
WIDTH = 900
HEIGHT = 700
GRID_WIDTH = 700

# colors.
# if you find it more suitable, change this dictionary to standalone constants like: RED = (255, 0, 0)
COLORS = {
    'RED': (50, 40, 45),          # closed nodes
    'GREEN': (80, 65, 70),        # open nodes
    'BLUE': (0, 0, 255),          # start node
    'YELLOW': (255, 255, 0),      # end node
    'WHITE': (255, 255, 255),     # unvisited nodes
    'BLACK': (0, 0, 0),           # barrier
    'PURPLE': (180, 150, 200),    # path
    'ORANGE': (255, 165 ,0),      # nodes being considered
    'GREY': (50, 40, 45),         # grid lines
    'TURQUOISE': (64, 224, 208),  # neighbor nodes

    'BACKGROUND': (33, 37, 41),
    'PANEL_BG': (33, 37, 41),
    'BUTTON_BG': (50, 40, 45),
    'BUTTON_HOVER': (73, 80, 87),
    'BUTTON_ACTIVE': (108, 117, 125),
    'PINK' : (80, 70, 75),
    'PINK_G' : (80, 70, 75),
    'TEXT': (248, 249, 250),

}