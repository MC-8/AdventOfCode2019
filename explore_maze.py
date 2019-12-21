""" Simple maze exploration """

char_maze = ["#########A#######.###",
             "#########.#######.###",
             "#########.###.###.###",
             "#########.........###",
             "#########.#######.###",
             "#########.#######.###",
             "#########.#######.###",
             "#########.#######.###",
             "##........#######.###",
             "####.############.###",
             "####........#####.###",
             "#####.#####.#####.###",
             "####.######.#####.###",
             "##...######...###.###",
             "###.#########.###.###",
             "##..#########.....###",
             "#############.#######",
             "#############.#######",
             "#############Z#######"]


start_pos = None
goal_pos = None
visited = {} # cell : previous cell
good_path = []
# Parse maze
for r in range(len(char_maze[:])):
    for c in range(len(char_maze[0])):
        if char_maze[r][c] == '.':
            good_path.append((r,c))
        if char_maze[r][c] == 'A':
            start_pos = (r,c)
        if char_maze[r][c] == 'Z':
            goal_pos = (r,c)

good_path.append(start_pos)
good_path.append(goal_pos)

frontier = [start_pos]
visited[r,c] = (r,c)

% Backtracking algorithm
while frontier:
    f = frontier.pop(0)

    up = (f[0]-1,f[1])
    down = (f[0]+1,f[1])
    left = (f[0],f[1]-1)
    right = (f[0],f[1]+1)
    if (up    not in visited) and (up    in good_path): 
        visited[up]    = f
        frontier.append(up)    # Add key, and from where it came from
    if (down  not in visited) and (down  in good_path): 
        visited[down]  = f
        frontier.append(down)  # Add key, and from where it came from
    if (left  not in visited) and (left  in good_path): 
        visited[left]  = f
        frontier.append(left)  # Add key, and from where it came from
    if (right not in visited) and (right in good_path): 
        visited[right] = f
        frontier.append(right) # Add key, and from where it came from

# Backtrack
pos = goal_pos
step = 0
if goal_pos not in visited:
    step = -1
else:
    while pos != start_pos:
        pos = visited[pos]
        step += 1

print(step)