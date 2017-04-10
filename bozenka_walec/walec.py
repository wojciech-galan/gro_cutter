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
            return res_num, res_name, atom_name, atom_num, x, y, z

        self.lines = [process_line(x) for x in content.split(os.linesep)]

    def process(self):
        points = []
        for line in self.lines:
            if line[0][-3:] in AMINOACIDS:
                points.append((line[3], line[4]))
        determine_center_and_radius(np.array(points))



def process_frame(frame_string):
    temp = frame_string.strip().split(os.linesep, 2)
    first_two_lines = temp[:2]
    last_line = temp[-1].rsplit(os.linesep, 1)[1]
    print first_two_lines
    print last_line
    print [temp[2][:30]]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='todo') # todo
    parser.add_argument('-i', help='input file')
    parser.add_argument('-o', help='output file')
    parser.add_argument('-s', '--solvent', default='TIP3', help='solvent')
    parser.add_argument('-k', '--skip', action='append', help='particles to skip')
    parser.add_argument('-c', '--contain', default='POPC',
                        help='particles to be contained in the output file without changes. '
                             'AminoAcis are always contained')
    args = parser.parse_args()
    print args

    if not os.path.exists(os.path.dirname(args.o)):
        os.makedirs(os.path.dirname(args.o))
    data = DatFrame(open(args.i, 'rb').read())
    data.process()
    #process_frame(open(args.i).read())

    # cont = []
    # for line in open('data/ramka.gro').readlines()[2:-1]:
    #     cont.append(line.split(None, 1)[0].translate(None, digits))
    # print set(cont)