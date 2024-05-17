import pygame
from pygame.math import Vector2
from snakegame import SnakeGame

def generateImgs(actions):
    rev_dir_map = {
        0: Vector2(1, 0),
        1: Vector2(0, 1),
        2: Vector2(-1, 0),
        3: Vector2(0, -1)
    }
    pygame.init()
    screen = pygame.display.set_mode((800, 800))
    game = SnakeGame()
    game.reset()
    images = []
    for action in actions:
        images.append(pygame.surfarray.array3d(game.draw_elements(screen)))
        game.snake.direction = rev_dir_map[action]
        game.update()
    images.append(pygame.surfarray.array3d(game.draw_elements(screen)))
    pygame.quit()
    return images

def to_gif(images, filename):
    import imageio
    imageio.mimsave(filename, images)