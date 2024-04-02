# VIRAY, Geraldine Marie M.
# CMSC 170 X5L

# REFERENCES:
# https://github.com/johnmichaelbacasno/8-Puzzle-Game/tree/main


# import libraries
import tkinter as tk
import time
import sys

from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog

from queue import PriorityQueue, Queue
from queue import LifoQueue

# function for returning all possible actions
def actions(state, empty_row, empty_col):
    actions = []
    # checks if swapping upward is possible
    if empty_row > 0:
        actions.append("U")

    # checks if swapping downward is possible
    if empty_col < 2:
        actions.append("R")

    # checks if swapping to left is possible
    if empty_row < 2:
        actions.append("D")

    # checks if swapping to right is possible
    if empty_col > 0:
        actions.append("L")

    return actions

# a function that gives the resulting state of a puzzle when an action is done to it
def result(state, action, zeroRow, zeroCol):
    # zeroRow, zeroCol = None, None

    # it will do the action and it will increment/decrement the position of the zero in the puzzle
    if action == "U" and zeroRow > 0:
        state[zeroRow][zeroCol], state[zeroRow - 1][zeroCol] = state[zeroRow - 1][zeroCol], state[zeroRow][zeroCol]
        zeroRow -= 1
    elif action == "R" and zeroCol < 2:
        state[zeroRow][zeroCol], state[zeroRow][zeroCol + 1] = state[zeroRow][zeroCol + 1], state[zeroRow][zeroCol]
        zeroCol += 1
    elif action == "D" and zeroRow < 2:
        state[zeroRow][zeroCol], state[zeroRow+1][zeroCol] = state[zeroRow+1][zeroCol], state[zeroRow][zeroCol]
        zeroRow += 1
    elif action == "L" and zeroCol > 0:
        state[zeroRow][zeroCol], state[zeroRow][zeroCol - 1] = state[zeroRow][zeroCol - 1], state[zeroRow][zeroCol]
        zeroCol -= 1
    else:
        return None, None, None

    return state, zeroRow, zeroCol

# function that returns the solution path of a puzzle after it uses brute-first search
def BFSearch(puzzle, zeroRow, zeroCol):
    # global puzzle, zeroRow, zeroCol
    print("BFS")
    print(puzzle)
    print(zeroRow)
    print(zeroCol)

    # create an empty set to keep track of all the visited states
    visited = set()

    # stores tuples containing the current puzzle state, the position of the empty tile, and the path taken to reach that state
    frontier = Queue()

    # initialize
    frontier.put((puzzle, zeroRow, zeroCol, []))

    # main loop of the bfs
    while not frontier.empty():
        print(len(visited))

        # dequeue a state from the frontier
        puzzle, zeroRow, zeroCol, path = frontier.get()

        visited.add(tuple(map(tuple, puzzle)))

        # goal test
        if puzzle_solved(puzzle):
            print(len(visited))
            print(path)
            return path
        
        # generate all possible actions for the current state
        for action in actions(puzzle, zeroRow, zeroCol):
            nextState, zeroRow_update, zeroCol_update = result(list(map(list, puzzle)), action, zeroRow, zeroCol)

            # enqueue state if it is not in visited 
            if tuple(map(tuple, nextState)) not in visited and (nextState, zeroRow_update, zeroCol_update, []):
                newPath = path + [action]
                frontier.put((nextState, zeroRow_update, zeroCol_update, newPath))

    return None

# function that implement depth-first search to find solution
def DFSearch(puzzle, zeroRow, zeroCol):
    # global puzzle, zeroRow, zeroCol
    print("DFS")
    print(puzzle)
    print(zeroRow)
    print(zeroCol)

    # visited to keep track of the visited states
    visited = set()

    # last in first out, containing current 
    frontier = LifoQueue()

    frontier.put((puzzle, zeroRow, zeroCol, []))

    # main dfs loop
    while frontier.qsize() > 0:
        print(len(visited))

        # removes current state from frontier
        puzzle, zeroRow, zeroCol, path = frontier.get()

        visited.add(tuple(map(tuple, puzzle)))

        # checks it the puzzle is already solved
        if puzzle_solved(puzzle):
            print(len(visited))
            print(path)
            return path
        
        # for each action, it calculates the resulting state, position of the empty tile, and the new path
        for action in actions(puzzle, zeroRow, zeroCol):
            nextState, zeroRow_update, zeroCol_update = result(list(map(list, puzzle)), action, zeroRow, zeroCol)

            # if it is a new state, it is queued nto the frontier for it to be explored
            if tuple(map(tuple, nextState)) not in visited and (nextState, zeroRow_update, zeroCol_update, []):
                newPath = path + [action]
                frontier.put((nextState, zeroRow_update, zeroCol_update, newPath))

    return None




