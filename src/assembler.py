import sys
import math

dir_path = "../TestCases/"
output_dir = "../../DCS/simulation/modelsim/"
localOutput_dir = "../MifFiles/"
mifFileHeader = "WIDTH = 16;\nDEPTH = 16384;\nADDRESS_RADIX = DEC;\nDATA_RADIX = BIN;\n\n\nCONTENT BEGIN\n"

# -------------------------------- INSTRUCTION -> Machine Code Dicts -------------------------------------
regRegInstr = {
    'in': '100000',
    'out': '100001',
    'cmpr': '110101',

    'swp': '100010',
    'cpy': '100011',

    'add': '101000',
    'sub': '101001',
    'mul': '101010',
    'div': '101011',

    'xor': '100100',
    'and': '100101',
    'or': '100110',
    'not': '100111',

    'fadd': '001000',
    'fsub': '001001',
    'fmul': '001010',
    'fdiv': '001011',

    'vadd': '110000',
    'vsub': '110001',
    'vmul': '110010',
    'vdiv': '110011'
}

regImmedInstr = {
    'cmpc': '010000',

    'srl': '010001',
    'sra': '010010',
    'rotl': '010011',
    'rotr': '010100',

    'addc': '010101',
    'subc': '010110',

    'rrc': '011000',
    'rrn': '011001',
    'rrz': '011010',

    'rln': '011100',
    'rlz': '011101'
}

jumpInstr = {
    'ju': '000100*00000',
    'jc1': '000100*10000',
    'jn1': '000100*01000',
    'jv1': '000100*00100',
    'jz1': '000100*00010',
    'jc0': '000100*01110',
    'jn0': '000100*10110',
    'jv0': '000100*11010',
    'jz0': '000100*11100'
}

callInstr = {
    'call': '111110',
    'ret': '111101'
}

memInstr = {
    'ld': '000000',
    'st': '000001',
    'lds' : '000010',
    'sts' : '000011'
}

reg = {'r0': '00000', 'r1': '00001', 'r2': '00010', 'r3': '00011', 'r4': '00100', 'r5': '00101', 'r6': '00110',
       'r7': '00111',
       'r8': '01000', 'r9': '01001', 'r10': '01010', 'r11': '01011', 'r12': '01100', 'r13': '01101', 'r14': '01110',
       'r15': '01111',
       'r16': '10000', 'r17': '10001', 'r18': '10010', 'r19': '10011', 'r20': '10100', 'r21': '10101', 'r22': '10110',
       'r23': '10111',
       'r24': '11000', 'r25': '11001', 'r26': '11010', 'r27': '11011', 'r28': '11100', 'r29': '11101', 'r30': '11110',
       'r31': '11111'}

# ------------------------------------------------------------------------------------------------------


