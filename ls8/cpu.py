"""CPU functionality."""

import sys

HLT = 1
LDI = 10000010 
PRN = 1000111
PUSH = 1000101 
POP = 1000110 
MUL = 10100010
ADD = 10100000

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256 
        self.reg = [0] * 8
        self.reg[7] = 244
        self.pc = 0
        self.fl = 0  

    def ram_read(self, MAR):
    # should accept the address to read and return the value stored there.
        if MAR < len(self.ram):
            return self.ram[MAR]
        else:
            return None

    def ram_write(self, MAR, MDR): 
    # should accept a value to write, and the address to write it to. 
        self.ram[MAR] = MDR


    def load(self, program = None):
        """Load a program into memory."""

        if len(sys.argv) < 2:
            print("Please pass in a second filename: python3 in_and_out.py second_filename.py")
            sys.exit()

        try:
            address = 0
            with open(program) as file:
                for line in file:
                    split_line = line.split('#')[0]
                    command = split_line.strip()

                    if command == '':
                        continue

                    instruction = int(command)
                    self.ram[address] = instruction

                    address += 1

        except FileNotFoundError:
            print(f'{sys.argv[0]}: {sys.argv[1]} file was not found')
            sys.exit()

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
            self.pc += 2
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
            self.pc += 2
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def get_index(self, binary): 
        binary_str = str(binary)
        binary_str.replace("0b", '')
        return int(binary_str, 2) 

    def ldi(self, reg_num, value):
        self.reg[reg_num] = value
        self.pc += 2

    def prn(self, reg_num):
        print(self.reg[reg_num])
        self.pc +=1

    def push(self, reg_num):
        # decrement the stack pointer
        self.reg[7] -= 1

        # get a value from the given register
        value = self.reg[reg_num]

        # put the value at the stack pointer address
        sp = self.reg[7]
        self.ram[sp] = value
        self.pc +=1

    def pop(self, operand_a):
        # get the stack pointer 
        sp = self.reg[7]

        # use stack pointer to get the value
        value = self.ram[sp]
        # put the value into the given register
        self.reg[operand_a] = value
        # increment our stack pointer
        self.reg[7] += 1
        self.pc +=1

    def run(self):
        """Run the CPU."""
        ir = self.ram_read(self.pc)

        while ir != HLT:
            ir = self.ram_read(self.pc)
            str_ir = str(ir)
            operand_a = self.get_index(self.ram_read(self.pc+1))
            operand_b = self.get_index(self.ram_read(self.pc+2))

            if ir == MUL:
                op = "MUL"
                self.alu(op, operand_a, operand_b)
            elif ir == ADD:
                op = "ADD"
                self.alu(op, operand_a, operand_b)
            elif ir == LDI:
                self.ldi(operand_a, operand_b)
            elif ir == PRN:
                self.prn(operand_a)
            elif ir == PUSH:
                self.push(operand_a)
            elif ir == POP:
                self.pop(operand_a)

            self.pc += 1 
