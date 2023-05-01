# Daniel Truong
# CPSC 386-02
# 2022-04-26
# anhduy1202@csu.fullerton.edu
# @anhduy1202
#
# Lab 05-00
#
# This is the menu file to display menu and handle interaciton
#
"""Menu"""

import pygame
import rgbcolors


class Menu:
    def __init__(self, screen):
        """Menu attribute"""
        self.screen = screen
        self.menu_shown = True
        title_font = pygame.font.Font(None, 42)
        self.title_text = "SPACE INVADERS"
        self.title = title_font.render(self.title_text, True, rgbcolors.ghost_white)
        self.font = pygame.font.Font(None, 36)
        self.x_coor = (self.screen.get_width() - (self.title.get_width() // 2)) // 2
        self.y_coor = 200
        self.spacing = 50
        self.options = ["Start Game", "High Scores", "Settings", "Quit"]
        self.rules_controls_text = "RULES:\n\n- Use the arrow keys to move your spaceship\n- Press the space bar to fire\n\nDESTROY ALL THE INVADERS TO WIN!"

    def hide_menu(self):
        """Hide the menu"""
        self.menu_shown = False


class Title(Menu):
    def __init__(self, screen):
        """Define title of the game"""
        super().__init__(screen)
        self.title_pos_x = (self.screen.get_width() - self.title.get_width()) // 2
        self.title_pos_y = 100
