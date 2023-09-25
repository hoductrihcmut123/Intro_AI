# // Function to find the max
import ast
import time


def getStackHeight(grid):
    max = 0;
    for stack in grid:
        if max < len(stack):
            max = len(stack);
            
    for i in range(len(grid)):
        grid[i] = grid[i].strip()
        
    return max;


# // Convert list of strings to
# // canonicalRepresentation of strings
def canonicalStringConversion(grid):
    finalString = ""
    grid.sort()
    for stack in grid:
        finalString += (stack + ";");
    # print(finalString)
    return finalString;

# // Function to check if it is solved
# // or not
def isSolved(grid, stackHeight):
    for stack in grid:
        if len(stack) == 0:
            continue;
        elif len(stack) < stackHeight:
            return False;
        elif stack.count(stack[0]) != stackHeight:
            return False;
    return True;

# // Check if the move is valid
def isValidMove(sourceStack, destinationStack, height):

    # // Can't move from an empty stack
    # // or to a FULL STACK
    if len(sourceStack) == 0 or len(destinationStack) == height:
        return False;

    colorFreqs = sourceStack.count(sourceStack[0]);

    # // If the source stack is same colored,
    # // don't touch it
    if colorFreqs == height:
        return False;

    
    if (len(destinationStack) == 0):
        # // If source stack has only
        # // same colored balls,
        # // don't touch it
        if colorFreqs == len(sourceStack):
            return False;
        return True;
    
    # Move multiple level of a color to the destination stack


    # topSourceFrequency = sourceStack.count(sourceStack[-1]);
    topSourceColor = sourceStack[-1]
    i = len(sourceStack) - 1
    topSourceFrequency = 0
    while i >= 0 and sourceStack[i] == topSourceColor:
        topSourceFrequency += 1
        i -= 1

    destinationSpace = height - len(destinationStack);
    if(topSourceFrequency > destinationSpace):
        return False;

    # print("height: ", end='')
    # print(height)
    # print("len(destinationStack): ", end='')
    # print(len(destinationStack))
    # print("topSourceFrequency: ", end='')
    # print(topSourceFrequency)
    return (sourceStack[-1] == destinationStack[-1]);

def setSearch(visited, canonicalString):
    for x in visited:
        if x == canonicalString:
            return True
    return False

# // Function to solve the puzzle
def solvePuzzle(grid, stackHeight, visited, answerMod):
    # if (stackHeight == -1):
    #     stackHeight = getStackHeight(grid);
    
    sortingGrid = grid.copy()
    visited.add(canonicalStringConversion(sortingGrid));

    for i in range(len(grid)):

        # // Iterate over all the stacks
        sourceStack = grid[i]
        for j in range(len(grid)):
            if (i == j):
                continue
            destinationStack = grid[j]
            
            if (isValidMove(sourceStack,destinationStack,stackHeight)):
                # // Creating a new Grid
                # // with the valid move
                # print("before")
                # print("sourceStack: " + sourceStack + "\ndestinationStack: " + destinationStack + "\n")
                newGrid = grid.copy()

                # // Adding the ball
                topSourceColor = newGrid[i][-1]
                # // Removing the ball
                # print(visited)
                # print()
                
                # print(grid)
                # print("i = ", end = '')
                # print(i);
                # print("j = ", end = '')
                # print(j);
                # print("sourceStack: " + sourceStack + "\ndestinationStack: " + destinationStack + "\n")
                while(len(newGrid[i]) > 0 and newGrid[i][-1] == topSourceColor):
                    newGrid[j] += newGrid[i][-1]
                    newGrid[i] = newGrid[i][:-1]
                # print("after")
                # print("sourceStack: " + newGrid[i] + "\ndestinationStack: " + newGrid[j] + "\n")
                
                sortingGrid = newGrid.copy()
                state = canonicalStringConversion(sortingGrid)
                if (isSolved(newGrid, stackHeight)):
                    answerMod.append([ state, i, j, 1 ])
                    return True
                
                sortingGrid = newGrid.copy()
                
                # if (visited.find(canonicalStringConversion(newGrid)) == visited.end()):
                if ( not setSearch(visited, canonicalStringConversion(sortingGrid))):
                    solveForTheRest = solvePuzzle(newGrid, stackHeight, visited, answerMod)
                    if solveForTheRest == True:
                        lastMove = answerMod[-1];

                        # // Optimisation - Concatenating
                        # // consecutive moves of the same
                        # // ball
                        if (lastMove[0] == i and lastMove[1] == j):
                            answerMod[-1][3]+=1;
                        else:
                            answerMod.append([state, i, j, 1]);
                        return True;
    
    return False;

