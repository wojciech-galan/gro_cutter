#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
import warnings
from matplotlib import pyplot as plt
from matplotlib.backend_bases import FigureCanvasBase


def plot(points, initialx, initialy, initial_radius, x, y, radius, outpath):
    """
    Plots nanodisk boundaries before and after fitting a circle to the boundaries
    :param points: boundaries (protein) atoms
    :param initialx: guessed x coordinate of the middle of the circle
    :param initialy: guessed y coordinate of the middle of the circle
    :param initial_radius: guessed radius of the circle
    :param x: final coordinate of the middle of the circle
    :param y: final coordinate of the middle of the circle
    :param radius: final radius of the circle
    :param outpath: output path
    :return:
    """
    circle = plt.Circle((x, y), radius, fill=False, edgecolor='r', label='after optimization')
    circle2 = plt.Circle((initialx, initialy), initial_radius, fill=False, edgecolor='c', label='before optimization')
    fig, ax = plt.subplots()
    plt.axis([0, 16, 0, 16])
    ax.add_artist(circle)
    ax.add_artist(circle2)
    orig = plt.scatter(points[:,0], points[:,1], c='y', s=4, label='original data')
    ax.legend(handles=[circle, circle2, orig])
    splited_name = os.path.basename(outpath).split('.')
    if len(splited_name)>1 and splited_name[-1] not in FigureCanvasBase.get_supported_filetypes():
        basename = '.'.join(splited_name[:-1])+'.jpg'
        outpath = os.path.join(os.path.dirname(outpath), basename)
        warnings.warn("Format not supported. Suported formats are: %s."%
                      ', '.join(FigureCanvasBase.get_supported_filetypes().keys()))
    plt.savefig(outpath)
    return outpath