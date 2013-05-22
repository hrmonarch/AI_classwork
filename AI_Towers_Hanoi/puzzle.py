'''
Towers of Hanoi
python 2.6.6
April 15, 2013
Bryan Ford  
'''
import os
import sys
import copy
from puzzleNode import Node


def main():
    start, goal = GetInfo()
    print '---Begin Search---'
    Solver(start, goal)                 # Data Driven
    print '---Search Complete---'
    sys.exit(0)
    
    
#-- Called by main(); returns the start state and goal state from file.
def GetInfo(): 
    cwd = os.path.dirname(__file__)                 # absolute path to cwd
    infile = 'puzzle.input'                         # infile stored in cwd
    inpath = os.path.join(cwd, infile)
    with open(inpath, "r") as input:
        puzzleStart = input.readline().split()
        puzzleGoal = input.readline().split()
    # Structure the input.  This is "putting the rings on the poles".
    nplates = 7
    puzzleStart = [puzzleStart[:nplates], puzzleStart[nplates:nplates*2], puzzleStart[nplates*2:nplates*3]]
    puzzleGoal = [puzzleGoal[:nplates], puzzleGoal[nplates:nplates*2], puzzleGoal[nplates*2:nplates*3]]
    print '--start--'
    print puzzleStart
    print '---goal---'
    print puzzleGoal
    return puzzleStart, puzzleGoal

    
#-- Called by main(); Finds a solution, stdout path from goal state to root state     
def Solver(start, goal):
    total_traversal = 0
    closed_nodes = []
    open_nodes = []
    head = Node(start, None, total_traversal)       # root node creation
    open_nodes.append(head)                         
    ###- safety precaution
    itt = 0
    ###-
    while not head.data == goal:                    # loop until goal is found
        head = Select(open_nodes)                   # Select our next node
        open_nodes.remove(head)                     # Remove selected node from "open nodes"
        closed_nodes.append(head)                   # Add selected node to "closed nodes"
        children = Breed(head, goal)                # Create the children of the selected node
        for child in children:                      # Add children nodes to "open nodes"
            if Unique(child, open_nodes, closed_nodes):
                open_nodes.append(child)
        ###-- safety precaution
        itt +=1
        if itt >= 6000:
            raw_input("--- 6000 loops completed.  Press Enter to continue --- ")
            itt = 0
        ###--        
    while not head.parent == None:                  # Print out path to root
        print head.data
        head = head.parent
    print head.data                                 # One more to print the root
    print 'Number of closed nodes: ' + str( len(closed_nodes) )


#-- Called by Solver; list of open nodes come in, best choice comes out
def Select(open_nodes):
    node_values = [node.total_traversal for node in open_nodes]
    minimum = min(node_values)
    for node in open_nodes:
        if node.total_traversal == minimum:
            #print 'Selected this state: ' + str(node.data)
            return node
    print '!Select() error!'
    sys.exit(0)
    
    
#-- Called by Solver; Takes a node, returns n children of the node
def Breed(head, goal): 
    TryMovePlate(head, 0,1)     # Try: Move top plate from FIRST tower to SECOND tower
    TryMovePlate(head, 1,0)     # Try: Move top plate from SECOND tower to FIRST tower
    TryMovePlate(head, 1,2)     # Try: Move top plate from SECOND tower to THIRD tower
    TryMovePlate(head, 2,1)     # Try: Move top plate from THIRD tower to SECOND tower
    TryMovePlate(head, 2,0)     # Try: Move top plate from THIRD tower to FIRST tower
    TryMovePlate(head, 0,2)     # Try: Move top plate from FIRST tower to THIRD tower
    return head.children


def TryMovePlate(head, ifrom, ito):
    temphead = copy.deepcopy(head.data)                                 # Copy working space while we use it
    for x in xrange(len(head.data[ifrom])):                             # Search a tower, "ifrom"
        if not head.data[ifrom][x] is '0':                              # Look for a plate on "ifrom"
            for y in xrange(len(head.data[ito]) -1,-1,-1):              # Search a tower, "ito"
                if head.data[ito][y] is '0':                            # Look for a plate to put plate on "ito"
                    if y == len(head.data[ito]) -1:                     # Notice if tower is empty
                        child = makeMove(temphead, ifrom, x, ito, y)    # Move is valid, spawn child
                        head.add_child( Node(child, head, head.total_traversal + Heuristic(child)) )   # f = h + g head.total_traversal + Heuristic(child)
                        break
                    if head.data[ito][y+1] > head.data[ifrom][x]:       # Tower is non-empty, check if move is legal
                        child = makeMove(temphead, ifrom, x, ito, y)    # Move is valid, spawn child
                        head.add_child( Node(child, head, head.total_traversal + Heuristic(child)) )    # f = h + g
                    break
            break

# Called by TryMovePlate(); Evaluates how close the state is to the goal 
# concidered is the position of the plates as well as the value of the 
# plates in what position ie the biggest plate at the goal is more important 
# than the smallest plate at the goal
def Heuristic(state):
    #return 0
    pega = pegb = pegc = 0
    
    for a in state[0]:
        pega += int(a) * 2
    for b in state[1]:
        pegb += int(b) * 1
    for c in state[2]:
        pegc += int(c) * 0
    
    return pega + pegb + pegc
    
#-- Compaire our new child to all previously visited nodes.
# If child is not unique, it will not be used (orphaned)
def Unique(wannabeNode, open_nodes, closed_nodes):
    for node in open_nodes:
        if wannabeNode.data == node.data:
            return False
    for node in closed_nodes:
        if wannabeNode.data == node.data:
            return False    
    return True
    
 
#-- Called by Breed();  Swaps two numbers
def makeMove(puzzle, a1, a2, b1, b2):
    puzzle[a1][a2], puzzle[b1][b2] = puzzle[b1][b2], puzzle[a1][a2]  
    return puzzle


if __name__ == '__main__':
    main()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    