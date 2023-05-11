# Daniel Truong
# CPSC 386-02
# 2022-04-26
# anhduy1202@csu.fullerton.edu
# @anhduy1202
#
# Lab 05-00
#
# This is the alien file to define alien logic
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
        self.WIDTH = 65
        self.HEIGHT = 65
        self.bullets = []
        self._is_exploding = False
        self._health = 1
        self._speed = 20
        self._bullet_velocity = random.randint(3, 5)
        self._screen = screen
        self.x_coor = x_pos
        self.y_coor = y_pos
        self.rect = pygame.Rect(self.x_coor, self.y_coor, self.WIDTH, self.HEIGHT)
        self.sprite = pygame.image.load(os.path.join(data_dir, "alien.png"))
        self.image = pygame.transform.scale(self.sprite, (self.WIDTH, self.HEIGHT))
        self.last_shot_time = pygame.time.get_ticks()
        self.last_pos = pygame.time.get_ticks()

    @property
    def bullet_velocity(self):
        """Return alien bullet velocity"""
        return self._bullet_velocity

    @property
    def is_exploding(self):
        """Return exploding state"""
        return self._is_exploding

    @property
    def health(self):
        """Return alien health"""
        return self._health

    @property
    def speed(self):
        """Return alien speed"""
        return self._speed

    @health.setter
    def minus_health(self, val):
        "Setter for health"
        self._health -= val

    @is_exploding.setter
    def is_exploding(self, val):
        """Setter for is_exploding"""
        self._is_exploding = val

    def handle_bullet(self, obstacles):
        """Handle bullet movement"""
        for bullet in self.bullets:
            bullet.y += self.bullet_velocity
            if bullet.y > self._screen.get_height() - 60:
                self.bullets.remove(bullet)
            """When bullet hit an obstacle"""
            obs_idx = bullet.collidelist([obstacle.rect for obstacle in obstacles])
            if obs_idx > -1:
                self.bullets.remove(bullet)

    def march_towards(self, alien_group):
        """Aliens march towards spaceship"""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_pos > random.randint(1000, 3000):
            self.last_pos = current_time
            dx = self.rect.x + self.speed
            dy = self.rect.y + self.speed
            if dy > self._screen.get_height() - 200:
                print("OUT OF BOUND")
                alien_group.stop_y = True
            if dx > self._screen.get_width() - self.WIDTH:
                alien_group.stop_x = True
            if dx <= 0:
                alien_group.stop_x = False
                if alien_group.stop_y is False:
                    self.rect.y += 1
            if alien_group.stop_x is False:
                self.rect.x += self.speed
            else:
                self.rect.x -= self.speed


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
        self.stop_x = False
        self.stop_y = False
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

    def handle_bullet(self, obstacles=None):
        """Handle alien bullets"""
        if len(self.alien_group) > 0:
            now = pygame.time.get_ticks()
            random_idx = random.randint(
                0,
                1 if len(self.alien_group) <= 0 else len(self.alien_group) - 1,
            )
            """Make alien shoot bullet one at a time randomly"""
            random_alien = self.alien_group.sprites()[random_idx]
            if len(random_alien.bullets) < random_alien.MAX_BULLETS:
                if now - random_alien.last_shot_time > random.randint(1000, 3000):
                    random_alien.last_shot_time = now
                    alien_bullet = pygame.Rect(
                        random_alien.rect.x + random_alien.WIDTH // 2,
                        random_alien.rect.y + random_alien.HEIGHT // 2 + 20,
                        5,
                        15,
                    )
                    random_alien.bullets.append(alien_bullet)
