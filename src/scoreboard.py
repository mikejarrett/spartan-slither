# -*- coding: utf-8 -*-

import utils
import color

class ScoreBoard(object):

    def __init__(self, display, pygame, width, height):
        self.display = display
        self.pygame = pygame
        self.resolution = utils.Resolution(width=width, height=height)
        self.score = 0
        self.height = height
        self.width = width
        self.background_color = color.SPARTAN

    def update(self):
        pass