# // Checks whether the grid is valid or not
def checkGrid(grid, stackHeight):

    numberOfStacks = len(grid);
    numBallsExpected = ((numberOfStacks) * stackHeight);
    # // Cause 2 empty stacks
    numBalls = 0;

    for i in grid:
        numBalls += len(i);
    # if (numBalls != numBallsExpected):
    # print(numBalls)
    # print(numBallsExpected)
    if (numBalls > numBallsExpected):
        print("Grid has incorrect # of balls\n")
        return False

    ballColorFrequency = {}
    for stack in grid:
        for ball in stack:
            if ballColorFrequency.get(ball) != None:
                ballColorFrequency[ball] += 1
            else:
                ballColorFrequency[ball] = 1
    
    numOfColors = len(ballColorFrequency.keys())
    if numOfColors > numberOfStacks:
        print("Number of colors is greater than number of stacks")
        return False;

    for ballColor in ballColorFrequency:
        if (ballColorFrequency[ballColor] != stackHeight):
            print("Color ", end='')
            print(ballColor, end='')
            print(" is not ", end='')
            print(getStackHeight(grid))
            return False;
    return True;



# stacks = ['a   ', 'aaa ']
# numberOfStacks = len(stacks);
# grid = stacks
# stackHeight = getStackHeight(grid)
# if (not checkGrid(grid, stackHeight)):
#     print("Invalid Grid")
# else:
#     if (isSolved(grid, stackHeight)):
#         print("Problem is already solved")
#     visited = set();
#     answerMod = [];

#     # // Solve the puzzle instance
#     solvePuzzle(grid, stackHeight,
#                 visited,
#                 answerMod);
#     # // Since the values of Answers are appended
#     # // When the problem was completely
#     # // solved and backwards from there
#     answerMod.reverse()
#     # print(answerMod)
#     i = 1
#     for v in answerMod:
#         print("Step " + str(i) + ": ", end='')
#         print("Move ", end = '') 
#         print(v[1] + 1, end = '') 
#         print(" to ", end = '')
#         print(v[2] + 1)
#         print(v[0])
#         print()
#         i += 1

#     print(len(answerMod))


# *********************************************** INPUT AND OUTPUT ***********************************************

for i in range(0,151):
    InputPath = "Input/Testcase" + str(i) +".txt"
    OutputPath = "Output_DFS/Solution_test" + str(i) +".txt"
    
    f = open(InputPath) 

    data = f.readline()
    level = int(data)

    data = f.readline()
    numberOfStacks = int(data)

    data = f.readline()
    stackBonus = int(data)

    data = f.readline()
    initialInput = ast.literal_eval(data)

    f.close()
    
    # grid = initialState
    grid = initialInput
    stackHeight = getStackHeight(grid)

    try:
        with open(OutputPath, mode='x') as f:
            title = "     -------------------** LEVEL " + str(level) + " **--------------------"
            print(title)
            print()
            f.write(title)
            f.write('\n\n')
            if (not checkGrid(grid, stackHeight)):
                print("Invalid Grid")
                f.write("Invalid Grid")
            else:
                if (isSolved(grid, stackHeight)):
                    print("Problem is already solved")
                    f.write("Problem is already solved")
                else:
                    start_time = time.time()
                    visited = set();
                    answerMod = [];
                    solvePuzzle(grid, stackHeight, visited, answerMod);
                    answerMod.reverse()
                    end_time = time.time()
                    
                    elapsed_time = end_time - start_time
                    print ('\n' + "* Algorithm run time : {0}".format(elapsed_time) + "[sec]")
                    f.write("* Algorithm run time : {0}".format(elapsed_time) + "[sec]" + '\n\n')
                    if len(answerMod) == 0:
                        f.write("Couldn not find the answer !")
                    else:
                        
                        i = 1
                        for step in answerMod:
                            f.write("STEP " + str(i) + " : " + "Move " + str(step[1] + 1) + " to " + str(step[2] + 1))
                            f.write('\n')
                            f.write(str(step[0]))
                            f.write('\n\n')
                            i += 1
            print('\n\n')
        
    except FileExistsError:
        f = open(OutputPath, 'w')
        title = "     -------------------** LEVEL " + str(level) + " **--------------------"
        print(title)
        print()
        f.write(title)
        f.write('\n\n')
        if (not checkGrid(grid, stackHeight)):
            print("Invalid Grid")
            f.write("Invalid Grid")
        else:
            if (isSolved(grid, stackHeight)):
                print("Problem is already solved")
                f.write("Problem is already solved")
            else: 
                start_time = time.time()
                visited = set();
                answerMod = [];
                solvePuzzle(grid, stackHeight, visited, answerMod);
                answerMod.reverse()
                end_time = time.time()
                elapsed_time = end_time - start_time
                print ('\n' + "* Algorithm run time : {0}".format(elapsed_time) + "[sec]")
                f.write("* Algorithm run time : {0}".format(elapsed_time) + "[sec]" + '\n\n')
                
                if len(answerMod) == 0:
                    f.write("Couldn not find the answer !")
                else:
                    

                    i = 1
                    for step in answerMod:
                        f.write("STEP " + str(i) + " : " + "Move " + str(step[1] + 1) + " to " + str(step[2] + 1))
                        f.write('\n')
                        f.write(str(step[0]))
                        f.write('\n\n')
                        i += 1
        print('\n\n')        