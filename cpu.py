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
MOD = 0b10000010    # Divide the value in the first register by the value in the second, storing the remainder of the result in registerA.
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
        self.HALTED = False
        branchTable = {
            HLT: halt_op,
            LDI: ldi_op,
            PRN: print_op,
            ADD: add_op,
            MUL: mul_op,
            PUSH: push_op,
            POP: pop_op,
            CALL: call_op,
            RET: ret_op,
            ADD: add_op,
            OR: or_op,
            XOR: xor_op,
            NOT: not_op,
            SHL: shl_op,
            SHR: shr_op,
            MOD: mod_op,
            INT: int_op,
            IRET: iret_op,
        }
    def halt_op ():
        self.HALT = True
    def pop_op():
        self.reg[operand_a] = self.ram_read(self.reg[self.sp])
        self.reg[self.sp] += 1
    def push_op():
        self.reg[self.sp] -= 1
        value = self.reg[operand_a]
        address = self.reg[self.sp]
        self.raw_write(address, value)
    def prn_op():
        print(self.reg[operand_a])
    def ldi_op():
        self.reg[operand_a] = operand_b
    def add_op():
        self.alu("ADD", operand_a, operand_b)
    def mul_op():
        self.alu("MUL", operand_a, operand_b)
    def call_op():
        pass
    def ret_op():
        pass
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
        #elif op == "SUB": etc
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
            # LDI = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            operands = (IR  >> 6 ) & 0b11000000
            if IR in branchTable:
                branchTable[IR]()
                self.pc += operands + 1
            else:
                raise Exception(f"Invalid instruction {hex(ir)} at address {hex(pc)}")

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
          
            
    