#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import argparse
import multiprocessing
import math
import numpy as np

import common
import plot
from walec import get_frames, DataFrame, process_frame_string, write_file, get_protein_atoms, \
    determine_center_and_radius


def main(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(description=common.package_description)
    parser.add_argument('-f', '--figure', action='store_true', help='plots circle fitted to all protein atoms in \
    the first frame')
    parser.add_argument('-i', required=True, help='input file')
    parser.add_argument('-o', required=True, help='output file')
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
    parser.add_argument('-p', '--processes', default=0, type=int, help="Number of additional cores used for \
                            computations. Values >=2 and <=num_of_available_cores are reasonable")
    args = parser.parse_args(args)

    if os.path.dirname(args.o) and not os.path.exists(os.path.dirname(args.o)):
        os.makedirs(os.path.dirname(args.o))

    if args.figure:
        first_frame_txt = next(get_frames(args.i))
        data = DataFrame(first_frame_txt)
        protein_atoms = np.array(get_protein_atoms(data.lines, False))
        # determine initial circle parameters
        initialx = np.mean(protein_atoms[:, 0])
        initialy = np.mean(protein_atoms[:, 1])
        initial_radius = (math.fabs(initialx) + math.fabs(initialy) - np.min(protein_atoms[:, 0]) - np.min(protein_atoms[:, 1])) / 2
        x, y, r = determine_center_and_radius(np.array(protein_atoms), args.xtol, initialx, initialy, initial_radius)
        outfile = plot.plot(protein_atoms, initialx, initialy, initial_radius, x, y, r, args.o)
    else:
        print "Num of cores:", 1 + args.processes
        if os.path.dirname(args.o) and not os.path.exists(os.path.dirname(args.o)):
            os.makedirs(os.path.dirname(args.o))
        open(args.o, 'w').close()  # create empty file
        x, y, r = None, None, None  # initial values

        if args.processes:
            assert args.processes > 0  # I wonder, what happens when an user run the program with -p -2 argument...
            pool = multiprocessing.Pool(processes=args.processes)
            iterator = get_frames(args.i)
            n = True
            while n:
                map_args = []
                for x in range(args.processes):
                    n = next(iterator, False)
                    if n:
                        map_args.append((n, x, y, r, args.contain, args.solvent, args.main_atom_in_solvent,
                                         args.skip_hydrogens, args.xtol))
                for data, lines, x, y, r in pool.map(process_frame_string, map_args):
                    write_file(data.first_line, lines, data.last_line, args.o)

            pool.close()
            pool.join()
        else:
            for frame in get_frames(args.i):
                data = DataFrame(frame)
                lines, x, y, r = data.process(args.contain, args.solvent, args.main_atom_in_solvent, args.skip_hydrogens,
                                              args.xtol, x, y, r)
                write_file(data.first_line, lines, data.last_line, args.o)
        outfile = args.o
    print "Result written to", outfile

if __name__ == '__main__':
    main()
