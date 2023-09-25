# // Function to find the max
def getStackHeight(grid):
    max = 0;
    for stack in grid:
        if max < len(stack):
            max = len(stack);
    return max;


# // Convert vector of strings to
# // canonicalRepresentation of strings
def canonicalStringConversion(grid):
    finalString = ""
    grid.sort()
    for stack in grid:
        finalString += (stack + ";");
    print(finalString)
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
    
    return (sourceStack[-1] == destinationStack[-1]);

def setSearch(visited, canonicalString):
    for x in visited:
        if x == canonicalString:
            return False
    return True

# // Function to solve the puzzle
def solvePuzzle(grid, stackHeight, visited, answerMod):
    if (stackHeight == -1):
        stackHeight = getStackHeight(grid);
    
    visited.add(canonicalStringConversion(grid));
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
                
                newGrid = grid

                # // Adding the ball
                
                # // Removing the ball
                if(len(newGrid[i]) > 0):
                    newGrid[j]+=newGrid[i][-1]
                    newGrid[i] = newGrid[i][:-1]
                
                if (isSolved(newGrid, stackHeight)):
                    answerMod.append([ i, j, 1 ])
                    
                    return True
                
                
                # if (visited.find(canonicalStringConversion(newGrid)) == visited.end()):
                if (setSearch(visited, canonicalStringConversion(newGrid))):
                    solveForTheRest = solvePuzzle(newGrid, stackHeight, visited, answerMod)
                    if solveForTheRest == True:
                        lastMove = answerMod[-1];

                        # // Optimisation - Concatenating
                        # // consecutive moves of the same
                        # // ball
                        if (lastMove[0] == i and lastMove[1] == j):
                            answerMod[-1][2]+=1;
                        else:
                            answerMod.append([i, j, 1]);
                        return True;
    
    return False;

# // Checks whether the grid is valid or not
def checkGrid(grid):

    numberOfStacks = len(grid);
    stackHeight = getStackHeight(grid);
    numBallsExpected = ((numberOfStacks - 2) * stackHeight);
    # // Cause 2 empty stacks
    numBalls = 0;

    for i in grid:
        numBalls += len(i);
    if (numBalls != numBallsExpected):
        print("Grid has incorrect # of balls\n")
        return False

    ballColorFrequency = {}
    for stack in grid:
        for ball in stack:
            if ballColorFrequency.get(ball) != None:
                ballColorFrequency[ball] += 1
            else:
                ballColorFrequency[ball] = 1

    
    for ballColor in ballColorFrequency:
        if (ballColorFrequency[ballColor] != getStackHeight(grid)):
            print("Color " + ballColor + " is not " + getStackHeight(grid))
            return False;
        
    return True;


# // Driver Code
    # // Including 2 empty stacks
numberOfStacks = 6;
stacks = ["gbbb", "ybry", "yggy", "rrrg", "", ""];
grid = stacks
if (not checkGrid(grid)):
    print("Invalid Grid")
else:
    if (isSolved(grid, getStackHeight(grid))):
        print("Problem is already solved")
    visited = set();
    answerMod = [];

    # // Solve the puzzle instance
    solvePuzzle(grid, getStackHeight(grid),
                visited,
                answerMod);
    # // Since the values of Answers are appended
    # // When the problem was completely
    # // solved and backwards from there
    answerMod.reverse()
    # print(answerMod)
    # for v in answerMod:
    #     print("Move " + (v[0] + 1) + " to " + (v[1] + 1) + " " + v[2] + " times")

