#Assembler developed for Spring 2025 RISC CPU project by Mohamed Wageh with ChatGPT.
"""
risc_assembler.py – Interactive two-pass assembler for the 32-bit RISC ISA
----------------------------------------------------------------------------
Usage:
  - Interactive mode: prompts for assembly, end with blank line, outputs hex, then asks to continue.
  - Batch mode: python risc_assembler.py source.asm [-o output.hex] [--sym symbols.txt]
Supports labels, comments (; or #), all R-/I-/SB-type instructions, decimal/hex immediates, PC-relative branches.
"""
import sys
import argparse
import re

def r_type_lsb(op, d, s1, s2, f):
    return (f << 21) | (s2 << 16) | (s1 << 11) | (d << 6) | op

def i_type_lsb(op, d, s1, imm16):
    imm16 &= 0xFFFF
    return (imm16 << 16) | (s1 << 11) | (d << 6) | op

def sb_type_lsb(op, s1, s2, imm):
    imm &= 0xFFFF
    imm_u = (imm >> 5) & 0x7FF
    imm_l = imm & 0x1F
    return (imm_u << 21) | (s2 << 16) | (s1 << 11) | (imm_l << 6) | op

# Instruction mapping: mnemonic -> function generating machine word
instr_map = {
    # R-type (op=0)
    'SLL':  lambda d,s1,s2,labels,pc: r_type_lsb(0, d, s1, s2, 0),
    'SRL':  lambda d,s1,s2,labels,pc: r_type_lsb(0, d, s1, s2, 1),
    'SRA':  lambda d,s1,s2,labels,pc: r_type_lsb(0, d, s1, s2, 2),
    'ROR':  lambda d,s1,s2,labels,pc: r_type_lsb(0, d, s1, s2, 3),
    'ADD':  lambda d,s1,s2,labels,pc: r_type_lsb(0, d, s1, s2, 4),
    'SUB':  lambda d,s1,s2,labels,pc: r_type_lsb(0, d, s1, s2, 5),
    'SLT':  lambda d,s1,s2,labels,pc: r_type_lsb(0, d, s1, s2, 6),
    'SLTU': lambda d,s1,s2,labels,pc: r_type_lsb(0, d, s1, s2, 7),
    'SEQ':  lambda d,s1,s2,labels,pc: r_type_lsb(0, d, s1, s2, 8),
    'XOR':  lambda d,s1,s2,labels,pc: r_type_lsb(0, d, s1, s2, 9),
    'OR':   lambda d,s1,s2,labels,pc: r_type_lsb(0, d, s1, s2,10),
    'AND':  lambda d,s1,s2,labels,pc: r_type_lsb(0, d, s1, s2,11),
    'NOR':  lambda d,s1,s2,labels,pc: r_type_lsb(0, d, s1, s2,12),
    'MUL':  lambda d,s1,s2,labels,pc: r_type_lsb(0, d, s1, s2,13),
    # I-type (op=1..16)
    'SLLI': lambda d,s1,imm,labels,pc: i_type_lsb(1,  d, s1, int(imm,0)),
    'SRLI': lambda d,s1,imm,labels,pc: i_type_lsb(2,  d, s1, int(imm,0)),
    'SRAI': lambda d,s1,imm,labels,pc: i_type_lsb(3,  d, s1, int(imm,0)),
    'RORI': lambda d,s1,imm,labels,pc: i_type_lsb(4,  d, s1, int(imm,0)),
    'ADDI': lambda d,s1,imm,labels,pc: i_type_lsb(5,  d, s1, int(imm,0)),
    'SLTI': lambda d,s1,imm,labels,pc: i_type_lsb(6,  d, s1, int(imm,0)),
    'SLTIU':lambda d,s1,imm,labels,pc: i_type_lsb(7,  d, s1, int(imm,0)),
    'SEQI': lambda d,s1,imm,labels,pc: i_type_lsb(8,  d, s1, int(imm,0)),
    'XORI': lambda d,s1,imm,labels,pc: i_type_lsb(9,  d, s1, int(imm,0)),
    'ORI':  lambda d,s1,imm,labels,pc: i_type_lsb(10, d, s1, int(imm,0)),
    'ANDI': lambda d,s1,imm,labels,pc: i_type_lsb(11, d, s1, int(imm,0)),
    'NORI': lambda d,s1,imm,labels,pc: i_type_lsb(12, d, s1, int(imm,0)),
    'SET':  lambda d,_,imm,labels,pc: i_type_lsb(13, d, 0, int(imm,0)),
    'SSET': lambda d,_,imm,labels,pc: i_type_lsb(14, d, 0, int(imm,0)),
    'JALR': lambda d,s1,imm,labels,pc: i_type_lsb(15, d, s1, (labels[imm]) if imm in labels else int(imm,0)),
    'LW':   lambda d,s1,imm,labels,pc: i_type_lsb(16, d, s1, int(imm,0)),
    # SB-type (op=17..23)
    'SW':   lambda s1,s2,imm,labels,pc: sb_type_lsb(17, s1, s2, int(imm,0)),
    'BEQ':  lambda s1,s2,off,labels,pc: sb_type_lsb(18, s1, s2, (labels[off] - (pc)) if off in labels else int(off,0)),
    'BNE':  lambda s1,s2,off,labels,pc: sb_type_lsb(19, s1, s2, (labels[off] - (pc)) if off in labels else int(off,0)),
    'BLT':  lambda s1,s2,off,labels,pc: sb_type_lsb(20, s1, s2, (labels[off] - (pc)) if off in labels else int(off,0)),
    'BGE':  lambda s1,s2,off,labels,pc: sb_type_lsb(21, s1, s2, (labels[off] - (pc)) if off in labels else int(off,0)),
    'BLTU': lambda s1,s2,off,labels,pc: sb_type_lsb(22, s1, s2, (labels[off] - (pc)) if off in labels else int(off,0)),
    'BGEU': lambda s1,s2,off,labels,pc: sb_type_lsb(23, s1, s2, (labels[off] - (pc)) if off in labels else int(off,0)),
}

