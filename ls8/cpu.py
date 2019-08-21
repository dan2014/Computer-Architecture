"""CPU functionality."""

import sys
import time
import re

class CPU:
    """Main CPU class."""

    def __init__(self,sleep=0):
        """Construct a new CPU."""
        self.sleep = sleep
        self.ram = [0] * 256
        self.pc = 0b00000000
        self.reg = [0b00000000,0b00000000,0b00000000,0b00000000,0b00000000,0b00000000,0b00000000,0b00000000]
        self.ir = 0b00000000
        self.branchtable = {}
        self.branchtable["ALU"] = self.handle_ALU
        self.branchtable["PC"] = self.handle_PC
        self.branchtable["OTHER"] = self.handle_OTHER

    def handle_ALU(self,operand,ins):
        alu_ops = {0b0000:"ADD",0b0001:"SUB",0b0010:"MUL",0b0011:"DIV",0b0100:"MOD",0b0101:"INC",0b0110:"DEC",0b0111:"CMP",0b1000:"AND",0b1001:"NOT",0b1010:"OR",0b1011:"XOR",0b1100:"SHL",0b1101:"SHR"}

    
    def handle_PC(self,operand,ins):
        pc_ops = {0b0000:"CALL",0b0001:"RET",0b0010:"INT",0b0011:"IRET",0b0100:"JMP",0b0101:"JEQ",0b0110:"JNE",0b0111:"JGT",0b1000:"JLT",0b1001:"JLE",0b1010:"JGE"}


    def handle_OTHER(self,operand,ins):
        other_ops = {0b0000:"NOP",0b0001:"HLT",0b0010:"LDI",0b0011:"LD",0b0100:"ST",0b0101:"PUSH",0b0110:"POP",0b0111:"PRN",0b1000:"PRA"}


    def ram_read(self,address):
        return self.ram[address]

    def ram_write(self):
        pass


    def load(self,args):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]
        if len(args) != 2:
            print("usage: file.py <filename>", file=sys.stderr)
            sys.exit(1)

        filepath = args[1]
        program = []
        try:
            with open(filepath) as f:
                for line in f:
                    m = re.compile("[0-1]{8}",)
                    match = m.search(line)
                    if match is not None:
                        program.append(match.group())
                    
        except FileNotFoundError:
            print(f"{args[0]}: {args[1]} not found")
            sys.exit(2)


        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

        # SET FL Register

    def cu(self):
        """Control Unit operations."""
        alu_bitmask = 0b00100000
        pc_bitmask = 0b00010000
        operand_bitmask = 0b11000000
        instruction_bitmask = 0b00001111
        instruction = 0

        operand_num = 0
        
        address = self.pc

        # Fetch
            # Copy Instruction from RAM into PC
            # Increment PC 
        opt_code = self.ram_read(address)
        self.ir = opt_code

         # Decode
            # Decode the contents of the IR register

        operand_num += opt_code & operand_bitmask
        instruction += opt_code & instruction_bitmask

        if alu_bitmask & opt_code:
        # Execute
            self.branchtable["ALU"](operand_num,instruction)
            self.pc += 1
        elif pc_bitmask & opt_code:
        # Execute
            self.branchtable["PC"](operand_num,instruction)
        else:
        # Execute
            self.branchtable["OTHER"](operand_num,instruction)
            self.pc += 1
        
    # def trace(self):
    #     """
    #     Handy function to print out the CPU state. You might want to call this
    #     from run() if you need help debugging.
    #     """

    #     print(f"TRACE: %02X | %02X %02X %02X |" % (
    #         self.pc,
    #         #self.fl,
    #         #self.ie,
    #         self.ram_read(self.pc),
    #         self.ram_read(self.pc + 1),
    #         self.ram_read(self.pc + 2)
    #     ), end='')

    #     for i in range(8):
    #         print(" %02X" % self.reg[i], end='')

    #     print()

    def run(self):
        """Run the CPU."""
        while self.ir != 0b00000001:
            if self.sleep != 0:
                time.sleep(self.sleep)

            self.cu()
