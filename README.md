# Sudoku Pair Solver and Generator

This is a simple project with 2 python files.

The file solve_sud.py is for solving a pair of Sudokus of given size with non-equal values in corresponding places of both Sudokus.

The file gen_sud.py is for generating a pair of Sudokus of given size.

## Requirements

   - Python v3.x.
   - pysat python package.
   - input csv file(s).


## File I/O

   - All test cases must be inside the "input_a" folder.
   - Name of csv file must be input_k.csv where k is the input value of sudoku size.

## Compiling and Running solve_sud.py

   - To install pysat, use the command -

   - pip install python-sat.

   - To compile and run the given python file, use the following command in command line within the given folder.

   - python solve_sud.py k

      where, k is input argument to command line.


## Test cases

   To edit the test cases go to "input_a" folder and edit the csv files as needed.


## Compiling and Running gen_sud.py

   To install pysat, use the command -

   - pip install python-sat

   To compile and run the given python file, use the following command in command line within the given folder.

   - python gen_sud.py k

      where, k is input argument to command line.
