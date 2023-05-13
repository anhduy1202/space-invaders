# Daniel Truong
# CPSC 386-02
# 2022-04-26
# anhduy1202@csu.fullerton.edu
# @anhduy1202
#
# Lab 05-00
#
# This is the game file to define main game logic
#
"""Game objects to create PyGame based games."""

import os
import warnings

import pygame
from gamestate import GameState
from scene import CutScene, Scene, SceneManager, SpriteScene


def display_info():
    """Print out information about the display driver and video information."""
    print(f'The display is using the "{pygame.display.get_driver()}" driver.')
    print("Video Info:")
    print(pygame.display.Info())


# If you're interested in using abstract base classes, feel free to rewrite
# these classes.
# For more information about Python Abstract Base classes, see
# https://docs.python.org/3.8/library/abc.html


class VideoGame:
    """Base class for creating PyGame games."""

    def __init__(
        self,
        window_width=800,
        window_height=800,
        window_title="My Awesome Game",
    ):
        """Initialize a new game with the given window size and window title."""
        pygame.init()
        self._window_size = (window_width, window_height)
        self._clock = pygame.time.Clock()
        self._screen = pygame.display.set_mode(self._window_size)
        self._main_dir = os.path.dirname(os.path.abspath(__file__))
        self._data_dir = os.path.join(self._main_dir, "data")
        self.bg_sound_track = os.path.join(self._data_dir, "background_audio.mp3")
        self._title = window_title
        pygame.display.set_caption(self._title)
        self._game_is_over = False
        if not pygame.font:
            warnings.warn("Fonts disabled.", RuntimeWarning)
        if not pygame.mixer:
            warnings.warn("Sound disabled.", RuntimeWarning)
        self._scene_graph = None

    @property
    def scene_graph(self):
        """Return the scene graph representing all the scenes in the game."""
        return self._scene_graph

    def build_scene_graph(self):
        """Build the scene graph for the game."""
        raise NotImplementedError

    def run(self):
        """Run the game; the main game loop."""
        raise NotImplementedError


class MyVideoGame(VideoGame):
    """Show a colored window with a colored message and a polygon."""

    def __init__(self):
        """Init the Pygame demo."""
        super().__init__(window_title="Space Invaders")
        self._scene_graph = SceneManager()
        self.build_scene_graph()

    def build_scene_graph(self):
        """Build scene graph for the game demo."""
        game_state = GameState()
        base_scene = Scene(
            self._screen,
            (0, 0, 0),
            self.bg_sound_track,
            game_state,
        )
        self.scene_graph.add(
            [
                SpriteScene(
                    self._screen, self.scene_graph, self.bg_sound_track, game_state
                ),
                CutScene(self._screen, self.scene_graph, game_state),
            ]
        )
        self._scene_graph.set_next_scene("0")

    def run(self):
        """Run the game; the main game loop."""
        scene_iterator = iter(self.scene_graph)
        current_scene = next(scene_iterator)
        while not self._game_is_over:
            current_scene.start_scene()
            while current_scene.is_valid():
                current_scene.delta_time = self._clock.tick(current_scene.frame_rate())
                for event in pygame.event.get():
                    current_scene.process_event(event)
                current_scene.update_scene()
                current_scene.draw()
                current_scene.render_updates()
                pygame.display.update()
            current_scene.end_scene()
            try:
                current_scene = next(scene_iterator)
            except StopIteration:
                self._game_is_over = True
        pygame.quit()
        return 0
