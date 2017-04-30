#! /usr/bin/python
# -*- coding: utf-8 -*-

from matplotlib import pyplot as plt
def plot():
    circle = plt.Circle((res1.x[0], res1.x[1]), res1.x[2], fill=False, edgecolor='r', label='squared')
    circle2 = plt.Circle((res2.x[0], res2.x[1]), res2.x[2], fill=False, edgecolor='g', label='not squared')
    circle3 = plt.Circle((initialx, initialy), initial_radius, fill=False, edgecolor='c', label='before optimisation')
    fig, ax = plt.subplots()
    plt.axis([0, 16, 0, 16])
    ax.add_artist(circle)
    ax.add_artist(circle2)
    ax.add_artist(circle3)
    orig, = plt.plot(points[:,0], points[:,1], c='y', label='original data')
    ax.legend(handles=[circle, circle2, circle3, orig])
    plt.show()