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
"""state objects for making state with PyGame."""


class GameState:
    """Game state"""

    def __init__(self):
        """init"""
        self.selected_option = "Menu"
        self.win = False
        self.lost = False