REG_RE = re.compile(r"R([0-9]|[12][0-9]|3[01])$")
def reg_num(tok):
    tok = tok.upper()
    if not REG_RE.match(tok): raise ValueError(f"Invalid register '{tok}'")
    return int(tok[1:])

def assemble(lines):
    # First pass: label addresses
    labels = {}
    pc = 0
    for l in lines:
        text = l.split(';')[0].split('#')[0].strip()
        if not text: continue
        if text.endswith(':'):
            lbl = text[:-1]
            labels[lbl] = pc
        else:
            pc += 1
    # Second pass: encode instructions
    machine = []
    pc = 0
    for l in lines:
        text = l.split(';')[0].split('#')[0].strip()
        if not text or text.endswith(':'): continue
        parts = text.replace(',', ' ').split()
        mnem = parts[0].upper()
        args = parts[1:]
        func = instr_map.get(mnem)
        if not func:
            print(f"Error: unknown mnemonic '{mnem}'")
            sys.exit(1)
        # dispatch based on arg count
        try:
            if mnem == 'SW':
                if re.match(r'-?\d+\(R[0-9]+\)', args[1]):
                        s2 = reg_num(args[0])  # value to store
                        offset, base = re.match(r'(-?\d+)\((R[0-9]+)\)', args[1]).groups()
                        s1 = reg_num(base)     # base address
                        imm = offset
                else:
                        s1 = reg_num(args[0])
                        s2 = reg_num(args[1])
                        imm = args[2]
                code = func(s1, s2, imm, labels, pc)
            elif mnem in ['BEQ','BNE','BLT','BGE','BLTU','BGEU']:
                s1 = reg_num(args[0]); s2 = reg_num(args[1]); off = args[2]
                code = func(s1, s2, off, labels, pc)
            elif mnem == 'LW':
                d = reg_num(args[0])
                if re.match(r'-?\d+\(R[0-9]+\)', args[1]):
                    offset, base = re.match(r'(-?\d+)\((R[0-9]+)\)', args[1]).groups()
                    s1 = reg_num(base)
                    imm = offset
                else:
                    s1 = reg_num(args[1])
                    imm = args[2]
                code = func(d, s1, imm, labels, pc)
            elif mnem in ['JALR', 'SET', 'SSET']:
                d = reg_num(args[0])
                s1 = reg_num(args[1]) if len(args) > 1 and args[1].startswith('R') else 0
                imm = args[-1]
                code = func(d, s1, imm, labels, pc)
            elif mnem in ['SLLI','SRLI','SRAI','RORI','ADDI','SLTI','SLTIU','SEQI','XORI','ORI','ANDI','NORI']:
                d = reg_num(args[0]); s1 = reg_num(args[1]); imm = args[2]
                code = func(d, s1, imm, labels, pc)
            else:
                # R-type all others
                d = reg_num(args[0]); s1 = reg_num(args[1]); s2 = reg_num(args[2])
                code = func(d, s1, s2, labels, pc)
        except Exception as e:
            print(f"Error encoding line {pc}: '{l.strip()}' → {e}")
            sys.exit(1)
        machine.append(code)
        pc += 1
    return machine, labels


def format_output(machine):
    hexes = [f"{w:08X}" for w in machine]
    return ['v2.0 raw'] + [ ' '.join(hexes[i:i+8]) for i in range(0, len(hexes), 8) ]


def run_interactive():
    while True:
        print("\nEnter assembly code (end with blank line):")
        lines = []
        while True:
            try:
                l = input()
            except EOFError:
                l = ''
                print()
            if not l.strip():
                break
            lines.append(l)
        if lines:
            machine, labels = assemble(lines)
            for out in format_output(machine): print(out)
        else:
            print("No input provided.")
        again = input("\nAssemble another program? (Y/N): ").strip().lower()
        if again and again.startswith('n'):
            break


def main():
    parser = argparse.ArgumentParser(description="Two-pass assembler for 32-bit RISC ISA.")
    parser.add_argument("input", nargs="?", help="Input assembly file")
    parser.add_argument("-o", "--output", help="Output file (default: stdout)")
    parser.add_argument("--sym", help="Output symbol table to file")
    args = parser.parse_args()

    if not args.input:
        run_interactive()
    else:
        try:
            with open(args.input, 'r') as f:
                lines = f.readlines()
        except FileNotFoundError:
            print(f"Error: File '{args.input}' not found.")
            sys.exit(1)

        machine, labels = assemble(lines)
        out_lines = format_output(machine)

        if args.output:
            with open(args.output, 'w') as f:
                f.write('\n'.join(out_lines) + '\n')
        else:
            for line in out_lines:
                print(line)

        if args.sym:
            with open(args.sym, 'w') as f:
                for label, addr in labels.items():
                    f.write(f"{label}: {addr}\n")


if __name__ == "__main__":
    main()
