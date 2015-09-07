#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import time

import pygame

from scenes import GameOver, Intro
import color
import constants
import scoreboard
import utils


class SpartanSlither(object):

    def __init__(self, resolution=constants.RESOLUTION, fps=constants.FPS):
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

        self.background_color = color.WHITE

        self.sparty_image = pygame.image.load("resources/sparty.png")
        self.block_s = pygame.image.load("resources/ms_block_s.png")
        self.wolvie_image = pygame.image.load("resources/wolvie.png")
        self.block_w = pygame.image.load("resources/block_w.png")

    def initialize_start(self):
        self.level = 10
        self.speed = 10

        self.display.fill(self.background_color)
        self.game_exit = False
        self.game_over = False
        self.lead_x = self.resolution.width / 2
        self.lead_y = self.resolution.height / 2
        self.lead_x_change = 10
        self.lead_y_change = 0

        self.score_board = scoreboard.ScoreBoard(
            display=self.display, pygame=pygame, width=self.resolution.width,
            height=self.resolution.height / 10
        )
        self._update_score = False

        self.sparty_size = 20
        self.sparty_head = (self.lead_x, self.lead_y)
        self.sparty_list = [self.sparty_head]
        self.sparty_length = 1
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

        self.lead_x += self.lead_x_change
        self.lead_y += self.lead_y_change

    def keydown_event(self, event):
        """ Logic for handling keydown event """
        if event.key == pygame.K_q:
            self.game_exit = True
        if event.key == pygame.K_LEFT:
            self.lead_x_change = self.speed * -1
            self.lead_y_change = 0
        elif event.key == pygame.K_RIGHT:
            self.lead_x_change = self.speed
            self.lead_y_change = 0
        elif event.key == pygame.K_UP:
            self.lead_y_change = self.speed * -1
            self.lead_x_change = 0
        elif event.key == pygame.K_DOWN:
            self.lead_y_change = self.speed
            self.lead_x_change = 0

    def update(self):
        self.display.fill(self.background_color)
        self.draw_wolvie()
        self.draw_sparty()
        self.update_score()
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
                y=round(random.randrange(self.score_board.height, y_max)),
                x_size=self.wolvie_size,
                y_size=self.wolvie_size
            )
        self.display.blit(self.wolvie_image, self.wolvie.dimensions)

    def update_score(self):
        if self._update_score:
            self.score_board.update()
        self._update_score = False

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
            self.lead_y < self.score_board.height
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
                self._update_score = True

    def is_game_over(self):
        if self.game_over:
            exit_game = GameOver(
                display=self.display, pygame=pygame,
                clock=self.clock,
                image=self.block_w,
                resolution=self.resolution
            ).run()
            if exit_game:
                self.game_exit = True
            else:
                self.initialize_start()

    def exit(self):
        """ Handle exiting the game, show a message, close it all down nicely.
        """
        self.display.fill(color.SPARTAN)
        utils.Renderer.display_message_to_screen(
            self.display, self.resolution, "Go Green! Go White!",
            self.background_color, pygame, y_displacement=-100,
            font_size=constants.MEDIUM
        )

        utils.Renderer.render_block_letter_image(
            self.display, self.block_s, self.resolution
        )

        utils.Renderer.display_message_to_screen(
            self.display, self.resolution, "Thanks for playing!",
            self.background_color, pygame, y_displacement=100
        )
        pygame.display.update()
        time.sleep(2)

        pygame.quit()
        quit()

    def intro_loop(self):
        start = Intro(
            display=self.display, pygame=pygame, clock=self.clock,
            resolution=self.resolution
        ).run()
        if start:
            self.initialize_start()
        else:
            self.game_exit = True


if __name__ == "__main__":
    SpartanSlither().run()
