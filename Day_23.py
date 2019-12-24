from intcode import intcode
from copy import deepcopy
from collections import namedtuple
from dataclasses import dataclass

@dataclass
class Packet:
    x: int
    y: int
    ip: int

puzzle_input = [3,62,1001,62,11,10,109,2255,105,1,0,2061,1550,1927,1618,1090,672,1649,870,1783,810,1818,2102,2030,1253,571,1154,841,779,1185,1412,1447,2224,907,1016,602,936,1519,1284,1121,1581,1055,2193,1686,1348,707,1752,1482,1317,1958,969,746,1379,1999,2162,1851,1886,2131,637,1220,1717,0,0,0,0,0,0,0,0,0,0,0,0,3,64,1008,64,-1,62,1006,62,88,1006,61,170,1106,0,73,3,65,20102,1,64,1,21002,66,1,2,21102,105,1,0,1106,0,436,1201,1,-1,64,1007,64,0,62,1005,62,73,7,64,67,62,1006,62,73,1002,64,2,132,1,132,68,132,1001,0,0,62,1001,132,1,140,8,0,65,63,2,63,62,62,1005,62,73,1002,64,2,161,1,161,68,161,1101,1,0,0,1001,161,1,169,1001,65,0,0,1101,0,1,61,1102,0,1,63,7,63,67,62,1006,62,203,1002,63,2,194,1,68,194,194,1006,0,73,1001,63,1,63,1106,0,178,21101,210,0,0,106,0,69,2102,1,1,70,1102,0,1,63,7,63,71,62,1006,62,250,1002,63,2,234,1,72,234,234,4,0,101,1,234,240,4,0,4,70,1001,63,1,63,1105,1,218,1106,0,73,109,4,21102,1,0,-3,21102,0,1,-2,20207,-2,67,-1,1206,-1,293,1202,-2,2,283,101,1,283,283,1,68,283,283,22001,0,-3,-3,21201,-2,1,-2,1106,0,263,21202,-3,1,-3,109,-4,2105,1,0,109,4,21102,1,1,-3,21101,0,0,-2,20207,-2,67,-1,1206,-1,342,1202,-2,2,332,101,1,332,332,1,68,332,332,22002,0,-3,-3,21201,-2,1,-2,1106,0,312,21202,-3,1,-3,109,-4,2105,1,0,109,1,101,1,68,359,20101,0,0,1,101,3,68,366,21001,0,0,2,21101,376,0,0,1106,0,436,21202,1,1,0,109,-1,2105,1,0,1,2,4,8,16,32,64,128,256,512,1024,2048,4096,8192,16384,32768,65536,131072,262144,524288,1048576,2097152,4194304,8388608,16777216,33554432,67108864,134217728,268435456,536870912,1073741824,2147483648,4294967296,8589934592,17179869184,34359738368,68719476736,137438953472,274877906944,549755813888,1099511627776,2199023255552,4398046511104,8796093022208,17592186044416,35184372088832,70368744177664,140737488355328,281474976710656,562949953421312,1125899906842624,109,8,21202,-6,10,-5,22207,-7,-5,-5,1205,-5,521,21101,0,0,-4,21101,0,0,-3,21101,51,0,-2,21201,-2,-1,-2,1201,-2,385,470,21001,0,0,-1,21202,-3,2,-3,22207,-7,-1,-5,1205,-5,496,21201,-3,1,-3,22102,-1,-1,-5,22201,-7,-5,-7,22207,-3,-6,-5,1205,-5,515,22102,-1,-6,-5,22201,-3,-5,-3,22201,-1,-4,-4,1205,-2,461,1106,0,547,21101,-1,0,-4,21202,-6,-1,-6,21207,-7,0,-5,1205,-5,547,22201,-7,-6,-7,21201,-4,1,-4,1106,0,529,22102,1,-4,-7,109,-8,2105,1,0,109,1,101,1,68,563,21002,0,1,0,109,-1,2105,1,0,1101,0,81181,66,1101,1,0,67,1102,598,1,68,1101,0,556,69,1102,1,1,71,1102,600,1,72,1105,1,73,1,-153,49,88318,1102,1,43591,66,1101,1,0,67,1101,629,0,68,1101,0,556,69,1101,3,0,71,1101,0,631,72,1105,1,73,1,2,23,122289,38,107907,38,215814,1102,39679,1,66,1101,0,3,67,1102,1,664,68,1101,0,302,69,1101,1,0,71,1102,1,670,72,1105,1,73,0,0,0,0,0,0,7,38518,1101,0,102077,66,1102,1,1,67,1101,699,0,68,1101,556,0,69,1101,3,0,71,1101,701,0,72,1105,1,73,1,5,29,33457,29,66914,38,179845,1101,71993,0,66,1101,5,0,67,1102,734,1,68,1102,253,1,69,1101,0,1,71,1101,744,0,72,1106,0,73,0,0,0,0,0,0,0,0,0,0,20,116758,1101,0,83561,66,1102,1,2,67,1101,0,773,68,1102,302,1,69,1102,1,1,71,1101,0,777,72,1105,1,73,0,0,0,0,45,141402,1101,51481,0,66,1102,1,1,67,1102,1,806,68,1102,1,556,69,1102,1,1,71,1102,808,1,72,1106,0,73,1,160,38,35969,1101,0,35999,66,1101,0,1,67,1102,837,1,68,1101,556,0,69,1102,1,1,71,1102,839,1,72,1105,1,73,1,571,6,17551,1102,18773,1,66,1102,1,1,67,1101,0,868,68,1101,0,556,69,1101,0,0,71,1101,0,870,72,1105,1,73,1,1631,1102,1,19259,66,1102,1,4,67,1101,897,0,68,1102,1,253,69,1102,1,1,71,1101,905,0,72,1105,1,73,0,0,0,0,0,0,0,0,41,54877,1101,83777,0,66,1101,0,1,67,1101,934,0,68,1101,556,0,69,1101,0,0,71,1101,0,936,72,1105,1,73,1,1967,1101,12071,0,66,1101,0,2,67,1102,963,1,68,1102,1,302,69,1102,1,1,71,1102,967,1,72,1105,1,73,0,0,0,0,7,19259,1101,0,23687,66,1101,1,0,67,1102,996,1,68,1101,556,0,69,1101,9,0,71,1102,998,1,72,1105,1,73,1,1,48,26783,27,181994,28,21722,40,83561,19,157161,18,118318,6,52653,23,40763,36,168807,1102,1,40763,66,1102,5,1,67,1101,0,1043,68,1102,302,1,69,1101,1,0,71,1101,0,1053,72,1106,0,73,0,0,0,0,0,0,0,0,0,0,34,143986,1102,1,1063,66,1101,0,3,67,1102,1,1082,68,1101,302,0,69,1101,1,0,71,1102,1088,1,72,1105,1,73,0,0,0,0,0,0,7,57777,1102,1,29789,66,1101,0,1,67,1101,0,1117,68,1101,556,0,69,1102,1,1,71,1102,1119,1,72,1105,1,73,1,463,23,203815,1102,10861,1,66,1101,2,0,67,1102,1,1148,68,1101,302,0,69,1101,0,1,71,1102,1152,1,72,1106,0,73,0,0,0,0,40,167122,1101,0,2689,66,1101,0,1,67,1101,1181,0,68,1101,0,556,69,1102,1,1,71,1101,0,1183,72,1105,1,73,1,47,45,47134,1102,59159,1,66,1101,3,0,67,1101,1212,0,68,1101,0,302,69,1102,1,1,71,1101,1218,0,72,1106,0,73,0,0,0,0,0,0,34,71993,1102,1,26783,66,1102,1,2,67,1101,1247,0,68,1102,302,1,69,1101,0,1,71,1101,0,1251,72,1106,0,73,0,0,0,0,27,90997,1101,0,91369,66,1101,1,0,67,1102,1,1280,68,1101,0,556,69,1102,1,1,71,1102,1282,1,72,1105,1,73,1,1346,6,35102,1102,90997,1,66,1102,2,1,67,1101,1311,0,68,1101,0,302,69,1101,0,1,71,1102,1315,1,72,1106,0,73,0,0,0,0,28,10861,1102,20479,1,66,1102,1,1,67,1102,1,1344,68,1101,556,0,69,1102,1,1,71,1102,1346,1,72,1105,1,73,1,113,23,163052,1102,1,40361,66,1102,1,1,67,1101,1375,0,68,1102,1,556,69,1102,1,1,71,1102,1,1377,72,1105,1,73,1,17,45,23567,1102,54877,1,66,1101,2,0,67,1102,1406,1,68,1101,0,351,69,1102,1,1,71,1101,1410,0,72,1105,1,73,0,0,0,0,255,42859,1102,1,52387,66,1102,1,3,67,1101,1439,0,68,1102,302,1,69,1102,1,1,71,1101,0,1445,72,1105,1,73,0,0,0,0,0,0,34,359965,1102,1,58379,66,1101,0,3,67,1101,0,1474,68,1102,302,1,69,1102,1,1,71,1102,1,1480,72,1105,1,73,0,0,0,0,0,0,25,24142,1102,56269,1,66,1101,4,0,67,1101,0,1509,68,1102,1,302,69,1101,0,1,71,1101,1517,0,72,1105,1,73,0,0,0,0,0,0,0,0,34,215979,1102,99469,1,66,1101,0,1,67,1101,0,1546,68,1101,0,556,69,1102,1,1,71,1102,1548,1,72,1106,0,73,1,147,45,117835,1102,94583,1,66,1101,0,1,67,1102,1577,1,68,1102,556,1,69,1102,1,1,71,1102,1,1579,72,1106,0,73,1,-42589,48,53566,1101,0,33457,66,1102,4,1,67,1102,1,1608,68,1102,1,302,69,1101,1,0,71,1101,0,1616,72,1105,1,73,0,0,0,0,0,0,0,0,38,71938,1101,0,22171,66,1101,1,0,67,1102,1,1645,68,1101,556,0,69,1101,1,0,71,1101,0,1647,72,1105,1,73,1,1483,18,177477,1101,0,17551,66,1101,4,0,67,1102,1676,1,68,1101,0,302,69,1102,1,1,71,1102,1,1684,72,1105,1,73,0,0,0,0,0,0,0,0,34,287972,1102,499,1,66,1101,1,0,67,1101,1713,0,68,1101,0,556,69,1101,0,1,71,1102,1,1715,72,1106,0,73,1,-281,18,59159,1102,44159,1,66,1102,1,3,67,1101,1744,0,68,1101,0,302,69,1101,0,1,71,1102,1750,1,72,1105,1,73,0,0,0,0,0,0,47,79358,1102,1,37781,66,1101,1,0,67,1102,1,1779,68,1102,556,1,69,1101,1,0,71,1101,0,1781,72,1105,1,73,1,67,36,225076,1101,0,66683,66,1102,1,1,67,1101,0,1810,68,1101,0,556,69,1101,3,0,71,1102,1812,1,72,1106,0,73,1,3,45,94268,6,70204,23,81526,1101,39461,0,66,1102,1,1,67,1102,1845,1,68,1101,0,556,69,1101,2,0,71,1101,1847,0,72,1106,0,73,1,10,29,100371,38,143876,1101,88289,0,66,1101,0,1,67,1102,1,1878,68,1102,1,556,69,1102,1,3,71,1102,1880,1,72,1106,0,73,1,7,45,70701,20,58379,49,132477,1101,0,23567,66,1101,6,0,67,1101,1913,0,68,1101,0,302,69,1102,1,1,71,1101,1925,0,72,1106,0,73,0,0,0,0,0,0,0,0,0,0,0,0,7,77036,1101,0,1471,66,1101,0,1,67,1101,0,1954,68,1102,1,556,69,1101,0,1,71,1102,1,1956,72,1105,1,73,1,101,36,56269,1101,0,35969,66,1101,6,0,67,1102,1985,1,68,1101,302,0,69,1101,1,0,71,1101,1997,0,72,1106,0,73,0,0,0,0,0,0,0,0,0,0,0,0,41,109754,1101,0,17299,66,1101,0,1,67,1102,1,2026,68,1102,1,556,69,1101,1,0,71,1102,1,2028,72,1106,0,73,1,-360,19,104774,1102,28351,1,66,1101,0,1,67,1102,1,2057,68,1101,0,556,69,1101,1,0,71,1101,2059,0,72,1106,0,73,1,1086,36,112538,1102,42859,1,66,1101,0,1,67,1101,2088,0,68,1102,556,1,69,1101,6,0,71,1102,1,2090,72,1105,1,73,1,25110,25,12071,47,39679,47,119037,30,1063,30,2126,30,3189,1102,1,84481,66,1101,0,1,67,1102,2129,1,68,1102,556,1,69,1101,0,0,71,1101,2131,0,72,1105,1,73,1,1635,1102,92357,1,66,1101,1,0,67,1101,2158,0,68,1102,1,556,69,1102,1,1,71,1102,2160,1,72,1106,0,73,1,49,49,44159,1101,0,39367,66,1101,1,0,67,1101,0,2189,68,1102,1,556,69,1102,1,1,71,1101,2191,0,72,1105,1,73,1,5821,19,52387,1101,0,13381,66,1101,1,0,67,1101,2220,0,68,1101,556,0,69,1102,1,1,71,1101,0,2222,72,1106,0,73,1,31,20,175137,1101,90971,0,66,1101,1,0,67,1101,0,2251,68,1101,0,556,69,1102,1,1,71,1101,2253,0,72,1105,1,73,1,125,29,133828]
puzzle_input.extend([0]*5000)

