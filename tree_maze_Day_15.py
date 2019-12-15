import h5py
import numpy as np
import heapq

class Node(object):
    def __init__(self, value):
        self.value      = value
        self.childs     = None
        self.n_childs   = 0

    def add_child(self, value):
        self.childs.append(value)
        self.n_childs+=1

class MazeTree(object):
    def __init__(self, value):
        self.root = Node(value)
# value = (distance, pos) 


def read_maze(filename):
    maze = None
    with h5py.File(filename, 'r') as file:
        maze = np.asarray(file['Z'],dtype=np.int32)
    return maze
    
def move(p, d):
    return (p[0] + d[0], p[1] + d[1])

dirs = {1: (0, 1), 2: (0, -1), 3: (-1, 0), 4: (1, 0)} # directions  
pos = (19, 19) # starting position
steps = 0
known_loc = {pos: " "}
mt = MazeTree((steps,pos))

# Exploration step, to build the tree
current_node = mt.root
new_cell = False
for c in current_node.childs:

    for d in dirs:
        next_cell = pos + move(pos, d)

        if next_cell not in known_loc:
            c.add_child((steps+1,next_cell))
            new_cell = True

        known_loc[next_cell] = maze[next_cell]

mazemap = []
maze = read_maze('maze.mat')
print(read_maze('maze.mat'))
