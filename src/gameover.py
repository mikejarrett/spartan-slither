# -*- coding: utf-8 -*-

import pygame

import color
import constants


class GameOver(object):

    def __init__(
        self, display, pygame, display_func, clock, render_block_func, image
    ):
        self.display = display
        self._pygame = pygame
        self.display_message_to_screen = display_func
        self._render_block_letter_image = render_block_func
        self.block_w = image
        self.clock = clock
        self.game_exit = False
        self.game_over = True

    def run(self):
        while self.game_over:
            self.display.fill(color.BLUE)
            self.display_message_to_screen(
                "The Wolvies Beat You!", color.MAIZE, y_displacement=-100,
                font_size=constants.MEDIUM
            )
            self._render_block_letter_image(self.block_w)
            self.display_message_to_screen(
                "Press C to play again or Q to quit.", color.MAIZE,
                y_displacement=100
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
