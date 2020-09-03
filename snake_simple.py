import pygame, sys
import collections, random

# Random seed for testing purposes
random.seed(101)

pygame.init()

# Board
board_size = width, height = 500, 300
score_bar_size = width, 30

# Screen
screen_size = board_size[0], board_size[1] + score_bar_size[1]
screen = pygame.display.set_mode(screen_size, flags=pygame.RESIZABLE)      # returns a new Surface object


# Colors
white = 255, 255, 255
black = 0, 0, 0
grey = 100, 100, 100
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
snake_unit_size = 18
snake_direction = K_RIGHT
snake_head = pygame.Rect(((width/4) // snake_unit_size * snake_unit_size, (height/2) // snake_unit_size * snake_unit_size), (snake_unit_size, snake_unit_size))     # multiple of snake_unit_size
snake = collections.deque([pygame.Rect((snake_head.x - (i * snake_unit_size), snake_head.y), (snake_unit_size, snake_unit_size)) 
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

food_unit_rad = snake_unit_size // 2
food_center = generateFoodPos(width, height, food_unit_rad)



# Initial rendering
for snake_unit_rect in snake:
    pygame.draw.rect(screen, blue, snake_unit_rect)
food_rect = pygame.draw.circle(screen, red, food_center, food_unit_rad)
score_bar = pygame.Surface((score_bar_size))
score_bar.fill(grey)
screen.blit(score_bar, (0, height))
score = 0

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
        snake_head.x -= snake_unit_size
    elif keys[K_RIGHT] and snake_direction != K_LEFT:
        snake_direction = K_RIGHT
        snake_head.x += snake_unit_size
    elif keys[K_UP] and snake_direction != K_DOWN:
        snake_direction = K_UP
        snake_head.y -= snake_unit_size
    elif keys[K_DOWN] and snake_direction != K_UP:
        snake_direction = K_DOWN
        snake_head.y += snake_unit_size
    else: 
        # No user input. Advance one step in dir
        if snake_direction == K_LEFT:
            snake_head.x -= snake_unit_size
        elif snake_direction == K_RIGHT:
            snake_head.x += snake_unit_size
        elif snake_direction == K_UP:
            snake_head.y -= snake_unit_size
        elif snake_direction == K_DOWN:
            snake_head.y += snake_unit_size
        
    # Wall collision
    if snake_head.x < 0 or snake_head.x >= width       \
    or snake_head.y < 0 or snake_head.y >= height:
        print("Snake out of bounds")
        break;
    
    # Self collision
    if snake_head.collidelist(snake) != -1:
        print("Snake hit itself")
        break;
    
    # Food collision
    if snake_head.colliderect(food_rect):
        score += 1
        food_center = generateFoodPos(width, height, food_unit_rad)
        food_rect = pygame.draw.circle(screen, red, food_center, food_unit_rad)
        while food_rect.collidelist(snake) != -1:
            print("Regenerate food position")
            food_center = generateFoodPos(width, height, food_unit_rad)
            food_rect = pygame.draw.circle(screen, red, food_center, food_unit_rad)
        snake.appendleft(tuple(snake_head))
    else:
        snake.appendleft(tuple(snake_head))
        snake.pop()

    # Render new states
    screen.fill(white)

    for snake_unit_rect in snake:
        pygame.draw.rect(screen, blue, snake_unit_rect)
    food_rect = pygame.draw.circle(screen, red, food_center, food_unit_rad)
    score_bar.fill(grey)
    font = pygame.font.SysFont(None, size=30)
    score_text = font.render("score: " + str(score), True, white)
    screen.blit(score_bar, (0, height))
    screen.blit(score_text, (width - round(1.5*score_text.get_width(),0), height + ((score_bar.get_height() - score_text.get_height()) // 2)))

    pygame.display.flip() #or update
    pygame.time.delay(50)


# On game over, freeze the state of snake
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