# Lexer Class to Tokenize the assembly file
class Lexer:
    def __init__(self, content):
        self.content = content

    content = ""

    # Trims white space to the left
    def trim_left(self):
        while len(self.content) != 0 and self.content[0].isspace():
            self.content = self.content[1::]

    def chopWhileNotEOL(self):
        while len(self.content) != 0 and self.content[0] != "\n":
            self.content = self.content[1::]
        self.content = self.content[1::]

    # chop the array n elements from the left
    def chop(self, n):
        token = self.content[0:n]
        self.content = self.content[n::]
        return token

    def chopWhileAlphaNum(self):
        n = 0
        while n < len(self.content) and self.content[n].isalnum():
            n += 1
        return self.chop(n)

    def chopWhileNum(self):
        n = 0
        while n < len(self.content) and self.content[n].isnumeric():
            n += 1
        return self.chop(n)

    def chopWileNotEndBrace(self):
        n = 0
        while n < len(self.content) and self.content[n] != "]":
            n += 1
        rVal = self.chop(n)
        self.chop(1)
        return rVal

    def chopWhileDotAlpha(self):
        n = 0
        if n < len(self.content) and self.content[n] == ".":
            n += 1
        while n < len(self.content) and self.content[n].isalpha() and self.content[n] != "\n":
            n += 1
        return self.chop(n)

    def chopWhileEqual(self):
        n = 0
        while n < len(self.content) and self.content[n] == "=":
            n += 1
        return self.chop(n)

    def chopWhileLessThan(self):
        n = 0
        while n < len(self.content) and self.content[n] == "<":
            n += 1
        return self.chop(n)


    def nextToken(self):
        # trim the whitespace 
        self.trim_left()
        if self.content[0:2] == "//":
            self.chopWhileNotEOL()
        self.trim_left()

        if len(self.content) == 0:
            return None

        elif self.content[0] == "m" and self.content[1] == "[":
            if self.content[2:4] == "0x":
                self.content = self.content[2:8] + self.content[9::]
                return self.chopWhileAlphaNum()
            else:
                self.content = self.content[2::]
                return self.chopWileNotEndBrace()

        elif self.content[0:2] == "0x":
            return self.chopWhileAlphaNum()

        elif self.content[0] == "=":
            return self.chopWhileEqual()

        elif self.content[0] == "<":
            return self.chopWhileLessThan()

        elif self.content[0] == ".":
            return self.chopWhileDotAlpha()

        elif self.content[0] == "#":
            self.content = self.content[1::]
            return "#" + self.chopWhileNum()

        elif self.content[0] == "@":
            self.content = self.content[1::]
            return "@" + self.chopWhileAlphaNum()
        elif self.content[0].isalpha():
            return self.chopWhileAlphaNum()

        elif self.content[0].isnumeric():
            return self.chopWhileNum()

        else:
            print(f"Reached invalid token: {self.content}")


# Parser Class to help with iterating the token lists
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens

    tokens = []

    # Look ahead n tokens and return its value
    def peek(self, n=0):
        return self.tokens[n]

    # Consume n tokens and shrink the tokens list
    def consume(self, n=1):
        self.tokens = self.tokens[n::]


class MultiProgramAssembler:
    def __init__(self, files, memoryMap):
        self.files = files
        self.memoryMap = memoryMap

    # Files that will be combined into one mif file for multiprogramming
    files = []

    # Memory map that will give the starting address of each program
    memoryMap = []

    def Multiprogram(self):
        mifInstrString = mifFileHeader
        mifDataString = mifFileHeader

        i = 0
        labelAddr = {}
        addrData = {}
        for file in self.files:
            symbolVal = {}
            forAddr = {}
            print(f"Tokenizing {file}...")
            tokens = tokenize(file)
            err = syntaxCheck(tokens, labelAddr, addrData, symbolVal, forAddr)
            if err[0] != 0:
                print(f"{err[0]} Errors in {file}")
                exit()
            # else:
            #     print(f"No errors in {file}")
            mifInstrString += translateCode(tokens, symbolVal, labelAddr, forAddr, self.memoryMap[i], self.memoryMap[i+1])
            i += 2

        mifDataString += translateData(addrData)
        mifInstrString += "\nEND;"
        mifDataString += "\nEND;"
        with open(output_dir + "test16.mif", "w") as f:
            f.write(mifInstrString)
        with open(output_dir + "test16_MM.mif", "w") as f:
            f.write(mifDataString)
        with open(localOutput_dir + "test16.mif", "w") as f:
            f.write(mifInstrString)
        with open(localOutput_dir + "test16_MM.mif", "w") as f:
            f.write(mifDataString)
        print("Instruction Mif File generated")
        print("Data Mif File generated")


'''
TODO:   REFACTOR THINGS 
TODO:   Create an assembly file class, but keep in mind that need to be able to multi-program
TODO:   Move the jump calculations into a separate step
            - just store the labels in an array instead of the dict and compare against that 
            - this will allow for more addons to be done
            - 
TODO:   Make output files not overlap, check to see if exists then do like (x).mif
TODO:   Implement an AST ..... someday
TODO:   Implement an include system for functions? 
            - could do parameter mapping to the CPU registers
'''

MAX_MEMORY_ADDR = 2**16 - 1

