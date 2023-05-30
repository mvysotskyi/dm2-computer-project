'''
Visualisation of forest fire.
'''
import pygame
pygame.init()

BLACK = (0, 0, 0)
ANT_COLOR = (0, 0, 0)
EMPTY_COLOR = (198,229,0)
FOOD_COLOR = (0, 223, 0)
BLUE_COLOR = (0, 189, 218)
PURPLE_COLOR = (242, 0, 250)
RED_COLOR = (250, 0, 0)
OBSTACLE_COLOR = (153,76,0)
WHITE = (260,260,260)
FIRESCREEN_WIDTH = 500
FIRESCREEN_HEIGHT = 500 

fire_screen = pygame.display.set_mode((FIRESCREEN_WIDTH, FIRESCREEN_HEIGHT ))
pygame.display.set_caption("Forest fire simulation")

def draw_board(screen, board, height, width, cell_size):
    '''
    Draws a board for each generation.
    '''
    screen.fill(BLACK)
    screen_width = screen.get_width()
    for row in range(height):
        for col in range(width):
            cell_state = board[row][col]
            cell_color = 0

            if cell_state == 1:
                cell_color = ANT_COLOR
            elif cell_state == 0:
                cell_color = EMPTY_COLOR
            elif cell_state == -3:
                cell_color = FOOD_COLOR
            elif cell_state == -1:
                cell_color = OBSTACLE_COLOR
            elif cell_state == -4 :
                cell_color = BLUE_COLOR
            elif cell_state == -5:
                cell_color = RED_COLOR
            elif cell_state == -6:
                cell_color = PURPLE_COLOR
            elif cell_color == 2:
                cell_color = WHITE
            pygame.draw.rect(screen, cell_color, (col * cell_size, \
                            row * cell_size, cell_size, cell_size))




    pygame.display.flip()
