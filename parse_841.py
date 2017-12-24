#------------------------------------------------------------------------------
# pycparser: parse_841.py
#
# Generates the necessary FOL statements from parsing the provided file.
#
# Eli Bendersky [http://eli.thegreenplace.net]
# License: BSD
#------------------------------------------------------------------------------
from __future__ import print_function
import sys

# This is not required if you've installed pycparser into
# your site-packages/ with setup.py
#
sys.path.extend(['.', '..'])

from pycparser import parse_file_841, c_parser


def generate_statements(filename):
    """ Let's do some stuff.
    """
    outstuff = parse_file_841(filename, use_cpp=True)
    output = []
    for command, stuff in outstuff:
        output.append("{}({})".format(command, 's'+',s'.join([str(x) for x in stuff])))
    return output

#------------------------------------------------------------------------------
if __name__ == "__main__":
    if len(sys.argv) > 2:
        f = open(sys.argv[2],'w')
        f.write('\n'.join(generate_statements(sys.argv[1]))+'\n')
        f.close()
        print("FOL statments have been printed to", sys.argv[2])
    else:
        print("Please provide a infile and outfile as arguments")
