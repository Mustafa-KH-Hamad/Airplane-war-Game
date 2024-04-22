import pygame
import sys
import random

from Controller import GameController
from Model import GameModel
from View import GameView

if __name__ == "__main__":
    # Initialize model, view, and controller
    model = GameModel()
    view = GameView(model)
    controller = GameController(model, view)

    # Run the game
    controller.run()
