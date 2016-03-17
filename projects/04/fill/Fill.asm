// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, the
// program clears the screen, i.e. writes "white" in every pixel.

(CHECK)
	@i
	M=0
	@KBD
	D=M

	@BLACK
	D; JNE
	
	@i
	M=0
	D=M
(WHITE)
	// if i > 8,192:
	//    goto CHECK
	// (SCREEN_MEMORY_SIZE == 8192)
	@8192
	D=A
	@i
	D=M-D
	@CHECK
	D; JGE
	
	@i
	D=M
	@SCREEN
	A=A+D
	M=0
	@i
	M=M+1
	@WHITE
	0; JMP
	
(BLACK)
	// if i > 8,192:
	//    goto CHECK
	// (SCREEN_MEMORY_SIZE == 8192)
	@8192
	D=A
	@i
	D=M-D
	@CHECK
	D; JGE
	
	@i
	D=M
	@SCREEN
	A=A+D
	M=-1
	@i
	M=M+1
	@BLACK
	0; JMP

		