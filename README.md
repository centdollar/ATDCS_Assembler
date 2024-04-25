# Principles of Computing Create Project
## Project Choice
The project I chose to develop was an assembler for a custom RISC CPU architecture that was developed in EEEE-721 (Advanced Topics of Digital Computer Systems). The assembler is needed because it will translate assembly instructions into machine code for the CPU to use for execution.

### Useful Links:
- Assemblers      -> https://en.wikipedia.org/wiki/Assembly_language#Assembler
- CPUS            -> https://computersciencewiki.org/index.php/Architecture_of_the_central_processing_unit_(CPU)
- Tokenization ->     https://www.cs.man.ac.uk/~pjj/farrell/comp3.html#:~:text=The%20tokenizer%20is%20responsible%20for,understanding%20of%20the%20language's%20grammar.                                  
- Syntax          -> https://en.wikipedia.org/wiki/Syntax_(programming_languages)
- CPU git -> https://github.com/centdollar/DCS
- Assembler git -> https://github.com/centdollar/ATDCS_Assembler/tree/PrinciplesOfComputing-CreateProject

### Notes:
- On the assembler git repo, their is a main branch which requires the code to be run through the command line using arguments to pass input files. If you end up on the git repo, make sure you are on the PrinciplesOfComputing-CreateProject Branch
- When looking through the code base, I reccomend folding all functions and looking at the main function and then the Multiprogram function inside of the MultiProgramAssembler Class. If you want to learn more about how the individual functions work unfold them and take a look one at a time to not get overwhelmed. Also if you have any questions, feel free to reach out to me and I am more than happy to help. My school email can be found in the classlist and just put the subject line as Principles of Computing Assembler questions, or something like that.

## Test Cases
Below are the three different test cases that I have, each one has a short description of its purpose as well and its source code.
### Addition:
The first test case is assembly program that will load two values from memory and then add them together and store the result back into memory. When running this test case, you should expect to see that the assembly process finished successfully and the program terminates. 
~~~
.const

let val1 = 0x0000
let val2 = 0x0001
let result = 0x0002

.endconst

.data
0x0000 = 0x0100
0x0001 = 0x0010
.enddata


.code

// Loads the data at address val1 and val2 into registers r5 and r6
ld r0 r5 m[val1]
ld r0 r6 m[val2]

// adds r5 to r6 and writes back result into r5
add r5 r6

// Stores the value in register r5 into the result address

st r0 r5 m[result]
.endcode
~~~

### SyntaxError:
This test case will show the assemblers syntax error detection capabilities. The user can fix this syntax error by following the comments laid out in the SyntaxError.asm file and then rerun it to show that fixing the error will allow the assembler to run properly. This test will result in the assembly process not completing and an error message will present itself to the user in the terminal. If the user fixes this syntax error then the assembly will complete without any errors.
~~~
.const


.endconst

.data
.enddata


.code

// Adds registers 4 and 5 together
add r4 r5

// Syntax error below, change r6 to #(constant) where constant is an integer
addc r5 r6

.endcode
~~~

### MultipleSources:
This test case will compile two seperate assembly files into one mif file. Labels are global within this context, so a call from one assembly file to another does work. The source code for the two assembly files are shown below. This test case should result in a successful assembly and show two sections of code translated to machine code.

#### File1
~~~
.const


.endconst

.data

.enddata


.code

@MM nop
add r1 r1
sub r2 r2
jz0 r1 MM


.endcode
~~~

#### File2
~~~
.const
let hello = 0x0000
let hello = 0x1234 


.endconst

.data

.enddata


.code

add r1 r1
sub r2 r2
add r4 r4
sub r5 r5
addc r1 #1
call r1 MM
for r12 = 0
for r13 = 0
for r14 = 0
for r15 = 0
for r16 = 0
addc r1 #3
sub r4 r5
vadd r4 r4
mul r5 r3
fadd r4 r5
endfor r16 < 12
endfor r15 < 12
endfor r14 < 12
endfor r13 < 12
endfor r12 < 12
jz0 r1 MM

.endcode

~~~

### Custom Assembly:
This test case can be populated by the user to write a program themselves if they want and see if it compiles. This test case will at first assemble without errors, but if the user changes it then they will need to follow the documented ISA for the program to assembly fully.
~~~
.const

.endconst

.data

.enddata


.code

// Write your own code here to test it!!!

nop
nop
nop

.endcode
~~~

## How to use the program:
#### PyCharm:
To use Pycharm with this project, navigate to the src folder in the directory view on the left side. Then click on assembler.py and click the run button for the python program. This will then display a selection menu which the user inputs what they wish to do in the terminal at the bottom of the screen. The Compile seciton will bring the user to the list of test cases that can be ran to see that the assembler works. There is also an option to use a custom assembly file which the user can change to see the assembler work on your own written code.

#### VSCode:
1) Clone the git repo and open that directory with vscode
2) Make sure you are on the Principles of Computing Branch in the git repo
3) Open the src folder and select assembly.py
4) In the top right hit the run button and then follow the instructions in the terminal
5) Run test cases and the like.

### General Program Flow
#### Inputs:
- Assembly File/s

#### Stage 1: Tokenization
The first stage in the assembly process is to tokenize the input files for further processing. This process uses a Lexer object to seperate the tokens by whitespace in the input files. Once the lexer has parsed the entire input file, the tokens are passed to the next stage as a list of strings.

#### Stage 2: Syntax Checking
Next, the individual tokens need to be parsed in order to confirm that they are valid tokens in our assembly language. This process uses a parser to look at the current and future tokens to see if they follow the defined programming language. More information about how parsing works can be found below.

#### Stage 3: Translation
Assuming that the syntax check returns with no errors, the tokens are passed to a translation function which will convert the assembly code into the machine code. This stage generates a string of data that is then passed along and written to an output file.


#### Outputs:
- MIF File



## More Details:
#### Tokenization: 
The tokenizer will create tokens using whitespace as the delimiter. Below are examples of tokens that will be produced.
- "Hello, World!" - > 2 tokens begin "Hello," and "World!"

#### Syntax Checking:
The syntax checking will compare the tokens that are generated from the tokenization stage to the valid tokens in the language. These valid tokens can be found in the InstrTranslation.py file. These tokens must also be used when writing your own assembly code to be compiled.

#### Translation:
The translation phase will only run if the syntax check returns with no errors. This function will do a 1 to 1 substitution for the valid token to its corresponding machine code. More information about the translation and ISA of the CPU can be found in the git repo for the CPU. One examples is shown below.
- add r1 r1 -> 1010000000100001
- (This will add the value in register 1 with itself and store the resultant in register 1)
- In this example, the add instruction is translated to the value 101000 and then the resgisters are translated to 00001