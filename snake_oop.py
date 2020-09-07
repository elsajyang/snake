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

class Snake:
    def __init__(self, position, unit_size):
        self.direction = K_RIGHT
        self.size = unit_size
        self.head = pygame.Rect(position, (self.size, self.size))
        self.body = collections.deque([
                pygame.Rect((self.head.x - (i*self.size), 
                self.head.y), (self.size, self.size)) for i in range(5)])
    
    def moveLeft(self):
        if self.direction != K_RIGHT:
            self.direction = K_LEFT
            self.head.x -= self.size
    
    def moveRight(self):
        if self.direction != K_LEFT:
            self.direction = K_RIGHT
            self.head.x += self.size
    
    def moveUp(self):
        if self.direction != K_DOWN:
            self.direction = K_UP
            self.head.y -= self.size
    
    def moveDown(self):
        if self.direction != K_UP:
            self.direction = K_DOWN
            self.head.y += self.size
      
    def advance(self):
        new_head = self.head.copy()
        self.body.appendleft(new_head)
        self.body.pop()

    def grow(self):
        new_head = self.head.copy()
        self.body.appendleft(new_head)

    def getDirection(self):
        return self.direction

    def getBody(self):
        return self.body

    def hasCollision(self, board=None):
        if not board:
            if self.head.collidelist(self.body) != -1:
                print("Snake hit itself")
                return True
        else:
            if self.head.x < 0 \
                    or self.head.x >= board.get_width() \
                    or self.head.y < 0  \
                    or self.head.y >= board.get_height():
                print("Snake out of bounds")
                return True

class Food:
    def __init__(self, center, unit_size):
        self.size = unit_size
        self.radius = unit_size // 2
        self.center = center

    def setCenter(self, position):
        self.center = position

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
        self.snake = Snake((self.width//4 * self.scale, self.height//2 * self.scale), self.scale)
        self.food = Food(self.generateFoodPos(self.scale), self.scale)  # Edge case: food generates on snake
        self.score = 0
    
    def generateFoodPos(self, size):
        """Generate a random (x,y) food position on a board 
        of size width by height.
        
        Since food is rendered as a circle
        with a center and radius, the position is returned
        as the center of the circle. Positions are assigned in food unit sized increments. """

        return (random.randrange(0, self.width) * size + (size//2), random.randrange(0, self.height) * size + (size//2)) 

        # return (random.randrange(self.radius, board.get_width() - self.radius, self.size), random.randrange(self.radius, board.get_height() - self.radius, self.size))
    
    def render(self):
        if self.running:
            self.board.fill(white)
            for unit in self.snake.getBody():
                pygame.draw.rect(self.board, blue, unit)
            pygame.draw.circle(self.board, red, self.food.center, self.food.radius)
            self.window.blit(self.board, (0,0))

            self.score_bar.fill(grey)
            font = pygame.font.SysFont(None, size=2*self.scale)
            score_text = font.render("score: " + str(self.score), True, white)

            self.window.blit(self.score_bar, (0, self.board.get_height()))
            self.window.blit(score_text, (0 + 1*self.scale,
                self.board.get_height() + 0.5*self.scale))

            pygame.display.flip()
            pygame.time.delay(50)
        else:
            font = pygame.font.SysFont(None, size=2*self.scale)
            endgame_screen = font.render("game over. try again?",
                                        True, black)
            self.window.blit(endgame_screen,
                (self.window.get_width()//4, self.window.get_height()//2))
            pygame.display.flip()
            pygame.time.delay(500)
    
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
        else:
            if self.snake.getDirection() == K_LEFT:
                self.snake.moveLeft()
            elif self.snake.getDirection() == K_RIGHT:
                self.snake.moveRight()
            elif self.snake.getDirection() == K_UP:
                self.snake.moveUp()
            elif self.snake.getDirection() == K_DOWN:
                self.snake.moveDown()

        if self.snake.hasCollision()    \
                or self.snake.hasCollision(self.board):
            self.running = False
            return
        
        food_rect = pygame.draw.circle(self.board, red, self.food.center, self.food.radius)
        if self.snake.head.colliderect(food_rect):
            self.score += 1
            self.snake.grow()
            while food_rect.collidelist(self.snake.getBody()) != -1:
                print("Regenerate food position")
                self.food.setCenter(self.generateFoodPos(self.food.size))
                food_rect = pygame.draw.circle(self.board, red, self.food.center, self.food.radius)
        else:        
            self.snake.advance()

        self.render()
    
    def gameOver(self):
        # On game over, freeze the state of snake
        pygame.time.delay(500)
        self.window.fill(white)

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
            
            self.render()


if __name__ == "__main__":
    sg = SnakeGame()
    # sg.start()
    while sg.running:
        sg.update()
    sg.gameOver()
