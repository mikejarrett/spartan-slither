# -*- coding: utf-8 -*-

from collections import namedtuple

import constants

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


class Renderer(object):

    @staticmethod
    def render_block_letter_image(display, image, resolution):
        block_letter_rect = image.get_rect()
        x_cordinates = resolution.width / 2
        y_cordinates = resolution.height / 2
        block_letter_rect.center = (x_cordinates, y_cordinates)
        display.blit(image, block_letter_rect)

    @staticmethod
    def display_message_to_screen(
        display, resolution, message, color, pygame,  y_displacement=0,
        font_size=constants.SMALL
    ):
        """ Display a message to screen

        :param message: String to be displayed to the game surface
        :param color: Tuple representing the color of the text
        """
        font_mapping = {
            'small': pygame.font.SysFont(None, 25),
            'medium': pygame.font.SysFont(None, 50),
            'large':  pygame.font.SysFont(None, 72)
        }
        font = font_mapping[font_size]

        text_surface = font.render(message, True, color)
        text_rect = text_surface.get_rect()
        x_cordinates = resolution.width / 2
        y_cordinates = resolution.height / 2 + y_displacement
        text_rect.center = (x_cordinates, y_cordinates)
        display.blit(text_surface, text_rect)


def get_rotation(x_direction, y_direction):
    rotation = 0
    if x_direction > 0:
        rotation = 0
    if y_direction < 0:
        rotation = 90
    if y_direction > 0:
        rotation = 270
    return rotation
