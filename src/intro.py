# -*- coding: utf-8 -*-

import pygame

import color
import constants


class Intro(object):

    def __init__(self, display, pygame, display_func, clock):
        self.display = display
        self._pygame = pygame
        self.display_message_to_screen = display_func
        self.clock = clock
        self.start_game = False
        self.intro = True

    def run(self):
        while self.intro:
            self.display.fill(color.SPARTAN)
            self.display_message_to_screen(
                "Welcome to Spartan Slither", color.WHITE, y_displacement=-100,
                font_size=constants.LARGE
            )
            self.display_message_to_screen(
                "Objective: Destroy the Wolvies.", color.WHITE,
                y_displacement=-50
            )
            self.display_message_to_screen(
                "The more wolvies you destroy, the bigger you become.",
                color.WHITE, y_displacement=-20
            )
            self.display_message_to_screen(
                "Don't get too close to the walls though or the wolvies will "
                "win.", color.WHITE, y_displacement=10
            )
            self.display_message_to_screen(
                "Press S to start or Q to quit.", color.WHITE,
                y_displacement=50, font_size=constants.MEDIUM
            )
            self._pygame.display.update()
            self.clock.tick(1)
            self.handle_intro_events()
        return self.start_game

    def handle_intro_events(self):
        for event in self._pygame.event.get():
            if event.type == pygame.QUIT:
                self.intro = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.intro = False
                if event.key == pygame.K_s:
                    self.intro = False
                    self.start_game = True
