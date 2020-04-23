"""CPU functionality."""

import sys

LDI = 130
PRN = 71
HLT = 1
MUL = 162
ADD = 160
PUSH = 69
POP = 70
CALL = 80
RET = 17
program_filename = sys.argv[1]

SP = 7


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.reg[SP] = 255

    def ram_read(self, MAR):
        value = self.ram[MAR]
        return value

    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR

    def load(self):
        """Load a program into memory."""
        address = 0
        with open(program_filename) as f:
            for line in f:
                line = line.split('#')
                line = line[0].strip()
                if line == '':
                    pass
                else:
                    self.ram[address] = int(line, 2)
                    address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

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
        """Run the CPU."""
        self.load()
        running = True
        while running:
            IR = self.ram[self.pc]
            if IR == LDI:
                operand_a = self.ram_read(self.pc+1)
                operand_b = self.ram_read(self.pc+2)
                self.reg[operand_a] = operand_b
                self.pc += 3
            elif IR == PRN:
                operand_a = self.ram_read(self.pc+1)
                print(self.reg[operand_a])
                self.pc += 2
            elif IR == MUL:
                self.reg[operand_a - 1] = self.reg[operand_a - 1] * \
                    self.reg[operand_a]
                self.pc += 3

            elif IR == ADD:
                operand_a = self.ram_read(self.pc+1)
                operand_b = self.ram_read(self.pc + 2)
                self.reg[operand_a] = self.reg[operand_a] + self.reg[operand_b]
                self.pc += 3
            elif IR == PUSH:
                self.reg[SP] -= 1
                operand_a = self.ram_read(self.pc+1)
                value = self.reg[operand_a]
                # self.ram[self.reg[SP]] = value
                self.ram_write(self.reg[SP], value)
                self.pc += 2
            elif IR == POP:
                value = self.ram_read(self.reg[SP])
                operand_a = self.ram_read(self.pc+1)
                self.reg[operand_a] = value
                self.reg[SP] += 1
                self.pc += 2

            elif IR == CALL:
                return_addr = self.pc + 2
                self.reg[SP] -= 1
                self.ram[self.reg[SP]] = return_addr
                operand_a = self.ram_read(self.pc + 1)
                dest_addr = self.reg[operand_a]
                self.pc = dest_addr

            elif IR == RET:
                return_addr = self.ram_read(self.reg[SP])
                self.reg[SP] += 1
                self.pc = return_addr

            elif IR == HLT:
                running = False
            else:
                print("Unknown instruction")
                running = False


ddd = CPU()
ddd.run()
