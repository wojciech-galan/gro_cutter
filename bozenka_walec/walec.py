#! /usr/bin/python
# -*- coding: utf-8 -*-

# jony wywalić, woda to tip3
# NANODYSK W PŁASZCZYŹNIE xy

import math
import os
import argparse
import struct
import numpy as np
from string import digits
from computations import determine_center_and_radius
from computations import distance2d, squared_distance2d
#            set(['POPC', 'GLN', 'TIP3', 'GLY', 'GLU', 'ASP', 'SER', 'HSD', 'LYS', 'PRO', 'ASN', 'VAL', 'THR', 'CLA',
#            'TRP', 'SOD', 'PHE', 'ALA', 'MET', 'LEU', 'ARG', 'TYR'])
AMINOACIDS = set(['GLN', 'GLY', 'GLU', 'ASP', 'SER', 'HSD', 'LYS', 'PRO', 'ASN', 'VAL', 'THR',
             'TRP', 'PHE', 'ALA', 'MET', 'LEU', 'ARG', 'TYR'])
# POPC TIP3 CLA SOD
GRO_FORMAT = "5s5s5s5s8s8s8s"

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

    def process(self, to_contain, solvent, main_in_solvent, to_skip, skip_hydrogens=False, simple_distance=False):
        if skip_hydrogens:
            protein_atoms = [(line[4], line[5]) for line in self.lines if line[1] in AMINOACIDS and line[2].startswith('H')]
        else:
            protein_atoms = [(line[4], line[5]) for line in self.lines if line[1] in AMINOACIDS]
        x, y, r = determine_center_and_radius(np.array(protein_atoms))
        output_lines = []
        for line in self.lines():
            if line[1] == to_contain or line[1] in AMINOACIDS:
                output_lines.append(line)
            elif line[1] == solvent:
                # zrobić słownik funkcji dystansowych może... {squared:cośtam, not_squared:cośtam innego
            # a potem distance = słownik[squared]
            elif line[1] == to_skip:
                pass
            else:
                import pdb
                pdb.set_trace()
                print 'sth went wronq'
                raise



def process_frame(frame_string):
    temp = frame_string.strip().split(os.linesep, 2)
    first_two_lines = temp[:2]
    last_line = temp[-1].rsplit(os.linesep, 1)[1]
    print first_two_lines
    print last_line
    print [temp[2][:30]]


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
    parser.add_argument('-d', '--simple_distance', default=False, action='store_true',
                        help='default distance is square, but you cau use the non-squared one')
    parser.add_argument('-k', '--skip', action='append', help='particles to skip')
    parser.add_argument('-c', '--contain', default='POPC',
                        help='''particles to be contained in the output file without changes.
                        AminoAcids are always contained''')
    args = parser.parse_args()
    print args

    if not os.path.exists(os.path.dirname(args.o)):
        os.makedirs(os.path.dirname(args.o))
    data = DatFrame(open(args.i, 'rb').read())
    data.process(args.c, args.skip_hydrogens, args.simple_distance)
    #process_frame(open(args.i).read())

    # cont = []
    # for line in open('data/ramka.gro').readlines()[2:-1]:
    #     cont.append(line.split(None, 1)[0].translate(None, digits))
    # print set(cont)