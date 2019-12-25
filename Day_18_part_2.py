# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
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

char_maze = ["#######",
             "#a.#Cd#",
             "##@#@##",
             "#######",
             "##@#@##",
             "#cB#.b#",
             "#######"]

char_maze = ["###############",
             "#d.ABC.#.....a#",
             "######@#@######",
             "###############",
             "######@#@######",
             "#b.....#.....c#",
             "###############"]

char_maze = ["#############",
             "#DcBa.#.GhKl#",
             "#.###@#@#I###",
             "#e#d#####j#k#",
             "###C#@#@###J#",
             "#fEbA.#.FgHi#",
             "#############"]

char_maze = ["#############",
             "#g#f.D#..h#l#",
             "#F###e#E###.#",
             "#dCba@#@BcIJ#",
             "#############",
             "#nK.L@#@G...#",
             "#M###N#H###.#",
             "#o#m..#i#jk.#",
             "#############"]

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
             "#.........#.................#...#...#..@#@..#.................#.#.....#.#.......#",
             "#################################################################################",
             "#.......#.................#............@#@#.....#...........#.........#...#.....#",
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
keys_set = set()
doors = []
lower_letters = 'abcdefghijklmnopqrstuvwxyz'
upper_letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
robot_id = 0
# Parse maze, non-wall cells are considered roads.
for r in range(len(char_maze[:])):
    for c in range(len(char_maze[0])):
        char = char_maze[r][c]
        if not char == '#': 
            road_cells.append((r,c))
        if char == '@':
            start_pos[char+str(robot_id)] = (r,c)
            robot_id += 1
        if char in lower_letters:
            keys.append(char)
            keys_set.add(char)
            start_pos[char] = (r,c)
        if char in upper_letters:
            doors.append(char)


depends = {}
steps_from_to = {}
bonus_keys_from_to = {}

for source, destination in permutations(start_pos.keys(),2):
    print(f"\n{source=}, \t{destination=}", end='', flush=True)
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
    if '@' in source and '@' not in destination and not destination in depends:
        depends[destination] = set()
    if pos not in visited:
        steps = -1
    else:
        while pos != start_pos[source]:
            pos = visited[pos]
            # Add dependencies if we crossed a door
            C = char_maze[pos[0]][pos[1]]
            if C in doors:
                if '@' in source and '@' not in destination:
                    depends[destination].add(C.lower())
            # Add "keys captured along they way kind of thing"
            if C in keys and C not in (source):
                bonus_keys_from_to[source,destination].add(C)
                # TRY TODO CHECK: to reduce tree, only allow first visible key to be reached (not the ones behind, even if there are no doors)
                if '@' in source and '@' not in destination:
                    depends[destination].add(C)
            steps += 1
    steps_from_to[source,destination] = steps
    steps_from_to[source,source] = 0
    bonus_keys_from_to[source,source] = set()
    print(f", \t{steps=}",end='',flush=True)
    print(f", \t{bonus_keys_from_to[source,destination]=}",end='',flush=True)
    if '@' in source and '@' not in destination:
        print(f", \t{depends[destination]=}",end='',flush=True)
print('\n')
print(f"{steps_from_to=}")
print(f"{depends=}") 


# %%
# Iterative solution to get all keys in the least amount of steps
stateNT = namedtuple('state','owned_keys reachable_keys steps current_position')
owned_keys = set()

state = stateNT( owned_keys = owned_keys, 
                 reachable_keys = get_reachable_keys(owned_keys, depends), 
                 steps = 0,
                 current_position = ['@0','@1','@2','@3'])
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

while Q:
    iterations+=1
    S = Q.popleft()
    if iterations%10000==0:
        print(f'{iterations=}, {n_solutions=}, {min_steps=}, {max_got_keys=}/{keys_target}, {len(Q)=}, {killed_branches=}')
    assert(isinstance(S.reachable_keys, set))
    assert(isinstance(S.owned_keys, set))
    for k in S.reachable_keys:
        steps = S.steps
        # if steps_from_to[S.current_position, k]==-1 or steps_from_to[S.current_position, k]==0:
        #     # Key is not reachable from here
        #     continue
        for idx, pos in enumerate(S.current_position): # Do every quadrant
            if steps_from_to[pos, k] > 0: # Can move!
                steps += steps_from_to[pos, k]
                owned_keys = deepcopy(S.owned_keys)
                # This does not take into account the keys that may be collected on the way to another key
                # For a first solution it's ok, because  when going from a to c in a-b-c
                # the a-c-b solution (fake) will be longer than a-b-c and discarded later on
                # Problem is that it adds many more iterations. Should consider to add a "keys captured
                # along the way to destination" kind of thing
                owned_keys.add(k)
                owned_keys.union(bonus_keys_from_to[pos, k])
                current_position = deepcopy(S.current_position)
                current_position[idx] = k
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
                else:
                    iset = sets_list.index(owned_keys)
                    # if steps >= steps_list[iset] and current_position==heads_list[iset]:
                    if  ((steps >= steps_list[iset] and current_position==heads_list[iset]) or 
                        steps > 1630): # We know we can do better than this
                        killed_branches+=1
                        continue_branch = False
                    else:
                        steps_list[iset] = steps
                        heads_list[iset] = current_position
                if owned_keys == keys_set:
                    # There are no more reachable keys! We may have them all :)
                    #print("ONE SOLUTION WAS FOUND!!!")
                    #print(new_state)
                    #solutions.append(new_state)
                    min_steps = min(min_steps, steps)
                    n_solutions += 1
                else:
                    if continue_branch:
                        if Q and (steps < Q[0].steps): # Prioritise shortest solutions
                            Q.appendleft(new_state)
                        else:
                            Q.append(new_state)
            else:
                pass
                # I can't move

# min_steps = 1e10
# for s in solutions:
#     if s.steps<min_steps:
#         min_steps = s.steps

print(f"Solution part 1 is: {min_steps=} among {n_solutions=} with a total of {iterations=}")


# %%


