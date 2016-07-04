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
	find . -mindepth 2 -name "*.jack" ! -name "Main.jack" -delete
	find . -name "*.vm" -delete

.PHONY: all tar clean