def main():
    # Needs to be populated in order of programs memory space [start of P1, end of P1, start of P2 ...]
    # memoryMap = [0, 1000, 2000, MAX_MEMORY_ADDR]
    # TODO: Check to make sure the memory map supports the number of files input for multi-programming
    # memoryMap = [0, 255, 256, 511, 512, MAX_MEMORY_ADDR]
    memoryMap = [0, MAX_MEMORY_ADDR]
    
    files = []
    if len(sys.argv) == 1:
        quit("Usage: python3 assembler.py [-h -M] [files]")
    if sys.argv[1] == "-h":
        quit("-h : prints the help screen\n-M [MemoryMap file] [files] : combines assembly files for "
             "multi-programing, expects 1 or more input files")
    elif sys.argv[1] == "-M":
        for i in range(2, len(sys.argv)):
            files.append(sys.argv[i])
        mp = MultiProgramAssembler(files, memoryMap)
        mp.Multiprogram()
    else:
        quit("Usage: python3 assembler.py [-h -M] [files]")

# ------------------------------------------------ Function Declarations -------------------------------
# tokenize(file)
#   file - path of the file to tokenize
# returns tokens[]
def tokenize(file):
    tokens = []
    with open(dir_path + file, "r") as f:
        # Read the file into a string
        F = f.read()
    # Create a lexer with the contents of the asm file
    lexer = Lexer(F)
    # Create tokens until none remain
    while 1:
        token = lexer.nextToken()
        if token:
            tokens.append(token)
        else:
            break
    return tokens


def syntaxCheckConst(tokens, start, end, symbolVal):
    p = Parser(tokens[start + 1: end])
    numErrors = 0
    while len(p.tokens):
        token = p.peek()
        p.consume()
        if token == "let":
            param1 = p.peek()
            param2 = p.peek(1)
            param3 = p.peek(2)

            if token in symbolVal:
                print(f"Warning: assigning data to an symbol address that has already been assigned: {token}")
                p.consume(3)
                continue

            if param1[0].isnumeric():
                print(f"ERROR: start of symbol can not be a number: {param1}")

            if param2 != "=":
                print(f"ERROR: Expected =, got: {token} *{param1}* {param2}")

            if param3[0:2] == "0x":
                if int(param3, 16) > int("0xFFFF", 16) or int(param3, 16) < int("0x0000", 16):
                    print(f"ERROR: memory address must be between 0x0000 and 0xFFFF: {token} ")
                    numErrors += 1
            p.consume(3)

            symbolVal[param1] = param3
        else:
            print(f"ERROR: Assignment must start with 'let': {token}")
            p.consume(3)
    return numErrors


