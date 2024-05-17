from snakegame import SnakeGame
from pygame.math import Vector2

# Q-learning
import numpy as np
import random

dir_map = {
    (1, 0): 0,
    (0, 1): 1,
    (-1, 0): 2,
    (0, -1): 3
}

rev_dir_map = {
    0: Vector2(1, 0),
    1: Vector2(0, 1),
    2: Vector2(-1, 0),
    3: Vector2(0, -1)
}

class QSnakeGame(SnakeGame):
    # head spaces = 20 x 20
    # apple up/down = 3
    # apple left/right = 3
    # can move straight = 2
    # can move left = 2
    # can move right = 2
    # curr direction = 4
    observation_space = (20 * 20) * 3 * 3 * 2 * 2 * 2 * 4
    action_space = 4

    def __init__(self):
        super().__init__()

    def encode(self):
        # encode state into one number following observation space order
        if not (0 <= self.snake.body[0].x < 20 and 0 <= self.snake.body[0].y < 20):
            return None

        encoded_state = 0
        head = self.snake.body[0]
        encoded_state += head.x
        encoded_state *= 20
        encoded_state += head.y
        encoded_state *= 3

        if self.apple.pos.x > head.x:
            encoded_state += 1
        elif self.apple.pos.x < head.x:
            encoded_state += 2
        encoded_state *= 3

        if self.apple.pos.y > head.y:
            encoded_state += 1
        elif self.apple.pos.y < head.y:
            encoded_state += 2
        encoded_state *= 2
        
        left, straight, right = self.can_move_where()
        encoded_state += straight
        encoded_state *= 2
        encoded_state += left
        encoded_state *= 2
        encoded_state += right
        encoded_state *= 4
        
        encoded_state += dir_map[(self.snake.direction.x, self.snake.direction.y)]
        
        return int(encoded_state)

    def decode(self, encoded_state):
        # decode state from encoded state
        direction = encoded_state % 4
        encoded_state //= 4
        right = encoded_state % 2
        encoded_state //= 2
        left = encoded_state % 2
        encoded_state //= 2
        straight = encoded_state % 2
        encoded_state //= 2
        apple_y = encoded_state % 3
        encoded_state //= 3
        apple_x = encoded_state % 3
        encoded_state //= 3
        head_y = encoded_state % 20
        encoded_state //= 20
        head_x = encoded_state % 20
        return head_x, head_y, apple_x, apple_y, straight, left, right, direction
    
    def can_move_where(self):
        head = self.snake.body[0]
        direction = self.snake.direction
        left = Vector2(direction.y, -direction.x)
        right = Vector2(-direction.y, direction.x)
        
        left = head + left
        right = head + right
        
        can_move = [0, 0, 0]
        if 0 <= left.x < 20 and 0 <= left.y < 20 and left not in self.snake.body:
            can_move[0] = 1
        if 0 <= right.x < 20 and 0 <= right.y < 20 and right not in self.snake.body:
            can_move[2] = 1
        if head + direction not in self.snake.body and  0 <= (head + direction).x < 20 and 0 <= (head + direction).y < 20:
            can_move[1] = 1
        return can_move
        

    def reset(self):
        return super().reset()

    def step(self, action):
        self.snake.direction = rev_dir_map[action]
        self.update()
        new_encode = self.encode()
        if new_encode is None:
            self.end = True
        return new_encode

    def sample(self):
        return random.randint(0,3) 

class QTable:
    def __init__(self, observation_space, action_space, alpha, gamma):
        self.q_table = np.zeros([observation_space, action_space])
        self.observation_space = observation_space
        self.action_space = action_space
        self.alpha = alpha
        self.gamma = gamma

    def get_action(self, state, epsilon):
        if random.uniform(0, 1) < epsilon:
            return random.randint(0, self.action_space - 1)
        else:
            return np.argmax(self.q_table[state])

    def update(self, state, action, next_state, SNAKE_GAME, ohead_x, ohead_y, oapple_x, oapple_y):
        alpha = self.alpha
        gamma = self.gamma

        if next_state is None:
            reward = -5
            new_value = (1 - alpha) * self.q_table[state, action] + alpha * reward
        else:
            nhead_x, nhead_y = SNAKE_GAME.snake.body[0].x, SNAKE_GAME.snake.body[0].y
            napple_x, napple_y = SNAKE_GAME.apple.pos.x, SNAKE_GAME.apple.pos.y
            oapple_dist = abs(ohead_x - oapple_x) + abs(ohead_y - oapple_y)
            napple_dist = abs(nhead_x - napple_x) + abs(nhead_y - napple_y)
            if oapple_x != napple_x or oapple_y != napple_y:
                reward = 10
            elif oapple_dist > napple_dist:
                reward = 1
            else:
                reward = -1

            next_max = np.max(self.q_table[next_state])
            new_value = (1 - alpha) * self.q_table[state, action] + alpha * (reward + gamma * next_max)
        self.q_table[state, action] = new_value
    

# Hyperparameters
alpha = 0.5
gamma = 0.9
epsilon = 0.1

# Initialize Q-table
qSnake = QSnakeGame()
q_table = QTable(QSnakeGame.observation_space, QSnakeGame.action_space, alpha, gamma)

for i in range(1, 10001):
    qSnake.reset()
    state = qSnake.encode()
    
    while qSnake.end == False:
        action = q_table.get_action(state, epsilon)
        ohead_x, ohead_y = qSnake.snake.body[0].x, qSnake.snake.body[0].y
        oapple_x, oapple_y = qSnake.apple.pos.x, qSnake.apple.pos.y
        next_state = qSnake.step(action)

        q_table.update(state, action, next_state, qSnake, ohead_x, ohead_y, oapple_x, oapple_y)

        state = next_state
    
    if i % 1000 == 0:
        print(f"Episode: {i}")

print("Training finished.\n")

# Simulate one game and visualize with pygame
actions = []
state = qSnake.reset()
state = qSnake.encode()
while not qSnake.end:
    action = np.argmax(q_table.q_table[state])
    actions.append(action)
    state = qSnake.step(action)


from GenerateGif import generateImgs, to_gif
imgs = generateImgs(actions)
to_gif(imgs, "qlearn_snake.gif")