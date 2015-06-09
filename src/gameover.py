# -*- coding: utf-8 -*-

import pygame

import color
import constants
import utils


class GameOver(object):

    def __init__(self, display, pygame, clock, image, resolution):
        self.display = display
        self._pygame = pygame
        self.block_w = image
        self.clock = clock
        self._resolution = resolution
        self.game_exit = False
        self.game_over = True

    def run(self):
        while self.game_over:
            self.display.fill(color.BLUE)
            utils.Renderer.display_message_to_screen(
                self.display, self._resolution, "The Wolvies Beat You!",
                color.MAIZE, self._pygame, y_displacement=-100,
                font_size=constants.MEDIUM
            )
            utils.Renderer.render_block_letter_image(
                self.display, self.block_w, self._resolution
            )
            utils.Renderer.display_message_to_screen(
                self.display, self._resolution,
                "Press C to play again or Q to quit.", color.MAIZE,
                self._pygame, y_displacement=100
            )
            pygame.display.update()
            self.handle_game_over_events()
        return self.game_exit

    def handle_game_over_events(self):
        for event in self._pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.game_exit = True
                    self.game_over = False
                if event.key == pygame.K_c:
                    self.game_over = False
