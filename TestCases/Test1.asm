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
@Label21 cmp r1 #15
add r1 r1
jz0 r1 Label21


for r19 = 0
add r1 r1
for r18 = 0
add r1 r1
addc r2 #2
endfor r18 < 10
endfor r19 < 10
add r1 r1
call r1 MM

ld r1 r10 m[0x2000]
addc r1 #2 
subc r2 #31 
st r0 r1 m[0x1200]
@Label123 ld r0 r1 m[0x3421]


@MM add r1 r1
sub r2 r3
ret


.endcode