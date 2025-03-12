"""
    Jhon Oliver Castillo Caraballo
    22-SISN-2-063
"""

import pygame as pg
from Utils.setup import Setup
from Utils.theme import Theme
from Game.game import Game


def run_game():
    # Stop menu music if playing
    pg.mixer.music.stop()

    # Initialize and start the game
    game = Game()
    game.run()


if __name__ == "__main__":
    # Validate assets before starting
    if not Setup.validate_assets():
        print("Error : Faltan archivos de recursos")
        exit(1)

    # Inicializar soporte para joystick
    has_joystick = Setup.initialize_controllers()

    # Initialize theme and start menu
    surface = Theme.initialize()

    # Start the menu
    Theme.menu_loop(run_game)
