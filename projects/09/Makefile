# --- Empty Makefile ---
all: ;

TAR_FILES=README *.jack 
TAR_FLAGS=-cvf
TAR_NAME=project9.tar
TAR=tar

tar: 
	$(TAR) $(TAR_FLAGS) $(TAR_NAME) $(TAR_FILES)

clean:
	rm -fv *.vm

.PHONY: all tar clean
