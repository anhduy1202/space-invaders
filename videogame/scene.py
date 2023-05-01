# Daniel Truong
# CPSC 386-02
# 2022-04-26
# anhduy1202@csu.fullerton.edu
# @anhduy1202
#
# Lab 05-00
#
# This is the scene file to define game sprites, update scenes
#
"""Scene objects for making games with PyGame."""

import os

import pygame
import rgbcolors
from menu import Menu, Title
from player import Player

# If you're interested in using abstract base classes, feel free to rewrite
# these classes.
# For more information about Python Abstract Base classes, see
# https://docs.python.org/3.8/library/abc.html


class Scene:
    """Base class for making PyGame Scenes."""

    def __init__(self, screen, background_color, soundtrack=None):
        """Scene initializer"""
        self._screen = screen
        self._background = pygame.Surface(self._screen.get_size())
        self._background.fill(background_color)
        self._frame_rate = 60
        self._is_valid = True
        "For the menu"
        self._select = 0
        self.selected_option = ""
        self.menu = Menu(screen)
        self.title = Title(screen)
        self._soundtrack = soundtrack
        self._render_updates = None

    def draw(self):
        """Draw the scene with menu to start with"""
        self._screen.blit(self._background, (0, 0))
        if self.menu.menu_shown:
            self._screen.blit(
                self.title.title, (self.title.title_pos_x, self.title.title_pos_y)
            )
        # Display the menu options
        if self.menu.menu_shown:
            for index, option in enumerate(self.menu.options):
                if index == self._select:
                    text = self.menu.font.render(option, True, rgbcolors.yellow1)
                else:
                    text = self.menu.font.render(option, True, rgbcolors.ghost_white)
                text_pos = (
                    self.menu.x_coor,
                    self.menu.y_coor + index * self.menu.spacing,
                )
                self._screen.blit(text, text_pos)

    def process_event(self, event):
        """Process a game event by the scene."""
        if event.type == pygame.KEYDOWN:
            if event.type == pygame.QUIT:
                print("Good Bye!")
                self._is_valid = False
            "Handle menu options"
            if self.menu.menu_shown:
                if event.key == pygame.K_UP:
                    "Move the selected option up"
                    self._select = (self._select - 1) % len(self.menu.options)
                elif event.key == pygame.K_DOWN:
                    "Move the selected option down"
                    self._select = (self._select + 1) % len(self.menu.options)
                elif event.key == pygame.K_RETURN:
                    if self.menu.options[self._select] == "Start Game":
                        self.selected_option = "Start Game"
                        self.menu.hide_menu()
                    elif self.menu.options[self._select] == "High Scores":
                        self.selected_option == "High Scores"
                        self.menu.hide_menu()
                    elif self.menu.options[self._select] == "Settings":
                        self.selected_option == "Settings"
                        self.menu.hide_menu()
                    elif self.menu.options[self._select] == "Quit":
                        self._is_valid = False

    def is_valid(self):
        """Is the scene valid? A valid scene can be used to play a scene."""
        return self._is_valid

    def render_updates(self):
        """Render all sprite updates."""

    def update_scene(self):
        """Update the scene state."""

    def start_scene(self):
        """Start the scene."""
        if self._soundtrack:
            try:
                pygame.mixer.music.load(self._soundtrack)
                pygame.mixer.music.set_volume(0.2)
            except pygame.error as pygame_error:
                print("Cannot open the mixer?")
                print("\n".join(pygame_error.args))
                raise SystemExit("broken!!") from pygame_error
            pygame.mixer.music.play(-1)

    def end_scene(self):
        """End the scene."""
        if self._soundtrack and pygame.mixer.music.get_busy():
            # Fade music out so there isn't an audible pop
            pygame.mixer.music.fadeout(500)
            pygame.mixer.music.stop()

    def frame_rate(self):
        """Return the frame rate the scene desires."""
        return self._frame_rate


class PressAnyKeyToExitScene(Scene):
    """Empty scene where it will invalidate when a key is pressed."""

    def process_event(self, event):
        """Process game events."""
        super().process_event(event)
        if event.type == pygame.QUIT:
            self._is_valid = False


class SpriteScene(PressAnyKeyToExitScene):
    """Sprite scene to display sprite on the window"""

    def __init__(self, screen):
        """Sprite init"""
        super().__init__(screen, rgbcolors.black, None)
        self._screen = screen
        self._main_dir = os.path.split(os.path.abspath(__file__))[0]
        self._data_dir = os.path.join(self._main_dir, "data")
        """ Load background image """
        self._background = pygame.transform.scale(
            pygame.image.load(os.path.join(self._data_dir, "background.jpg")),
            (screen.get_width(), screen.get_height()),
        )
        self._player = Player(self._data_dir, self._screen)

    def draw(self):
        """Draw player, bullets, enemies"""
        super().draw()
        if self.selected_option == "Start Game":
            self._screen.blit(
                self._player.player,
                (self._player.player_rect.x, self._player.player_rect.y),
            )
            for bullet in self._player.bullets:
                pygame.draw.rect(self._screen, rgbcolors.sky_blue, bullet)

    def process_event(self, event):
        """Detect movement"""
        super().process_event(event)
        if (
            event.type == pygame.KEYDOWN
            and event.key == pygame.K_SPACE
            and len(self._player.bullets) < self._player.MAX_BULLETS
        ):
            bullet = pygame.Rect(
                self._player.player_rect.x + self._player.WIDTH // 2 - 2,
                self._player.player_rect.y + self._player.HEIGHT // 2 - 20,
                5,
                15,
            )
            self._player.bullets.append(bullet)

    def update_scene(self):
        """Detect and handle movement"""
        super().update_scene()
        key_pressed = pygame.key.get_pressed()
        self._player.handle_movement(key_pressed)
        self._player.handle_bullet()
