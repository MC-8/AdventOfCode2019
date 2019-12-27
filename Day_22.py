import re
from enum import Enum
import numpy as np
from collections import deque
from copy import deepcopy
class Operation(Enum):
    DEAL_WITH_INCREMENT = 0
    CUT = 1
    DEAL_INTO_NEW_STACK = 2

def parse_step(str_step):
    if ' increment' in str_step:
        S = Operation.DEAL_WITH_INCREMENT
        V = int(str_step.split()[-1])
        return S, V
    if 'cut' in str_step:
        S = Operation.CUT
        V = int(str_step.split()[-1])
        return S, V
    if 'deal into new stack' in str_step:
        S = Operation.DEAL_INTO_NEW_STACK
        V = None
        return S, V

def cut(l, n):
    lq = deque(l)
    lq.rotate(-n)
    return list(lq)

def deal_with_increment(l, n):
    idx = 0
    nl = np.zeros_like(l)
    for e in l:
        dest_idx = n*idx % len(l)
        nl[dest_idx] = e
        idx += 1
    return list(nl)

def deal_into_new_stack(l):
    return list(l[::-1])

with open("Day_22_input.txt", 'r') as f:
    procedure = f.readlines()
    sequence = []
    for step in procedure:
        sequence.append(parse_step(step))
    # Part 1
    L = range(10007)
    for op_val in sequence:
        if op_val[0] == Operation.DEAL_INTO_NEW_STACK:
            L = deal_into_new_stack(L)
        if op_val[0] == Operation.DEAL_WITH_INCREMENT:
            L = deal_with_increment(L, op_val[1])
        if op_val[0] == Operation.CUT:
            L = cut(L, op_val[1])
    print(f"Part 1 solution = {L.index(2019)}")
    sequence = []
    with open("Day_22_input.txt", 'r') as f:
        procedure = f.readlines()
        for step in procedure:
            sequence.append(parse_step(step))
    m = 119315717514047
    n = 101741582076661
    a = 1 # Gradient
    b = 0 # Offset
    pos = 2020
    for op_val in sequence:
        if op_val[0] == Operation.DEAL_INTO_NEW_STACK:
            a = -a %m
            b = (m-1-b) %m
        if op_val[0] == Operation.DEAL_WITH_INCREMENT:
            x = op_val[1]            
            a = a*x %m
            b = b*x %m
        if op_val[0] == Operation.CUT:
            x = op_val[1]            
            b = b - x

    r = (b * pow(1-a, m-2, m)) % m
    solution = ((pos-r) * pow(a, n*(m-2),m) +r) %m
    print(f"Part 2 {solution=}")