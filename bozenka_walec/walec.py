#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
import argparse
import struct
import time
import numpy as np
from computations import determine_center_and_radius
from computations import squared_distance2d

AMINOACIDS = set(['GLN', 'GLY', 'GLU', 'ASP', 'SER', 'HSD', 'LYS', 'PRO', 'ASN', 'VAL', 'THR',
             'TRP', 'PHE', 'ALA', 'MET', 'LEU', 'ARG', 'TYR'])
GRO_FORMAT = "5s5s5s5s8s8s8s"
GRO_FORMAT_C = "%5d%-5s%5s%5d%8.3f%8.3f%8.3f"
PATTERN = 'Generated'

# TODO
# najpierw wczytywanie już istniejącego pliku wynikowego, żeby zobaczyć, co zostało policzone, a potem dopisywanie do niego


class DataFrame(object):

    def __init__(self, frame_string):
        super(DataFrame, self).__init__()
        temp = frame_string.strip().split(os.linesep, 2)
        self.first_line = temp[0]
        content, self.last_line = temp[-1].rsplit(os.linesep, 1)

        def process_line(line, line_format=GRO_FORMAT):
            res_num, res_name, atom_name, atom_num, x, y, z = struct.unpack(line_format, line)
            res_num = int(res_num)
            atom_num = int(atom_num)
            res_name = res_name.rstrip()
            atom_name = atom_name.lstrip()
            x = float(x)
            y = float(y)
            z = float(z)
            return res_num, res_name, atom_name, atom_num, x, y, z

        self.lines = [process_line(x) for x in content.split(os.linesep)]

    def process(self, to_contain, solvent, main_in_solvent, skip_hydrogens, xtol, x, y, r):
        if skip_hydrogens:
            protein_atoms = [(line[4], line[5]) for line in self.lines if line[1] in AMINOACIDS and line[2].startswith('H')]
        else:
            protein_atoms = [(line[4], line[5]) for line in self.lines if line[1] in AMINOACIDS]
        x, y, r = determine_center_and_radius(np.array(protein_atoms), xtol, x, y, r)
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
        return output_lines, x, y, r


def write_file(first_line, lines, last_line, outfile):
    def process_line(line, line_format=GRO_FORMAT_C):
        return line_format % line
    with open(outfile, 'a') as f:
        f.write(first_line)
        f.write(os.linesep)
        f.write(str(len(lines)))
        f.write(os.linesep)
        f.write(os.linesep.join(process_line(line) for line in lines))
        f.write(os.linesep)
        f.write(last_line)
        f.write(os.linesep)


def determine_frame_size(file_handle, read_size=10000,\
                         pattern=PATTERN, start=1):
    s = ''
    found = -1
    while found < 0:
        s += file_handle.read(read_size)
        found = s.find(pattern, start)
        read_size = int(read_size*2)
    read_size = found
    return s, read_size


def determine_file_size(file_handle):
    curr_pos = file_handle.tell()
    file_handle.seek(0, os.SEEK_END)
    file_size = file_handle.tell()
    file_handle.seek(curr_pos)
    return file_size


def get_frames(fname, pattern=PATTERN, start=1):
    with open(fname) as f:
        # determine frame size
        s, read_size = determine_frame_size(f, pattern=pattern, start=start)
        # determine file size
        file_size = determine_file_size(f)
        yield s[:read_size].strip()
        s = s[read_size:]
        # main loop
        while f.tell() < file_size - 2: # -2 for /n in unix or /r/n in windows - the characters could be found on the
                                        # end on the file
            t = time.time()
            s += f.read(read_size)
            found = s.find(pattern, start)
            while found < 0 and f.tell() < file_size:
                s += f.read(read_size)
                found = s.find(pattern, start)
            if f.tell() < file_size: # works for every - but the last -frame
                print time.time() - t, "reading"
                yield s[:found].strip()
                s = s[found:]
                found = False
            else:
                yield s




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
    parser.add_argument('-c', '--contain', default='POPC',
                        help='''particles to be contained in the output file without changes.
                        AminoAcids are always rewriten to the output file''')
    parser.add_argument('--xtol', default=1e-8, type=float, help='xtol parameter of the scipy.optimize.least_squares \
                        function used for fitting a circle to the protein atoms. The lower, the more time will it take \
                        to complete the computations.')
    args = parser.parse_args()
    # print len(open(args.i).read())
    # s = open('data/ramki.gros').read()
    # import re
    # found = re.search(FRAME_PATTERN, s, re.DOTALL)
    # print found.end()
    # raise
    t = time.time()
    if os.path.dirname(args.o) and not os.path.exists(os.path.dirname(args.o)):
        os.makedirs(os.path.dirname(args.o))
    open(args.o, 'w').close() # create empty file
    x, y, r = None, None, None # initial values
    for frame in get_frames(args.i):
        print '--------------------------'
        print frame.split(os.linesep, 1)[0]
        print frame.rsplit(os.linesep, 1)[1]
        ti = time.time()
        data = DataFrame(frame)
        print time.time() -ti, "constructing frame object"
        ti = time.time()
        lines, x, y, r = data.process(args.contain, args.solvent, args.main_atom_in_solvent, args.skip_hydrogens,
                                      args.xtol, x, y, r)
        print time.time() -ti, "processing data"
        ti=time.time()
        write_file(data.first_line, lines, data.last_line, args.o)
        print time.time() -ti, "writing data"

    print time.time()-t
    raise

    print args
    import time
    t = time.time()
    data = DataFrame(open(args.i, 'rb').read())
    lines = data.process(args.contain, args.solvent, args.main_atom_in_solvent, set(args.skip), args.skip_hydrogens)
    write_file(data.first_line, lines, data.last_line, args.o)
    print time.time() - t