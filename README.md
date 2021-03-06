# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: *Naked twins strategy is just another constraint that is applied to the sudoku grid in order to reduce the solution space.
    The strategy examines all available units (vertical, horizontal, squares) and tries to identify any tiwn boxes in the unit,
    e.g. any boxes with identical two digit values. Since the twin boxes have no other possibilities but the two values assigned to them,
    we can eliminate these values from all other boxes. For example, if we find twin boxes with values 2 and 3 in a square unit, 
    we'll assume that no other boxes in this unit can take on values of either 2 or 3, thus 2 and 3 can be removed from all other squares in this unit.
    In this specific instance, "naked twin" strategy is executed after "only choice" strategy, e.g. after the solution space has already been reduced by "elimination" and "only choice" constraint.*

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: *Diagonal sudoku problem is no different from how constraint propagation is used for the original problem.
    This problem only differs in how the problem units are constructed. In this case there's an addition of 2 diagonal units.
    Each constrain is applied to each unit, including the additional diagonal units. First "elimination" constraint is applied to all units 
    (vertical, horizontal, squares, diagonals), then "only choice" constraint is applied and then "naked twins" is applied to all of the units.
    Moreover, adding diagonal units did not warrant any changes to how constraint propagation is applied.*

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