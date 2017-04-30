#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import argparse
import multiprocessing
import common
from walec import get_frames, DataFrame, process_frame_string, write_file


def main(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(description=common.package_description)
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

if __name__ == '__main__':
# todo opcja z obejrzeniem nanodysku
    main()
