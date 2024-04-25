"""--------------------------------------------------------------------------------------------------------------------------------------------+
|   Principles Of Computing: Create Project                                                                                                    |
|   Created by: Vincent Michelini, EE                                                                                                          |
|                                                                                                                                              |
|                                                                                                                                              |
|   Project:    The goal of this project was to create an assembler which compiles assembly code into machine code.                            |
|               Machine code is read by a CPU in computers and encodes the actual instructions that are ran on the physical hardware.          |
|                                                                                                                                              |
|   Program Flow:                                                                                                                              |
|       Inputs: Assembly files (contain the code written in assembly)                                                                          |
|       Outputs: A mif file with the compiled assembly files in machine code                                                                   |
|                                                                                                                                              |
|       Input Files -> Tokenize -> Syntax Checked -> Translation -> Output File (.mif)                                                         |
|                                                                                                                                              |
|       Tokenize:   The tokenization phase reads the input files and breaks them up into individual token, in this project                     |
|                   a token is any string inbetween two whitespace characters (" "). This is done using a Lexer object.                        |
|                                                                                                                                              |
|       Syntax Check:   The tokens from the previous function are then sent through a function that checks the tokens to make sure they        |
|                       are valid in our custom assembly language. More information about this can be found in the README.                     |
|                                                                                                                                              |
|       Translation:    This stage is ran if the syntax check came back error free. This takes the tokens and generate a mif file with the     |
|                       machine code in it. The translation dictionaries can be found in the include file (___). This dictionary maps the valid|
|                       token to its binary representation following the ISA.                                                                  |
|                                                                                                                                              |
|   Useful Links:   Assemblers      -> https://en.wikipedia.org/wiki/Assembly_language#Assembler                                               |
|                   CPUS            -> https://computersciencewiki.org/index.php/Architecture_of_the_central_processing_unit_(CPU)             |
|                   Tokenization    ->                                                                                                         |
|                   Syntax          -> https://en.wikipedia.org/wiki/Syntax_(programming_languages)                                            |
+----------------------------------------------------------------------------------------------------------------------------------------------+"""
# Importing some common packages
import math

# Importing the Instruciton Translation dictionaries from another python file
import InstrTranslation 

# Lexer Class to Tokenize the assembly file
import Lexer

# Parser Class to help with iterating the token lists
import Parser

regRegInstr = InstrTranslation.regRegInstr        # putting the dict from the import into a local variable
regImmedInstr = InstrTranslation.regImmedInstr
callInstr = InstrTranslation.callInstr
jumpInstr = InstrTranslation.jumpInstr
memInstr = InstrTranslation.memInstr
reg = InstrTranslation.reg

# Assign the local output path of the assembled mif file
dir_path = "./TestCases/"
# output_dir = "../MifFiles/"
localOutput_dir = "./MifFiles/"

# Configuration
ADDR_WIDTH = 16
MAX_MEMORY_ADDR = 2**ADDR_WIDTH - 1

# Constant Header information for the mif file
mifFileHeader = f"WIDTH = {ADDR_WIDTH};\nDEPTH = {MAX_MEMORY_ADDR};\nADDRESS_RADIX = DEC;\nDATA_RADIX = BIN;\n\n\nCONTENT BEGIN\n"


# This class handles assembling for single and multiple files
class MultiProgramAssembler:
    def __init__(self, files, memoryMap, outputFileName):
        self.files = files
        self.memoryMap = memoryMap
        self.outputFileName = outputFileName

    # Files that will be combined into one mif file for multiprogramming
    files = []

    outputFileName = ""

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
        # with open(output_dir + "output.mif", "w") as f:
        #     f.write(mifInstrString)
        # with open(output_dir + "output_MM.mif", "w") as f:
        #     f.write(mifDataString)
        with open(localOutput_dir + self.outputFileName +".mif", "w") as f:
            f.write(mifInstrString)
        with open(localOutput_dir + self.outputFileName + "_MM.mif", "w") as f:
            f.write(mifDataString)
        print("Instruction Mif File generated")
        print("Data Mif File generated")


