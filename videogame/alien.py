# Daniel Truong
# CPSC 386-02
# 2022-04-26
# anhduy1202@csu.fullerton.edu
# @anhduy1202
#
# Lab 05-00
#
# This is the alient file to define alien logic
#
"""Alien object"""
import os

import pygame

WIDTH = 80
HEIGHT = 80
SPACING = 10


class Alien(pygame.sprite.Sprite):
    "Alien class"

    def __init__(self, data_dir, screen, x_pos=0, y_pos=50):
        """Alien attributes"""
        pygame.sprite.Sprite.__init__(self)
        self.MAX_BULLETS = 1
        self.bullets = []
        self.health = 1
        self._velocity = 3
        self._screen = screen
        self.x_coor = x_pos
        self.y_coor = y_pos
        self.rect = pygame.Rect(self.x_coor, self.y_coor, WIDTH, HEIGHT)
        self.sprite = pygame.image.load(os.path.join(data_dir, "alien.png"))
        self.image = pygame.transform.scale(self.sprite, (WIDTH, HEIGHT))
        self.last_shot_time = pygame.time.get_ticks()
        self.shoot_timer = 0

    def handle_bullet(self):
        """Detect bullets"""
        for bullet in self.bullets:
            bullet.y += 7

    def can_shoot(self):
        return self.shoot_timer >= 3000


class Aliens:
    "Bunch of aliens"

    def __init__(self, data_dir, screen):
        """Commond attributes between all aliens"""
        self.ROWS = 4
        self.MAX_ALIENS = 40
        self.X_INIT = 0
        self.Y_INIT = 10
        self.data_dir = data_dir
        self.screen = screen
        self.alien_group = pygame.sprite.Group()
        self.group_aliens()

    def group_aliens(self):
        """Group aliens"""
        for row in range(self.ROWS):
            for col in range(self.MAX_ALIENS // self.ROWS):
                x_pos = self.X_INIT + col * (WIDTH + SPACING)
                y_pos = self.Y_INIT + row * (HEIGHT + SPACING)
                alien = Alien(self.data_dir, self.screen, x_pos, y_pos)
                self.alien_group.add(alien)