"""

open list contains all nodes that are candidates for examination (frontier)
- initially contains the starting position of the empty tile

closed list contains all nodes that have already been examined (explored)
- initially has an empty content

f(n) = g(n) + h(n)

g(n)
- exact cost of the path from the starting node to node n
- total number of tile moves from the start of the game to its current configuration

h(n)
- heuristic estimated cost from node n to goal node
- manhattan distance (distance = |x1 - x2| + |y1 - y2|)
- manhattan distance of each tile, including the empty tile

"""

# distance of each tile to its goal
def manhattanDistance (tile, currentPosition, goalPosition):
    if tile == 0:
        return 0
    
    # gets current position
    currRow, currCol = currentPosition

    # goal state
    goalRow, goalCol = goalPosition[tile]

    distance = abs(currRow - goalRow) + abs(currCol - goalCol)

    return distance

# total manhattan distance of all tiles
def computeManhattanDistance (currState):
    goalState = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

    goalPosition = {}
    distances = []

     # iterate through the goalState to populate the goalPosition
    for i in range(3):
        for j in range(3):
            tile = goalState[i][j]
            goalPosition[tile] = (i, j)

    # iterate through the current state to compute Manhattan distances
    for i in range(3):
        for j in range(3):
            tile = currState[i][j]
            current_position = (i, j)
            distance = manhattanDistance(tile, current_position, goalPosition)
            distances.append(distance)

    return distances

# function for removing and returning the state with the minimum total manhattan distance from frontier
def removeMinF(frontier):

    # initialization
    min_state = None
    min_distance = float('inf')

    # loop until frontier is empty
    while not frontier.empty():
        state, zeroRow, zeroCol, path = frontier.get()

        # get the distances for tiles in current state
        distances = computeManhattanDistance(state)

        # calculate the total distance for this state
        total_distance = sum(distances)

        # if total distance is less than current minimum, update
        if total_distance < min_distance:
            min_distance = total_distance
            min_state = (state, zeroRow, zeroCol, path)

    # return state with minimum distance
    return min_state

# function for A* algorithm
def aStarAlgo(puzzle, zeroRow, zeroCol):
    # frontier
    openList = PriorityQueue()
    # visited
    closedList = set()

    # intialize
    openList.put((puzzle, zeroRow, zeroCol, []))

    while not openList.empty():
        print(len(closedList))

        # get the state with the minimum manhattan distance
        bestNode = removeMinF(openList)
        state, zeroRow, zeroCol, path = bestNode

        # add state to closed list
        closedList.add(tuple(map(tuple, state)))

        # if puzzle is solved, return path
        if puzzle_solved(state):
            print(len(closedList))
            print(f"Path Cost: {len(path)}")
            print(f"Path Solution: {' '.join(path)}")
            return path

        # generate all possible actions
        for action in actions(state, zeroRow, zeroCol):
            # get resulting state after action
            nextState, zeroRow_update, zeroCol_update = result(list(map(list, state)), action, zeroRow, zeroCol)

            # check if state is in closed list, and has a valid path
            if tuple(map(tuple, nextState)) not in closedList and (nextState, zeroRow_update, zeroCol_update, []):
                newPath = path + [action]
                # add state to openlist
                openList.put((nextState, zeroRow_update, zeroCol_update, newPath))

    return None



