.. -*- mode: rst -*-
gro_cutter
====
Cuts .gro files with molecular dynamics of a nanodisks. In each simulation frame fits a circle to the nanodisk
boundaries (protein atoms). Then rewrites the file keeping solvent particles lying below and above the nanodisk and
discards the particles lying outside the nanodisk boundaries. Nanodisk in each simulation timestamp should lie in a
vertical plane. Could be run in multiprocessing mode. Compatible with GROMACS 2019.

Installation
------------

Dependencies
~~~~~~~~~~~~

gro_cutter requires:

- Tkinter
- Python >= 2.7
- SciPy >= 0.18.1
- Matplotlib >= 1.5


User installation
~~~~~~~~~~~~~~~~~

If you already have a working installation of scipy, the easiest way to install gro_cutter is using ``pip`` ::

    pip install -U git+https://github.com/wojciech-galan/gro_cutter.git


Source code
-----------

You can check the latest sources with the command::

    git clone https://github.com/wojciech-galan/gro_cutter


Usage
-----

Simplest usage:

    gro_cutter -i input_file -o output_file -s solvent_particle -c lipid_particle

Solvent particle defaults to TIP3 and lipid to POP3.

Nanodisk contains many types of lipids?

    gro_cutter -i input_file -o output_file -s solvent_particle -c lipid_particle1 lipid_particle2 lipid_particle3

Multiprocessing mode (you supply the number of additional processes, meaningfull values are >=2):

    gro_cutter -i input_file -o output_file -s solvent_particle -c lipid_particle -p 4

Wish to change the main atom in solvent, which is used to determine the solvent particles' coordinates?

    gro_cutter -i input_file -o output_file -s solvent_particle -c lipid_particle -m main_atom_in_solvent

You can shrink the circle to contain only lipid particles (shrinking the radius to the distance between center of the circle and the closest protein atom):

    gro_cutter -i input_file -o output_file -s solvent_particle -c lipid_particle --shrink

Program runs too slow? You can run it in multiprocessing mode or skip hydrogens in protein particles while determining
nanodisk boundaries:

    gro_cutter -i input_file -o output_file -s solvent_particle -c lipid_particle --skip_hydrogens

you can also fit a circle to the data less precisely, increasing xtol value (default 1e-8):

    gro_cutter -i input_file -o output_file -s solvent_particle -c lipid_particle --xtol 1e-6

When you change the value it is recommended to confirm that the circle is properly fitted to the data. Run it with -f
option and look at the output file:

    gro_cutter -i input_file -o output_file.jpg -s solvent_particle -c lipid_particle --xtol 1e-6 -f


Platform compatibility
--------
gro_cutter was written and optimized under python2.7 and then ported to python3.5. Please let me know if you experience any problems under python3.

Citation
--------

# TODO

Questions/comments?
-------------------

Contact me via e-mail  wojciech.galan at gmail.com
