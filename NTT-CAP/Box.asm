// Box.asm  (K = 47)
// Box starts at row 47 -> address 16384 + 32*47 = 17888
// 20 rows tall, ((47 mod 4)+1) = 4 words = 64 pixels wide, from the left edge.
// While any key is pressed the box is black; when released it is white.

(MAIN)
    @KBD
    D=M
    @BLACK
    D;JNE           // key pressed -> black
    @color
    M=0             // no key -> white (0)
    @DRAW
    0;JMP
(BLACK)
    @color
    M=-1            // all 16 bits set = black
(DRAW)
    @17888
    D=A
    @addr
    M=D             // addr = first word of the current row
    @20
    D=A
    @rows
    M=D             // rows left = 20
(ROWLOOP)
    @4
    D=A
    @cols
    M=D             // 4 words per row
    @addr
    D=M
    @p
    M=D             // p = pointer to current word
(COLLOOP)
    @color
    D=M
    @p
    A=M
    M=D             // RAM[p] = color
    @p
    M=M+1
    @cols
    M=M-1
    D=M
    @COLLOOP
    D;JGT
    @32
    D=A
    @addr
    M=D+M           // next row = +32 words
    @rows
    M=M-1
    D=M
    @ROWLOOP
    D;JGT
    @MAIN
    0;JMP