# function that displays the solution step by step
def showSolution():
    global currStep, solution, puzzle, zeroRow, zeroCol

    # check if there are more steps in solution path to display
    if currStep < len(solution):

        action = solution[currStep]
        
        # calculate resulting state after applying the action
        resultState, zeroRow, zeroCol = result(list(map(list, puzzle)), action, zeroRow, zeroCol)


        if resultState:
            # update current puzzle state with the new state
            puzzle[:] = resultState

            # update the position of the zeroRow and zeroCol
            for i in range(3):
                for j in range(3):
                    if puzzle[i][j] == 0:
                        zeroRow = i
                        zeroCol = j

            # update ui
            update_ui()

            # if puzzle reached the end step
            if puzzle_solved(puzzle):
                messagebox.showinfo("Puzzle Solution Shown.", "The end of the puzzle is reached.")
                # root.destroy()

            currStep += 1
        else:
            messagebox.showerror("Invalid Action", "Cannot perform the next action.")


# a function to determine if the puzzle is solvable or not
def is_solvable(puzzle):
    inversionCount = 0
    numArray = []

    # loop to go through the numbers of puzzle, then append it to numArray
    for row in puzzle:
        for val in row:
            if val != 0:
                numArray.append(val)

    # calculate the inversion count by comparing pairs of elements in the numArray
    # inversion is counted when a larger number appears before a smaller number
    for i in range(len(numArray)-1):
        for j in range(i+1, len(numArray)):
            if numArray[i] > numArray[j]:
                inversionCount = inversionCount + 1
    
    # if the inversion count is even, the puzzle is solvable
    # if not, the puzzle is not solvable
    if (inversionCount%2 == 0):
        return True
    else:
        return False

# checks if the puzzle is already solved
def puzzle_solved(puzzle):
    numArray = []

    # collect all values of the puzzle, including the space
    for row in puzzle:
        for val in row:
            numArray.append(val)

    # compares if numArray is equal to [1, 2, 3, 4, 5, 6, 7, 8, 0]
    # if yes, then the puzzle is already solved
    # if not, then the puzzle is not yet solved
    if numArray == list(range(1,9)) + [0]:
        return True
    else:
        return False

# function that reads puzzle.in
def read_puzzle(puzzlein):
    puzzle = []
    try:
        # opens the file in read
        with open(puzzlein, 'r') as file:
            for line in file:
                # strip removes the leading and trailing spaces from the line
                # split separates the elements, with space as its delimiter
                # map converts each element to int
                rowline = map(int, line.strip().split())

                # converts it to a list
                row = list (rowline)

                # each row is appended to the puzzle array
                puzzle.append(row)
    except FileNotFoundError:
        messagebox.showerror("puzzle.in not found.", "Please create a file for initial input of the puzzle. Name it as puzzle.in.")
        exit()
    return puzzle

# function that updates the ui every time a move is made
def update_ui():

    # loop for accessing each value of the grid
    for i in range(3):
        for j in range(3):
            tilenum = puzzle[i][j]

            # if tilenum is 0, it indicates that it is the empty space
            # it cannot be interacted with
            if tilenum == 0:
                buttons[i][j].config(text="", state=tk.DISABLED)
            # tilenum is the number inside the button
            # it can be interacted with
            else:
                if notClickable is False:
                    buttons[i][j].config(text=str(tilenum), state=tk.NORMAL)
                else:
                    buttons[i][j].config(text=str(tilenum), state=tk.DISABLED, disabledforeground="white")


# function for moving when a button is clicked
def button_click(row, col):
    # checks if the tile can be moved (if it has an adjacent empty tile)

    if notClickable is False:
        # if the button is not on the top row and the empty tile is above it, it will swap
        if row > 0 and puzzle[row - 1][col] == 0:
            puzzle[row][col], puzzle[row-1][col] = puzzle[row-1][col], puzzle[row][col]
        # if the button is not on the bottom row and the empty tile is below it, it will swap
        elif row < 2 and puzzle[row+1][col] == 0:
            puzzle[row][col], puzzle[row+1][col] = puzzle[row+1][col], puzzle[row][col]
        # if the button is not on the leftmost column and the tile on its left is the empty tile, it will swap
        elif col > 0 and puzzle[row][col-1] == 0:
            puzzle[row][col], puzzle[row][col-1] = puzzle[row][col-1], puzzle[row][col]
        # if the button is not on the rightmost column and the tile on its right is the empty tile, it will swap
        elif col < 2 and puzzle[row][col+1] == 0:
            puzzle[row][col], puzzle[row][col+1] = puzzle[row][col+1], puzzle[row][col]

    # updates ui every move
    update_ui()

    # checks if the puzzle is already solved
    # displays a prompt and exits the program if yes
    if puzzle_solved(puzzle):
        messagebox.showinfo("PUZZLE SOLVED!", "Congratulations! You have solved the puzzle!")
        root.destroy()