N_NIC = 50

# Inefficiently use a list of lists to store packets to each destination
packets_table = [[]]*N_NIC
exit_condition = False
Nic = [None]*N_NIC

for i in range(N_NIC):
    Nic[i] = intcode.IntCode(program = deepcopy(puzzle_input), instance=i)
    Nic[i].push_input(i)
solution = -1
while not exit_condition:

    for i in range(N_NIC):
        # Run until output is available and pass it to the next Niclifier. 
        # Until they are done. Use a round robin approah
        rr = 0
        RR_SLICE = 50
        while(len(Nic[i]._out_list)<3 and not Nic[i].done and rr < RR_SLICE):
            Nic[i].step()
            rr +=1
        if (len(Nic[i]._out_list)==3):
            ip = Nic[i].pop_output()
            x = Nic[i].pop_output()
            y = Nic[i].pop_output()
            if ip==255:
                exit_condition = True
                solution = y
            else:
                packets_table[ip].append([x,y]) # Store for future use
                packets_table 
                Nic[ip].push_input([x,y])
            continue

print(f"Solution part 1: {solution}")

####
# Part 2
N_NIC = 50

packets_table = []
exit_condition = False
Nic = [None]*N_NIC
NAT_messages_to_0 = []
NAT = [None, None]
last_NAT_msg = [None, None]

