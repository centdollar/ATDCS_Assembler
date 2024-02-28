import sys
# import pdb; pdb.set_trace()

dir_path = "../TestCases/"

regRegInstr = {
'in'    :'100000', 
'out'   :'100001',

'swp'   :'100010', 
'cpy'   :'100011',

'add'   :'101000', 
'sub'   :'101001', 
'mul'   :'101010', 
'div'   :'101011',

'xor'   :'100100', 
'and'   :'100101', 
'or'    :'100110',
'not'   :'100111',

'fadd'  :'001000',
'fsub'  :'001001',
'fmul'  :'001010',
'fdiv'  :'001011',

'vadd'  :'110000', 
'vsub'  :'110001',
'vmul'  :'110010', 
'vdiv'  :'110011'
}


regImmedInstr = {
'cmp'   :'010000',

'srl'   :'010001', 
'sra'   :'010010',
'rotl'  :'010011', 
'rotr'  :'010100', 

'addc'  :'010101', 
'subc'  :'010110', 

'rrc'   :'011000',
'rrn'   :'011001', 
'rrz'   :'011010',

'rln'   :'011100', 
'rlz'   :'011101'
}


jumpInstr = {
'ju'   :'000100*00000', 
'jc1'   :'000100*10000', 
'jn1'   :'000100*01000', 
'jv1'   :'000100*00100', 
'jz1'   :'000100*00010', 
'jc0'   :'000100*01110', 
'jn0'   :'000100*10110', 
'jv0'   :'000100*11010', 
'jz0'   :'000100*11100'
}


memInstr = {
'ld'    :'000000', 
'st'     :'000001'
}


reg = {'r0' :'00000', 'r1' :'00001', 'r2' :'00010', 'r3' :'00011', 'r4' :'00100', 'r5' :'00101', 'r6' :'00110', 'r7' :'00111', 
       'r8' :'01000', 'r9' :'01001', 'r10':'01010', 'r11':'01011', 'r12':'01100', 'r13':'01101', 'r14':'01110', 'r15':'01111',
       'r16':'10000', 'r17':'10001', 'r18':'10010', 'r19':'10011', 'r20':'10100', 'r21':'10101', 'r22':'10110', 'r23':'10111', 
       'r24':'11000', 'r25':'11001', 'r26':'11010', 'r27':'11011', 'r28':'11100', 'r29':'11101', 'r30':'11110', 'r31':'11111'}



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
            n+=1
        while n < len(self.content) and self.content[n].isalpha():
            n += 1
        return self.chop(n)

    def chopWhileEqual(self):
        n = 0
        while n < len(self.content) and self.content[n] == "=":
            n += 1
        return self.chop(n)

    def nextToken(self):
        # trim the whitespace 
        self.trim_left()
        # print(self.content[0])

        if len(self.content) == 0:
            return None

        elif self.content[0] =="m":
            if self.content[1] == "[":
                self.content = self.content[2:8] + self.content[9::]
                return self.chopWhileAlphaNum()
        
        elif self.content[0:2] == "0x":
            return self.chopWhileAlphaNum()

        elif self.content[0] == "=":
            return self.chopWhileEqual() 

        elif self.content[0] ==".":
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


class syntaxChecker:
    def __init__(self, tokens):
        self.tokens = tokens

    tokens = []

    def peek(self, n = 0):
        return self.tokens[n]
    
    def consume(self, n = 1):
        self.tokens = self.tokens[n::]

def main():
    labelAddr = {}    
    addrData = {}    
    symbolVal = {}
    file1tokens = tokenize(sys.argv[1])
    err = syntaxCheck(file1tokens, labelAddr, addrData, symbolVal)
    if err[0] != 0:
        print(f"{err[0]} Errors")
        exit()
    else:
        print("No errors")
    # print(labelAddr)

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
def syntaxCheck(tokens, labelAddr, addrData, symbolVal):
    global memInstr
    global reg
    global regRegInstr
    global regImmedInstr



    num_warnings = 0
    num_errors = 0
    currentAddress = 0

    # Tracks if the code section exists 
    # val of 2 means there are both a start and end of code sect
    validCodeSect = 0
    validDataSect = 0
    validConstSect = 0

    # Check if code section exists
    if ".code" not in tokens:
        print("ERROR: no .code directive")
    else:
        codeSectStart = tokens.index(".code")
        validCodeSect += 1

    if ".endcode" not in tokens:
        print("ERROR: no .endcode directive")
    else:
        codeSectEnd= tokens.index(".endcode")
        validCodeSect += 1
    
    # Check is data section exists
    if ".data" not in tokens:
        print("Warning: no data section")
        num_warnings += 1
    else:
        dataSectStart = tokens.index(".data")
        validDataSect += 1
    
    if ".enddata" not in tokens:
        print("Warning: no enddata section")
        num_warnings += 1
    else:
        dataSectEnd = tokens.index(".enddata")
        validDataSect += 1

    # Check is const section exists
    if ".const" not in tokens:
        print("Warning: no const section")
        num_warnings += 1
    else:
        constSectStart = tokens.index(".const")
        validConstSect += 1
    
    if ".endconst" not in tokens:
        print("Warning: no endconst section")
        num_warnings += 1
    else:
        constSectEnd = tokens.index(".endconst")
        validConstSect += 1
    

    # Checks that data section is valid
    if validCodeSect != 2:
        print("ERROR: No valid code section")
        num_errors += 1
    else:
        # Creates syntax checker for the code section
        codeChecker = syntaxChecker(tokens[codeSectStart + 1:codeSectEnd])
    
    if validDataSect != 2:
        print("ERROR: No valid data section")
        num_errors += 1
    else:
        # Creates syntax checker for data section
        dataChecker = syntaxChecker(tokens[dataSectStart + 1: dataSectEnd])

    # Checks that the const section is valid
    if validConstSect != 2:
        print("ERROR: No valid const section")
        num_errors += 1
    else:
        # Creates syntax checker for const section
        constChecker = syntaxChecker(tokens[constSectStart + 1: constSectEnd])


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
                dataChecker.consume(3)





    else:
        print("No Valid const section")


    # syntax checking for code section
    if validCodeSect == 2:
        while len(codeChecker.tokens):
            token = codeChecker.peek()
            # Label Handling
            if token[0] == "@":
                if token in labelAddr:
                    print("ERROR: reassignment of label attempted: {token}")
                    num_errors += 1
                else:
                    labelAddr[token] = currentAddress 
                codeChecker.consume()
                continue

            # REGREG Instructions
            elif token in regRegInstr:
                codeChecker.consume()
                currentAddress += 1
                param1 = codeChecker.peek() 
                param2 = codeChecker.peek(1) 
                if param1 not in reg:
                    print(f"ERROR: expected a register {token} {param1} {param2}")
                    num_errors += 1

                codeChecker.consume()

                # expects two registers as arguments
                if param2 not in reg:
                    print(f"ERROR: expected a register {token} {param1} {param2}")
                    num_errors += 1
                codeChecker.consume()
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
                    print(f"ERROR: memory address must be between 0x0000 and 0xFFFF: {token} {param1} {param2} *{param3}*")
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
                if param2 not in labelAddr:
                    print(f"ERROR: label needs to exist to jump to it: {token} {param1} *{param2}*")
                    num_errors += 1
                codeChecker.consume()
                continue


            else:
                num_errors += 1
                print(f"Invalid token: {token}")
                codeChecker.consume()
    else:
        print(f"No valid code section")
    
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
    return (num_errors, num_warnings)

            


if __name__ == "__main__":
    main()

