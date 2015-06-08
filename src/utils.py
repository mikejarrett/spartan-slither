# -*- coding: utf-8 -*-

from collections import namedtuple

Resolution = namedtuple('Resolution', ['width', 'height'])

class Wolvie(object):

    def __init__(self, x, y, x_size, y_size):
        self.x = x
        self.y = y
        self.x_size = x_size
        self.y_size = y_size

    @property
    def dimensions(self):
        return (self.x, self.y, self.x_size, self.y_size)


def get_rotation(x_direction, y_direction):
    rotation = 0
    if x_direction > 0:
        rotation = 0
    if y_direction < 0:
        rotation = 90
    if y_direction > 0:
        rotation = 270
    return rotation
