import pygame, sys
import collections

pygame.init()

board_size = width, height = 500, 250
screen = pygame.display.set_mode(board_size, flags=pygame.RESIZABLE)      # returns a new Surface object

white = 255, 255, 255
black = 0, 0, 0
red = 255, 0, 0     # reflect red
blue = 0, 0, 255

QUIT = pygame.QUIT
KEYDOWN = pygame.KEYDOWN
KEYUP = pygame.KEYUP
K_LEFT = pygame.K_LEFT
K_RIGHT = pygame.K_RIGHT
K_UP = pygame.K_UP
K_DOWN = pygame.K_DOWN
KMOD_LCTRL = pygame.KMOD_LCTRL
K_w = pygame.K_w
pygame.key.set_repeat(100) # (delay, interval)

snake_unit_size = 10
snake_direction = K_RIGHT
snake_head = [width/4, height/2]

snake = collections.deque([(snake_head[0] - (i * snake_unit_size), snake_head[1]) 
                            for i in range(10)])
for unit in snake:
    snake_unit_rect = pygame.Rect(unit, (snake_unit_size, snake_unit_size))
    pygame.draw.rect(screen, blue, snake_unit_rect)

while 1:
    for event in pygame.event.get():
        if event.type == QUIT: 
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN or event.type == KEYUP:
            if event.mod == pygame.KMOD_NONE:
                print("No modifier keys were in a pressed" 
                    "state when this event occurred.")
            else:
                if event.mod & KMOD_LCTRL and event.key == K_w:
                    pygame.quit()
                    sys.exit()

    keys = pygame.key.get_pressed()
    if keys[K_LEFT] and snake_direction != K_RIGHT:
        snake_direction = K_LEFT
        snake_head[0] -= snake_unit_size
    elif keys[K_RIGHT] and snake_direction != K_LEFT:
        snake_direction = K_RIGHT
        snake_head[0] += snake_unit_size
    elif keys[K_UP] and snake_direction != K_DOWN:
        snake_direction = K_UP
        snake_head[1] -= snake_unit_size
    elif keys[K_DOWN] and snake_direction != K_UP:
        snake_direction = K_DOWN
        snake_head[1] += snake_unit_size
    else: 
        # no keys pressed, move one step in dir
        if snake_direction == K_LEFT:
            snake_head[0] -= snake_unit_size
        elif snake_direction == K_RIGHT:
            snake_head[0] += snake_unit_size
        elif snake_direction == K_UP:
            snake_head[1] -= snake_unit_size
        elif snake_direction == K_DOWN:
            snake_head[1] += snake_unit_size 
    snake.appendleft(tuple(snake_head))
    snake.pop()


    screen.fill(white)

    for unit in snake:
        snake_unit_rect = pygame.Rect(unit, (snake_unit_size, snake_unit_size))
        pygame.draw.rect(screen, blue, snake_unit_rect)

    pygame.display.flip() #or update
    pygame.time.delay(30)

