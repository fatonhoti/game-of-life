from sys import exit

import pygame

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

ALIVE = 1
DEAD = 0

pygame.init()

PADDING = 10
CELL_SIZE = 10
MATRIX_SIZE = 80

BOARD_WIDTH = (MATRIX_SIZE * CELL_SIZE) + (MATRIX_SIZE * 1) + (4 * PADDING)
BOARD_HEIGHT = (MATRIX_SIZE * CELL_SIZE) + (MATRIX_SIZE * 1) + (4 * PADDING)

screen = pygame.display.set_mode((BOARD_WIDTH, BOARD_HEIGHT))
pygame.display.set_caption("Game of Life")

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Create a matrix of cells
board = []
for x in range(MATRIX_SIZE):
    r = []
    for y in range(MATRIX_SIZE):
        r.append([x, y, DEAD])
    board.append(r)


def count_neighbours(cell):

    """
    Counts the neighbours of a cell including diagonal ones.
    """

    r, c, cell_state = cell
    neighbours = 0

    starting_row = r if (r - 1) < 0 else r - 1
    ending_row = r + 1 if (r + 1) < MATRIX_SIZE else r

    starting_col = c if (c - 1) < 0 else c - 1
    ending_col = c + 1 if (c + 1) < MATRIX_SIZE else c

    for row in range(starting_row, ending_row + 1):
        for col in range(starting_col, ending_col + 1):
            if (col, row) != (c, r) and board[row][col][2] == ALIVE:
                neighbours += 1
    return neighbours


def update_cells():

    """
    Simultaneously update the game-state of the cells
    """

    global board

    from copy import deepcopy

    board_ = deepcopy(board)
    assert id(board_) != id(board)
    for row in board:
        for cell in row:
            r, c, cell_state = cell
            amount_of_neighbours = count_neighbours(cell)
            if (cell_state == DEAD and amount_of_neighbours == 3) or (
                cell_state == ALIVE and amount_of_neighbours in [2, 3]
            ):
                board_[r][c][2] = ALIVE
            else:
                board_[r][c][2] = DEAD
    board = deepcopy(board_)


def draw_cell(cell):

    """
    Draws a cell on the screen
    """

    y, x, cell_state = cell

    outer_rect = pygame.Rect(
        20 + (x * (CELL_SIZE + 1)), 20 + (y * (CELL_SIZE + 1)), CELL_SIZE, CELL_SIZE
    )
    pygame.draw.rect(screen, BLACK, outer_rect)

    inner_rect = pygame.Rect(
        20 + (x * (CELL_SIZE + 1) + 1),
        20 + (y * (CELL_SIZE + 1) + 1),
        CELL_SIZE - 2,
        CELL_SIZE - 2,
    )

    if cell_state == DEAD:
        pygame.draw.rect(screen, BLACK, inner_rect)
    else:
        pygame.draw.rect(screen, GREEN, inner_rect)


def draw_board():

    """
    Draws the full board of cells
    """

    for row in board:
        for cell in row:
            draw_cell(cell)


def run():
    
    from random import random

    # Generate a random board of cells
    for row in board:
        for cell in row:
            board[cell[0]][cell[1]][2] = round(random())

    # -------- Main Program Loop -----------
    done = False
    while not done:
        # --- Main event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        # --- Game logic
        update_cells()

        # --- Screen-clearing
        screen.fill(BLACK)

        # --- Drawing
        pygame.draw.rect(
            screen,
            WHITE,
            (19, 19, BOARD_WIDTH - 4 * PADDING + 1, BOARD_HEIGHT - 4 * PADDING + 1),
            1,
        )  # Draws a white frame around the board
        draw_board()

        # --- Update the screen
        pygame.display.flip()

        # --- Limit to 10 frames per second
        clock.tick(10)

    # Close the window and quit.
    pygame.quit()
    exit()


if __name__ == "__main__":
    run()
