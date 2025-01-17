"""CPU functionality."""

import sys

ADD = 0b10100000    # Add the value in two registers and store the result in registerA.
AND = 0b10101000    # Bitwise-AND the values in registerA and registerB, then store the result in registerA.
CALL = 0b01010000   # Calls a subroutine (function) at the address stored in the register.
CMP = 0b10100111    # Compare the values in two registers. LGE for three last positions
DEC = 0b01100110    # Decrement (subtract 1 from) the value in the given register.
DIV = 0b10100011    # Divide the value in the first register by the value in the second, storing the result in registerA.
HLT = 0b00000001    # Halt the CPU (and exit the emulator).
INC = 0b01100101    # Increment (add 1 to) the value in the given register.
INT = 0b01010010    # Issue the interrupt number stored in the given register.
IRET = 0b00010011   # Return from an interrupt handler.
JEQ = 0b01010101    # If equal flag is set (true), jump to the address stored in the given register.
JGE = 0b01011010    # If greater-than flag or equal flag is set (true), jump to the address stored in the given register.
JGT = 0b01010111    # If greater-than flag is set (true), jump to the address stored in the given register.
JLE = 0b01011001    # If less-than flag or equal flag is set (true), jump to the address stored in the given register.
JLT = 0b01011000    # If less-than flag is set (true), jump to the address stored in the given register.
JMP = 0b01010100    # Jump to the address stored in the given register.
JNE = 0b01010110    # If E flag is clear (false, 0), jump to the address stored in the given register.
LD =  0b10000011    # Loads registerA with the value at the memory address stored in registerB.
LDI = 0b10000010    # Set the value of a register to an integer.
MOD = 0b10100100   # Divide the value in the first register by the value in the second, storing the remainder of the result in registerA.
MUL = 0b10100010    # Multiply the values in two registers together and store the result in registerA.
NOP = 0b00000000    # No operation. Do nothing for this instruction.
NOT = 0b01101001    # Perform a bitwise-NOT on the value in a register.
OR = 0b10101010     # Perform a bitwise-OR between the values in registerA and registerB, storing the result in registerA.
POP = 0b01000110    # Pop the value at the top of the stack into the given register.
PRA = 0b01001000    # Print alpha character value stored in the given register.
PRN = 0b01000111    # Print numeric value stored in the given register.
PUSH = 0b01000101   # Push the value in the given register on the stack.
RET = 0b00010001    # Pop the value from the top of the stack and store it in the PC.
SHL = 0b10101100    # Shift the value in registerA left by the number of bits specified in registerB, filling the low bits with 0.
SHR = 0b10101101    # Shift the value in registerA right by the number of bits specified in registerB, filling the high bits with 0.
ST = 0b10000100     # Store value in registerB in the address stored in registerA.
SUB = 0b10100001    # Subtract the value in the second register from the first, storing the result in registerA.
XOR = 0b10101011    # Perform a bitwise-XOR between the values in registerA and registerB, storing the result in registerA.


# create functions for each activity




