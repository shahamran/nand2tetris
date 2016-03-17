// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

	@R2
	M=0
	@IS_NEG
	M=0
	
	@R1
	D=M
	@END
	D; JEQ
	@NEGATIVE
	D; JLT
	@POS_R1
	M=D
	@START
	0; JMP
	
(NEGATIVE)
	@IS_NEG
	M=1
	@POS_R1
	M=-D
	
(START)
	@i
	M=1
	@R0
	D=M
	@R2
	M=D

(SHIFT)
	@POS_R1
	D=M
	@i
	D=M-D
	@ADD
	D; JGT
	
	@i
	M=M<<
	@R2
	M=M<<
	@SHIFT
	0; JMP
	
(ADD)
	@i
	M=M>>
	@R2
	M=M>>
(LOOP)
	@POS_R1
	D=M
	@i
	D=M-D
	@CHECK_NEG
	D; JGE
	
	@i
	M=M+1
	@R0
	D=M
	@R2
	M=M+D
	
	@LOOP
	0; JMP
	
(CHECK_NEG)
	@IS_NEG
	D=M
	@END
	D; JEQ
	@R2
	M=-M
	@END
	0; JMP
	
(END)
	@END
	0; JMP