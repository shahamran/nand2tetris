# --- Empty Makefile ---
all: 
	echo "Done."

TAR_FILES=README Makefile *.jack
TAR_FLAGS=-cvf
TAR_NAME=project12.tar
TAR=tar

tar: 
	$(TAR) $(TAR_FLAGS) $(TAR_NAME) $(TAR_FILES)

clean:
	rm -fv *.vm

.PHONY: all tar clean
