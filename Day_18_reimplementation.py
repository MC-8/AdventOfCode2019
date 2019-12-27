""" Reimplementation of Day 18 solution after seeing Johnatan Paulson YouTube stream
"""
from collections import deque, namedtuple
maze = []
for line in open('18.in','r').readlines():
    maze.append(list(line.strip()))
rows = len(maze)
cols = len(maze[0])

Q = deque()
all_keys = set()
State = namedtuple('State','r c keys d') # row, column, owned keys, n_steps made
for r in range(rows):
    for c in range(cols):
        char = maze[r][c]
        if char== '@': # Initial state
            Q.append(State(r,c,set(),0))
        if 'a'<= char <='z':
            all_keys.add(char)

seen = set()
print(Q[0])
got_keys = 0
while Q:
    S = Q.popleft()
    seen_state = (S.r, S.c, tuple(sorted(S.keys))) # Why tuple S.keys instead of just S.keys? 
                                                   # Because if key in seen would not be hashable otherwise
                                                   # Also, sort it to have a unique combination for the "key"
    got_keys = max(got_keys, len(S.keys)) 
    if seen_state in seen:
        continue
    seen.add(seen_state)
    if len(seen)%100000==0:
        print(f"{len(seen)=}, {len(Q)=}, {got_keys=}/{len(all_keys)}")
    if not( 0<S.r<rows and 0<S.c<cols and maze[S.r][S.c] != '#'):
        continue
    newkeys = set(S.keys)
    if 'a'<= maze[S.r][S.c] <='z': # found a key
        newkeys.add(maze[S.r][S.c])
        if newkeys==all_keys:
            print(f"Part 1 solution = {S.d}")
            break
    if 'A'<= maze[S.r][S.c] <='Z' and maze[S.r][S.c].lower() not in newkeys: # We don't have a key for this door
        continue
    # Add to queue the next locations
    for dr, dc in zip((-1,0,1,0), (0,1,0,-1)):
        Q.append(State(S.r + dr, S.c + dc, newkeys, S.d+1))


