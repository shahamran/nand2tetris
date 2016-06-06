# --- Empty Makefile ---
all: 
	chmod +x JackCompiler

TAR_FILES=README Makefile *.py JackCompiler 
TAR_FLAGS=-cvf
TAR_NAME=project11.tar
TAR=tar

tar: 
	$(TAR) $(TAR_FLAGS) $(TAR_NAME) $(TAR_FILES)

clean:
	rm -fv *.vm

.PHONY: all tar clean
