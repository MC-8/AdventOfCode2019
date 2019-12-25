from itertools import permutations
from collections import namedtuple, deque
from copy import deepcopy

def get_reachable_keys(owned_keys, key_dependencies):
    reachable_keys = set()
    for k in key_dependencies.keys():
        if key_dependencies[k].issubset(owned_keys):
            reachable_keys.add(k)
    # Purge owned keys from reachable keys
    #if reachable_keys.intersection(owned_keys):
    for k in reachable_keys.intersection(owned_keys):
        reachable_keys.remove(k)
    return reachable_keys

char_maze = ["#########",
             "#b.A.@.a#",
             "#########"]

char_maze = ["########################",
             "#f.D.E.e.C.b.A.@.a.B.c.#",
             "######################.#",
             "#d.....................#",
             "########################"]

char_maze = ["########################",
             "#...............b.C.D.f#",
             "#.######################",
             "#.....@.a.B.c.d.A.e.F.g#",
             "########################"]

char_maze = ["#################",
             "#i.G..c...e..H.p#",
             "########.########",
             "#j.A..b...f..D.o#",
             "########@########",
             "#k.E..a...g..B.n#",
             "########.########",
             "#l.F..d...h..C.m#",
             "#################"]

start_pos = {}
goal_pos = {}
road_cells = []
keys = []
doors = []
lower_letters = 'abcdefghijklmnopqrstuvwxyz'
upper_letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

# Parse maze, non-wall cells are considered roads.
for r in range(len(char_maze[:])):
    for c in range(len(char_maze[0])):
        char = char_maze[r][c]
        if not char == '#': 
            road_cells.append((r,c))
        if char == '@':
            start_pos[char] = (r,c)
        if char in lower_letters:
            keys.append(char)
            start_pos[char] = (r,c)
        if char in upper_letters:
            doors.append(char)


depends = {}
steps_from_to = {}

for source, destination in permutations(start_pos.keys(),2):
    print(f"{source=}, {destination=}")


    # Explore maze from, to
    frontier = [start_pos[source]]
    visited = {} # cell : previous cell
    #visited[start_pos[source]] = start_pos[source]
    # Backtracking algorithm
    while frontier:
        f = frontier.pop(0)

        up = (f[0]-1,f[1])
        down = (f[0]+1,f[1])
        left = (f[0],f[1]-1)
        right = (f[0],f[1]+1)
        if (up    not in visited) and (up    in road_cells): 
            visited[up]    = f
            frontier.append(up)    # Add key, and from where it came from
        if (down  not in visited) and (down  in road_cells): 
            visited[down]  = f
            frontier.append(down)  # Add key, and from where it came from
        if (left  not in visited) and (left  in road_cells): 
            visited[left]  = f
            frontier.append(left)  # Add key, and from where it came from
        if (right not in visited) and (right in road_cells): 
            visited[right] = f
            frontier.append(right) # Add key, and from where it came from
    
    # Backtrack, and record dependencies
    pos = start_pos[destination]
    steps = 0
    if source=='@':
        depends[destination] = set()
    if pos not in visited:
        steps = -1
    else:
        while pos != start_pos[source]:
            pos = visited[pos]
            # Add dependencies if we crossed a door
            if char_maze[pos[0]][pos[1]] in doors:
                D = char_maze[pos[0]][pos[1]]
                if source=='@':
                    depends[destination].add(D.lower())

            steps += 1
    steps_from_to[source,destination] = steps

print(steps_from_to)
print(depends)

# Iterative solution to get all keys in the least amount of steps
stateNT = namedtuple('state','owned_keys reachable_keys steps current_position')
owned_keys = set()
state = stateNT( owned_keys = owned_keys, 
                 reachable_keys = get_reachable_keys(owned_keys, depends), 
                 steps = 0,
                 current_position = '@')

Q = deque()
Q.append(state)
solutions = []
# BFS, try to get all keys!
iterations = 0
while Q:
    iterations+=1
    if iterations%5000==0:
        print(f'{iterations=}')
    S = Q.popleft()
    assert(isinstance(S.reachable_keys, set))
    assert(isinstance(S.owned_keys, set))
    for k in S.reachable_keys:
        steps = S.steps
        steps += steps_from_to[S.current_position, k]
        #print(f"Go from {S.current_position} to {k}")
        owned_keys = deepcopy(S.owned_keys)
        # This does not take into account the keys that may be collected on the way to another key
        # For a first solution it's ok, because  when going from a to c in a-b-c
        # the a-c-b solution (fake) will be longer than a-b-c and discarded later on
        owned_keys.add(k) 
        current_position = k
        reachable_keys = get_reachable_keys(owned_keys, depends)
        new_state = stateNT(owned_keys = owned_keys, 
                            reachable_keys = reachable_keys, 
                            steps = steps, 
                            current_position = current_position)
        #print(new_state)
        if not new_state.reachable_keys:
            # There are no more reachable keys! We may have them all :)
            solutions.append(new_state)
        else:
            Q.append(new_state)

min_steps = 1e10
for s in solutions:
    if s.steps<min_steps:
        min_steps = s.steps

print(f"Solution part 1 is: {min_steps} ")