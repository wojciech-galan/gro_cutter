#! /usr/bin/python
# -*- coding: utf-8 -*-

import math
import numpy as np
from scipy.optimize import minimize


def distance2d((x1, y1), (x2, y2)):
    '''Calculates euclidean distancer between two 2D points'''
    return math.sqrt(squared_distance2d((x1, y1), (x2, y2)))


def squared_distance2d((x1, y1), (x2, y2)):
    '''Calculates squared euclidean distancer between two 2D points'''
    return (x1 - x2) ** 2 + (y1 - y2) ** 2


def distance_from_circle(point, center, radius, distance_f):
    '''Computes distance between point and a circle'''
    return math.fabs(radius-distance_f(point, center))


def cumulative_distance_from_circle(points, center, radius, distance_f=squared_distance2d):
    return sum(distance_from_circle(point, center, radius, distance_f) for point in points)


def determine_center_and_radius(points, distance_f):
    initialx = np.mean(points[:,0])
    initialy = np.mean(points[:,1])
    initial_radius = (math.fabs(initialx) + math.fabs(initialy) - np.min(points[:,0]) - np.min(points[:,1]))/2
    print initialx, initialy, initial_radius
    def cumulative_distance_from_circle_wraper(x, distance_func=distance_f):
        return cumulative_distance_from_circle(points, (x[0], x[1]), x[2], distance_f=distance_func)
    res = minimize(cumulative_distance_from_circle_wraper, [initialx, initialy, initial_radius], method='nelder-mead',
                   options={'xtol': 1e-8, 'disp': True})
    # import functools
    # res2 = minimize(functools.partial(cumulative_distance_from_circle_wraper, distance_func=distance2d), [initialx, initialy, initial_radius], method='nelder-mead',
    #                options={'xtol': 1e-8, 'disp': True})
    # print res.x
    # print res2.x
    # from matplotlib import pyplot as plt
    # circle = plt.Circle((res.x[0], res.x[1]), res.x[2]/2, fill=False)
    # circle2 = plt.Circle((res2.x[0], res2.x[1]), res2.x[2] / 2, fill=False)
    # fig, ax = plt.subplots()
    # plt.axis([-1, 5, -3, 3])
    # ax.add_artist(circle)
    # ax.add_artist(circle2)
    # plt.plot(points[:,0], points[:,1])
    # plt.show()
    return res.x


if __name__ == '__main__':
    #p = [(0, 0), (1, 1), (2, 0), (1, -1), (1+math.sqrt(2)/2, math.sqrt(2)/2), (1-math.sqrt(2)/2, -math.sqrt(2)/2)]
    p = np.array([(2+math.sin(x*math.pi/180), 2*math.cos(x*math.pi/180)) for x in range(360)])
    print determine_center_and_radius(p, squared_distance2d)