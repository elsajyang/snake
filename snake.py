import pygame, sys
import collections

pygame.init()

board_size = width, height = 500, 250
screen = pygame.display.set_mode(board_size, flags=pygame.RESIZABLE)      # returns a new Surface object

white = 255, 255, 255
black = 0, 0, 0
red = 255, 0, 0     # reflect red
blue = 0, 0, 255

snake_unit_size = 10

snake = collections.deque([(width/4 - (i * snake_unit_size), height/2) for i in range(5)])
for unit in snake:
    snake_unit_rect = pygame.Rect(unit, (snake_unit_size, snake_unit_size))
    pygame.draw.rect(screen, blue, snake_unit_rect)

while 1:
    event = pygame.event.poll()
    
    if event.type == pygame.QUIT: sys.exit()

    screen.fill(white)

    for unit in snake:
        snake_unit_rect = pygame.Rect(unit, (snake_unit_size, snake_unit_size))
        pygame.draw.rect(screen, blue, snake_unit_rect)

    pygame.display.flip() #or update