# function to create the initial puzzle grid
def initial_puzzle():
    global zeroRow, zeroCol
    
    # for each item in [row][col]
    for i in range(3):
        rows = []
        for j in range(3):
            # if value of tile is 0, it is an empty tile
            if puzzle[i][j] == 0:
                tile_label = ""
                zeroRow = i
                zeroCol = j
            
            # else, the value is the number
            else:
                tile_label = str(puzzle[i][j])
            
            # creates a button tkinter widget
            # command is a lambda function, calls the button_click function that accepts i and j as values
            button = tk.Button(root, text=tile_label, width=5, height=2, command=lambda i=i, j=j: button_click(i, j), bg="#9E4244", font=("Arial", 30, "bold"), fg="White")
            # this puts the button on a certain position in the window
            button.grid(row=i, column=j)
            # button will be appended on rows array
            rows.append(button)
        # rows will be appended on buttons array
        buttons.append(rows)


# function that checks what algorithm the user chose to solve the puzzle
def solvePuzzle():
    global solution, notClickable, currStep, puzzle, zeroCol, zeroRow
    start_time = time.time()
    start_memory = sys.getsizeof({})

    print(puzzle)

    # get the selected algorithm from the dropdown menu
    algorithm = algorithm_dropdown.get()

    # initialize
    puzzle = read_puzzle('puzzle.in')

    # if there is an uploaded puzzle already, read puzzle through filepath then update ui
    if filepath:
        print(filepath)
        puzzle = read_puzzle(filepath)
        update_ui()
    # else, update ui with the initial puzzle.in
    else:
        print("no filepath")
        update_ui()

    print(puzzle)
    
    currStep = 0
    notClickable = True

    # assign zeroRow and zeroCol
    for i in range(3):
        rows = []
        for j in range(3):
            # if value of tile is 0, it is an empty tile
            if puzzle[i][j] == 0:
                tile_label = ""
                zeroRow = i
                zeroCol = j

    if algorithm == "BFS":
        print(puzzle)

        # find the solution using bfs
        pathSoln = BFSearch(puzzle, zeroRow, zeroCol)
        solution = pathSoln

        # for displaying the solution to gui
        if len(solution) < 10:
            current_step_label.config(text=f"Path Cost: {len(solution)} \nPath Solution: {' '.join(solution)}")
        else:
            current_step_label.config(text=f"Path Cost: {len(solution)} \nPath Solution: Path is too long to display.")

    elif algorithm == "DFS":
        print(puzzle)

        # find the solution using dfs
        pathSoln = DFSearch(puzzle, zeroRow, zeroCol)
        solution = pathSoln

        # for displaying the solution to gui
        if len(solution) < 10:
            current_step_label.config(text=f"Path Cost: {len(solution)} \nPath Solution: {' '.join(solution)}")
        else:
            current_step_label.config(text=f"Path Cost: {len(solution)} \nPath Solution: Path is too long to display.")


    elif algorithm == "A-STAR":
        print(puzzle)
        print("A-star selected")

        # find the solution using a*
        pathSoln = aStarAlgo(puzzle, zeroRow, zeroCol)
        solution = pathSoln

        # for displaying the solution to gui
        if len(solution) < 10:
            current_step_label.config(text=f"Path Cost: {len(solution)} \nPath Solution: {' '.join(solution)}")
        else:
            current_step_label.config(text=f"Path Cost: {len(solution)} \nPath Solution: Path is too long to display.")

    else:
        messagebox.showerror("Invalid Algorithm", "Please select a valid algorithm.")
        return
    
    if pathSoln:
        end_time = time.time()
        end_memory = sys.getsizeof({})
        execution_time = end_time - start_time
        space_occupied = end_memory - start_memory
        print(f"Execution time: {execution_time} seconds")

        print(f"Space occupied: {space_occupied:.2f} bytes")

        # store the path solution to the global variable
        solution = pathSoln

        # save the solution to puzzle.out
        with open("puzzle.out", "w") as outfile:
            outfile.write(" ".join(pathSoln))
        
        messagebox.showinfo("Puzzle Solved", "The solution has been saved to 'puzzle.out'.")


