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
        self._health = 3
        self._win = False
        self.scores = 0
        self._velocity = 5
        self._screen = screen
        self.x_coor = self._screen.get_width() // 2 - self.WIDTH // 2
        self.y_coor = self._screen.get_height() - 100
        self.rect = pygame.Rect(self.x_coor, self.y_coor, self.WIDTH, self.HEIGHT)
        self.sprite = pygame.image.load(os.path.join(data_dir, "player.png"))
        self.player = pygame.transform.scale(self.sprite, (self.WIDTH, self.HEIGHT))

    @property
    def health(self):
        """Return player health"""
        return self._health

    @health.setter
    def set_health(self, val):
        """Set player health"""
        self._health = val

    @property
    def player_velocity(self):
        """Return player velocity"""
        return self._velocity

    @property
    def win_game(self):
        """Return if player win or not"""
        return self._win

    @win_game.setter
    def win_game(self, val):
        """Setter for win_game"""
        self._win = val

    def handle_movement(self, key_pressed):
        """Handle movement of player"""
        """Move left and right"""
        if key_pressed[pygame.K_LEFT] and self.rect.x - self.player_velocity > 0:
            self.rect.x -= self.player_velocity
        if key_pressed[pygame.K_RIGHT] and self.rect.x + self.player_velocity < (
            self._screen.get_width() - self.WIDTH
        ):
            self.rect.x += self.player_velocity

    def handle_shooting(self, event):
        """Shooting movement"""
        if (
            event.type == pygame.KEYDOWN
            and event.key == pygame.K_SPACE
            and len(self.bullets) < self.MAX_BULLETS
        ):
            player_bullet = pygame.Rect(
                self.rect.x + self.WIDTH // 2 - 2,
                self.rect.y + self.HEIGHT // 2 - 20,
                5,
                15,
            )
            self.bullets.append(player_bullet)

    def handle_collision(self, aliens, obstacles):
        """Detect when player hit spaceship"""
        for bullet in self.bullets:
            bullet.y -= 7
            if bullet.y < self.HEIGHT:
                self.bullets.remove(bullet)
            else:
                """When bullet hit an alien"""
                alien_idx = bullet.collidelist([c.rect for c in aliens])
                """When bullet hit an obstacle"""
                obs_idx = bullet.collidelist([obstacle.rect for obstacle in obstacles])
                if alien_idx > -1:
                    Explosion(aliens.sprites()[alien_idx])
                    collided_alien = aliens.sprites()[alien_idx]
                    collided_alien.minus_health = 1
                    if collided_alien.health == 0:
                        collided_alien.is_exploding = True
                        aliens.sprites()[alien_idx].kill()
                        self.scores += 1
                    self.bullets.remove(bullet)
                if obs_idx > -1:
                    self.bullets.remove(bullet)

        """Detect when bullet hit player"""
        for alien in aliens:
            for bullet in alien.bullets:
                if self.rect.colliderect(bullet):
                    if self.health == 0:
                        print("IM DEAD")
                    else:
                        alien.bullets.remove(bullet)
                        self.set_health -= 1
