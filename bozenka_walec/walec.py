#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
import argparse
import struct
import numpy as np
from computations import determine_center_and_radius
from computations import squared_distance2d

AMINOACIDS = set(['GLN', 'GLY', 'GLU', 'ASP', 'SER', 'HSD', 'LYS', 'PRO', 'ASN', 'VAL', 'THR',
             'TRP', 'PHE', 'ALA', 'MET', 'LEU', 'ARG', 'TYR'])
GRO_FORMAT = "5s5s5s5s8s8s8s"
GRO_FORMAT_C = "%5d%-5s%5s%5d%8.3f%8.3f%8.3f"

class DatFrame(object):

    def __init__(self, frame_string):
        super(DatFrame, self).__init__()
        temp = frame_string.strip().split(os.linesep, 2)
        self.first_two_lines = temp[:2]
        content, self.last_line = temp[-1].rsplit(os.linesep, 1)

        def process_line(line, line_format=GRO_FORMAT):
            res_num, res_name, atom_name, atom_num, x, y, z = struct.unpack(line_format, line)
            x, y, z = map(float, (x, y, z))
            res_num, atom_num = map(int, (res_num, atom_num))
            res_name, atom_name = map(str.strip, (res_name, atom_name))
            return res_num, res_name, atom_name, atom_num, x, y, z

        self.lines = [process_line(x) for x in content.split(os.linesep)]

    def process(self, to_contain, solvent, main_in_solvent, to_skip, skip_hydrogens): #todo remove skip
        if skip_hydrogens:
            protein_atoms = [(line[4], line[5]) for line in self.lines if line[1] in AMINOACIDS and line[2].startswith('H')]
        else:
            protein_atoms = [(line[4], line[5]) for line in self.lines if line[1] in AMINOACIDS]
        x, y, r = determine_center_and_radius(np.array(protein_atoms))
        center = (x, y)
        sqared_r = r**2
        output_lines = []
        control = False
        for line in self.lines:
            if line[1] == to_contain or line[1] in AMINOACIDS:
                output_lines.append(line)
            elif line[1] == solvent :
                if line[2] == main_in_solvent:
                    if squared_distance2d(center, (line[4], line[5])) <= sqared_r:
                        output_lines.append(line)
                        control = True
                    else:
                        control = False
                elif control:
                    output_lines.append(line)
        return output_lines


def write_file(first_two_lines, lines, last_line, outfile):
    def process_line(line, line_format=GRO_FORMAT_C):
        return line_format % line
    with open(outfile, 'a') as f:
        f.write(os.linesep.join(first_two_lines))
        f.write(os.linesep)
        f.write(os.linesep.join(process_line(line, GRO_FORMAT) for line in lines))
        f.write(os.linesep)
        f.write(last_line)


if __name__ == '__main__':
    # todo opcja z obejrzeniem nanodysku
    parser = argparse.ArgumentParser(description='todo') # todo
    parser.add_argument('-i', help='input file')
    parser.add_argument('-o', help='output file')
    parser.add_argument('-s', '--solvent', default='TIP3', help='solvent')
    parser.add_argument('-m', '--main_atom_in_solvent', default='OH2',
                        help="coordinates of this atom are used as particle's coordinates")
    parser.add_argument('--skip_hydrogens', default=False, action='store_true',
                        help='whether to use hydrogens to determine the midddle of the circle and its radius')
    parser.add_argument('-k', '--skip', action='append', help='particles to skip')
    parser.add_argument('-c', '--contain', default='POPC',
                        help='''particles to be contained in the output file without changes.
                        AminoAcids are always rewriten to the output file''')
    args = parser.parse_args()
    if not os.path.exists(os.path.dirname(args.o)):
        os.makedirs(os.path.dirname(args.o))
    open(args.o, 'w').close() # create empty file
    print args
    import time
    t = time.time()
    data = DatFrame(open(args.i, 'rb').read())
    lines = data.process(args.contain, args.solvent, args.main_atom_in_solvent, set(args.skip), args.skip_hydrogens)
    write_file(data.first_two_lines, lines, data.last_line, args.o)
    print time.time() - t