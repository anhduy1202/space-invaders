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
import random

import pygame

SPACING = 10


class Alien(pygame.sprite.Sprite):
    "Alien class"

    def __init__(self, data_dir, screen, x_pos=0, y_pos=50):
        """Alien attributes"""
        pygame.sprite.Sprite.__init__(self)
        self.MAX_BULLETS = 1
        self.WIDTH = 70
        self.HEIGHT = 70
        self.bullets = []
        self._is_exploding = False
        self.health = 1
        self._velocity = random.randint(3, 5)
        self._screen = screen
        self.x_coor = x_pos
        self.y_coor = y_pos
        self.rect = pygame.Rect(self.x_coor, self.y_coor, self.WIDTH, self.HEIGHT)
        self.sprite = pygame.image.load(os.path.join(data_dir, "alien.png"))
        self.image = pygame.transform.scale(self.sprite, (self.WIDTH, self.HEIGHT))
        self.last_shot_time = pygame.time.get_ticks()
        self.shoot_timer = 0

    @property
    def get_velocity(self):
        return self._velocity

    @property
    def is_exploding(self):
        return self._is_exploding

    @is_exploding.setter
    def is_exploding(self, val):
        self._is_exploding = val

    def handle_bullet(self):
        """Handle bullet movement"""
        for bullet in self.bullets:
            bullet.y += self.get_velocity
            if bullet.y > self._screen.get_height() - 60:
                self.bullets.remove(bullet)


class Aliens(Alien):
    "Bunch of aliens"

    def __init__(self, data_dir, screen):
        """Commond attributes between all aliens"""
        super().__init__(data_dir, screen)
        self.ROWS = 3
        self.MAX_ALIENS = 30
        self.X_INIT = 0
        self.Y_INIT = 100
        self.data_dir = data_dir
        self.screen = screen
        self.alien_group = pygame.sprite.Group()
        self.group_aliens()

    def group_aliens(self):
        """Group aliens"""
        for row in range(self.ROWS):
            for col in range(self.MAX_ALIENS // self.ROWS):
                x_pos = self.X_INIT + col * (self.WIDTH + SPACING)
                y_pos = self.Y_INIT + row * (self.HEIGHT + SPACING)
                alien = Alien(self.data_dir, self.screen, x_pos, y_pos)
                self.alien_group.add(alien)

    def handle_bullet(self):
        """Handle alien bullets"""
        if len(self.alien_group) > 0:
            now = pygame.time.get_ticks()
            random_idx = random.randint(
                0,
                1 if len(self.alien_group) <= 0 else len(self.alien_group) - 1,
            )
            """Make alien shoot bullet one at a time randomly"""
            random_alien = self.alien_group.sprites()[random_idx]
            random_alien.shoot_timer += now
            if len(random_alien.bullets) < random_alien.MAX_BULLETS:
                if now - random_alien.last_shot_time > random.randint(1000, 3000):
                    random_alien.last_shot_time = now
                    alien_bullet = pygame.Rect(
                        random_alien.x_coor + random_alien.WIDTH // 2,
                        random_alien.y_coor + random_alien.HEIGHT // 2 + 20,
                        5,
                        15,
                    )
                    random_alien.bullets.append(alien_bullet)
