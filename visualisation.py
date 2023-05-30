'''
Visualisation of forest fire.
'''
from math import ceil
import pygame
pygame.init()

SEARCH_COLOR = (255, 255, 255)
EMPTY_COLOR = (0,0,0)
FOOD_COLOR = (104, 188, 95)
BLUE_COLOR = (0, 189, 218)
PURPLE_COLOR = (242, 0, 250)
RED_COLOR = (250, 0, 0)
OBSTACLE_COLOR = (174,117,68)
BASE_COLOR = (102,0,102)
RETURN_COLOR = (255, 119, 0)

FIRESCREEN_WIDTH = 600
FIRESCREEN_HEIGHT = 600

fire_screen = pygame.display.set_mode((FIRESCREEN_WIDTH, FIRESCREEN_HEIGHT ))
pygame.display.set_caption("Ant colony")

def draw_board(screen, board, height, width, cell_size, maxes):
    '''
    Draws a board for each generation.
    '''
    screen.fill(EMPTY_COLOR)
    for row in range(height):
        for col in range(width):
            cell_state = board[row][col]
            cell_color = 0

            if cell_state == 1:
                cell_color = SEARCH_COLOR
            elif cell_state == -3:
                cell_color = FOOD_COLOR
            elif cell_state == -1:
                cell_color = OBSTACLE_COLOR
            elif cell_state == -4 or cell_state == -7:
                cell_color = BLUE_COLOR
            elif cell_state == -5:
                cell_color = RED_COLOR
            elif cell_state == -6:
                cell_color = PURPLE_COLOR
            elif cell_state == 2:
                cell_color = RETURN_COLOR
            elif cell_state == -2:
                cell_color = BASE_COLOR

            if cell_state != 0:
                if cell_state in (-4, -5, -6):
                    mycircle = pygame.Surface((cell_size, cell_size))
                    mycircle.fill(EMPTY_COLOR)
                    if cell_state == -6:
                        mycircle.set_alpha(ceil((maxes[0][row, col]+maxes[1][row, col])/((maxes[2]+maxes[3])/255))+35)
                    elif cell_state == -5:
                        mycircle.set_alpha(ceil(maxes[1][row, col]/(maxes[3]/255))+35)
                    else:
                        mycircle.set_alpha(ceil(maxes[0][row, col]/(maxes[2]/255))+35)
                    pygame.draw.circle(mycircle, cell_color, (cell_size/1.5,cell_size/1.5), cell_size/1.5)
                    screen.blit(mycircle, (col * cell_size, \
                                    row * cell_size))
                else:
                    myrect = pygame.Surface((cell_size, cell_size))
                    pygame.draw.rect(myrect, cell_color, myrect.get_rect())
                    screen.blit(myrect, (col * cell_size, row * cell_size))

    pygame.display.flip()
