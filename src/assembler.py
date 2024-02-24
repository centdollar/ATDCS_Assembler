import sys

def main():
    # print(f"Arguments List: {sys.argv}")
    file1tokens = tokenize(sys.argv[1])
    if(not syntaxCheck(file1tokens)):
        print("No errors")
    else:
        exit()

    # print(file1tokens)

# tokenize(file)
#   file - path of the file to tokenize
# returns tokens[]
def tokenize(file):
    tokens = []
    with open(file, "r") as f:
        # Read file into variable array F
        F = f.readlines()

        # method for removing newlines as the lines in the file is populated into the tokens array
        stripnewline = lambda x: x.strip("\n")

        # populates tokens array
        tokens = [(stripnewline(F[i])) for i in range(len(F))]

        # filters out any empty lines in the token list
        tokens = list(filter(lambda x: x != '', tokens))
    return tokens


# syntaxCheck(tokens)
#   tokens -> array of tokens to parse (will include all tokens gathered from source .asm file)
#   Will provide syntax feedback, and print out errors in syntax
# return 1 for errors and 0 for no errors
def syntaxCheck(tokens):
    print("No Syntax Errors")
    tokenList = []
    for instructions in tokens:
        tokenList.extend(instructions.split(" "))

    # break the tokens into their sections for further processing
    # TODO: handle errors if their are no .code and .codeend
    codeSectStart = tokenList.index(".code")
    codeSectEnd = tokenList.index(".endcode")
    codeTokens = tokenList[codeSectStart:codeSectEnd]
    print(codeTokens)
    

    print(tokenList)



if __name__ == "__main__":
    main()


# RISC ISA valid instructions
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
