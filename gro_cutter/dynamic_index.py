#! /usr/bin/python
# -*- coding: utf-8 -*-

import subprocess
import sys
import os
import argparse
import tempfile
import shutil
from walec import get_frames

make_ndx = 'make_ndx -f %s -o %s'
density = 'g_density -f %s -s %s -n %s -o %s -ng 2'

def main(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(description='blah') # TODO meaningful description
    parser.add_argument('-i', required=True, help="input file")
    parser.add_argument('-o', required=True, help="output file")
    parser.add_argument('-t', required=True, help='.tpr file')
    args = parser.parse_args(args)
    temp_dir = tempfile.mkdtemp()
    for i, frame in enumerate(get_frames(args.i)):
        name = os.path.basename(args.i)
        base, extension = name.split('.')
        temp_name = os.path.join(os.path.join(temp_dir, base+'_'+str(i)+'.'+extension))
        index_name = os.path.join(os.path.join(temp_dir, base+'_'+str(i)+'.ndx'))
        out_part_name = os.path.join(os.path.join(temp_dir, base+'_'+str(i)+'.xvg'))
        open(temp_name, 'w').write(frame)
        p = subprocess.Popen(make_ndx%(temp_name, index_name), stdin=subprocess.PIPE, shell=True)
        p.stdin.write("13 & a P O12 O13 O14\n")
        p.stdin.write("q\n")
        p.wait()
        #print density%(temp_name, index_name, out_part_name)
        p = subprocess.Popen(density%(temp_name, args.t, index_name, out_part_name), stdin=subprocess.PIPE, shell=True)
        p.stdin.write("17\n")
        p.stdin.write("14\n")
        p.wait()
        os.remove(temp_name)
        os.remove(index_name)
    shutil.rmtree(temp_dir)

if __name__ == '__main__':
    main(sys.argv[1:])
