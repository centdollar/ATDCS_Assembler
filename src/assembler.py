import sys

# import pdb; pdb.set_trace()

dir_path = "../TestCases/"
output_dir = "../MifFiles/"
mifFileHeader = "WIDTH = 16\nDEPTH = 16384\nADDRESS_RADIX = DEC\nDATA_RADIX = BIN\n\n\nCONTENT BEGIN\n"

# -------------------------------- INSTRUCION -> Machine Code Dicts -------------------------------------
regRegInstr = {
    'in': '100000',
    'out': '100001',

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
    'cmp': '010000',

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
    'st': '000001'
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

    def trim_left(self):
        while len(self.content) != 0 and self.content[0].isspace():
            self.content = self.content[1::]

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

    def chopWhileDotAlpha(self):
        n = 0
        if n < len(self.content) and self.content[n] == ".":
            n += 1
        while n < len(self.content) and self.content[n].isalpha():
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
        # print(self.content[0])

        if len(self.content) == 0:
            return None

        elif self.content[0] == "m" and self.content[1] == "[":
            self.content = self.content[2:8] + self.content[9::]
            return self.chopWhileAlphaNum()

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
            print("Reached invalid token")


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
            i += 1

        mifDataString += translateData(addrData)
        mifInstrString += "\nEND;"
        mifDataString += "\nEND;"
        with open(output_dir + "output.mif", "w") as f: f.write(mifInstrString)
        with open(output_dir + "outputMM.mif", "w") as f: f.write(mifDataString)
        print("Instruction Mif File generated")
        print("Data Mif File generated")


'''
TODO:   REFACTOR THINGS 
TODO:   Move the jump calculations into a separate step
            - just store the labels in an array instead of the dict and compare against that 
            - this will allow for more addons to be done
            - 
TODO:   Make output files not overlap, check to see if exists then do like (x).mif
TODO:   Implement an AST ..... someday
TODO:   Implement an include system for functions? 
            - could do parameter mapping to the CPU registers
'''


def main():
    memoryMap = [0, 1000, 2000,16383]
    i = 0
    files = []
    if len(sys.argv) == 1:
        quit("Usage: python3 assembler.py [-h -M] [files]")
    if sys.argv[1] == "-h":
        quit("-h : prints the help screen\n-M [MemoryMap file] [files] : combines assembly files for "
             "multi-programing, expects 1 or more input files")
    if sys.argv[1] == "-M":
        for i in range(2, len(sys.argv)):
            files.append(sys.argv[i])
        multiprogramming = MultiProgramAssembler(files, memoryMap)
        multiprogramming.Multiprogram()


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

    num_warnings = 0
    num_errors = 0
    currentAddress = 0

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

    # Checks that data section is valid
    if validCodeSect != 2:
        print("ERROR: No valid code section")
        num_errors += 1
    # Creates syntax checker for the code section
    else: codeChecker = Parser(tokens[codeSectStart + 1:codeSectEnd])

    if validDataSect != 2:
        print("ERROR: No valid data section")
        num_errors += 1
    # Creates syntax checker for data section
    else: dataChecker = Parser(tokens[dataSectStart + 1: dataSectEnd])

    # Checks that the const section is valid
    if validConstSect != 2:
        print("ERROR: No valid const section")
        num_errors += 1
    # Creates syntax checker for const section
    else: constChecker = Parser(tokens[constSectStart + 1: constSectEnd])

    # Only check the syntax if the const section exists
    if validConstSect == 2:
        while len(constChecker.tokens):
            token = constChecker.peek()
            if token == "let":
                param1 = constChecker.peek(1)
                param2 = constChecker.peek(2)
                param3 = constChecker.peek(3)


                if token in symbolVal:
                    print(f"Warning: assigning data to an symbol address that has already been assigned: {token}")
                    constChecker.consume(3)
                    continue

                if param1[0].isnumeric():
                    print(f"ERROR: start of symbol can not be a number: {param1}")
                constChecker.consume(1)

                if param2 != "=":
                    print(f"ERROR: Expected =, got: {token} *{param1}* {param2}")
                constChecker.consume()

                if param3[0:2] == "0x":
                    if int(param3, 16) > int("0xFFFF", 16) or int(param3, 16) < int("0x0000", 16):
                        print(f"ERROR: memory address must be between 0x0000 and 0xFFFF: {token} ")
                        num_errors += 1
                constChecker.consume()
                constChecker.consume()

                symbolVal[param1] = param3
            else:
                print(f"ERROR: Assignment must start with 'let': {token}")
                constChecker.consume(3)
    else:
        print("No Valid const section")

    # syntax checking for code section
    if validCodeSect == 2:
        forLoopCount = 0
        endForLoopCount = 0
        while len(codeChecker.tokens):
            token = codeChecker.peek()
            # Label Handling
            if token[0] == "@":
                if token in labelAddr:
                    print("ERROR: reassignment of label attempted: {token}")
                    num_errors += 1
                else: labelAddr[token] = currentAddress
                codeChecker.consume()
                continue

            # REGREG Instructions
            elif token in regRegInstr:
                codeChecker.consume()
                currentAddress += 1
                param1 = codeChecker.peek()
                param2 = codeChecker.peek(1)
                codeChecker.consume(2)
                if param1 not in reg:
                    print(f"ERROR: expected a register {token} {param1} {param2}")
                    num_errors += 1

                # expects two registers as arguments
                if param2 not in reg:
                    print(f"ERROR: expected a register {token} {param1} {param2}")
                    num_errors += 1
                continue

            # REGIMM Instructions
            elif token in regImmedInstr:
                codeChecker.consume()
                currentAddress += 1
                param1 = codeChecker.peek()
                param2 = codeChecker.peek(1)
                if param1 not in reg:
                    print(f"ERROR: expected a register {token} *{param1}* {param2}")
                    num_errors += 1
                codeChecker.consume()

                if param2[0] != "#":
                    print(f"ERROR: immediate needs to be #(val): {token} {param1} *{param2}*")
                    num_errors += 1

                if int(param2[1::]) > 31 or int(param2[1::]) < 0:
                    print(f"ERROR: Immediate value needs to be between 0 and 31: {token} {param1} *#{param2[1::]}*")
                    num_errors += 1
                codeChecker.consume()
                continue

            # MEM Instructions
            elif token in memInstr:
                codeChecker.consume()
                currentAddress += 2
                param1 = codeChecker.peek()
                param2 = codeChecker.peek(1)
                param3 = codeChecker.peek(2)
                if param1 not in reg:
                    print(f"ERROR: expected a register {token} *{param1}* {param2} {param3}")
                    i = i + 1
                    num_errors += 1
                codeChecker.consume()

                if param2 not in reg:
                    print(f"ERROR: expected a register {token} {param1} *{param2}* {param3}")
                    num_errors += 1
                codeChecker.consume()

                if int(param3, 16) > int("0xFFFF", 16) or int(param3, 16) < int("0x0000", 16):
                    print(
                        f"ERROR: memory address must be between 0x0000 and 0xFFFF: {token} {param1} {param2} *{param3}*")
                    num_errors += 1
                codeChecker.consume()
                continue

            # Jump instructions
            elif token in jumpInstr:
                codeChecker.consume()
                currentAddress += 2
                param1 = codeChecker.peek()
                param2 = codeChecker.peek(1)
                if param1 not in reg:
                    print(f"ERROR: expected a register {token} *{param1}* {param2}")
                    num_errors += 1
                codeChecker.consume()

                param2 = "@" + param2
                # Remove this temporarily because it does not allow forward jumps due to the label not being parsed yet
                # if param2 not in labelAddr:
                #     print(f"ERROR: label needs to exist to jump to it: {token} {param1} *{param2}*")
                #     num_errors += 1
                codeChecker.consume()
                continue

            elif token in callInstr:
                if token == "ret":
                    codeChecker.consume()
                    continue
                codeChecker.consume()
                currentAddress += 2
                param1 = codeChecker.peek()
                param2 = codeChecker.peek(1)
                if param1 not in reg:
                    print(f"ERROR: expected a register {token} *{param1}* {param2}")
                    num_errors += 1
                codeChecker.consume()
                codeChecker.consume()
                continue

            elif token == "for":
                codeChecker.consume()
                param1 = codeChecker.peek()
                param2 = codeChecker.peek(1)
                param3 = codeChecker.peek(2)

                if param1 not in reg:
                    print(f"ERROR: register needs to be assigned as iterator: {token} *{param1}* {param2} {param3}")
                    num_errors += 1
                codeChecker.consume()

                if param2 != "=":
                    print(f"ERROR: invalid token, needs to be = : {token} {param1} *{param2}* {param3}")
                    num_errors += 1
                codeChecker.consume()

                if int(param3) > 31 or int(param3) < 0:
                    print(f"ERROR: iterator initial value must be between 0 and 31: {token} {param1} {param2} *{param3}*")
                    num_errors += 1
                codeChecker.consume()
                currentAddress += 1
                forAddr[token + str(forLoopCount)] = currentAddress
                forLoopCount += 1
                continue

            elif token == "endfor":
                codeChecker.consume()
                param1 = codeChecker.peek()
                param2 = codeChecker.peek(1)
                param3 = codeChecker.peek(2)
                if param1 not in reg:
                    print(f"ERROR: register needs to be assigned as iterator: {token} *{param1}* {param2} {param3}")
                    num_errors += 1
                codeChecker.consume()

                if param2 != "<":
                    print(f"ERROR: invalid token, comparison can only be less than for now: {token} {param1} *{param2}* {param3}")
                    num_errors += 1
                codeChecker.consume()

                if int(param3) < 0 or int(param3) > 31:
                    print(f"ERROR: iterator initial value must be between 0 and 31: {token} {param1} {param2} *{param3}*")
                    num_errors += 1
                codeChecker.consume()
                currentAddress += 3
                endForLoopCount += 1
                continue


            else:
                num_errors += 1
                print(f"Invalid token: {token}")
                codeChecker.consume()

    else:
        print(f"No valid code section {validCodeSect}")

    # if forLoopCount != endForLoopCount: quit("Syntax Error: number of for and endfor are not equal")

    # Syntax checking for the data section
    if validDataSect == 2:
        while len(dataChecker.tokens):
            token = dataChecker.peek()

            if token[0:2] == "0x":
                if token in addrData:
                    print(f"Warning: assigning data to an address that has already been assigned: {token}")
                    dataChecker.consume(3)
                    continue
                param1 = dataChecker.peek(1)
                param2 = dataChecker.peek(2)
                if int(token, 16) > int("0xFFFF", 16) or int(token, 16) < int("0x0000", 16):
                    print(f"ERROR: memory address must be between 0x0000 and 0xFFFF: {token} ")
                    num_errors += 1
                dataChecker.consume()

                if param1 != "=":
                    print(f"ERROR: Expected =, got: {token} *{param1}* {param2}")
                dataChecker.consume()

                if int(param2, 16) > int("0xFFFF", 16) or int(param2, 16) < int("0x0000", 16):
                    print(f"ERROR: memory address must be between 0x0000 and 0xFFFF: {token} ")
                    num_errors += 1
                dataChecker.consume()
                addrData[token] = param2
                continue
            else:
                print(f"ERROR: invalid token {token}")
                dataChecker.consume(3)
    else:
        print("No valid data section")

    # syntax checking for data section
    return num_errors, num_warnings


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
    codeParser = Parser(tokens[tokens.index(".code") + 1:tokens.index(".endcode")])
    currAddr = startAddr
    tlatedTokens = ''
    forLoopCount = 0
    while len(codeParser.tokens):
        token = codeParser.peek()

        machineCode = ""
        # Translate regreg instructions

        if token[0] == "@":
            codeParser.consume()
            continue

        if token in regRegInstr:
            machineCode += regRegInstr[token]
            machineCode += reg[codeParser.peek(1)]
            machineCode += reg[codeParser.peek(2)]
            tlatedTokens += f"{currAddr}:{machineCode}; % {token} {codeParser.peek(1)} {codeParser.peek(2)} % \n"
            codeParser.consume(3)
            currAddr += 1
            continue
        elif token in regImmedInstr:
            machineCode += regImmedInstr[token]
            machineCode += reg[codeParser.peek(1)]
            machineCode += bin(int(codeParser.peek(2)[1::]))[2::].zfill(5)  # Kinda gross lmao, but it works
            tlatedTokens += f"{currAddr}:{machineCode}; % {token} {codeParser.peek(1)} {codeParser.peek(2)} % \n"
            codeParser.consume(3)
            currAddr += 1
            continue
        elif token in jumpInstr:
            machineCode += jumpInstr[token]
            currReg = codeParser.peek(1)
            machineCode = machineCode.replace("*", reg[currReg])
            tlatedTokens += f"{currAddr}:{machineCode}; % {token} {codeParser.peek(1)} % \n"
            currAddr += 1
            codeParser.consume(2)

            jAddr = labelAddr["@" + codeParser.peek()]
            # Handles Different jumping modes
            # TODO: Implement the rest of jumping modes
            if currReg == "r1":
                if currAddr > jAddr:
                    jumpVal = twosComp(currAddr - jAddr + 1, 16)
                else:
                    jumpVal = jAddr - currAddr - 1
                tlatedTokens += f"{currAddr}:{bin(jumpVal)[1::].zfill(16)[2::]}; % {codeParser.peek()} % \n"
                codeParser.consume()

            currAddr += 1
            continue

        elif token in memInstr:
            machineCode += memInstr[token]
            machineCode += reg[codeParser.peek(1)]
            machineCode += reg[codeParser.peek(2)]
            tlatedTokens += f"{currAddr}:{machineCode}; % {token} {codeParser.peek(1)} {codeParser.peek(2)} % \n"
            codeParser.consume(3)

            currAddr += 1
            addr = codeParser.peek()
            if addr in symbolVal:
                # TODO: check to see if memeory symbol is in the const section
                print("Not implemented")
                tlatedTokens += f"NOT DONE"
                # tlatedTokens += f"{currAddr}:{symbolVal[addr]}"
            else:
                tlatedTokens += f"{currAddr}:{bin(int(addr, 16))[2::].zfill(16)}; % {addr} % \n"
            codeParser.consume()
            currAddr += 1
            continue

        elif token in callInstr:
            if token == "ret":
                zero = "0"
                tlatedTokens += f"{currAddr}:{callInstr[token].ljust(16, zero)}; % {token} % \n"
                codeParser.consume()
                currAddr += 1
                continue
            machineCode += callInstr[token]
            currReg = codeParser.peek(1)
            machineCode += reg[currReg]
            machineCode += "00000"
            tlatedTokens += f"{currAddr}:{machineCode}; % {token} {codeParser.peek(1)} {codeParser.peek(2)} % \n"
            currAddr += 1
            codeParser.consume(2)

            jAddr = labelAddr["@" + codeParser.peek()]
            if currReg == "r1":
                if currAddr > jAddr:
                    jumpVal = twosComp(currAddr - jAddr + 1, 16)
                else:
                    jumpVal = jAddr - currAddr - 1
                tlatedTokens += f"{currAddr}:{bin(jumpVal)[2::].zfill(16)}; % {codeParser.peek()} % \n"
                codeParser.consume()
            currAddr += 1
            continue


        elif token == "for":
            machineCode += regRegInstr["sub"]
            machineCode += reg[codeParser.peek(1)]
            machineCode += reg[codeParser.peek(1)]
            # TODO: Add support for different starting value for a for loop
            # Adds the instruction to clear the iterator register
            tlatedTokens += f"{currAddr}:{machineCode}; % {token}{forLoopCount} {codeParser.peek(1)} {codeParser.peek(3)} % \n"
            forLoopCount += 1
            currAddr += 1
            codeParser.consume(4)
            continue

        elif token == "endfor":
            machineCode += regImmedInstr["cmp"]
            machineCode += reg[codeParser.peek(1)]
            machineCode += bin(int(codeParser.peek(3)))[2::].zfill(5)
            # Adds the compare instruciton to the mif file
            tlatedTokens += f"{currAddr}:{machineCode}; % cmp {codeParser.peek(1)} {codeParser.peek(3)} % \n"

            currAddr += 1
            # Add the jump instruction to the mif file
            # Add the jump instruction to the mif file
            # TODO: implement all jump types
            machineCode = jumpInstr["jz0"].replace("*", reg["r1"])
            tlatedTokens += f"{currAddr}:{machineCode}; % jz0 r1 for{forLoopCount - 1} % \n"
            currAddr += 1
            jAddr = "for" + str(forLoopCount - 1)
            jAddrBin = bin((twosComp((currAddr - startAddr) - (forAddr[jAddr]) + 1, 16)))[2::].zfill(16)[1::]
            tlatedTokens += f"{currAddr}:{jAddrBin}; % offset to jump to for{forLoopCount - 1} % \n"
            currAddr += 1
            forLoopCount -= 1
            codeParser.consume(4)
            continue
        else:
            codeParser.consume()
            print(token)
    tlatedTokens += f"[{currAddr} .. {endAddr - 1}] : 11111111111111; %EMPTY MEMORY LOCATIONS % \n"

    return tlatedTokens


# TODO: Refactor this
def writeMifFile(filepath, tokens, labelAddr, addrData, symbolVal, startingAddress, nextStartingAddress = "16383"):
    # Write to the mif file as one large string
    tlatedTokens = ""



    tlatedTokens += translateCode(tokens, symbolVal, labelAddr, startingAddress, nextStartingAddress)

    return tlatedTokens


def translateData(addrData):
    sorted_dict = dict(sorted(addrData.items()))
    tlatedData = ''
    for key in sorted_dict:
        tlatedData += f"{int(key, 16)}:{bin(int(sorted_dict[key], 16))[2::].zfill(16)[1::]}; % {key} = {sorted_dict[key]} % \n"

    return tlatedData


if __name__ == "__main__":
    main()
