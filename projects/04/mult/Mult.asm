// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

	// Initalize the result to 0
	@R2
	M=0
	// If R0==0: goto END (0*X=0 for all X)
	@R0
	D=M
	@END
	D; JEQ

// For i = 0 to R1: result += R0 (where result is R2)
	// Initialize: i = 0
	@i
	M=0
(LOOP)
	@i
	D=M
	// if i >= R1: goto END
	@R1
	D=M-D
	@END
	D; JLE
	// R2 = R2 + R0
	@R0
	D=M
	@R2
	M=M+D
	// ++i
	@i
	M=M+1
	// End for (back to LOOP)
	@LOOP
	0; JMP

// Busy waiting
(END)
	@END
	0; JMP
