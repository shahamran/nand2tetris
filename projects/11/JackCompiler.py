#!/usr/bin/env ipython3
from CompilationEngine import *
import os


def translate_file(filename):
    if filename.endswith('.jack'):
        outfilename = filename[:-5] + '.vm'
        result = CompilationEngine(filename)
        with open(outfilename, 'w') as outfile:
            outfile.write(str(result))


def main():
    if not os.path.exists(sys.argv[1]):
        return
    fullpath = os.path.abspath(sys.argv[1])

    print("Compiling " + fullpath)
    if os.path.isfile(fullpath):
        translate_file(fullpath)
    elif os.path.isdir(fullpath):
        for filename in os.listdir(fullpath):
            translate_file(os.path.join(fullpath, filename))
        

if __name__ == "__main__":
    main()