for i in range(N_NIC):
    Nic[i] = intcode.IntCode(program = deepcopy(puzzle_input), instance=i)
    Nic[i].push_input(i)
solution = -1
idle_counter = 0
while not exit_condition:
    
    network_idle = True
    
    for i in range(N_NIC):
        # Run until output is available and pass it to the next Nic. 
        # Until they are done. Use a round robin approach
        rr = 0
        RR_SLICE = 400
        Nic[i].idle = False
        while(len(Nic[i]._out_list)<3 and not Nic[i].done and rr < RR_SLICE and not Nic[i].idle):
            Nic[i].step()
            rr +=1
        network_idle = network_idle and (len(Nic[i]._out_list)==0)
        if (len(Nic[i]._out_list)==3):
            ip = Nic[i].pop_output()
            x = Nic[i].pop_output()
            y = Nic[i].pop_output()
            if ip==255:
                NAT = [x,y]
            else:
                packets_table.append([ip,x,y]) # Store for future inspection
                Nic[ip].push_input(deepcopy([x,y]))
        network_idle = network_idle and (len(Nic[i]._in_list)==0)

    if network_idle and not NAT==[None, None]:
        Nic[0].push_input(NAT)
        print(NAT)
        NAT_messages_to_0.append(NAT)
        if last_NAT_msg[1]==NAT[1]:
            if len(NAT_messages_to_0) > 100:
                exit_condition = True
        last_NAT_msg = NAT

print(NAT_messages_to_0)
print(f"Solution part 2: {last_NAT_msg[1]}") # For some reason, Y is actually 17494 but if I keep running it the solution is 17493...
