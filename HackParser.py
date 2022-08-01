import argparse
import io
import logging
import logging.handlers
import os
import sys
import time

class HackParser:
    """
    Encapsulates access to the input code. Reads an assembly language
    statement, parses it, and provides convenient access to the statement's
    components (fields and symbols). In addition, removes all white
    space and comments.
    """

    def __init__(self):
        """
        Process command line arguments, process the input filename,
        open and read it, construct the output filename.
        """

        # initialize instance variables
        self.currentInst = ''   # the current instruction being processed
        self.lines = []         # list of lines in the input file
        self.nLines = 0         # number of lines in the input file
        self.currentLine = 0    # the number of the current line being processed
        self.currentWord = 0    # the number of the current word (instruction address)

        # process command line arguments
        parser = argparse.ArgumentParser(
            description='An assembler for the Hack assembly language.',
            epilog='Hack assembler by Jack Christensen. Project 06 from "The Elements of Computing Systems" by Nisan and Schocken, MIT Press. Also www.nand2tetris.org')
        parser.add_argument('infile', help='Input file, e.g. [/dir/.../]myfile.asm')
        args = parser.parse_args()

        # process the input filename
        inDir, inFilename = os.path.split(args.infile)
        try:
            filename, ext = inFilename.rsplit(sep='.', maxsplit=1)
        except Exception as e:
            print('Error, input file must have .asm extension.', file=sys.stderr)
            sys.exit(1)
        if ext != 'asm':
            print('Error, input file must have .asm extension.', file=sys.stderr)
            sys.exit(2)

        # read the input file into a list
        try:
            with open(args.infile, 'r') as f:
                self.lines = f.readlines()
        except Exception as e:
            print(f'Error reading {args.infile}: {str(e)}', file=sys.stderr)
            sys.exit(3)
        self.nLines = len(self.lines)

        # construct the output filename
        self.outFilename = filename + '.hack'
        if inDir:
            self.outFilename = inDir + os.sep + self.outFilename

    def hasMoreLines(self) -> bool:
        """Are there more commands in the input?"""
        return self.currentLine < self.nLines

    def advance(self) -> None:
        """
        Reads the next line from the input and makes it the current
        instruction. Should be called only if hasMoreLines() is true.
        Initially there is no current instruction.
        """
        self.currentInst = self.lines[self.currentLine]
        print(self.currentLine+1, self.currentWord, self.currentInst, sep='\t', end='')
        self.currentLine += 1
        while self.instructionType() == 'NOT_INST':
            self.currentInst = self.lines[self.currentLine]
            print(self.currentLine+1, self.currentWord, self.currentInst, sep='\t', end='')
            self.currentLine += 1
        if self.instructionType() == 'A_INST' or self.instructionType() == 'C_INST':
            self.currentWord += 1

    def instructionType(self) -> str:
        """Returns the type of the current instruction."""
        # remove all whitespace
        self.currentInst = self.currentInst.strip().replace(' ','')
        self.currentInst = self.currentInst.split('//')[0]
        if len(self.currentInst) == 0:   return 'NOT_INST'
        elif self.currentInst[0] == '@': return 'A_INST'
        elif self.currentInst[0] == '(': return 'L_INST'
        else: return 'C_INST'

    def symbol(self) -> str:
        """
        Returns the symbol or decimal value xxx from
        an A instruction @xxx or the symbol from a label
        pseudo-op (xxx). Should be called only when instructionType()
        is A_INST or L_INST.
        """
        if self.currentInst[0] == '@': return self.currentInst[1:]
        elif self.currentInst[0] == '(': return self.currentInst[1:-1]
        else: return ''

    def reset(self) -> None:
        """Resets the parser for the second pass."""
        self.currentInst = ''   # the current instruction being processed
        self.currentLine = 0    # the number of the current line being processed
        self.currentWord = 0    # the number of the current word (instruction address)

    def dest(self) -> str:
        """Extracts the dest mnemonic from dest=comp;jump"""
        d = self.currentInst.split(sep='=', maxsplit=1)
        if len(d) < 2:
            return 'n/a'
        else:
            return d[0]

    def comp(self) -> str:
        """Extracts the comp mnemonic from dest=comp;jump"""
        c = self.currentInst.split(sep='=', maxsplit=1)
        if len(c) > 1:
            comp = c[1]
        c = self.currentInst.split(sep=';', maxsplit=1)
        if len(c) > 1:
            return c[0]
        else:
            return comp

    def jump(self) -> str:
        """Extracts the jump mnemonic from dest=comp;jump"""
        j = self.currentInst.split(sep=';', maxsplit=1)
        if len(j) < 2:
            return 'n/a'
        else:
            return j[1]
