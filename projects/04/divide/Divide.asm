// Divides R13 by R14 and stores the result in R15.
// Uses the shift and add algorithm.

	// Initalize result
	@R15
	M=1
	// If R13<R14 then R15=0
	@R13
	D=M
	@R14
	D=M-D
	@END
	D; JGT
	
// Initialize variables: temp = R14, R15 = 1
(START)
	@R14
	D=M
	@temp
	M=D

// Multiply temp by 2 log_2(R13/R14) times
(SHIFT)
	@temp
	D=M
	@R13
	D=M-D // R13 - temp
	@ADD
	D; JLT // R13-temp < 0 <=> temp > R13 Q.E.D
	
	@temp
	M=M<<
	@R15
	M=M<<
	@SHIFT
	0; JMP

// 
(ADD)
	@temp
	M=M>>
	@R15
	M=M>>
(LOOP)
	@temp
	D=M
	@R13
	D=M-D // R13-temp
	@END
	D; JLT 
	
	@R15
	M=M+1
	@R14
	D=M
	@temp
	M=M+D
	
	@LOOP
	0; JMP
	

(END)
	@R15
	M=M-1
