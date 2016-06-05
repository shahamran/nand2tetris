# --- Empty Makefile ---
all: 
	chmod +x JackAnalyzer
	chmod +x JackAnalyzer.py

TAR_FILES=README Makefile *.py JackAnalyzer 
TAR_FLAGS=-cvf
TAR_NAME=project10.tar
TAR=tar

tar: 
	$(TAR) $(TAR_FLAGS) $(TAR_NAME) $(TAR_FILES)

clean:
	rm -fv *.xml

.PHONY: all tar clean
