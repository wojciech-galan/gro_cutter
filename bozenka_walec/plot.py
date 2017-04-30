#! /usr/bin/python
# -*- coding: utf-8 -*-

from matplotlib import pyplot as plt
def plot(points, initialx, initialy, initial_radius, x, y, radius): #TODO outfile
    """
    Plots nanodisk boundaries before and after fitting a circle to the boundaries
    :param points: boundaries (protein) atoms
    :param initialx: guessed x coordinate of the middle of the circle
    :param initialy: guessed y coordinate of the middle of the circle
    :param initial_radius: guessed radius of the circle
    :param x: final coordinate of the middle of the circle
    :param y: final coordinate of the middle of the circle
    :param radius: final radius of the circle
    :return:
    """
    circle = plt.Circle((x, y), radius, fill=False, edgecolor='r', label='after optimization')
    circle2 = plt.Circle((initialx, initialy), initial_radius, fill=False, edgecolor='c', label='before optimization')
    fig, ax = plt.subplots()
    plt.axis([0, 16, 0, 16])
    ax.add_artist(circle)
    ax.add_artist(circle2)
    orig, = plt.plot(points[:,0], points[:,1], c='y', label='original data')
    ax.legend(handles=[circle, circle2, orig])
    plt.show()