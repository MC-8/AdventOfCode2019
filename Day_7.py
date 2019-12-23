from intcode import intcode
from copy import deepcopy
from itertools import permutations

puzzle_input =  [3,8,1001,8,10,8,105,1,0,0,21,34,43,64,85,98,179,260,341,422,99999,3,9,1001,9,3,9,102,3,9,9,4,9,99,3,9,102,5,9,9,4,9,99,3,9,1001,9,2,9,1002,9,4,9,1001,9,3,9,1002,9,4,9,4,9,99,3,9,1001,9,3,9,102,3,9,9,101,4,9,9,102,3,9,9,4,9,99,3,9,101,2,9,9,1002,9,3,9,4,9,99,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,2,9,4,9,99,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,99,3,9,101,1,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,99]
puzzle_input.extend([0]*5000)
#puzzle_input = [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]
N_STAGES = 5

Amp =[None]*N_STAGES
max_energy = 0
# Part 1
for perm in permutations(range(N_STAGES)):
    
    for i in range(N_STAGES):
        Amp[i] = intcode.IntCode(program = deepcopy(puzzle_input), instance=i)
        Amp[i].push_input(perm[i])
    Amp[0].push_input(0)
    
    for i in range(N_STAGES):
        Amp[i].run()
        o = Amp[i].pop_output()
        Amp[(i+1)%N_STAGES].push_input(o)

    max_energy = max(max_energy, o)

print(f"Solution part 1: {max_energy}")

# Part 2
Amp =[None]*N_STAGES
max_energy = 0
o4 = []
for perm in permutations(range(5, 5 + N_STAGES)):
    
    for i in range(N_STAGES):
        Amp[i] = intcode.IntCode(program = deepcopy(puzzle_input), instance=i)
        Amp[i].push_input(perm[i])
    Amp[0].push_input(0)
    
    while not Amp[-1].done:
        for i in range(N_STAGES):
            # Run until output is available and pass it to the next amplifier. 
            # Until they are done
            while(not Amp[i].output_available() and not Amp[i].done):
                Amp[i].step()
            if (Amp[i].done):
                continue
            o = Amp[i].pop_output()
            o4.append(o)
            Amp[(i+1)%N_STAGES].push_input(o)


print(o4)
print(f"Solution part 2: {max(o4)}")