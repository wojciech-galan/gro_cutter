#! /usr/bin/python
# -*- coding: utf-8 -*-

# jony wywalić, woda to tip3
# NANODYSK W PŁASZCZYŹNIE xy

import math
from string import digits



cont = []
for line in open('data/ramka.gro').readlines()[2:-1]:
    cont.append(line.split(None, 1)[0].translate(None, digits))
print cont[0], cont[-1]