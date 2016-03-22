// Bubble Sort
	@swapped
	M=1

(MAIN_LOOP)
	// i = 0
	@i
	M=0
	// Check if swapped. if not, end execution
	// Happens at most n times, where n==RAM[15]
	@swapped
	D=M
	@END
	D; JEQ
	@swapped
	M=0
// Check if every two following numbers are in the correct order.
// If not, swap them.
(SUB_LOOP)
	@R15
	D=M // D = n
	@i
	D=M-D
	D=D+1 
	// if i >= n-1 goto next iteration
	@MAIN_LOOP
	D; JGE
	
	@R14
	D=M // D = arr
	@i
	A=D+M // A = arr + i
	D=A
	// temp = arr + i
	@temp
	M=D
	// D = arr[i]
	A=D
	D=M
	// a = arr[i]
	@a
	M=D
	
	@temp
	A=M+1
	D=M // D = b = arr[i+1]
	@b
	M=D
	@a
	D=D-M // D = b - a
	
	// ++i
	@i
	M=M+1
	
	// if a>=b goto next iteration
	@SUB_LOOP
	D; JLE
		
	// SWAP: b,a = a,b
	@swapped
	M=1
	
	@b
	D=M
	@temp
	A=M
	M=D
	
	@a
	D=M
	@temp
	A=M+1
	M=D
	
	@SUB_LOOP
	0; JMP
	
(END)
