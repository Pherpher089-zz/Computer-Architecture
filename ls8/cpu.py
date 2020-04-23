"""CPU functionality."""

import sys

HLT = 1
LDI = 130
PRN = 71
MUL = 162

debugging = False


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.running = False

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

        #program = [0b00000001]
        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
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

    def run(self):
        self.running = True
        while self.running == True:
            command = self.ram[self.pc]
            if debugging:
                print(f'Command at address {self.pc} is {command}')
            if command == HLT:
                if debugging:
                    print('halting')
                self.running = False
            elif command == LDI:
                if debugging:
                    print('LDI')
                    print(
                        f'Loading {self.ram[self.pc + 2]} into register {self.ram[self.pc + 1]}')
                self.reg[self.ram[self.pc + 1]] = self.ram[self.pc + 2]
                self.pc += 3
            elif command == PRN:
                print(self.reg[self.ram[self.pc + 1]])
                self.pc += 2
            elif command == MUL:
                if debugging:
                    print(
                        f'Multiplying {self.reg[self.ram[self.pc + 1]]} by {self.reg[self.ram[self.pc + 2]]}')
                self.reg[self.ram[self.pc + 1]] = self.reg[self.ram[self.pc + 1]
                                                           ] * self.reg[self.ram[self.pc + 2]]
                self.pc += 3
            else:
                print("Error!")
