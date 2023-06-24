import pygame
import constant
from client_stub import StubClient
from client_game import game_mech



if __name__ == '__main__':
    pygame.init()
    stub = StubClient()
    ui = game_mech(stub,constant.carro1.png, constant.STAW,constant.LEFT_KEYS)
    ui.run()