def syntaxCheckCode(tokens, start, end, labelAddr, symbolAddr, forAddr):
    p = Parser(tokens[start + 1:end])
    forLoopCount = 0
    currforLoopCount = 0
    endForLoopCount = 0
    lastForPeekValue = 0
    numErrors = 0
    currentAddress = 0
    while len(p.tokens):
        token = p.peek()
        p.consume()
        # Label Handling
        if token[0] == "@":
            if token in labelAddr:
                print("ERROR: reassignment of label attempted: {token}")
                numErrors += 1
            else:
                labelAddr[token] = currentAddress + 1
            continue
        elif token == "nop":
            currentAddress += 1
            continue
        # REGREG Instructions
        elif token in regRegInstr:
            currentAddress += 1
            param1 = p.peek()
            param2 = p.peek(1)
            p.consume(2)
            if param1 not in reg:
                print(f"ERROR: expected a register {token} {param1} {param2}")
                numErrors += 1

            # expects two registers as arguments
            if param2 not in reg:
                print(f"ERROR: expected a register {token} {param1} {param2}")
                numErrors += 1
            continue

        # REGIMM Instructions
        elif token in regImmedInstr:
            currentAddress += 1
            param1 = p.peek()
            param2 = p.peek(1)
            if param1 not in reg:
                print(f"ERROR: expected a register {token} *{param1}* {param2}")
                numErrors += 1

            if param2[0] != "#":
                print(f"ERROR: immediate needs to be #(val): {token} {param1} *{param2}*")
                numErrors += 1

            if int(param2[1::]) > 31 or int(param2[1::]) < 0:
                print(f"ERROR: Immediate value needs to be between 0 and 31: {token} {param1} *#{param2[1::]}*")
                numErrors += 1
            p.consume(2)
            continue

        # MEM Instructions
        elif token in memInstr:
            currentAddress += 2
            param1 = p.peek()
            param2 = p.peek(1)
            param3 = p.peek(2)
            if param1 not in reg:
                print(f"ERROR: expected a register {token} *{param1}* {param2} {param3}")
                numErrors += 1

            if param2 not in reg:
                print(f"ERROR: expected a register {token} {param1} *{param2}* {param3}")
                numErrors += 1

            if param3 not in symbolAddr:
                if int(param3, 16) > int("0xFFFF", 16) or int(param3, 16) < int("0x0000", 16):
                    print(
                        f"ERROR: memory address must be between 0x0000 and 0xFFFF: {token} {param1} {param2} *{param3}*")
                    numErrors += 1
            p.consume(3)
            continue

        # Jump instructions
        elif token in jumpInstr:
            currentAddress += 2
            param1 = p.peek()
            param2 = p.peek(1)
            if param1 not in reg:
                print(f"ERROR: expected a register {token} *{param1}* {param2}")
                numErrors += 1
            p.consume(2)
            continue

        elif token in callInstr:
            if token == "ret":
                continue
            currentAddress += 2
            param1 = p.peek()
            param2 = p.peek(1)
            if param1 not in reg:
                print(f"ERROR: expected a register {token} *{param1}* {param2}")
                numErrors += 1
            p.consume(2)
            continue

        elif token == "for":
            param1 = p.peek()
            param2 = p.peek(1)
            param3 = p.peek(2)

            if param1 not in reg:
                print(f"ERROR: register needs to be assigned as iterator: {token} *{param1}* {param2} {param3}")
                numErrors += 1

            if param2 != "=":
                print(f"ERROR: invalid token, needs to be = : {token} {param1} *{param2}* {param3}")
                numErrors += 1

            if int(param3) > 31 or int(param3) < 0:
                print(f"ERROR: iterator initial value must be between 0 and 31: {token} {param1} {param2} *{param3}*")
                numErrors += 1
            p.consume(3)
            lastForPeekValue = [index for index, char in enumerate(p.tokens) if char == 'endfor']
            print(lastForPeekValue)
            print(forLoopCount)
            print(forAddr)
            if (int(p.tokens[lastForPeekValue[currforLoopCount] + 3]) < 32):
                forAddr[token + str(forLoopCount)] = currentAddress
                currentAddress += 1
            else:
                forAddr[token + str(forLoopCount)] = currentAddress + 1
                currentAddress += 5
            forLoopCount += 1
            currforLoopCount += 1
            continue

        elif token == "endfor":
            param1 = p.peek()
            param2 = p.peek(1)
            param3 = p.peek(2)
            if param1 not in reg:
                print(f"ERROR: register needs to be assigned as iterator: {token} *{param1}* {param2} {param3}")
                numErrors += 1

            if param2 != "<":
                print(
                    f"ERROR: invalid token, comparison can only be less than for now: {token} {param1} *{param2}* {param3}")
                numErrors += 1

            if int(param3) < 0 or (int(param3) > 31 and int(param3) % 2) :
                print(f"ERROR: iterator initial value must be between 0 and 31: {token} {param1} {param2} *{param3}*")
                numErrors += 1
            p.consume(3)
            currforLoopCount -= 1
            currentAddress += 3
            endForLoopCount += 1
            continue

        else:
            numErrors += 1
            print(f"Invalid token: {token}")
            p.consume()
    return numErrors


