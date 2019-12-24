from itertools import product as iprod
import numpy as np
from copy import deepcopy
import matplotlib.pyplot as plt

puzzle_input = ["##.#.",
                ".##..",
                "##.#.",
                ".####",
                "###.."]
def bio_score(grid):
    i = 0 # Used for power of two
    score = 0
    grid = grid_to_dict(grid)
    for x,y in iprod(range(5), range(5)):
        if (x,y) in grid:
            score+= pow(2,i)
        i += 1
    return score

def grid_to_dict(grid):
    if isinstance(grid, dict):
        return deepcopy(grid)
    D = {}
    for x,y in iprod(range(5), range(5)):
        if grid[x][y]=='#':
            D[(x,y)] = '#'
    return D


def evolve(Dgrid):
    weight_grid = np.zeros([7,7], dtype = int)
    D = deepcopy(Dgrid)
    
    # Initialise weights
    for x,y in D.keys():
        weight_grid[x+1,y+1] = 1
            
    for x,y in iprod(range(1,6), range(1,6)):
        s = 0
        # Adjacent sum of weights
        s += weight_grid[x-1][y]
        s += weight_grid[x+1][y]
        s += weight_grid[x][y-1]
        s += weight_grid[x][y+1]
        if (x-1, y-1) not in D and (s==1 or s==2):
            D[(x-1,y-1)] = '#'
        elif (x-1, y-1) in D and not(s==1):
            D.pop((x-1,y-1),'')
    
    return D


def count_bugs(D):
    bugs_count = 0
    for k in D.keys():
        v = D.get(k,0)
        if isinstance(v,dict):
            v = 0
        bugs_count += v
    return bugs_count

def get_weight(D_rec, row, col, layer):
    if isinstance(D_rec.get((row, col, layer)), dict):
        return {}

    n = layer
    if row == 0:
        top = D_rec.get((1, 2, n-1),0)
    else:
        top = D_rec.get((row-1, col, n),0)
        if isinstance(top, dict):
            top = 0 # will be set later

    if col == 0:
        left = D_rec.get((2, 1, n-1),0)
    else:
        left = D_rec.get((row, col-1, n),0)
        if isinstance(left, dict):
            left = 0 # will be set later

    if col == 4:
        right = D_rec.get((2, 3, n-1),0)
    else:
        right = D_rec.get((row, col+1, n),0)
        if isinstance(right, dict):
            right = 0 # will be set later

    if row == 4:
        bottom = D_rec.get((3, 2, n-1),0)
    else:
        bottom = D_rec.get((row+1, col, n),0)
        if isinstance(bottom, dict):
            bottom = 0 # will be set later

    if row==1 and col==2:
        bottom = D_rec.get((0, 0, n+1),0) + D_rec.get((0, 1, n+1),0) + D_rec.get((0, 2, n+1),0) +D_rec.get((0, 3, n+1),0) + D_rec.get((0, 4, n+1),0)
    if row==3 and col==2:
        top = D_rec.get((4, 0, n+1),0) + D_rec.get((4, 1, n+1),0) + D_rec.get((4, 2, n+1),0) +D_rec.get((4, 3, n+1),0) + D_rec.get((4, 4, n+1),0)
    if row==2 and col==1:
        right = D_rec.get((0, 0, n+1),0) + D_rec.get((1, 0, n+1),0) + D_rec.get((2, 0, n+1),0) +D_rec.get((3, 0, n+1),0) + D_rec.get((4, 0, n+1),0)
    if row==2 and col==3:
        left = D_rec.get((0, 4, n+1),0) + D_rec.get((1, 4, n+1),0) + D_rec.get((2, 4, n+1),0) +D_rec.get((3, 4, n+1),0) + D_rec.get((4, 4, n+1),0)

    weight = top + left + right + bottom
    return weight

def recursive_evolve(D):
    D_copy = deepcopy(D) # Create a copy, which is the one will be updated
    D_weights = {}
    for k in D.keys():
        D_weights[k] = get_weight(D,*k)
        if D_copy[k]==1: # Bug
            if not D_weights[k]==1:
                D_copy[k] = 0 # A bug dies (becoming an empty space) unless there is exactly one bug adjacent to it.
        elif D_copy[k]==0: # Empty
            if D_weights[k]==1 or D_weights[k]==2:
                D_copy[k] = 1 # An empty space becomes infested with a bug if exactly one or two bugs are adjacent to it.
    return D_copy

def show_planet(D=None, depth=1):
    rows = 1
    cols = depth*2+1
    A = np.zeros((rows*5,cols*5))
    off_x = 0
    off_y = 0
    for n in range(-depth,depth+1):
        for x,y in iprod(range(5), range(5)):
            mult = 1
            if n==0:
                mult = 2
            if not(x==2 and y==2):
                A[x + off_x, y + off_y] = D[(x,y,n)]*mult
        off_y +=5

    # do stuff to randomly change some values of A
    #plt.ion()
    plt.matshow(A,cmap='PuBuGn')
    plt.show()

if __name__ == '__main__':
    D_phases = {}
    D_phases[0] = D = grid_to_dict(puzzle_input)
    
    i = 1
    exit_condition = False
    while not exit_condition:
        D_evo = evolve(D)
        print(bio_score(D_evo))
        for d in D_phases.values():
            if d==D_evo:
                print(f"Solution part 1: {bio_score(D_evo)}")
                exit_condition = True
                break
        D_phases[i] = D_evo
        D = deepcopy(D_evo)
        i+=1

    # Part 2
    # Initialise dictionary
    # 200 Minutes would need ~200 layers (one per side). We could create new entry as needed but 
    # creating them now helps me approach the problem.
    # Opt for flat hierarchy (row, column, layer) rather than nested. Central cell has no weight but is an empty dictionary
    D_rec = {}
    for i in range(-100,101):
        for x,y in iprod(range(5),range(5)):
            D_rec[(x,y,i)] = 0
        D_rec[(2,2,i)] = {}
    
    
    # Convert puzzle input in a 1s dict (1= bug) with middle dictionary, fill the master dictionary
    for x,y in iprod(range(5), range(5)):
        if puzzle_input[x][y]=='#':
            D_rec[(x,y,0)] = 1

    for i in range(200): # 200 minutes
        D_rec = recursive_evolve(D_rec)

    n_bugs = count_bugs(D_rec)
    print(f"Solution part 2: {n_bugs}")
    show_planet(D_rec,100)
