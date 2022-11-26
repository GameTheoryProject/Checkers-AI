import pygame

M, N = 3, 3 # parameter: M, N.
ROWS, COLS = 2 * M, 2 * N
WIDTH, HEIGHT = 600//ROWS*COLS, 600
SQUARE_SIZE = WIDTH//COLS

# rgb
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREY = (128,128,128)

MAX_STEP = 2 * (M-1) * N * 10
WHITE_WIN = "white"
RED_WIN = "red"
DRAW = "draw"

CROWN = pygame.transform.scale(pygame.image.load('assets/crown.png'), (44, 25))