def syntaxCheckData(tokens, start, end, addrData):
    p = Parser(tokens[start + 1: end])
    errorCount = 0
    while len(p.tokens):
        token = p.peek()
        p.consume()

        if token[0:2] == "0x":
            if token in addrData:
                print(f"Warning: assigning data to an address that has already been assigned: {token}")
                p.consume(2)
                continue
            param1 = p.peek()
            param2 = p.peek(1)
            if int(token, 16) > MAX_MEMORY_ADDR or int(token, 16) < int("0x0000", 16):
                print(f"ERROR: memory address must be between 0x0000 and {hex(MAX_MEMORY_ADDR)}: {token} ")
                errorCount += 1

            if param1 != "=":
                print(f"ERROR: Expected =, got: {token} *{param1}* {param2}")

            if int(param2, 16) > int("0xFFFF", 16) or int(param2, 16) < int("0x0000", 16):
                print(f"ERROR: memory address must be between 0x0000 and 0xFFFF: {token} ")
                errorCount += 1
            p.consume(2)
            addrData[token] = param2
            continue
        else:
            print(f"ERROR: invalid token {token}")
            p.consume(2)
    return errorCount


# syntaxCheck(tokens)
#   tokens -> array of tokens to parse (will include all tokens gathered from source .asm file)
#   Will provide syntax feedback, and print out errors in syntax
# return 1 for errors and 0 for no errors
def syntaxCheck(tokens, labelAddr, addrData, symbolVal, forAddr):
    print("Syntax checking...")
    global memInstr
    global reg
    global regRegInstr
    global regImmedInstr

    warningsCount = 0
    errorCount = 0

    # used as flags for if an assembly section is present and valid
    validCodeSect = 0
    validDataSect = 0
    validConstSect = 0

    # Check if code section exists
    (codeSectStart, codeSectEnd, validCodeSect) = isSectionValid("code", validCodeSect, tokens)
    # Check is data section exists
    (dataSectStart, dataSectEnd, validDataSect) = isSectionValid("data", validDataSect, tokens)
    # Check is const section exists
    (constSectStart, constSectEnd, validConstSect) = isSectionValid("const", validConstSect, tokens)

    # Only check the syntax if the const section exists
    if validConstSect == 2:
        errorCount += syntaxCheckConst(tokens, constSectStart, constSectEnd, symbolVal)
    else:
        print("Warning: No valid const section")
        warningsCount += 1

    # Syntax checking for the data section
    if validDataSect == 2:
        errorCount += syntaxCheckData(tokens, dataSectStart, dataSectEnd, addrData)
    else:
        print("No valid data section")
        warningsCount += 1

    # syntax checking for code section
    if validCodeSect == 2:
        errorCount += syntaxCheckCode(tokens, codeSectStart, codeSectEnd, labelAddr, symbolVal, forAddr)
    else:
        print("No valid code section")
        errorCount += 1


    # syntax checking for data section
    return errorCount, warningsCount


def isSectionValid(section, section_flag, tokens):
    start = 0
    end = 0
    if ("." + section) not in tokens:
        print(f"ERROR: no {section} directive")
    else:
        start = tokens.index(f".{section}")
        section_flag += 1

    if (".end" + section) not in tokens:
        print(f"ERROR: no .end{section} directive")
    else:
        end = tokens.index(f".end{section}")
        section_flag += 1

    return start, end, section_flag


def twosComp(val, bits):
    val = val - (1 << bits)
    return val


