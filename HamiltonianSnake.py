from snakegame import SnakeGame
from GenerateGif import generateImgs, to_gif

# Hamiltonian cycle actions for 20x20 grid starting at 10, 10
# moving right
# 0 is right, 1 is down, 2 is left, 3 is up
def get_actions_hamiltonian():
    actions = []
    for _ in range(9):
        actions.append(0)
    
    actions.append(1)
    for _ in range(4):
        for _ in range(18):
            actions.append(2)
        actions.append(1)    
        for _ in range(18):
            actions.append(0)
        actions.append(1)

    for _ in range(19):
        actions.append(2)
    for _ in range(19):
        actions.append(3)
    
    actions.append(0)
    for _ in range(5):
        for _ in range(18):
            actions.append(0)
        actions.append(1)
        for _ in range(18):
            actions.append(2)
        actions.append(1)
    for _ in range(9):
        actions.append(0)
    return actions

actions = get_actions_hamiltonian()
for i in range(2):
    actions.extend(actions)
# Generate images of the game
images = generateImgs(actions)
to_gif(images, "hamiltonian.gif")