import copy
import ast
import time


# Find the maximum capacity of the tanks
def getStackHeight(grid):
    max = 0;
    for stack in grid[0]:
        if max < len(stack):
            max = len(stack);
    return max;


# Convert vector of strings to canonicalRepresentation of strings
def canonicalStringConversion(grid):
    finalString = ""
    for stack in grid[0]:
        finalString += (stack + ";");
    return finalString;


# Function to check if it is solved or not
def isSolved(grid, stackHeight):
    for stack in grid[0]:
        if len(stack) == 0:
            continue;
        elif len(stack) < stackHeight:
            return False;
        elif stack.count(stack[0]) != stackHeight:
            return False;
    return True;


# Check if a state has been visited
def checkVisited(visited, canonicalString):
    for x in visited:
        if x == canonicalString:
            return False
    return True


# Check if the move is valid
def isValidMove(sourceStack, destinationStack, height):

    # Can't move from an empty stack
    # or to a FULL STACK
    if len(sourceStack) == 0 or len(destinationStack) == height:
        return False;

    colorFreqs = sourceStack.count(sourceStack[0]);
    # If the source stack is same colored,
    # don't touch it
    if colorFreqs == height:
        return False;
    
    # Check if it is possible to transfer the same consecutive colors 
    # from sourceStack to destinationStack
    destinationStack_empty = height - len(destinationStack)
    sourceStack_sameColor = 0
    for i in range(len(sourceStack)):
        if (sourceStack[-1] == sourceStack[len(sourceStack)-1-i]):
            sourceStack_sameColor += 1
        else:
            break
    if (destinationStack_empty < sourceStack_sameColor):
        return False;
    
    if (len(destinationStack) == 0):
        return True;

    return (sourceStack[-1] == destinationStack[-1]);


def aStarAlgorithm(initialGrid, stackHeight, stackBonus):
    
    open_set = [initialGrid] 
    closed_set = []
    g = {} #store distance from starting node.  "g(n)""
    parents = {} #parents contains an adjacency map of all nodes
    visited = set()
    
    #distance of starting node fromprint itself is zero
    g[canonicalStringConversion(initialGrid)] = 0
    #start_node is root node i.e it has no parent nodes
    #so start_node is set to its own parent node
    parents[canonicalStringConversion(initialGrid) + str(initialGrid[2]) + str(initialGrid[3])] = initialGrid
    
    
    while len(open_set) > 0:
        n = None
 
        #node with lowest f() is found.  "f(n) = g(n) + h(n)"
        for v in open_set:
            if n == None or g[canonicalStringConversion(v)] + heuristic(v,stackBonus) < g[canonicalStringConversion(n)] + heuristic(n,stackBonus):
                n = v
                visited.add(canonicalStringConversion(n))
                
        if isSolved(n, stackHeight) :
                pass
        else:
            for nextGrid in get_neighbors(n,visited,stackHeight):
                nextGrid_String = canonicalStringConversion(nextGrid)
                if nextGrid not in open_set and nextGrid not in closed_set:
                    open_set += [nextGrid]
                    # plus String to avoid duplicate key in Dictionary
                    parents[nextGrid_String + str(nextGrid[2]) + str(nextGrid[3])] = n 
                    g[nextGrid_String] = g[canonicalStringConversion(n)] + nextGrid[1]
                else:
                    # #for each node m,compare its distance from start i.e g(m) to the n node
                    if g[nextGrid_String] > g[canonicalStringConversion(n)] + nextGrid[1]:
                        #update g(m)
                        g[nextGrid_String] = g[canonicalStringConversion(n)] + nextGrid[1]
                        #change parent of m to n
                        # plus String to avoid duplicate key in Dictionary
                        parents[nextGrid_String + str(nextGrid[2]) + str(nextGrid[3])] = n 
                             
                        #if m in closed set,remove and add to open set
                        if nextGrid in closed_set:
                            closed_set.remove(nextGrid)
                            open_set += [nextGrid]   
                             
        if n == None:
            print('Couldn not find the answer !')
            return None
            
        # if the current node is the stop_node
        # then we begin reconstructin the path from it to the start_node
        if isSolved(n, stackHeight):
            path = []
 
            while parents[canonicalStringConversion(n) + str(n[2]) + str(n[3])] != n:
                path.append(n)
                n = parents[canonicalStringConversion(n) + str(n[2]) + str(n[3])]
 
            path.append(initialGrid)
 
            path.reverse()
 
            # for step in path:
            #     print(step)
            return path
            
        # remove n from the open_list, and add it to closed_list
        # because all of it's neighbors were inspected
        
        open_set.remove(n)
        closed_set += [n]
                   
    print('Couldn not find the answer !')
    return None    
                
            
# define fuction to return neighbor from the passed node
def get_neighbors(grid, visited, stackHeight):
    neighbors_set = []
    for i in range(len(grid[0])):
    
        # // Iterate over all the stacks
        sourceStack = grid[0][i]
        for j in range(len(grid[0])):
            if (i == j):
                continue
            destinationStack = grid[0][j]
            
            if (isValidMove(sourceStack,destinationStack,stackHeight)):
                # Creating a new Grid with the valid move
                
                newGrid = copy.deepcopy(grid)

                # // Adding colors from top of sourceStack to destinationStack
                # // Removing colors from top of sourceStack
                if(len(newGrid[0][i]) > 0):
                    
                    sourceStack_sameColor = 0
                    for k in range(len(sourceStack)):
                        if (sourceStack[-1] == sourceStack[len(sourceStack)-1-k]):
                            sourceStack_sameColor += 1
                        else:
                            break
                    
                    for numTrans in range(0,sourceStack_sameColor):
                        newGrid[0][j]+=newGrid[0][i][-numTrans-1]
                    
                    newGrid[0][i] = newGrid[0][i][:-sourceStack_sameColor]
                    newGrid[1] += 1
                    newGrid[2] = i + 1
                    newGrid[3] = j + 1
                    
                    if (checkVisited(visited,canonicalStringConversion(newGrid))):
                        neighbors_set += [newGrid]    
                          
    return neighbors_set
                      
    