def translateCode(tokens, symbolVal, labelAddr, forAddr, startAddr, endAddr):
    p = Parser(tokens[tokens.index(".code") + 1:tokens.index(".endcode")])
    currAddr = startAddr
    tlatedTokens = ''
    forLoopCount = 0
    currforLoopCount = 0
    print(p.tokens)
    while len(p.tokens):
        token = p.peek()

        machineCode = ""
        # Translate regreg instructions

        if token[0] == "@":
            p.consume()
            continue

        if token == "nop":
            p.consume()
            machineCode += "1110000000000000"
            tlatedTokens += f"{currAddr}:{machineCode}; % {token} % \n"
            currAddr += 1
            continue
        if token in regRegInstr:
            machineCode += regRegInstr[token]
            machineCode += reg[p.peek(1)]
            machineCode += reg[p.peek(2)]
            tlatedTokens += f"{currAddr}:{machineCode}; % {token} {p.peek(1)} {p.peek(2)} % \n"
            p.consume(3)
            currAddr += 1
            continue
        elif token in regImmedInstr:
            machineCode += regImmedInstr[token]
            machineCode += reg[p.peek(1)]
            machineCode += bin(int(p.peek(2)[1::]))[2::].zfill(5)  # Kinda gross lmao, but it works
            tlatedTokens += f"{currAddr}:{machineCode}; % {token} {p.peek(1)} {p.peek(2)} % \n"
            p.consume(3)
            currAddr += 1
            continue
        elif token in jumpInstr:
            machineCode += jumpInstr[token]
            currReg = p.peek(1)
            machineCode = machineCode.replace("*", reg[currReg])
            tlatedTokens += f"{currAddr}:{machineCode}; % {token} {p.peek(1)} % \n"
            currAddr += 1
            p.consume(2)

            jAddr = labelAddr["@" + p.peek()]
            print(labelAddr)
            # Handles Different jumping modes
            # TODO: Implement the rest of jumping modes

            if currReg == "r1":
                if currAddr > jAddr:
                    jumpVal = twosComp(currAddr - jAddr + 1, 16)
                    # Slice starting at 3 because there is a negative sign to cut off
                    jumpVal = bin(jumpVal)[3::].zfill(16)
                else:
                    jumpVal = int(jAddr) - currAddr - 1
                    # No negative sign so slice starting at 2
                    jumpVal = bin(jumpVal)[2::].zfill(16)
                print("---------------------")
                print(currAddr)
                print(jAddr)
                print(twosComp(int(jumpVal, 2), 16) + 1)
                tlatedTokens += f"{currAddr}:{jumpVal}; % {p.peek()} % \n"
                p.consume()

            currAddr += 1
            continue

        elif token in memInstr:
            machineCode += memInstr[token]
            machineCode += reg[p.peek(1)]
            machineCode += reg[p.peek(2)]
            tlatedTokens += f"{currAddr}:{machineCode}; % {token} {p.peek(1)} {p.peek(2)} % \n"
            p.consume(3)

            currAddr += 1
            addr = p.peek()
            if addr in symbolVal:
                tlatedTokens += f"{currAddr}:{bin(int(symbolVal[addr], 16))[2::].zfill(16)}; % {addr} %\n"
            else:
                tlatedTokens += f"{currAddr}:{bin(int(addr, 16))[2::].zfill(16)}; % {addr} % \n"
            p.consume()
            currAddr += 1
            continue

        elif token in callInstr:
            if token == "ret":
                zero = "0"
                tlatedTokens += f"{currAddr}:{callInstr[token].ljust(16, zero)}; % {token} % \n"
                p.consume()
                currAddr += 1
                continue
            machineCode += callInstr[token]
            currReg = p.peek(1)
            machineCode += reg[currReg]
            machineCode += "00000"
            tlatedTokens += f"{currAddr}:{machineCode}; % {token} {p.peek(1)} {p.peek(2)} % \n"
            currAddr += 1
            p.consume(2)

            jAddr = labelAddr["@" + p.peek()]
            if currReg == "r1":
                if currAddr > jAddr:
                    jumpVal = twosComp(currAddr - jAddr + 1, 16)
                else:
                    jumpVal = jAddr - currAddr - 1
                tlatedTokens += f"{currAddr}:{bin(jumpVal)[2::].zfill(16)}; % {p.peek()} % \n"
                p.consume()
            currAddr += 1
            continue

        elif token == "for":
            # TODO: Add support for different starting value for a for loop
            # Adds the instruction to clear the iterator register
            machineCode += regRegInstr["sub"]
            machineCode += reg[p.peek(1)]
            machineCode += reg[p.peek(1)]
            tlatedTokens += f"{currAddr}:{machineCode}; % {token}{forLoopCount} {p.peek(1)} {p.peek(3)} % \n"
            currAddr += 1
            p.consume(4)
            machineCode = ""
            print(forAddr)

            # Support for using register compare
            # TODO: Make it work with more than just powers of 2
            #       Also make the compare register be choosable
            #       Or support it through a load instruction 
            lastForPeekValue = [index for index, char in enumerate(p.tokens) if char == 'endfor']
            if (int(p.peek(lastForPeekValue[currforLoopCount] + 3)) > 31):
                print("IN HERE")
                machineCode += regRegInstr["sub"]
                machineCode += reg["r29"]
                machineCode += reg["r29"]
                tlatedTokens += f"{currAddr}:{machineCode}; % sub r29 r29 % \n"
                currAddr += 1
                machineCode = ""

                machineCode += regImmedInstr["addc"]
                machineCode += reg["r29"]
                machineCode += "00001" 
                tlatedTokens += f"{currAddr}:{machineCode}; % addc r29 1 % \n"
                currAddr += 1
                machineCode = ""

                machineCode += regImmedInstr["rotl"]
                machineCode += reg["r29"]
                machineCode += bin(int(math.log2(float(p.peek(lastForPeekValue[forLoopCount] + 3)))))[2::].zfill(5) 
                tlatedTokens += f"{currAddr}:{machineCode}; % rotl r29 {int(math.log2(float(p.peek(lastForPeekValue[forLoopCount] + 3))))} % \n"
                currAddr += 1
                machineCode = ""
            forLoopCount += 1
            currforLoopCount += 1
            continue

        elif token == "endfor":
            machineCode += regImmedInstr["addc"]
            machineCode += reg[p.peek(1)]
            machineCode += "00001"
            tlatedTokens += f"{currAddr}:{machineCode}; % addc {p.peek(1)} #1 % \n"
            currAddr += 1

            if int(p.peek(3)) > 31:
                machineCode = regRegInstr["cmpr"]
                machineCode += reg[p.peek(1)]
                # TODO: Right now r29 is dedicated to this functionality!!
                machineCode += reg["r29"] 
            else:
                machineCode = regImmedInstr["cmpc"]
                machineCode += reg[p.peek(1)]
                machineCode += bin(int(p.peek(3)))[2::].zfill(5)
            # Adds the compare instruciton to the mif file
            tlatedTokens += f"{currAddr}:{machineCode}; % cmp {p.peek(1)} {p.peek(3)} % \n"

            currAddr += 1
            # Add the jump instruction to the mif file
            # Add the jump instruction to the mif file
            # TODO: implement all jump types
            machineCode = jumpInstr["jz0"].replace("*", reg["r1"])
            tlatedTokens += f"{currAddr}:{machineCode}; % jz0 r1 for{forLoopCount - 1} % \n"
            currAddr += 1
            jAddr = "for" + str(currforLoopCount - 1)
            jAddrBin = bin((twosComp((currAddr - startAddr) - (forAddr[jAddr]) + 1, 16)))[2::].zfill(16)[1::]
            print("-------------------------")
            print(jAddr)
            print(forAddr[jAddr])
            print(forLoopCount)
            print(currAddr)
            print(twosComp(int(jAddrBin, 2), 16))
            tlatedTokens += f"{currAddr}:{jAddrBin}; % offset to jump to for{forLoopCount - 1} % \n"
            currAddr += 1
            currforLoopCount -= 1
            # forLoopCount -= 1
            p.consume(4)
            continue
        else:
            p.consume()
            print(token)
    tlatedTokens += f"[{currAddr} .. {endAddr}] : 11111111111111; %EMPTY MEMORY LOCATIONS % \n"

    return tlatedTokens


def translateData(addrData):
    sorted_dict = dict(sorted(addrData.items()))
    tlatedData = ''
    for key in sorted_dict:
        tlatedData += f"{int(key, 16)}:{bin(int(sorted_dict[key], 16))[2::].zfill(16)[1::]}; % {key} = {sorted_dict[key]} % \n"

    return tlatedData


if __name__ == "__main__":
    main()
