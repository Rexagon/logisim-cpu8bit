import sys
import re

class AsmSyntaxParseError (RuntimeError):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Token:
    def __init__(self, value):
        self.value = value

    def getValue(self):
        return self.value


class Label (Token):
    __labels = {}

    def __init__(self, name):
        self.name = str(name)

    @staticmethod
    def registerLabel(name, value):
        Label.__labels[name] = value

    def getValue(self):
        try:
            return Label.__labels[self.name]
        except KeyError:
            raise AsmSyntaxParseError('Undefined label "' + self.name + '"')

def packArguments(operation, lhs=0, rhs=0, im=None):
    bytes = []

    bytes.append(Token(
        ((int(operation) << 4) | 
        ((int(lhs) & 0b11) << 2) | 
        ((int(rhs) & 0b11) << 0)) & 0xff))

    if im:
        if re.match(r'0x[0-9a-f]{2}', im, flags=re.I):
            bytes.append(Token(int(im, 0) & 0xff))
        else:
            bytes.append(Label(im))

    return bytes


def assemble(asm):
    asm = re.sub(r'[ ]*([;#].*)?$', '', asm, flags=re.M) # remove comments
    asm = re.sub(r':', ':\n', asm, flags=re.M) # move labels to new lines
    asm = re.sub(r'^\s+', '', asm, flags=re.M) # remove blank lines ans useless spaces

    lines = asm.split('\n')

    tokens = []

    operations = [
        (r'and\s*r([0-3])\s*,\s*r([0-3])', lambda r: packArguments(0x0, r[0], r[1])),
        (r'or\s*r([0-3])\s*,\s*r([0-3])',  lambda r: packArguments(0x1, r[0], r[1])),
        (r'add\s*r([0-3])\s*,\s*r([0-3])', lambda r: packArguments(0x2, r[0], r[1])),
        (r'sub\s*r([0-3])\s*,\s*r([0-3])', lambda r: packArguments(0x3, r[0], r[1])),

        (r'lw\s*r([0-3])\s*,\s*\(r\s*([0-3])\s*\)', lambda r: packArguments(0x4, r[0], r[1])),
        (r'sw\s*r([0-3])\s*,\s*\(r\s*([0-3])\s*\)', lambda r: packArguments(0x5, r[0], r[1])),

        (r'mov\s*r([0-3])\s*,\s*r([0-3])', lambda r: packArguments(0x6, r[0], r[1])),

        (r'inp\s*r([0-3])\s*', lambda r: packArguments(0x7, r[0])),

        (r'jeq\s*r([0-3])\s*,\s*(0x[0-9a-f]{2}|[a-z]+)', lambda r: packArguments(0x8, r[0], im=r[1])),
        (r'jne\s*r([0-3])\s*,\s*(0x[0-9a-f]{2}|[a-z]+)', lambda r: packArguments(0x9, r[0], im=r[1])),
        (r'jgt\s*r([0-3])\s*,\s*(0x[0-9a-f]{2}|[a-z]+)', lambda r: packArguments(0xa, r[0], im=r[1])),
        (r'jlt\s*r([0-3])\s*,\s*(0x[0-9a-f]{2}|[a-z]+)', lambda r: packArguments(0xb, r[0], im=r[1])),

        (r'lw\s*r([0-3])\s*,\s*(0x[0-9a-f]{2}|[a-z]+)', lambda r: packArguments(0xc, r[0], im=r[1])),
        (r'sw\s*r([0-3])\s*,\s*(0x[0-9a-f]{2}|[a-z]+)', lambda r: packArguments(0xd, r[0], im=r[1])),
        (r'li\s*r([0-3])\s*,\s*(0x[0-9a-f]{2}|[a-z]+)', lambda r: packArguments(0xe, r[0], im=r[1])),

        (r'jmp\s*(0x[0-9a-f]{2}|[a-z]+)', lambda r: packArguments(0xf, im=r[0]))
    ]

    for line in lines:
        found = False

        for pattern, action in operations:
            r = re.match(pattern, line, flags=re.I)
            if r:
                tokens.extend(action(r.groups()))
                found = True
                break

        if not found:
            r = re.match(r'([a-z]+):', line, flags=re.I)
            if r:
                Label.registerLabel(r.groups()[0], len(tokens))
                found = True

        if not found:
            raise AsmSyntaxParseError('Unknown syntax "' + line + '"')

    return tokens


def main(args):
    if len(args) > 1:
        filename = str(args[1])

        try:
            with open(filename, 'r') as inputFile:
                tokens = assemble(inputFile.read())

                asm = " ".join(map(lambda t: format(t.getValue(), '02x'), tokens))
                print('Result [' + str(len(tokens)) + ' bytes]:')
                print(asm)

                if len(args) > 2:
                    resultFilename = str(args[2])
                    with open(resultFilename, "w") as outputFile:
                        outputFile.write('v2.0 raw\n' + asm)
                        print('\nSaved result to file "' + resultFilename + '"')

        except IOError,e:
            print('Error: Unable to open file "' + filename + '"')
        except AsmSyntaxParseError,e:
            print('Error: ' + e.value)


if __name__ == '__main__':
    main(sys.argv)
