# Daniel Truong
# CPSC 386-02
# 2022-04-26
# anhduy1202@csu.fullerton.edu
# @anhduy1202
#
# Lab 05-00
#
# This is the obstacle file to define obstacle properties
#
"""Obstacle object"""

import pygame


class Obstacle:
    "Obstacle class"

    def __init__(self, x_coor, y_coor):
        """Obstacle attribute"""
        self.WIDTH = 140
        self.HEIGHT = 80
        self.rect = pygame.Rect(x_coor, y_coor, self.WIDTH, self.HEIGHT)
