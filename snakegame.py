import pygame
import random
from pygame.math import Vector2
import numpy as np

tile_size = 40
tile_count = 20

class Apple:
    def __init__(self):
        x = random.randint(0, tile_count-1)
        y = random.randint(0, tile_count-1)
        self.pos = Vector2(x, y) 

    def draw(self, screen):
        pygame.draw.rect(screen, (200, 15, 15), (int(self.pos.x * tile_size), int(self.pos.y * tile_size), tile_size, tile_size))
        # pygame.draw.circle(screen, (200, 15, 15), (int(self.pos.x * tile_size + tile_size // 2), int(self.pos.y * tile_size + tile_size // 2)), tile_size // 2 - 2)


class Snake:
    def __init__(self):
        self.body = [Vector2(tile_count // 2, tile_count // 2), Vector2(tile_count // 2 - 1, tile_count // 2), Vector2(tile_count // 2 - 2, tile_count // 2)]
        self.direction = Vector2(1, 0)
        self.new_block = False

    def draw(self, screen):
        for block in self.body:
            pygame.draw.rect(screen, (60, 180, 60), (int(block.x * tile_size), int(block.y * tile_size), tile_size, tile_size))

    def move(self):
        if self.new_block:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True

    def reset(self):
        self.body = [Vector2(tile_count // 2, tile_count // 2), Vector2(tile_count // 2 - 1, tile_count // 2), Vector2(tile_count // 2 - 2, tile_count // 2)]
        self.direction = Vector2(1, 0)
        self.new_block = False
        self.score = 0

class Text:
    def __init__(self, text, size, color, pos, centered=False):
        self.text = text
        self.size = size
        self.color = color
        self.pos = pos
        self.centered = centered
        self.font = pygame.font.Font(None, self.size)
        self.render = self.font.render(self.text, True, self.color)

    def draw(self, screen,):
        if self.centered:
            screen.blit(self.render, (screen.get_width() // 2 - self.render.get_width() // 2, screen.get_height() // 2 - self.render.get_height() // 2))
        else:
            screen.blit(self.render, self.pos)
    
    def get_height(self):
        return self.render.get_height()

    def get_width(self):
        return self.render.get_width()


class EndScreen:
    def __init__(self, screen, score):
        self.game_over_text = Text("Game Over", 48, (255, 255, 255), (screen.get_width() // 2, screen.get_height() // 2), centered=True)
        self.final_score_text = Text(f"Score: {score}", 24, (255, 255, 255), (screen.get_width() // 2, screen.get_height() // 2 + self.game_over_text.get_height()), centered=True)
        self.restart_text = Text("Press R to restart", 24, (255, 255, 255), (screen.get_width() // 2, screen.get_height() // 2 + self.game_over_text.get_height() + self.final_score_text.get_height()), centered=True)

    def draw(self):
        self.game_over_text.draw(screen)
        self.final_score_text.draw(screen)
        self.restart_text.draw(screen)

class SnakeGame:
    def __init__(self):
        self.snake = Snake()
        self.apple = Apple()
        while self.apple.pos in self.snake.body:
            self.apple = Apple()
        self.score = 0
        self.end = False

    def get_state(self):
        state = np.zeros((tile_count, tile_count))
        state[int(self.snake.body[0].x)][int(self.snake.body[0].y)] = 2
        for block in self.snake.body[1:]:
            state[int(block.x)][int(block.y)] = 1
        state[int(self.apple.pos.x)][int(self.apple.pos.y)] = 3
        return state
    
    def update(self):
        self.snake.move()
        self.check_collision()
        self.check_fail()
        if self.end:
            return None
        return self.get_state()
    
    def draw_elements(self, screen):
        screen.fill((0,0,0))
        self.snake.draw(screen)
        self.apple.draw(screen)
        return screen

    def check_collision(self):
        if self.snake.body[0] == self.apple.pos:
            self.snake.add_block()
            self.apple = Apple()
            while self.apple.pos in self.snake.body:
                self.apple = Apple()
            self.score += 1
    
    def check_fail(self):
        if not 0 <= self.snake.body[0].x < tile_count or not 0 <= self.snake.body[0].y < tile_count:
            self.game_over()
        elif self.snake.body[0] in self.snake.body[1:]:
            self.game_over()
    
    def game_over(self):
        self.end = True
    
    def reset(self):
        self.snake.reset()
        self.apple = Apple()
        while self.apple.pos in self.snake.body:
            self.apple = Apple()
        self.score = 0
        self.end = False
        return self.get_state()
    

if __name__ == "__main__":
    pygame.init()

    screen = pygame.display.set_mode((tile_size * tile_count, tile_size * tile_count))
    pygame.display.set_caption("Snake Game")
    clock = pygame.time.Clock()

    gaming = True

    SCREEN_UPDATE = pygame.USEREVENT
    pygame.time.set_timer(SCREEN_UPDATE, 150)

    LEFT = Vector2(-1, 0)
    RIGHT = Vector2(1, 0)
    UP = Vector2(0, -1)
    DOWN = Vector2(0, 1)

    main_game = SnakeGame()

    while gaming:
        while not main_game.end:
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    main_game.end = True
                    gaming = False
                if event.type == SCREEN_UPDATE:
                    main_game.update()
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_UP, pygame.K_w) and main_game.snake.direction != DOWN:
                        main_game.snake.direction = UP
                    elif event.key in (pygame.K_DOWN, pygame.K_s) and main_game.snake.direction != UP:
                        main_game.snake.direction = DOWN
                    elif event.key in (pygame.K_LEFT, pygame.K_a) and main_game.snake.direction != RIGHT: 
                        main_game.snake.direction = LEFT
                    elif event.key in (pygame.K_RIGHT, pygame.K_d) and main_game.snake.direction != LEFT:
                        main_game.snake.direction = RIGHT
                    
            # checker the board
            for row in range(tile_count):
                for col in range(tile_count):
                    if (row + col) % 2 == 0:
                        pygame.draw.rect(screen, (50, 50, 50), (row * tile_size, col * tile_size, tile_size, tile_size))
                    else:
                        pygame.draw.rect(screen, (60, 60, 60), (row * tile_size, col * tile_size, tile_size, tile_size))
            main_game.draw_elements(screen)
            score_font = pygame.font.Font(None, 24)
            score_text = score_font.render(f"Score: {main_game.score}", True, (255, 255, 255))
            screen.blit(score_text, (10, 10))

            pygame.display.flip()
            clock.tick(60)

        end_screen = EndScreen(screen, main_game.score)
        end_screen.draw()
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gaming = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    main_game.reset()

        clock.tick(60)

    pygame.quit()