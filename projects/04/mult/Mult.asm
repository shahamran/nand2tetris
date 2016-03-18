// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

	// Initalize the result to 0
	@R2
	M=0
	// If R1==0 or R2 == 0, goto END
	@R1
	D=M
	@END
	D; JEQ
	@R2
	D=M
	@END
	D; JEQ
	
// Initialize variables: i = 1, R2 = R0
(START)
	@i
	M=1
	@R0
	D=M
	@R2
	M=D

// Multiply R2 by 2 log_2(R1) times
(SHIFT)
	@R1
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

// Add R0 to R2 R1-floor{log_2(R1)} times
(ADD)
	@i
	M=M>>
	@R2
	M=M>>
(LOOP)
	@R1
	D=M
	@i
	D=M-D
	@END
	D; JGE
	
	@i
	M=M+1
	@R0
	D=M
	@R2
	M=M+D
	
	@LOOP
	0; JMP
	
// Busy waiting
(END)
	@END
	0; JMP