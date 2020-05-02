"""CPU functionality."""

import sys

HLT = 1
LDI = 130
PRN = 71
MUL = 162
ADD = 160
CMP = 167
JEQ = 85
JNE = 86
POP = 70
PUSH = 69
CALL = 80
RET = 17
JMP = 84

debugging = False


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.ir = 0
        self.mar = 0
        self.mdr = 0
        self.fl = 0b00000000
        self.running = False
        self.branchtable = {}
        self.branchtable[HLT] = self.hlt
        self.branchtable[LDI] = self.ldi
        self.branchtable[PRN] = self.prn
        self.branchtable[MUL] = self.mul
        self.branchtable[ADD] = self.add
        self.branchtable[CMP] = self.cmp
        self.branchtable[JEQ] = self.jeq
        self.branchtable[JNE] = self.jne
        self.branchtable[POP] = self.pop
        self.branchtable[PUSH] = self.push
        self.branchtable[CALL] = self.call
        self.branchtable[RET] = self.ret
        self.branchtable[JMP] = self.jmp

    def load(self, file):
        """Load a program into memory."""
        address = 0
        program = []

        f = open(file, 'r')

        for instruction in f:
            byte_string = '0b'
            for i in instruction:
                if i != "1" and i != "0":
                    break
                byte_string += i
            if byte_string != '0b':
                x = int(byte_string, 2)
                program.append(x)
        f.close()

        # program = [0b00000001]
        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "DIV":
            self.reg[reg_a] /= self.reg[reg_b]
        elif op == 'CMP':
            #print(f'Comparing {self.reg[reg_a]} to {self.reg[reg_b]}')
            if self.reg[reg_a] < self.reg[reg_b]:
                self.fl = 0b100
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.fl = 0b10
            else:
                self.fl = 0b1
            # print(bin(self.fl))
        else:
            raise Exception("Unsupported ALU operation")

    def ram_read(self, pc):
        return self.ram[pc]

    def ram_write(self, data, address):
        self.ram[address] = data

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """
        print('trace')

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def ldi(self):

        self.reg[self.ram[self.pc + 1]] = self.ram[self.pc + 2]
        self.pc += 3

    def prn(self):
        print(self.reg[self.ram[self.pc + 1]])
        self.pc += 2

    def mul(self):
        self.alu('MUL', self.ram[self.pc+1], self.ram[self.pc + 2])
        self.pc += 3

    def add(self):
        self.alu('ADD', self.ram[self.pc+1], self.ram[self.pc + 2])
        self.pc += 3

    def cmp(self):
        self.alu('CMP', self.ram[self.pc + 1], self.ram[self.pc+2])
        self.pc += 3

    def pop(self):
        self.reg[self.ram[self.pc+1]] = self.ram[self.reg[7]]
        self.reg[7] += 1
        self.pc += 2

    def push(self):
        self.reg[7] -= 1
        self.ram[self.reg[7]] = self.reg[self.ram[self.pc + 1]]
        self.pc += 2

    def call(self):
        self.reg[7] += 1
        self.ram[self.reg[7]] = self.pc + 2
        self.pc = self.reg[self.ram[self.pc+1]]

    def ret(self):
        self.pc = self.ram[self.reg[7]]
        self.ram[7] += 1

    def jmp(self):
        self.pc = self.reg[self.ram[self.pc + 1]]

    def jeq(self):

        if self.fl == 0b1:
            self.pc = self.reg[self.ram[self.pc + 1]]
        else:
            self.pc += 2

    def jne(self):

        if self.fl != 0b1:
            self.pc = self.reg[self.ram[self.pc + 1]]
        else:
            self.pc += 2

    def hlt(self):
        self.running = False

    def run(self):
        # Handle power on state
        for i in range(8):
            if i < 7:
                self.reg[i] = 0
            else:
                self.reg[i] = 0XF4
        # start the program loop
        self.running = True

        while self.running == True:
            # set the intruction register to the current instruction
            self.ir = self.ram[self.pc]
            #print(f'current instruction: {self.ir} at {self.pc}')
            # Not really seeing how this will come in handy just yet but ive got the AA bits isolated for future use
            bin_op = self.ir >> 6

            if self.ir in self.branchtable:
                self.branchtable[self.ir]()
            else:
                print("Error!")
                print(self.ram[self.pc])
                print(self.reg[0])
                print(self.reg[1])
                print(bin(self.fl))
                self.running = False
