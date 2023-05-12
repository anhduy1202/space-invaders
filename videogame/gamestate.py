# Daniel Truong
# CPSC 386-02
# 2022-04-26
# anhduy1202@csu.fullerton.edu
# @anhduy1202
#
# Lab 05-00
#
# This is the state file to define game state
#
"""state objects for making global state for the game to easily manage it."""


class GameState:
    """Game state"""

    def __init__(self):
        """Global state for the game"""
        self.selected_option = "Menu"
        self.win = False
        self.health = 3
        self.score = 0
        self.lost = False
