# ATDCS_Assembler
 Translation from a custom RISC ISA to machine code to run on the CPU found at this repo:

# Usage
- to use from the command line, move to the src directory and run the following command: python3 assembler.py -M Test1.asm Test2.asm



# Syntax and Semantics
 Program = Sections | {Sections}
 Sections = instruction | {instrucion}
 instruction = opcode | opcode Ri Rj | opcode Ri # | opcode Ri Rj mem | immediate
 immediate = Address Value (number)
 Ri = number 0 - 31
 Rj = number 0 - 31
 opcode = 6 bit binary number
 mem = memory address