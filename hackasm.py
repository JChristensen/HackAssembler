#!/usr/bin/python3
# J.Christensen 23Jul2022
# Hack assembler.

import HackSymtab
import HackParser
import HackCode
import sys

def main() -> None:
    """
    Hack assembler by Jack Christensen Jul-2022.
    Project 06 from "The Elements of Computing Systems"
    by Nisan and Schocken, MIT Press. Also www.nand2tetris.org
    """

    parser = HackParser.HackParser()
    symtab = HackSymtab.HackSymtab()
    hackcode = HackCode.HackCode()

    # first pass: add label declarations to the symbol table
    print('---- PASS 1 ----')
    while parser.hasMoreLines():
        parser.advance()
        if parser.instructionType() == 'L_INST':
            sym = parser.symbol()
            if symtab.contains(sym):
                print(f'\nError at line {parser.currentLine}: {sym} was previously defined.')
                print('**** ASSEMBLY TERMINATED ****')
                sys.exit(1)
            else:
                symtab.addEntry(sym, parser.currentWord)

    # second pass: handle variables, assemble a and c instructions
    parser.reset()
    words = []          # holds the assembled instructions
    varAddr = 16        # memory address for the next variable
    print('\n---- PASS 2 ----')
    while parser.hasMoreLines():
        parser.advance()
        if parser.instructionType() == 'A_INST':
            sym = parser.symbol()
            if sym.isnumeric():
                words.append(format(int(sym), '016b') + '\n')
            elif symtab.contains(sym):
                words.append(format(symtab.getAddress(sym), '016b') + '\n')
            else:
                symtab.addEntry(sym, varAddr)
                words.append(format(symtab.getAddress(sym), '016b') + '\n')
                varAddr += 1

        elif parser.instructionType() == 'C_INST':
            words.append('111'
                   + hackcode.comp(parser.comp())
                   + hackcode.dest(parser.dest())
                   + hackcode.jump(parser.jump()) + '\n')

    # write the output file
    outFilename = parser.outFilename
    with open(outFilename, 'w') as f:
        f.writelines(words)

    # all done
    print('\n---- SYMBOL TABLE ----')
    print(symtab.symtab)
    print(f'\n**** ASSEMBLY COMPLETE, wrote {len(words)} words to {outFilename} ****', file=sys.stderr)

if __name__ == '__main__':
    main()
