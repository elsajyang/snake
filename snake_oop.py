import pygame, time, sys
import collections, random

# Random seed for testing purposes
random.seed(101)

pygame.init()

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

# Colors
white = 255, 255, 255
black = 0, 0, 0
grey = 100, 100, 100
red = 255, 0, 0     # reflect red
blue = 0, 0, 255


class SnakeGame:
    width, height = 30, 20
    scale = 20
    running = True

    def __init__(self):
        width = self.width * self.scale
        height = self.height * self.scale

        self.board = pygame.Surface((width, height))
        self.score_bar = pygame.Surface((width, 2 * self.scale))
        window_size = width, height + self.score_bar.get_height()
        self.window = pygame.display.set_mode(window_size, 
                        flags=pygame.RESIZABLE)      
                        # returns a new Surface object
        self.snake = Snake(self.scale)
        # self.food = Food(scale)
        self.score = 0
    
    def render(self):
        self.board.fill(white)
        for unit in self.snake.body:
            pygame.draw.rect(self.board, blue, unit)
        self.window.blit(self.board, (0,0))

        self.score_bar.fill(grey)
        font = pygame.font.SysFont(None, size=2*self.scale)
        score_text = font.render("score: " + str(self.score), True, white)

        self.window.blit(self.score_bar, (0, self.board.get_height()))
        self.window.blit(score_text, (0 + 1*self.scale,
            self.board.get_height() + 0.5*self.scale))

        pygame.display.flip()
        pygame.time.delay(50)
    
    def update(self):
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

        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            self.snake.moveLeft()
        elif keys[K_RIGHT]:
            self.snake.moveRight()
        elif keys[K_UP]:
            self.snake.moveUp()
        elif keys[K_DOWN]:
            self.snake.moveDown()
        # else: 
        #     # No user input. Advance one step in dir
        #     if snake_direction == K_LEFT:
        #         snake_head.x -= snake_unit_size
        #     elif snake_direction == K_RIGHT:
        #         snake_head.x += snake_unit_size
        #     elif snake_direction == K_UP:
        #         snake_head.y -= snake_unit_size
        #     elif snake_direction == K_DOWN:
        #         snake_head.y += snake_unit_size

        # if self.hasCollision():
        #     self.running = False
        #     return

        self.render()
    


class Snake:
    def __init__(self, unit_size):
        self.direction = K_RIGHT
        self.size = unit_size
        self.head = pygame.Rect((SnakeGame.width//4 * self.size, 
                SnakeGame.height//2 * self.size), 
                (self.size, self.size))
        self.body = collections.deque([
                pygame.Rect((self.head.x - (i*self.size), 
                self.head.y), (self.size, self.size)) for i in range(5)])
    
    def moveLeft(self):
        if self.direction != K_RIGHT:
            self.direction = K_LEFT
            self.head.x -= self.size

            new_head = self.head.copy()
            self.body.appendleft(new_head)
            self.body.pop()
    
    def moveRight(self):
        if self.direction != K_LEFT:
            self.direction = K_RIGHT
            self.head.x += self.size

            new_head = self.head.copy()
            self.body.appendleft(new_head)
            self.body.pop()
    
    def moveUp(self):
        if self.direction != K_DOWN:
            self.direction = K_UP
            self.head.y -= self.size

            new_head = self.head.copy()
            self.body.appendleft(new_head)
            self.body.pop()
    
    def moveDown(self):
        if self.direction != K_UP:
            self.direction = K_DOWN
            self.head.y += self.size

            new_head = self.head.copy()
            self.body.appendleft(new_head)
            self.body.pop()

if __name__ == "__main__":
    sg = SnakeGame()
    # sg.start()
    while sg.running:
        sg.update()
    # sg.game_over()
