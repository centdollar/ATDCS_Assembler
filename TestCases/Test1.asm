.const
let hello = 0x0000
let hello = 0x1234 


.endconst

.data
0x0000 = 0xFFFF
0x1000 = 0xFFFE
0x1200 = 0xFFFE
0x1030 = 0xFFFE
0x1001 = 0xFFFE
0x0100 = 0xFFFE

.enddata


.code


for r19 = 0
add r2 r1
mul r4 r2


endfor r19 < 10



sub r31 r31
addc r31 #1
add r1 r2
out r31 r0


.endcode