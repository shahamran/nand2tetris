// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, the
// program clears the screen, i.e. writes "white" in every pixel.

	// Initialize a constant variable SCREEN_SIZE
	@8192
	D=A
	@SCREEN_SIZE
	M=D

(CHECK)
	// Initialize i = 0
	@i
	M=0
	// Get the keyboard input
	@KBD
	D=M
	
	// If any key is pressed, go BACK to BLACK
	@BLACK
	D; JNE
	// Else, continue to WHITE

// Loop to paint the whole screen white	
(WHITE)
	@SCREEN_SIZE
	D=M
	@i
	D=M-D
	
	// if i > SCREEN_SIZE:
	//    goto CHECK
	@CHECK
	D; JGE
	
	// SCREEN[i] = 0 == WHITE_PIXELS
	@i
	D=M
	@SCREEN
	A=A+D
	M=0
	// ++i
	@i
	M=M+1
	
	// Loop
	@WHITE
	0; JMP

// Loop to paint it black	
(BLACK)
	@SCREEN_SIZE
	D=M
	@i
	D=M-D
	
	// if i > SCREEN_SIZE:
	//    goto CHECK
	@CHECK
	D; JGE
	
	// SCREEN[i]=-1 == BLACK_PIXELS
	@i
	D=M
	@SCREEN
	A=A+D
	M=-1
	// ++i
	@i
	M=M+1
	
	// Loop
	@BLACK
	0; JMP
