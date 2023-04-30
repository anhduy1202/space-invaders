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
    def __init__(self, data_dir):
        self.WIDTH = 55
        self.HEIGHT = 44
        self.health = 3
        self._velocity = 5
        self.x_coor = 0
        self.y_coor = 0
        self.sprite = pygame.image.load(os.path.join(data_dir, "player.png"))
        self.player = pygame.transform.scale(self.sprite, (self.WIDTH, self.HEIGHT))

    @property
    def player_velocity(self):
        return self._velocity