class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.sp = 7
        self.flag = 0b000
        self.reg[self.sp]= 0xF4
        self.HALTED = False
        self.sub_routine = False
        self.branchTable = {
            HLT: self.halt_op,
            LDI: self.ldi_op,
            PRN: self.prn_op,
            ADD: self.add_op,
            MUL: self.mul_op,
            PUSH: self.push_op,
            POP: self.pop_op,
            CMP: self.cmp_op,
            JEQ: self.jeq_op,
            JNE: self.jne_op,
            JMP: self.jmp_op,
            CALL: self.call_op,
            RET: self.ret_op,
            AND: self.and_op,
            OR: self.or_op,
            XOR: self.xor_op,
            NOT: self.not_op,
            SHL: self.shl_op,
            SHR: self.shr_op,
            MOD: self.mod_op,
            INT: self.int_op,
            IRET: self.iret_op,
            }

    

    
    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        address = 0

        if len(sys.argv) != 2:
            print("usage: ls8.py <filename>")
            sys.exit(1)

        try:
            with open(sys.argv[1]) as instructions:
                # read each instruction line
                for line in instructions:
                    # split each line into instructions and comments
                    split_instruction_line = line.split("#")
                    
                    # remove whitespace
                    one_and_zeroes = split_instruction_line[0].strip()

                    # ignore blank lines / comment only lines
                    if len(one_and_zeroes) == 0:
                        continue

                    # set the number to an integer of base 2
                    instruction = int(one_and_zeroes, 2)
                    self.ram[address] = instruction
                    address += 1

        except FileNotFoundError:
            print(f"{sys.argv[0]}: {sys.argv[1]} not found")
            sys.exit(2)



    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
            # for add operation
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
            # for mulitplication operation
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "AND":
            result = self.reg[reg_a] & self.reg[reg_b]
            self.reg[reg_a] = result
        elif op == "OR":
            result = self.reg[reg_a] | self.reg[reg_b]
            self.reg[reg_a] = result
        elif op == "XOR":
            result = self.reg[reg_a] ^ self.reg[reg_b]
            self.reg[reg_a] = result
        elif op == "SHL":
            result = self.reg[reg_a] << self.reg[reg_b]
            self.reg[reg_a] = result
        elif op == "SHR":
            result = self.reg[reg_a] >> self.reg[reg_b]
            self.reg[reg_a] = result
        elif op == "NOT":
            # Perform a bitwise-NOT on the value in a register
            result = ~self.reg[reg_a]
            self.reg[reg_a] = result
        elif op == "MOD":
            if self.reg[reg_b] == 0:
                raise Exception(f'Can not perform operation at {self.IR:08b}')
                self.handle_HLT(None)
            else:
                result = self.reg[reg_a] % self.reg[reg_b]
                self.reg[reg_a] = result 
        #elif op == "SUB": etc
        elif op == 'CMP':
            if self.reg[reg_a] == self.reg[reg_b]:
                self.flag = 0b001
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.flag = 0b010
            elif self.reg[reg_a] < self.reg[reg_b]:
                self.flag = 0b100
            else:
                self.flag = 0b000

        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()
    def ram_read(self , MAR):
        return self.ram[MAR]

    def raw_write(self , MAR , MDR):
        self.reg[MAR] = MDR
        

    def run(self):
        """Run the CPU."""
 
        while not self.HALTED:
            IR = self.ram[self.pc]
            operands = IR  >> 6  & 0b11
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
        
            if IR in self.branchTable:
                self.branchTable[IR](operand_a , operand_b)
            else:
                raise Exception(f"Invalid instruction {IR:08b} at address {hex(self.pc)}")
            if not self.sub_routine:
                self.pc += operands + 1

            # mask the remaining aspect of the code and then right shift
            # so it basically becomes the first value in IR * 2^1 + second value in IR*2^0
           
            # if IR == HLT:
            #     self.HALTED = True
            # elif IR == LDI:
            #     self.reg[operand_a] = operand_b
            # elif IR == PRN:
            #     print(self.reg[operand_a])
            # elif IR == MUL:
            #     self.alu("MUL", operand_a, operand_b)
            # elif IR == PUSH:
            #     self.reg[self.sp] -= 1
            #     value = self.reg[operand_a]
            #     address = self.reg[self.sp]
            #     self.raw_write(address, value)
            # elif IR == POP:
            #     self.reg[operand_a] = self.ram_read(self.reg[self.sp])
            #     self.reg[self.sp] += 1
            # else:
            #     print(f"Unknown Instruction {IR:08b}")
            #     sys.exit(1)
          
    def halt_op(self, operand_a , operand_b):
        self.HALTED = True

    def pop_op(self, operand_a , operand_b):
        self.reg[operand_a] = self.ram_read(self.reg[self.sp])
        self.reg[self.sp] += 1

    def push_op(self, operand_a , operand_b):
        self.reg[self.sp] -= 1
        value = self.reg[operand_a]
        address = self.reg[self.sp]
        self.raw_write(address, value)
        self.sub_routine = False

    def prn_op(self, operand_a , operand_b):
        print(self.reg[operand_a])
        self.sub_routine = False

    def ldi_op(self, operand_a , operand_b):
        self.reg[operand_a] = operand_b
        self.sub_routine = False

    def add_op(self, operand_a , operand_b):
        self.alu("ADD", operand_a, operand_b)
        self.sub_routine = False

    def mul_op(self, operand_a , operand_b):
        self.alu("MUL", operand_a, operand_b)
        self.sub_routine = False

    def call_op(self, operand_a , operand_b):
        self.reg[self.sp] -= 1
        self.raw_write(self.reg[self.sp] , self.pc + 2)
        self.pc = self.reg[operand_a]
        self.sub_routine = True

    def ret_op(self, operand_a , operand_b):
        self.pc = self.ram_read(self.reg[self.sp])
        self.reg[self.sp] += 1
        self.sub_routine = True
        
    def jmp_op(self, operand_a , operand_b):
        self.pc = self.reg[operand_a]
        self.sub_routine = True
        
    def cmp_op(self, operand_a , operand_b):
        self.alu('CMP', operand_a, operand_b)
        self.sub_routine = False
        
    def jeq_op(self, operand_a , operand_b):
        if self.flag == 0b001:
            self.pc = self.reg[operand_a]
            self.sub_routine = True
        else:
            self.sub_routine = False
    def jne_op(self, operand_a , operand_b):
        if self.flag == 0b100 or self.flag == 0b010 :
            self.pc = self.reg[operand_a]
            self.sub_routine = True
        else:
            self.sub_routine = False
    #stretch
    def st(self):
        pass
    def and_op(self, operand_a , operand_b):
        self.alu('AND', operand_a , operand_b)
        self.sub_routine = False
    def or_op(self):
        self.alu('OR', operand_a , operand_b)
        self.sub_routine = False
    def xor_op(self):
        pass
    def not_op(self):
        pass
    def shl_op(self):
        pass
    def shr_op(self):
        pass
    def mod_op(self):
        pass
    def int_op(self):
        pass
    def iret_op(self):
        pass
    
    