# Heuristic function.  "h(n)"
def heuristic(checkGrid, stackBonus):
    different_Color_point = 0
    bonus_Stack_used = 0
    num_Stack_used = 0
    for stack in checkGrid[0]:
        if len(stack) > 0:
            num_Stack_used += 1
        for i in range(len(stack)-1):
            if stack[i] != stack[i+1]:
                different_Color_point += 500
                
    bonus_Stack_used = num_Stack_used - (len(grid[0]) - stackBonus)
    
    return different_Color_point + 5*bonus_Stack_used


# // Checks whether the grid is valid or not
def checkGrid(grid, stackBonus, level):
    
    if level != 0:
        numberOfStacks = len(grid[0]);
        stackHeight = getStackHeight(grid);
        numColorSpaceExpected = ((numberOfStacks - stackBonus) * stackHeight);
    
        numColorSpace = 0;

        for i in grid[0]:
            numColorSpace += len(i);
        if (numColorSpace != numColorSpaceExpected):
            print("Grid has incorrect\n")
            return False

        ColorSpaceFrequency = {}
        for stack in grid[0]:
            for colorSpace in stack:
                if ColorSpaceFrequency.get(colorSpace) != None:
                    ColorSpaceFrequency[colorSpace] += 1
                else:
                    ColorSpaceFrequency[colorSpace] = 1

    
        for Color in ColorSpaceFrequency:
            if (ColorSpaceFrequency[Color] != stackHeight):
                print("Color " + str(Color) + " is not " + str(stackHeight))
                return False;
        
    return True;



# *********************************************** INPUT AND OUTPUT ***********************************************

for i in range(0,151):
    InputPath = "Input/Testcase" + str(i) +".txt"
    OutputPath = "Output_Astar/Solution_test" + str(i) +".txt"
    
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

    # initialState[1] is the number of steps taken
    # initialState[2] is the serial number of the original vial to be poured in to complete this state
    # initialState[3] is the sequence number of the target vial that was poured in to complete this state 
    initialState = [initialInput,0,0,0]; 
    
    grid = initialState
    stackHeight = getStackHeight(grid)

    try:
        with open(OutputPath, mode='x') as f:
            title = "     -------------------** LEVEL " + str(level) + " **--------------------"
            print(title)
            print()
            f.write(title)
            f.write('\n\n')
            if (not checkGrid(grid, stackBonus, level)):
                print("Invalid Grid")
                f.write("Invalid Grid")
            else:
                if (level == 0):
                    print ('\n' + "* Algorithm run time : 0.0[sec]")
                    f.write("* Algorithm run time : 0.0[sec]" + '\n\n')
                    f.write("STEP 1 : Move 0 to 0")
                    f.write('\n')
                    f.write(str(initialInput))
                    f.write('\n\n')
                    f.write("STEP 0 : Move 0 to 1")
                    f.write('\n')
                    f.write("['', 'aaaa']")
                    
                elif (isSolved(grid, stackHeight)):
                    print("Problem is already solved")
                    f.write("Problem is already solved")
                else: 
                    start_time = time.time()
                    result = aStarAlgorithm(grid, stackHeight, stackBonus)
                    end_time = time.time()
                    
                    if result == None:
                        f.write("Couldn not find the answer !")
                    else:
                        elapsed_time = end_time - start_time
                        print ('\n' + "* Algorithm run time : {0}".format(elapsed_time) + "[sec]")
                        f.write("* Algorithm run time : {0}".format(elapsed_time) + "[sec]" + '\n\n')
                        
                        for step in result:
                            f.write("STEP " + str(step[1]) + " : " + "Move " + str(step[2]) + " to " + str(step[3]))
                            f.write('\n')
                            f.write(str(step[0]))
                            f.write('\n\n')
            print('\n\n')
        
    except FileExistsError:
        f = open(OutputPath, 'w')
        title = "     -------------------** LEVEL " + str(level) + " **--------------------"
        print(title)
        print()
        f.write(title)
        f.write('\n\n')
        if (not checkGrid(grid, stackBonus, level)):
            print("Invalid Grid")
            f.write("Invalid Grid")
        else:
            if (level == 0):
                print ('\n' + "* Algorithm run time : 0.0[sec]")
                f.write("* Algorithm run time : 0.0[sec]" + '\n\n')
                f.write("STEP 0 : Move 0 to 0")
                f.write('\n')
                f.write(str(initialInput))
                f.write('\n\n')
                f.write("STEP 1 : Move 0 to 1")
                f.write('\n')
                f.write("['', 'aaaa']")
                
            elif (isSolved(grid, stackHeight)):
                print("Problem is already solved")
                f.write("Problem is already solved")
            else: 
                start_time = time.time()
                result = aStarAlgorithm(grid, stackHeight, stackBonus)
                end_time = time.time()
                
                if result == None:
                    f.write("Couldn not find the answer !")
                else:
                    elapsed_time = end_time - start_time
                    print ('\n' + "* Algorithm run time : {0}".format(elapsed_time) + "[sec]")
                    f.write("* Algorithm run time : {0}".format(elapsed_time) + "[sec]" + '\n\n')

                    for step in result:
                        f.write("STEP " + str(step[1]) + " : " + "Move " + str(step[2]) + " to " + str(step[3]))
                        f.write('\n')
                        f.write(str(step[0]))
                        f.write('\n\n')
        print('\n\n')        