#! /usr/bin/python
# -*- coding: utf-8 -*-

import math
import functools
import numpy as np
from scipy.optimize import minimize


def distance2d((x1, y1), (x2, y2)):
    '''Calculates euclidean distancer between two 2D points'''
    return math.sqrt(squared_distance2d((x1, y1), (x2, y2)))


def squared_distance2d((x1, y1), (x2, y2)):
    '''Calculates squared euclidean distancer between two 2D points'''
    return (x1 - x2) ** 2 + (y1 - y2) ** 2


def distance_from_circle(point, center, radius):
    '''Computes distance between point and a circle'''
    return math.fabs(radius**2-squared_distance2d(point, center))


def cumulative_distance_from_circle(points, center, radius):
    return sum(distance_from_circle(point, center, radius) for point in points)


def determine_center_and_radius(points, initialx=None, initialy=None, initial_radius=None):
    if initialx is None:
        initialx = np.mean(points[:,0])
    if initialy is None:
        initialy = np.mean(points[:,1])
    if initial_radius is None:
        initial_radius = (math.fabs(initialx) + math.fabs(initialy) - np.min(points[:,0]) - np.min(points[:,1]))/2
    def cumulative_distance_from_circle_wraper(x):
        return cumulative_distance_from_circle(points, (x[0], x[1]), x[2])
    from scipy.optimize import least_squares
    return least_squares(functools.partial(cumulative_distance_from_circle_wraper),
                         [initialx, initialy, initial_radius],
                         xtol=1e-8).x
    return minimize(functools.partial(cumulative_distance_from_circle_wraper),
                    [initialx, initialy, initial_radius], method='nelder-mead', #method='nelder-mead',
                   options={'xtol': 1e-8}).x
    # res1 = minimize(functools.partial(cumulative_distance_from_circle_wraper, squared=True),
    #                 [initialx, initialy, initial_radius], method='nelder-mead',
    #                options={'xtol': 1e-8, 'disp': True})
    # res2 = minimize(functools.partial(cumulative_distance_from_circle_wraper, squared=False),
    #                 [initialx, initialy, initial_radius], method='nelder-mead',
    #                options={'xtol': 1e-8, 'disp': True})
    # print res1.x
    # print res2.x
    # from matplotlib import pyplot as plt
    # circle = plt.Circle((res1.x[0], res1.x[1]), res1.x[2], fill=False, edgecolor='r', label='squared')
    # circle2 = plt.Circle((res2.x[0], res2.x[1]), res2.x[2], fill=False, edgecolor='g', label='not squared')
    # circle3 = plt.Circle((initialx, initialy), initial_radius, fill=False, edgecolor='c', label='before optimisation')
    # fig, ax = plt.subplots()
    # plt.axis([0, 16, 0, 16])
    # ax.add_artist(circle)
    # ax.add_artist(circle2)
    # ax.add_artist(circle3)
    # orig, = plt.plot(points[:,0], points[:,1], c='y', label='original data')
    # ax.legend(handles=[circle, circle2, circle3, orig])
    # plt.show()
    # return res1.x


if __name__ == '__main__':
    #p = [(0, 0), (1, 1), (2, 0), (1, -1), (1+math.sqrt(2)/2, math.sqrt(2)/2), (1-math.sqrt(2)/2, -math.sqrt(2)/2)]
    p = np.array([(2+math.sin(x*math.pi/180), 2*math.cos(x*math.pi/180)) for x in range(360)])
    print determine_center_and_radius(p)