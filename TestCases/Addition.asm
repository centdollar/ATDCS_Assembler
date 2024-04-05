.const
let hello = 0x0000
let hello = 0x1234 


.endconst

.data
0x01ff = 0x0100
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