# open a new puzzle from file and update the game
def new_puzzle():
    global puzzle, zeroRow, zeroCol, notClickable, currStep, filepath

    # select file
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.in *.txt")])

    print (filepath)

    # assigns to global variable
    filepath = file_path
    print (filepath)

    # prompt
    if file_path:
        messagebox.showinfo("New Puzzle", "New puzzle pattern is uploaded. Puzzle will update.")

        # reads new puzzle
        puzzle = read_puzzle(file_path)

        for i in range(3):
            for j in range(3):
                # if value of tile is 0, it is an empty tile
                if puzzle[i][j] == 0:
                    zeroRow = i
                    zeroCol = j

        # make the game clickable again
        notClickable = False

        # reset
        currStep = 0
        update_ui()
        current_step_label.config(text="Solution will be displayed here.")
        

# function for resetting the puzzle
def reset_puzzle():
    global puzzle
    puzzle = read_puzzle('puzzle.in')
    update_ui()

# function for quitting app
def quit_app():
    if messagebox.askokcancel("Quit", "Do you really want to quit?"):
        root.destroy()

# root is an instance of tkinter
root = tk.Tk()

# sets the title of the application
root.title("Eight-Puzzle Game")

zeroRow, zeroCol = None, None

# reads puzzle input file
puzzle = read_puzzle('puzzle.in')
currentPuzzle = puzzle

# initialize buttons
buttons = []

# initialize path solution
solution = []

# initialize puzzle buttons
initial_puzzle()

# for checking if the buttons should be clickable or not
notClickable = False

# for displaying solution
currStep = 0

# filepath
filepath = ""


# checks if the puzzle is solvable, calls function
if not is_solvable(puzzle):
    messagebox.showerror("Puzzle is Unsolvable.", "Do not try to solve the puzzle. It is not solvable.")
    root.destroy()

# adds reset button to grid
reset_button = tk.Button(root, text="Reset Puzzle", command=reset_puzzle, bg="#DE3161", fg="white", font=("Arial", 10, "bold"))
reset_button.grid(row=6, column=0, pady=10)

# adds quit button to grid
quit_button = tk.Button(root, text="Quit Game", command=quit_app, bg="#DE0A26", fg="white", font=("Arial", 10, "bold"))
quit_button.grid(row=6, column=2, pady=10)

# dropdown for algorithms options
algorithms = ["BFS", "DFS", "A-STAR"]
algorithm_dropdown = ttk.Combobox(root, values=algorithms, state="readonly", width = 10, font=("Arial", 10, "bold"))
algorithm_dropdown.set("Algorithms")
algorithm_dropdown.grid(row=5, column=0, padx=10, pady= 10)

# button for solving the puzzle
solve_button = tk.Button(root, text="Solve Puzzle", command=solvePuzzle, bg="#FC7F9C", font=("Arial", 10, "bold"))
solve_button.grid(row=5, column=1, pady=10)

# button for traversing the path solution
next_button = tk.Button(root, text="Next State", command=showSolution, bg="#FC7F9C", font=("Arial", 10, "bold"))
next_button.grid(row=5, column=2, pady=10)

# for displaying solution
current_step_label = tk.Label(root, text="Solution will be displayed here.", bg="pink", font=("Arial", 12, "bold"))
current_step_label.grid(row=4, column=0, columnspan=3, pady=10)

# button for selecting new pattern for puzzle
new_puzzle = tk.Button(root, text="New Puzzle", command = new_puzzle, bg="#FC7F9C", font=("Arial", 10, "bold"))
new_puzzle.grid(row=6, column=1, pady=10)

# manhattan_distances = computeManhattanDistance(puzzle)

# for i in range(3):
#     for j in range(3):
#         tile = puzzle[i][j]
#         if (tile != 0):
#             print(f"Manhattan distance for tile {tile}: {manhattan_distances[tile-1]}")

root.config(bg="pink")
root.resizable(0, 0)
root.mainloop()