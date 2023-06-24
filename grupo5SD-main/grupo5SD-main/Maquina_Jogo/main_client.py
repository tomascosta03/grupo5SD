from client_stub import StubClient
from client_game import Game
import pygame

def main():
    pygame.init()
    stub = StubClient()
    ui = Game(stub)
    ui.run()


main()