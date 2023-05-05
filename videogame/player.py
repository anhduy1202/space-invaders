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
import rgbcolors
from animation import Explosion


class Player(pygame.sprite.Sprite):
    """Player class aka the spaceship"""

    def __init__(self, data_dir, screen):
        """Player attributes"""
        pygame.sprite.Sprite.__init__(self)
        self.WIDTH = 100
        self.HEIGHT = 60
        self.MAX_BULLETS = 3
        self.HEALTH_FONT = pygame.font.Font(None, 52)
        self.SCORE_FONT = pygame.font.Font(None, 52)
        self.bullets = []
        self.health = 3
        self.scores = 0
        self._velocity = 5
        self._screen = screen
        self.x_coor = self._screen.get_width() // 2 - self.WIDTH // 2
        self.y_coor = self._screen.get_height() - 100
        self.rect = pygame.Rect(self.x_coor, self.y_coor, self.WIDTH, self.HEIGHT)
        self.sprite = pygame.image.load(os.path.join(data_dir, "player.png"))
        self.player = pygame.transform.scale(self.sprite, (self.WIDTH, self.HEIGHT))

    @property
    def player_velocity(self):
        """Return player velocity"""
        return self._velocity

    def handle_movement(self, key_pressed):
        """Move left and right"""
        if key_pressed[pygame.K_LEFT] and self.rect.x - self.player_velocity > 0:
            self.rect.x -= self.player_velocity
        if key_pressed[pygame.K_RIGHT] and self.rect.x + self.player_velocity < (
            self._screen.get_width() - self.WIDTH
        ):
            self.rect.x += self.player_velocity

    def handle_bullet(self, aliens, player):
        """Detect when player hit spaceship"""
        for bullet in self.bullets:
            bullet.y -= 7
            if bullet.y < self.HEIGHT:
                self.bullets.remove(bullet)
            else:
                # When bullet hit an alien
                index = bullet.collidelist([c.rect for c in aliens])
                if index > -1:
                    Explosion(aliens.sprites()[index])
                    collided_alien = aliens.sprites()[index]
                    collided_alien.is_exploding = True
                    collided_alien.kill()
                    self.scores += 1
                    self.bullets.remove(bullet)
        """Detect when bullet hit player"""
        for alien in aliens:
            for bullet in alien.bullets:
                if self.rect.colliderect(bullet):
                    if self.health == 0:
                        print("IM DEAD")
                    else:
                        alien.bullets.remove(bullet)
                        self.health -= 1
