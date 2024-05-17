# SnakeShenanigans
Made Snake Game and run some solving algorithms on it

I know that the Hamiltonian path actions running over and over will eventually lead to the maximum snake score. However, the way I am generating gifs and such will run out of memory before that.

Q-Learning was the main point of the project. It isn't the greatest, and it is nowhere near perfect. However I learned a lot about how to make reward functions and what leads to more efficient training. Also I learned about what to feed the model in the encoding so that there are not 100 trillion possible states. The simplification I probably accounts for all of the error which I understand.


To check out the code, run the individual python files. \
Running snakegame.py gives you the game for you to play \
Running qLearnSnake.py has the agent qLearn the game \
Running HamiltonianSnake.py generates the gif of two hamiltonian cycles because of memory constraints.

Be sure to check out the generated gifs!
