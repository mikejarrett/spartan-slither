#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import time

import pygame

import color
import utils

RESOLUTION = (800, 600)
FPS = 30


class SpartanSlither(object):

    def __init__(self, resolution=RESOLUTION, fps=FPS):
        pygame.init()

        if not isinstance(resolution, (tuple, list)):
            raise TypeError(
                "{} is not a valid resolution. Was expecting tuple or "
                "list".format(resolution)
            )
        self.resolution = utils.Resolution(*resolution)

        self.clock = pygame.time.Clock()
        self.fps = fps
        self.display = pygame.display.set_mode(self.resolution)
        pygame.display.set_caption("Spartan Slither")

        self.small_font = pygame.font.SysFont(None, 25)
        self.medium_font = pygame.font.SysFont(None, 50)
        self.large_font = pygame.font.SysFont(None, 72)

        self.background_color = color.WHITE

        self.sparty_image = pygame.image.load("sparty.png")
        self.block_s = pygame.image.load("ms_block_s.png")
        self.wolvie_image = pygame.image.load("wolvie.png")
        self.block_w = pygame.image.load("block_w.png")
        self.intro = True

    def initialize_start(self):
        self.display.fill(self.background_color)
        self.game_exit = False
        self.game_over = False
        self.lead_x = self.resolution.width / 2
        self.lead_y = self.resolution.height / 2
        self.lead_x_change = 10
        self.lead_y_change = 0

        self.sparty_size = 20
        self.sparty_head = (self.lead_x, self.lead_y)
        self.sparty_list = [self.sparty_head]
        self.sparty_length = 1
        self.level = 10
        self.wolvie_size = 20
        self.wolvie = utils.Wolvie(0, 0, 0, 0)

    def run(self):
        self.intro_loop()
        while not self.game_exit:
            self.sparty_head = (self.lead_x, self.lead_y)
            self.is_game_over()
            self.handle_events()
            self.check_location()
            self.update()
            self.clock.tick(self.fps)

        self.exit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_exit = True

            if event.type == pygame.KEYDOWN:
                self.keydown_event(event)

            if event.type == pygame.KEYUP:
                self.keyup_event(event)
        self.lead_x += self.lead_x_change
        self.lead_y += self.lead_y_change

    def keydown_event(self, event):
        if event.key == pygame.K_q:  # Quit
            self.game_exit = True
        if event.key == pygame.K_LEFT:
            self.lead_x_change = -10  # (-2 * self.level) + 1
            self.lead_y_change = 0
        elif event.key == pygame.K_RIGHT:
            self.lead_x_change = 10  # (2 * self.level) - 1
            self.lead_y_change = 0
        elif event.key == pygame.K_UP:
            self.lead_y_change = -10  # (-2 * self.level) + 1
            self.lead_x_change = 0
        elif event.key == pygame.K_DOWN:
            self.lead_y_change = 10  # (2 * self.level) - 1
            self.lead_x_change = 0

    def keyup_event(self, event):
        return
        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
            self.lead_x_change = 0

        if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
            self.lead_y_change = 0

    def update(self):
        self.display.fill(self.background_color)
        self.draw_wolvie()
        self.draw_sparty()
        pygame.display.update()

    def draw_sparty(self):
        if len(self.sparty_list) > self.sparty_length:
            del self.sparty_list[0]

        if self.lead_x_change or self.lead_y_change:
            self.sparty_list.append(self.sparty_head)

        sparty_image = self._get_sparty_image()
        self.display.blit(sparty_image, self.sparty_list[-1])

        for x_pos, y_poz in self.sparty_list[:-1]:
            pygame.draw.rect(
                self.display, color.SPARTAN,
                [x_pos, y_poz, self.sparty_size, self.sparty_size]
            )

    def _get_sparty_image(self):
        if self.lead_x_change < 0:
            sparty_rotated = pygame.transform.flip(
                self.sparty_image, True, False)
        else:
            rotation = utils.get_rotation(
                self.lead_x_change, self.lead_y_change
            )
            sparty_rotated = pygame.transform.rotate(
                self.sparty_image, rotation)
        return sparty_rotated

    def draw_wolvie(self):
        if not (self.wolvie.x or self.wolvie.y):
            x_max = self.resolution.width - self.wolvie_size
            y_max = self.resolution.height - self.wolvie_size
            self.wolvie = utils.Wolvie(
                x=round(random.randrange(0, x_max)),
                y=round(random.randrange(0, y_max)),
                x_size=self.wolvie_size,
                y_size=self.wolvie_size
            )
        self.display.blit(self.wolvie_image, self.wolvie.dimensions)

    def check_location(self):
        self._check_boundary_collision()
        self._did_sparty_destroy_wolvie()

        if len(self.sparty_list) > 1:
            for segment in self.sparty_list[:-1]:
                if segment == self.sparty_head:
                    self.game_over = True

    def _check_boundary_collision(self):
        if (
            self.lead_x + self.sparty_size > self.resolution.width or
            self.lead_x < 0 or
            self.lead_y + self.sparty_size > self.resolution.height or
            self.lead_y < 0
        ):
            self.game_over = True

    def _did_sparty_destroy_wolvie(self):
        """
        Checks collission of Sparty with the wolverine. This takes into account
        if they are different sizes
        """
        sparty_size = self.lead_x + self.sparty_size
        wolvie_size = self.wolvie.x + self.wolvie_size
        if (
            self.lead_x >= self.wolvie.x and self.lead_x <= wolvie_size or
            sparty_size >= self.wolvie.x and sparty_size <= wolvie_size
        ):
            sparty_size = self.lead_y + self.sparty_size
            wolvie_size = self.wolvie.y + self.wolvie_size
            if (
                self.lead_y >= self.wolvie.y and self.lead_y <= wolvie_size or
                sparty_size >= self.wolvie.y and sparty_size <= wolvie_size
            ):
                self.wolvie.x = 0
                self.wolvie.y = 0
                self.sparty_length += 5

    def display_message_to_screen(
        self, message, color, y_displacement=0, font=None
    ):
        """ Display a message to screen

        :param message: String to be displayed to the game surface
        :param color: Tuple representing the color of the text
        """
        if font is None:
            font = self.small_font

        text_surface = font.render(message, True, color)
        text_rect = text_surface.get_rect()
        x_cordinates = self.resolution.width / 2
        y_cordinates = self.resolution.height / 2 + y_displacement
        text_rect.center = (x_cordinates, y_cordinates)
        self.display.blit(text_surface, text_rect)

    def is_game_over(self):
        while self.game_over:
            self.display.fill(color.BLUE)
            self.display_message_to_screen(
                "The Wolvies Beat You!", color.MAIZE, y_displacement=-100,
                font=self.medium_font
            )
            self._render_block_letter_image(self.block_w)
            self.display_message_to_screen(
                "Press C to play again or Q to quit.", color.MAIZE,
                y_displacement=100
            )
            pygame.display.update()
            self.handle_game_over_events()

    def handle_game_over_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:  # Quit
                    self.game_exit = True
                    self.game_over = False
                if event.key == pygame.K_c:  # Continue playing
                    self.initialize_start()

    def exit(self):
        """ Handle exiting the game, show a message, close it all down nicely.
        """
        self.display.fill(color.SPARTAN)
        self.display_message_to_screen(
            "Go Green! Go White!", self.background_color, y_displacement=-100,
            font=self.medium_font
        )

        self._render_block_letter_image(self.block_s)

        self.display_message_to_screen(
            "Thanks for playing!", self.background_color, y_displacement=100
        )
        pygame.display.update()
        time.sleep(2)

        pygame.quit()
        quit()

    def _render_block_letter_image(self, image):
        block_letter_rect = image.get_rect()
        x_cordinates = self.resolution.width / 2
        y_cordinates = self.resolution.height / 2
        block_letter_rect.center = (x_cordinates, y_cordinates)
        self.display.blit(image, block_letter_rect)

    def intro_loop(self):
        while self.intro:
            self.display.fill(color.SPARTAN)
            self.display_message_to_screen(
                "Welcome to Spartan Slither", color.WHITE, y_displacement=-100,
                font=self.large_font
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
                y_displacement=50, font=self.medium_font
            )
            pygame.display.update()
            self.clock.tick(1)
            self.handle_intro_events()

    def handle_intro_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_exit = True
                self.intro = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.game_exit = True
                    self.game_over = False
                    self.intro = False
                if event.key == pygame.K_s:
                    self.intro = False
                    self.initialize_start()


if __name__ == "__main__":
    SpartanSlither().run()
