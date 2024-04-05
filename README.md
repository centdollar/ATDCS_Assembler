# Principles of Computing Create Project
### Project Choice
The project I chose to develop was an assembler for a custom RISC CPU architecture that was developed in EEEE-721 (Advanced Topics of Digital Computer Systems). The assembler is needed because it will translate assembly instructions into machine code for the CPU to use for execution.

### Useful Links:
- Assemblers      -> https://en.wikipedia.org/wiki/Assembly_language#Assembler
- CPUS            -> https://computersciencewiki.org/index.php/Architecture_of_the_central_processing_unit_(CPU)
- Tokenization ->                                                                                
- Syntax          -> https://en.wikipedia.org/wiki/Syntax_(programming_languages)
- CPU git ->
- Assembler git ->


### How to use the program:
#### PyCharm:
To use Pycharm with this project, navigate to the src folder in the directory view on the left side. Then click on assembler.py and click the run button for the python program. This will then display a selection menu which the user inputs what they wish to do in the terminal at the bottom of the screen. The Compile seciton will bring the user to the list of test cases that can be ran to see that the assembler works. There is also an option to use a custom assembly file which the user can change to see the assembler work on your own written code.


#### Another:

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