def main():
    menuPrint("Make a selection", ["Compile", "Help", "Quit"])          # Print the menu
    
    # Wait until a user input is a valid selection
    userSelection = int(input("|"))
    while userSelection < 1 or userSelection > 3:
        print(f"Pick a valid option: not {userSelection}")
        userSelection = int(input("|"))
    
    menuSelect = userSelection
    if menuSelect == 1:                 # Select the correct menu choice
        compileSelection = ["Addition", "SyntaxError", "MultipleSourceFiles", "", "Custom Assembly"]
        menuPrint("Which test which you like to run", compileSelection)

        userSelection = int(input("|"))
        while userSelection < 1 or userSelection > len(compileSelection):
            print(f"Pick a valid option: not {userSelection}")
            userSelection = int(input("|"))

        # Get an output file name from the user
        print("| Select an output file name: ")
        outputfilename = str(input("|"))
        # make sure that the name is not over 32 characters and more than 1
        while len(outputfilename) > 32  or not outputfilename:
            print("| Please have the output file name be less than 32 characters")
            outputfilename = str(input("|"))

        if userSelection == 1:
            testFile = compileSelection[userSelection - 1] + ".asm"
            fileList = [testFile]
            memoryMap = [0, MAX_MEMORY_ADDR]
            mp = MultiProgramAssembler(fileList, memoryMap, outputfilename)
            mp.Multiprogram()
        if userSelection == 2:
            testFile = compileSelection[userSelection - 1] + ".asm"
            fileList = [testFile]
            memoryMap = [0, MAX_MEMORY_ADDR]
            mp = MultiProgramAssembler(fileList, memoryMap, outputfilename)
            mp.Multiprogram()
        if userSelection == 3:
            testFile = compileSelection[userSelection - 1] + ".asm"
            fileList = ["Test2.asm", "Test3.asm"]
            memoryMap = [0, 1000, 1001,MAX_MEMORY_ADDR]
            mp = MultiProgramAssembler(fileList, memoryMap, outputfilename)
            mp.Multiprogram()
        if userSelection == 5:
            testFile = compileSelection[userSelection - 1] + ".asm"
            fileList = [testFile]
            memoryMap = [0, MAX_MEMORY_ADDR]
            mp = MultiProgramAssembler(fileList, memoryMap, outputfilename)
            mp.Multiprogram()

        print("-----------------------------------")
        with open(localOutput_dir + outputfilename + ".mif" ,"r") as f:
            print(f.read())
        print("-----------------------------------")
        print("Above is the generated mif file")
    elif menuSelect == 2:
        helpList = ["In the src directory", "back"]
        menuPrint("If things aren't working ensure the following", helpList)


    




# ------------------------------------------------ Function Declarations -------------------------------
def menuPrint(title, selections):
    fill = "-"
    print(f"+{45*fill}+")
    print(f"|{title:45}|")
    for i in range(len(selections)):
        print(f"|{i+1:>3}. {selections[i]:40}|")
    print(f"+{45*fill}+")


# tokenize(file)
#   file - path of the file to tokenize
# returns tokens[]
# TODO: Interesting bug where if a file does not exist a output is generated
def tokenize(file):
    tokens = []
    try:
        with open(dir_path + file, "r") as f:
            # Read the file into a string
            F = f.read()
    except IOError:
        print("Error: Could not open file")
        exit()
    # Create a lexer with the contents of the asm file
    lexer = Lexer.Lexer(F)
    # Create tokens until none remain
    while 1:
        token = lexer.nextToken()
        if token:
            tokens.append(token)
        else:
            break
    return tokens


def syntaxCheckConst(tokens, start, end, symbolVal):
    p = Parser.Parser(tokens[start + 1: end])
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
    p = Parser.Parser(tokens[start + 1:end])
    forLoopCount = 0
    currforLoopCount = 0
    endForLoopCount = 0
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
            if int(p.tokens[lastForPeekValue[currforLoopCount] + 3]) < 32:
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

            if int(param3) < 0 or (int(param3) > 31 and int(param3) % 2):
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
    p = Parser.Parser(tokens[start + 1: end])
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
    p = Parser.Parser(tokens[tokens.index(".code") + 1:tokens.index(".endcode")])
    currAddr = startAddr
    tlatedTokens = ''
    forLoopCount = 0
    currforLoopCount = 0
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

            # Support for using register compare
            # TODO: Make it work with more than just powers of 2
            #       Also make the compare register be choosable
            #       Or support it through a load instruction 
            lastForPeekValue = [index for index, char in enumerate(p.tokens) if char == 'endfor']
            if int(p.peek(lastForPeekValue[currforLoopCount] + 3)) > 31:
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
