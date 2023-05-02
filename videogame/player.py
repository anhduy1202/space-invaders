# Daniel Truong
# CPSC 386-02
# 2022-04-26
# anhduy1202@csu.fullerton.edu
# @anhduy1202
#
# Lab 05-00
#
# This is the player file to define player logic
#
"""Player object"""
import os

import pygame


class Player:
    """Player class aka the spaceship"""

    def __init__(self, data_dir, screen):
        """Player attributes"""
        self.WIDTH = 100
        self.HEIGHT = 60
        self.MAX_BULLETS = 3
        self.bullets = []
        self.health = 3
        self._velocity = 5
        self._screen = screen
        self.x_coor = self._screen.get_width() // 2 - self.WIDTH // 2
        self.y_coor = self._screen.get_height() - 100
        self.player_rect = pygame.Rect(
            self.x_coor, self.y_coor, self.WIDTH, self.HEIGHT
        )
        self.sprite = pygame.image.load(os.path.join(data_dir, "player.png"))
        self.player = pygame.transform.scale(self.sprite, (self.WIDTH, self.HEIGHT))

    @property
    def player_velocity(self):
        """Return player velocity"""
        return self._velocity

    def handle_movement(self, key_pressed):
        """Move left and right"""
        if key_pressed[pygame.K_LEFT] and self.player_rect.x - self.player_velocity > 0:
            self.player_rect.x -= self.player_velocity
        if key_pressed[pygame.K_RIGHT] and self.player_rect.x + self.player_velocity < (
            self._screen.get_width() - self.WIDTH
        ):
            self.player_rect.x += self.player_velocity

    def handle_bullet(self):
        """Detect bullets"""
        for bullet in self.bullets:
            bullet.y -= 7
            if bullet.y < self.HEIGHT:
                self.bullets.remove(bullet)
