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
