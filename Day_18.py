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

def get_visible_keys(owned_keys, key_dependencies):
    visible_keys = set()
    for k in key_dependencies.keys():
        if key_dependencies[k].issubset(owned_keys):
            visible_keys.add(k)
    # Purge owned keys from visible keys
    #if visible_keys.intersection(owned_keys):
    for k in visible_keys.intersection(owned_keys):
        visible_keys.remove(k)
    return visible_keys

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

char_maze = ["#################", # Hard one, is a bit slow
             "#i.G..c...e..H.p#",
             "########.########",
             "#j.A..b...f..D.o#",
             "########@########",
             "#k.E..a...g..B.n#",
             "########.########",
             "#l.F..d...h..C.m#",
             "#################"]

char_maze = ["########################",
             "#@..............ac.GI.b#",
             "###d#e#f################",
             "###A#B#C################",
             "###g#h#i################",
             "########################"]

char_maze = ["#################################################################################",
             "#...#.....#......c....#...#.Q.......#...#f#a....#..j..........#...............#.#",
             "#.#.#.#.###.#######.#.#.#.#.###.###.#.#.#.#.###.#.#######.###.#.#.###########.#.#",
             "#.#.#v#.....#.....#.#...#.#.#...#...#.#.#.#...#.......#...#.#.#.#...#...#.....N.#",
             "###.#.#######.###.#X#######.#.###.###.###.###.#########R###.#.#.###.#.#.#.#######",
             "#.K.#.....#...#...#.....#...#.#.....#...#.....#.......#.#.#...#...#.#.#.#...#...#",
             "#.#.#####.#.###.#######.#.###.#####.#.#.#.#####.#####.#.#.#.#####.#.#.#.#####.#.#",
             "#.#.#.U.#.#.#...#...#...#...#...#...#.#.#.#...#.#...#...#.#.....#.#...#.......#.#",
             "#.#.###.#.#.#.#####.#.#.###.###.#.#####.#.#.#.#.###.#####.#####.#####.#####.###.#",
             "#.#.#...#...#.....#.#.#...#.#.#.#.....#.#.#.#.#.Y.#.....#.....#.....#.#...#...#.#",
             "#.#.#.#.#########.#.#.#####.#.#.#####.#.#.###.###.###.#.###.#.#####.###.#.#####.#",
             "#.#...#.#.........#.#.........#.#...#...#.#...#...#...#.#...#.#...#...#.#.......#",
             "#.#######.#########.###########.###.###.#.#.###.###.###.#.###.###.###.#.#######.#",
             "#.....#...#.#...........#.......#.....#.#...#...#.#...#...#.........#.#.#...#...#",
             "#.###.#.###.#.#########.#.#######.#####.#####.###.#.#.###############.#.#.#.#.###",
             "#.#.#.#...#.....#.......#.#.............#.....#.....#.....#.....#...#.#...#.#...#",
             "#.#.#.###.#####.#.#######.#.#####.#####.#.#####.#####.###.#.###.#.#.#.#.###.#####",
             "#.#.#...#.O...#.#.#.......#.#...#.#...#.#...#...#...#...#...#...#.#...#...#.....#",
             "#.#.#.#######.###.#.#####.###.#.#.#.#.#.#.#.#####.#.###.#####.###.#######.#####.#",
             "#.#.#.......#.....#.....#t#...#.#.#.#.#.#.#.#.....#.#.......#.....#.....#.#.....#",
             "#.#.#####.#######.#####.###.###.###.#.#.###.#.#####.###########.###.###.###.###.#",
             "#.......#.........#...#...#.#.#.....#.#.#...#.....#.#.....#...#.....#...#...#.#.#",
             "#######.###########.#####.#.#.#######.#.#.#####.###.#.###.#.###.#####.###.###.#.#",
             "#.......#.......#...#...#.#...#...#...#.#.#.....#...#.#.#.#...#.#...#.....#.#...#",
             "#.#####.#.#######.###.#.#.###.#.###.#####.#.#####.###.#.#.###.###.#.#.#####.#.###",
             "#.#...#...#...#...#...#.#.#...#...#.....#...#...#.......#...#...#.#.#.#...#...#.#",
             "#.#.#.#####.#.#.###.###.#.#.#####.#####.#P###.#.#######.###.###.#.#.###.#.###.#.#",
             "#.#.#.......#...#...#.....#.#.....#...#.#.#i..#...#...#.#.....#...#.#...#...#...#",
             "###.###############.#######.#.#.#.###.#.#.#####.###.#.###.#########.#.#####.###.#",
             "#...#.............#...#...#.#.#.#.#...#.#.....#.#...#.....#.......#.#...#...#.#.#",
             "#.###.#######.###.#.#.#.#.#.###.#.#.#.#.#####.#.#.#.#######.#####.#.###.###.#.#.#",
             "#.#.........#.#...#.#...#.......#...#.#.#.....#.#.#.#...#...#...#.#...#...#.#.#.#",
             "#.###########.#.###.###############.###.#.#####.#.###.#.#.###.###.###.###.#.#.#Z#",
             "#...#.........#.#.#.#.#.......#.....#...#.#.....#.#...#...#...#.....#.....#.#...#",
             "###.#.#########.#.#.#.#.#####.#.#####.#.#.###.###.#.#########.#.###.#######.#.###",
             "#.#...#.....#...#.#...#.#...#.#...#...#.#.#...#...#.#.......#.#...#.#.......#.#.#",
             "#.#####.#.###.###.###.#.#.#.#.#####.###.#.#.###.#.#.###.###.#.###.#.#.#######.#.#",
             "#.....#.#...#.#.......#...#.#.#...#.#...#.#.#...#.#.....#...#...#.#.#.#.....#..x#",
             "#.#####.###.#.#############.#.#.#.#.#.###.#.#.###########.###.#.#.###.#.#.#####.#",
             "#.........#.................#...#...#.......#.................#.#.....#.#.......#",
             "#######################################.@.#######################################",
             "#.......#.................#...............#.....#...........#.........#...#.....#",
             "#.#####.#.#########.#####.#.###########.#.#.###.#.#.#######.#.#.#######.#.###.#.#",
             "#...#.#.#.#...#...#.....#.#...#...#.....#.#...#...#.....#...#.#...#.....#.#...#.#",
             "###.#.#.###.#.#.#.#####.#.#####.#.#.###.#.###.#########.#####.###.#.#####.#V#####",
             "#...#.#...#.#.#.#.....#.#.#.....#.#.#...#...#.#.....#.#.....#...#...#...#.#.....#",
             "#.###.###.#.#.#.#####.#.#.#.#####.#.#.###.###.#.#.#.#.#####.###.#######.#.#####.#",
             "#...#...#.#.#.#.....#...#.#.#.....#.#...#.#...#.#.#.W.#...#...#.........#.....#.#",
             "#.#.###.#G#.#.#####.#####.#.#.#####.#####.#.#####.###.###.###.#####.#########.#.#",
             "#.#.#...#...#.#.....#...#...#.#.........#...#...#...#.......#.....#.#.....#...#.#",
             "###.#.#######.#.#######.#####.#.#######.#.###.#.###.#######.#.#####.#.###.#.###.#",
             "#...#.#.....#...#...........#.#.....#...#p....#...#.....#...#......r#.#.....#...#",
             "#.###.#.#.#######.###.#.#####.#.#####.#.#########.#.###.#E###########.#######.#.#",
             "#.#.....#.#.........#.#.#...#.#.#.....#.#...#...#.#.#...#...#.S.....#...#.....#.#",
             "#.#######.#.#########.#.#.#.#.#.#.#######.###.#.#.#.#.#####.###.#######.#.###.###",
             "#.L.....#.#z....#.....#.#.#.#.#.#...#...#.#...#...#.#.#.........#.......#.#.#...#",
             "#.#####.#.#####.#.#####.#.#.#.#####.#.#.#.#.#########.#.#########.#######.#.###.#",
             "#.#...#.#...#...#.....#.#.#...#.....#.#.#.#.......#...#.#...#.....#.#..o#.#.#...#",
             "#.#.###.###.#.#######.###.#####.#####.#.#.#######.#.###.#.#.#.#####.#.#.#.#.#.###",
             "#.#.#...#...#.......#...#.#.#...I.....#.#...#...#.#...#...#b#.#.......#.#...#...#",
             "#.#.#.###.#####.#######.#.#.#.#########.#.#.###.#.###.#######.#.#######.###.###.#",
             "#.#.#.#.#.......#.....#.#.#......y..#.#.#.#.....#...#...#...#.#..l#..g#.#.....#.#",
             "#.#.#.#.#.#######H#####.#.###.#####.#.#.#.###.#####.#.#.#.#.#####.#.#.#.#.#####.#",
             "#...#.#.#...#...#.#..h#.#...#.#...#...#.#.#...#.....#.#.#.#.....#.#.#.#.#.#.#...#",
             "#.###.#.###.#.#.#.#.#.#.###.###.#.#####.#.#####.#######.#.###.#.#.#.#.#.#.#.#.#.#",
             "#.#...#.......#.#...#.#.....#...#...#...#...#...#.....#.#...#.#.#.#.#...#...#.#.#",
             "#.#.###########.#####D#####.#.#####.#.#.#.#.#.###.###.#.###.#.#.#.#.#######.#.#.#",
             "#.#.#.....#.......#.#.....#...#.....#.#.#.#.#.#...#...#.....#.#.#.#...#.....#.#.#",
             "#M#.#.###.#######.#.#####.#####.#####.#####.#.#.###.###.#####.###.###.#.#####.#.#",
             "#.#.....#.#.....#.......#...#.#.#.......#...#...#...#...#...#.......#...#...#.#.#",
             "#.#######.#.###.#.#########.#A#.###.###.#.#######.#######.#.#.###########.#.#.#.#",
             "#.#w....#.#...#.#.#....d....#.#...#...#.#.......#...#...#.#.#..m#.....#...#...#.#",
             "#.#.###.#.###.#.###.#########.###.#####.#.###.#####.#.#.#.#.###.#.###.#.#######.#",
             "#k#...#.#u#...#...B.#.....#.....#.....#.#...#.....#...#.#.#...#.#.#.#...#..n#...#",
             "#.###.#.#.#.#########.###.#.#.#.#####J#.###.###.#.#####.#.###.###.#.#######.#.###",
             "#.#...#...#...#...#...#.#...#.#.....#.#.#...#.#.#.....#.#...#...#.#.........#.#.#",
             "###.#########.#.###F###.#####.#######.#.#.###.#.#####T#.###.###.#.#.#.#####.#.#.#",
             "#...#.......#s#...#.........#...#...#...#.#...#.....#.#...#...#.#q#.#.#.....#...#",
             "#.###.#####.#.#.#.#########.###.#.#.###.#.#.#.#####.#####.###.#.#.#.#.#########C#",
             "#..e......#...#.#.............#...#.....#...#.....#...........#...#.#...........#",
             "#################################################################################"]

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
bonus_keys_from_to = {}
key_order_from_to = {}

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
    bonus_keys_from_to[source,destination] = set()
    key_order_from_to[source,destination] = []
    if source=='@':
        depends[destination] = set()
    if pos not in visited:
        steps = -1
    else:
        while pos != start_pos[source]:
            pos = visited[pos]
            # Add dependencies if we crossed a door
            C = char_maze[pos[0]][pos[1]]
            if C in doors:
                if source=='@':
                    depends[destination].add(C.lower())
            # Add "keys captured along they way kind of thing"
            if C in keys and not C==destination:
                bonus_keys_from_to[source,destination].add(C)
                key_order_from_to[source,destination].append(C)
                # TRY TODO CHECK: to reduce tree, only allow first visible key to be reached (not the ones behind, even if there are no doors)
                if source=='@':
                    depends[destination].add(C)
            steps += 1
    steps_from_to[source,destination] = steps
    key_order_from_to[source,destination].reverse()
