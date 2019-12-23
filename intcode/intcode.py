from collections import namedtuple
from enum import Enum
from dataclasses import dataclass
from copy import deepcopy

OpParams = namedtuple('OpParams', 'inparam outparam func')

class Mode(Enum):
    POSITION = 0
    IMMEDIATE = 1
    RELATIVE = 2

@dataclass
class Parameter:
    value: int
    mode: Mode
    real_value: int = 0 # Initialise to 0, it will be assigned at runtime

class IntCode(object):
    
    def op_sum(self, a, b, out_addr):
        self._mem[out_addr] = a+b
        return a+b

    def op_mul(self,a,b,out_addr):
        self._mem[out_addr] = a*b
        return a+b
    
    def op_input(self,addr):
        self._mem[addr] = self._in_list.pop(0)
        return self._mem[addr]

    def op_output(self,val):
        self._out_list.append(val)
        return val

    def op_jumpiftrue(self,condition,addr):
        if condition:
            self._pc = addr
        return condition, addr

    def op_jumpiffalse(self,condition,addr):
        if not condition:
            self._pc = addr
        return condition, addr

    def op_lessthan(self,a,b,out_addr):
        self._mem[out_addr] = int(a<b)
        return a,b,out_addr
    
    def op_equals(self,a,b,out_addr):
        self._mem[out_addr] = int(a==b)
        return a,b,out_addr

    def op_addtorelbaseoffs(self, offset):
        self._pc_offset += offset
        return self._pc_offset
    
    def op_terminate(self):
        self.done = True

    _in_list = []
    _out_list = []
    _mem = []
    _pc = 0          # Program counter
    _id = 0
    _pc_offset = 0
    done = False
    operations = {} # Holds Params in/out
    operations['01'] =  OpParams( 2, 1, op_sum )
    operations['02'] =  OpParams( 2, 1, op_mul )
    operations['03'] =  OpParams( 0, 1, op_input )
    operations['04'] =  OpParams( 1, 0, op_output )
    operations['05'] =  OpParams( 2, 0, op_jumpiftrue )
    operations['06'] =  OpParams( 2, 0, op_jumpiffalse )
    operations['07'] =  OpParams( 2, 1, op_lessthan )
    operations['08'] =  OpParams( 2, 1, op_equals )
    operations['09'] =  OpParams( 1, 0, op_addtorelbaseoffs )
    operations['99'] = OpParams( 0, 0, op_terminate )

    def __init__(self, program, instance=0):
        assert(isinstance(program, list))
        self._mem = program
        self._pc = 0
        _pc_offset = 0
        self._id = instance

    def push_input(self, v):
        assert(isinstance(v, int) or isinstance(v, list))
        if isinstance(v, int):
            self._in_list.append(v)
        if isinstance(v, list):
            self._in_list.extend(v)

    def pop_output(self):
        if len(self._out_list) > 0:
            return self._out_list.pop(0)
        else:
            return None

    def run(self):
        while self._pc < len(self._mem) and not self.done:
            self.step()

    def step(self):
        op_word = str(self._mem[self._pc]).rjust(5,'0')
        #print(f"{op_word=}")
        self._pc += 1
        opcode = op_word[-2::]  # Last two characters are the opcode
        
        # # Check if we reached the end of the program
        # if opcode=='99':
        #     self.done
        #     return

        # Check if operation exists
        assert opcode in self.operations, f"{opcode=}"

        # Parameters with their mode
        par_in = []
        par_out = []
        modes = list(op_word[0:3])

        # Parse input parameters
        for _ in range(self.operations[opcode].inparam):
            par_in.append(Parameter(value = self._mem[self._pc],
                                    mode = Mode(int(modes.pop(-1)))))
            self._pc += 1

        # Parse output parameters
        for _ in range(self.operations[opcode].outparam):
            par_out.append(Parameter(value = self._mem[self._pc],
                                    mode = Mode(int(modes.pop(-1)))))
            self._pc += 1
        
        # Parse get values of parameters depending on their mode
        for i in range(len(par_in)):
            if par_in[i].mode == Mode.POSITION:
                par_in[i].real_value = self._mem[par_in[i].value]
            if par_in[i].mode == Mode.IMMEDIATE:
                par_in[i].real_value = par_in[i].value
            if par_in[i].mode == Mode.RELATIVE:
                par_in[i].real_value = self._mem[par_in[i].value + self._pc_offset]

        # Parse get values of parameters depending on their mode
        for i in range(len(par_out)):
            if par_out[i].mode == Mode.POSITION:
                par_out[i].real_value = par_out[i].value
            if par_out[i].mode == Mode.IMMEDIATE:
                assert(0)
            if par_out[i].mode == Mode.RELATIVE:
                par_out[i].real_value = par_out[i].value + self._pc_offset
        
        pars = [p.real_value for p in par_in]
        pars.extend([p.real_value for p in par_out])

        # Execute operations
        #print(f"Executing {self.operations[opcode].func} with {pars}")
        r = self.operations[opcode].func(self, *pars)
        
        if r is not None: # Value must be assigned
            pass



        




                                    





    


