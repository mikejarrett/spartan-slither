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


class Intro(object):

    def __init__(self, display, pygame, clock, resolution):
        self.display = display
        self._pygame = pygame
        self.clock = clock
        self.resolution = resolution
        self.start_game = False
        self.intro = True

    def run(self):
        while self.intro:
            self.display.fill(color.SPARTAN)
            utils.Renderer.display_message_to_screen(
                self.display, self.resolution,
                "Welcome to Spartan Slither", color.WHITE, self._pygame,
                y_displacement=-100,
                font_size=constants.LARGE
            )
            utils.Renderer.display_message_to_screen(
                self.display, self.resolution,
                "Objective: Destroy the Wolvies.", color.WHITE, self._pygame,
                y_displacement=-50
            )
            utils.Renderer.display_message_to_screen(
                self.display, self.resolution,
                "The more wolvies you destroy, the bigger you become.",
                color.WHITE, self._pygame, y_displacement=-20
            )
            utils.Renderer.display_message_to_screen(
                self.display, self.resolution,
                "Don't get too close to the walls though or the wolvies will "
                "win.", color.WHITE, self._pygame, y_displacement=10
            )
            utils.Renderer.display_message_to_screen(
                self.display, self.resolution,
                "Press S to start or Q to quit.", color.WHITE, self._pygame,
                y_displacement=50, font_size=constants.MEDIUM
            )
            self._pygame.display.update()
            self.clock.tick(15)
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