# print(steps_from_to)
# print(depends)

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
sets_list = []
steps_list = [] # Min steps associated to get that set of keys (kill early combinations that took too many steps)
heads_list = [] # Position associated with a set of keys
# BFS, try to get all keys!
iterations = 0
min_steps = 10000
n_solutions = 0
keys_target = len(keys)
max_got_keys = 0
killed_branches = 0
min_steps_max_keys = 10000
while Q:
    iterations+=1
    S = Q.popleft()
    if iterations%10000==0:
        print(f'{iterations=}, {n_solutions=}, {min_steps=}, {max_got_keys=}/{keys_target}, {len(Q)=}, {killed_branches=}')
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
        # Problem is that it adds many more iterations. Should consider to add a "keys captured
        # along the way to destination" kind of thing
        owned_keys.add(k)
        owned_keys.union(bonus_keys_from_to[S.current_position, k])
        current_position = k
        reachable_keys = get_reachable_keys(owned_keys, depends)
        new_state = stateNT(owned_keys = owned_keys, 
                            reachable_keys = reachable_keys, 
                            steps = steps, 
                            current_position = current_position)
        #print(new_state)
        continue_branch = True
        if owned_keys not in sets_list:
            sets_list.append(owned_keys)
            steps_list.append(steps)
            heads_list.append(current_position)
            max_got_keys = max(max_got_keys, len(owned_keys))
            if max_got_keys == len(owned_keys):
                min_steps_max_keys = min(steps, min_steps_max_keys)
        else:
            iset = sets_list.index(owned_keys)
            # if steps >= steps_list[iset] and current_position==heads_list[iset]:
            if  ((steps >= steps_list[iset] and 
                  current_position==heads_list[iset]) or
                steps > 3864): # We know we can do better than this
                killed_branches+=1
                continue_branch = False
            else:
                steps_list[iset] = steps
                heads_list[iset] = current_position
        if not new_state.reachable_keys:
            # There are no more reachable keys! We may have them all :)
            #print("ONE SOLUTION WAS FOUND!!!")
            #print(new_state)
            #solutions.append(new_state)
            min_steps = min(min_steps, steps)
            n_solutions += 1
        else:
            if continue_branch:
                if Q and (steps < Q[0].steps): # Prioritise shortest solutions
                    Q.appendleft(deepcopy(new_state))
                else:
                    Q.append(deepcopy(new_state))

# min_steps = 1e10
# for s in solutions:
#     if s.steps<min_steps:
#         min_steps = s.steps

print(f"Solution part 1 is: {min_steps=} among {n_solutions=} with a total of {iterations=}")