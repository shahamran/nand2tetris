# --- Empty Makefile ---
SHELL=bash

all: 
	@echo "Done."

JACK_EXT=.jack
JACK_COMPILER=../../tools/JackCompiler.sh
TAR_FILES=README Makefile *$(JACK_EXT)
TAR_FLAGS=-cvf
TAR_NAME=project12.tar
TAR=tar

tar: 
	$(TAR) $(TAR_FLAGS) $(TAR_NAME) $(TAR_FILES)

JACK_FILES=*$(JACK_EXT)
TEST_DIR="Test/"
LINK=ln
links:
	@echo Creating test files...
	@for f in $(JACK_FILES); do \
		f_clean=$$(basename $$f $(JACK_EXT)); \
		f_dir=$$f_clean$(TEST_DIR); \
		$(LINK) $$f $$f_dir$$f || break; \
		echo Created link: $$f_dir$$f; \
	done

compile: 
	@echo Compiling test directories...
	@for d in *$(TEST_DIR); do \
		$(JACK_COMPILER) $$d; \
	done


clean:
	@echo Removing test files...
	@find . -mindepth 2 -maxdepth 2 -name "*$(JACK_EXT)" ! -name "Main.jack" -print -delete
	@echo Removing vm files...
	@find . -name "*.vm" -not -path "*/Tetris/*" -print -delete

.PHONY: all tar clean
