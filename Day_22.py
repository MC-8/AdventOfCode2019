import re
from enum import Enum
import pprint
import numpy as np
from collections import deque
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
    pp = pprint.PrettyPrinter()
    #pp.pprint(sequence)
    
    # # Basics
    # L = range(10)
    # print(deal_into_new_stack(L))
    # print(cut(L,3))
    # print(cut(L,-4))
    # print(deal_with_increment(L, 3))
    
    # # Example
    # L = range(10)
    # L = deal_with_increment(L, 7)
    # L = deal_into_new_stack(L)
    # L = deal_into_new_stack(L)
    # print(L)
    # L = range(10)
    # L = cut(L,6)
    # L = deal_with_increment(L, 7)
    # L = deal_into_new_stack(L)
    # print(L)
    # L = range(10)
    # L = deal_with_increment(L, 7)
    # L = deal_with_increment(L, 9)
    # L = cut(L,-2)
    # print(L)
    # L = range(10)
    # L = deal_into_new_stack(L)
    # L = cut(L,-2)
    # L = deal_with_increment(L, 7)
    # L = cut(L,8)
    # L = cut(L,-4)
    # L = deal_with_increment(L, 7)
    # L = cut(L,3)
    # L = deal_with_increment(L, 9)
    # L = deal_with_increment(L, 3)
    # L = cut(L,-1)
    # print(L)
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
    print(f"=================================")

    # Check values...
    L = list(range(10007))
    v = 2020
    res_list = []
    res_dict = {}
    val_before_shuffle = L[v]
    while (val_before_shuffle not in res_list):
        for op_val in sequence:
            if op_val[0] == Operation.DEAL_INTO_NEW_STACK:
                L = deal_into_new_stack(L)
            if op_val[0] == Operation.DEAL_WITH_INCREMENT:
                L = deal_with_increment(L, op_val[1])
            if op_val[0] == Operation.CUT:
                L = cut(L, op_val[1])
        res_list.append(L[v])
        
    with open('your_file.txt', 'w') as f:
        for item in L:
            f.write("%s\n" % item)
    # with open('your_file.txt', 'w') as f:
    #     for item in L:
    #         f.write("%s\n" % item)
    # print("\n-----------------------\n")
    # print(L)
    # print("\n-----------------------\n")
    # print(len(res_list))
    # print("\n-----------------------\n")
    # print(res_list)
    # print("\n-----------------------\n")
    # print(f"Begin part 2")
    # L = range(119315717514047)
    # for op_val in sequence:
    #     if op_val[0] == Operation.DEAL_INTO_NEW_STACK:
    #         L = deal_into_new_stack(L)
    #     if op_val[0] == Operation.DEAL_WITH_INCREMENT:
    #         L = deal_with_increment(L, op_val[1])
    #     if op_val[0] == Operation.CUT:
    #         L = cut(L, op_val[1])
    # print("Done 1 step on huge deck")

