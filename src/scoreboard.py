# -*- coding: utf-8 -*-

import colors
import utils


class ScoreBoard(object):

    def __init__(self, display, pygame, width, height):
        self.display = display
        self.pygame = pygame
        self.resolution = utils.Resolution(width=width, height=height)

    def update(self, length, ):
