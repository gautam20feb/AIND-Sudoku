# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: Naked twins is another method to reduce the solution space for sudoku along with the already discussed elimination, only choice etc. Therefore, while solving for sudoku, we apply Naked twin also to reduce the search space at each stage.
We make use of the Sudoku constraints while utilising the naked twin technique.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: Diagonal Sudoku is a modified sudoko with addition constraint that the diagonals also have to follow the constraint that along these diagonals, only 1-9 digits come and only once.
Therefore we identify these diagonals as a unit while defining the unit space and therefore, while defining the peers for any box, we also consider the peers along the diagonals(if any).
So, when we apply our sudoku solving techniques, we look into the modified possibilities to reduce the search space.


### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solutions.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Data

The data consists of a text file of diagonal sudokus for you to solve.
