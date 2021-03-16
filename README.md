# SudokuSolverAI

## About the Project

This project demonstrates an approach to solving Sudoku as a Constraint Satisfaction Problem. The implemented code makes use of backtracking and depth-first search to find an appropriate solution to a solvable sudoku board. This program makes use of 5 sudoku solving heuristics to minimize backtracking:

#### Variable Selection Heuristics:
- **Minimum Remaining Value (MRV)**: The empty square with the least number of remaining possible values (smallest domain) is chosen to be filled next
- **Minimum Remaining Value with Degree heuristic as a tie-breaker (MAD)**: The same as MRV, but if there are multiple squares with the same minimum domain, a tie-breaker is determined by the square with the most unassigned neighbor squares (highest degree)

#### Value Selection Heuristics:
- **Least Constraining Value (LCV)**: The least constraining value is the one that will eliminate the least amount of values out of it's neighbors' domains

#### Consistency Checks:
- **Forward Checking (FC)**: If a variable is assigned, then eliminate that value from the square's neighbors' domains to maintain consistency
- **Norvig's Check (NOR)**: First does forward checking, and if a constraint has only one possible place for a value, then put the value there

*\*Note that for each of the sections above, only one heuristic can be used. For example, you can use MRV + LCV + NOR, but FC and NOR cannot be used at the same time, since their logic conflicts*

---
In this project, the AI will solve puzzles that follow the basic rules of Sudoku, but allows for an NxN grid, where N can be *any* positive integer including N > 9. These puzzles are described by four parameters:

- **N** = the length of one side of the NxN grid, which is also the distinct number of tokens (i.e. a 9x9 grid has 9 tokens)
- **P** = the number of rows in each block
- **Q** = the number of columns in each block
- **M** = the number values filled in from the start

For example, consider the following board (where 0 means an empty space)

	8 0 0 | 0 0 0 | 0 0 0  
	0 0 0 | 0 0 0 | 0 0 0  
	5 0 6 | 0 0 0 | 0 0 0  
	- - - - - - - - - - -  
	0 0 0 | 0 9 0 | 0 0 0  
	0 1 3 | 0 0 0 | 0 0 0  
	0 0 0 | 0 0 0 | 0 0 0  
	- - - - - - - - - - -  
	0 0 0 | 0 0 0 | 0 0 0  
	0 0 0 | 0 0 2 | 0 0 0  
	0 0 0 | 0 0 0 | 0 0 0  
								
For this board, N = 9, P = 3, Q = 3, and M = 7


## Getting Started

#### Prerequisites
This program only requires Python 3 to be run. Python3 can be downloaded here: https://www.python.org/downloads/

#### Installation
	git clone https://github.com/tsamonte/SudokuSolverAI.git
	
## Usage

#### Basic Run
This project is run directly from the command line. To run the program without any setup, run the following command from the project directory (on machines the can run bash scripts):

	./run.sh
	
This will run the AI solver with the MAD, LCV, and NOR heuristics on a randomly generated 9x9 board.  

If you would like to run the heuristics on a specified board, you can pass in a file representing a sudoku puzzle:

	./run.sh <board_file_name>.txt

For example, we could use the sample boards from the Sample_Boards directory in this project

	./run.sh Sample_Boards/board16x16.txt
	
#### Advanced Run
If you would like to choose the heuristics you want to run, or use no heuristics at all, you can run the project using the following while in the project directory:

	python3 src/Main.py [MRV | MAD] [LCV] [FC | NOR] [board_file_name]

## Optional Supplement: Board Generation
In this repo, I have included a board generator to generate random sudoku puzzles with parameters specified by you. To generate random sudoku puzzles, change into the "Sudoku_Generator" directory and run the following command:

	make
	
You will be asked to enter a value for P, Q, M, and how many boards to make.  

*\*Note that boards generated this way are still very likely to have a solution, but are not guaranteed to have one*
