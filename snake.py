import pygame, sys
import collections, random

# Random seed for testing purposes
random.seed(101)

pygame.init()

# Board
board_size = width, height = 500, 300
screen = pygame.display.set_mode(board_size, flags=pygame.RESIZABLE)      # returns a new Surface object

# Colors
white = 255, 255, 255
black = 0, 0, 0
red = 255, 0, 0     # reflect red
blue = 0, 0, 255

# Pygame Constants
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

# Snake
snake_unit_size = 10
snake_direction = K_RIGHT
snake_head = [(width/4) // snake_unit_size * snake_unit_size, (height/2) // snake_unit_size * snake_unit_size]     # multiple of snake_unit_size
snake = collections.deque([(snake_head[0] - (i * snake_unit_size), snake_head[1]) 
                            for i in range(10)])

# Food
def generateFoodPos(width, height, food_unit_rad):
    """Generate a random (x,y) food position on a board 
    of size width by height.
    
    Since food is rendered as a circle
    with a center and radius, the position is returned
    as the center of the circle. Positions are assigned in food unit sized increments. """

    return (random.randrange(food_unit_rad, width-food_unit_rad+1, 2*food_unit_rad), 
                random.randrange(food_unit_rad, height-food_unit_rad+1, 2*food_unit_rad))

food_unit_rad = 5
food_center = generateFoodPos(width, height, food_unit_rad)



# Initial rendering
for unit in snake:
    snake_unit_rect = pygame.Rect(unit, (snake_unit_size, snake_unit_size))
    pygame.draw.rect(screen, blue, snake_unit_rect)
food_rect = pygame.draw.circle(screen, red, food_center, food_unit_rad)

while 1:
    for event in pygame.event.get():
        if event.type == QUIT: 
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN or event.type == KEYUP:
            if event.mod == pygame.KMOD_NONE:
                print("No modifier keys were in a" 
                    " pressed state when this event occurred.")
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
        # No user input. Advance one step in dir
        if snake_direction == K_LEFT:
            snake_head[0] -= snake_unit_size
        elif snake_direction == K_RIGHT:
            snake_head[0] += snake_unit_size
        elif snake_direction == K_UP:
            snake_head[1] -= snake_unit_size
        elif snake_direction == K_DOWN:
            snake_head[1] += snake_unit_size
        
    # Wall collision
    if snake_head[0] < 0 or snake_head[0] >= width       \
    or snake_head[1] < 0 or snake_head[1] >= height:
        print("Snake out of bounds")
        break;
    
    # Self collision
    if tuple(snake_head) in snake:
        print("Snake hit itself")
        break;
    
    # Food collision
    snake_head_rect = pygame.Rect(snake_head, (snake_unit_size, snake_unit_size))
    if snake_head_rect.colliderect(food_rect):
        food_center = generateFoodPos(width, height, food_unit_rad)
        snake.appendleft(tuple(snake_head))
    else:
        snake.appendleft(tuple(snake_head))
        snake.pop()

    # Render new states
    screen.fill(white)

    for unit in snake:
        snake_unit_rect = pygame.Rect(unit, (snake_unit_size, snake_unit_size))
        pygame.draw.rect(screen, blue, snake_unit_rect)
    food_rect = pygame.draw.circle(screen, red, food_center, food_unit_rad)

    pygame.display.flip() #or update
    pygame.time.delay(50)


# Freeze the state of snake on game over
pygame.time.delay(500)
screen.fill(white)

# Render game over
while 1:
    for event in pygame.event.get():
        if event.type == QUIT: 
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN or event.type == KEYUP:
            if event.mod == pygame.KMOD_NONE:
                print("No modifier keys were in a pressed " 
                    "state when this event occurred.")
            else:
                if event.mod & KMOD_LCTRL and event.key == K_w:
                    pygame.quit()
                    sys.exit()

    font = pygame.font.SysFont(None, size=40)
    endgame_screen = font.render("game over. try again?",
                                True, black)
    screen.blit(endgame_screen, (width/4, height/2))
    pygame.display.flip()
    pygame.time.delay(500)