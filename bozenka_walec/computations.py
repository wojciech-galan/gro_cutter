#! /usr/bin/python
# -*- coding: utf-8 -*-

import math
import functools
import numpy as np
from scipy.optimize import least_squares


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


def determine_center_and_radius(points, xtol, initialx=None, initialy=None, initial_radius=None):
    if initialx is None:
        initialx = np.mean(points[:,0])
    if initialy is None:
        initialy = np.mean(points[:,1])
    if initial_radius is None:
        initial_radius = (math.fabs(initialx) + math.fabs(initialy) - np.min(points[:,0]) - np.min(points[:,1]))/2
    def cumulative_distance_from_circle_wraper(x):
        return cumulative_distance_from_circle(points, (x[0], x[1]), x[2])
    return least_squares(functools.partial(cumulative_distance_from_circle_wraper),
                         [initialx, initialy, initial_radius],
                         xtol=xtol).x


if __name__ == '__main__':
    #p = [(0, 0), (1, 1), (2, 0), (1, -1), (1+math.sqrt(2)/2, math.sqrt(2)/2), (1-math.sqrt(2)/2, -math.sqrt(2)/2)]
    p = np.array([(2+math.sin(x*math.pi/180), 2*math.cos(x*math.pi/180)) for x in range(360)])
    print determine_center_and_radius(p)