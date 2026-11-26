"""Hack assembler (Nand to Tetris) - two-pass.
Usage: python assembler.py Prog.asm   -> writes Prog.hack
Extra feature (K=47, K mod 3 = 2): warn if the same label is defined twice.
"""
import sys

COMP = {
    '0': '0101010', '1': '0111111', '-1': '0111010',
    'D': '0001100', 'A': '0110000', '!D': '0001101', '!A': '0110001',
    '-D': '0001111', '-A': '0110011', 'D+1': '0011111', 'A+1': '0110111',
    'D-1': '0001110', 'A-1': '0110010', 'D+A': '0000010', 'D-A': '0010011',
    'A-D': '0000111', 'D&A': '0000000', 'D|A': '0010101',
    'M': '1110000', '!M': '1110001', '-M': '1110011', 'M+1': '1110111',
    'M-1': '1110010', 'D+M': '1000010', 'D-M': '1010011', 'M-D': '1000111',
    'D&M': '1000000', 'D|M': '1010101',
}
JUMP = {'': '000', 'JGT': '001', 'JEQ': '010', 'JGE': '011',
        'JLT': '100', 'JNE': '101', 'JLE': '110', 'JMP': '111'}

SYMBOLS = {'SP': 0, 'LCL': 1, 'ARG': 2, 'THIS': 3, 'THAT': 4,
           'SCREEN': 16384, 'KBD': 24576}
for i in range(16):
    SYMBOLS['R%d' % i] = i


def clean(line):
    """Remove comments and all whitespace."""
    return line.split('//')[0].replace(' ', '').replace('\t', '').strip()


def comp_bits(c):
    if c in COMP:
        return COMP[c]
    # Strict like the official assembler: M+D is invalid, only D+M is allowed.
    raise ValueError('invalid comp field "%s"' % c)


def assemble(path):
    with open(path) as f:
        raw = f.readlines()

    # ---------- First pass: remove junk, record labels ----------
    symbols = dict(SYMBOLS)
    seen_labels = set()
    lines = []                    # (original line number, instruction)
    for num, text in enumerate(raw, 1):
        line = clean(text)
        if not line:
            continue
        if line.startswith('('):
            label = line[1:-1]
            if label in seen_labels:                       # extra feature
                print('Warning: Line %d: label (%s) is defined more than once'
                      % (num, label))
            seen_labels.add(label)
            symbols[label] = len(lines)   # address of next real instruction
        else:
            lines.append((num, line))

    # ---------- Second pass: translate ----------
    out = []
    next_var = 16
    for num, line in lines:
        try:
            if line.startswith('@'):
                s = line[1:]
                if s.isdigit():
                    val = int(s)
                else:
                    if s not in symbols:
                        symbols[s] = next_var
                        next_var += 1
                    val = symbols[s]
                out.append(format(val, '016b'))
            else:
                dest, jump = '', ''
                if '=' in line:
                    dest, line = line.split('=')
                if ';' in line:
                    line, jump = line.split(';')
                d = ('1' if 'A' in dest else '0') + \
                    ('1' if 'D' in dest else '0') + \
                    ('1' if 'M' in dest else '0')
                out.append('111' + comp_bits(line) + d + JUMP[jump])
        except (ValueError, KeyError) as e:
            print('Line %d: invalid instruction (%s)' % (num, e))
    return out


if __name__ == '__main__':
    src = sys.argv[1]
    result = assemble(src)
    dst = src.rsplit('.', 1)[0] + '.hack'
    with open(dst, 'w') as f:
        f.write('\n'.join(result) + '\n')
    print('Wrote %s (%d instructions)' % (dst, len(result)))
