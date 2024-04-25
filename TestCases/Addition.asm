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