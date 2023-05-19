import pygame
import pygame

import client_stub
import game_mech

# Defining constants for the moves
M_UP = 0
M_RIGHT = 1
M_DOWN = 2
M_LEFT = 3


class Player(pygame.sprite.DirtySprite):
    def __init__(self, number: int, name: str, pos_x: int, pos_y: int, sq_size: int, *groups):
        super().__init__(*groups)
        self.number = number
        self.name = name

        if self.number == 0:
            self.image = pygame.image.load('carro1.png')
        elif self.number == 1:
            self.image = pygame.image.load('carro2.png')

        initial_size = self.image.get_size()
        self.sq_size = sq_size
        size_rate = sq_size / initial_size[0]
        self.new_size = (int(self.image.get_size()[0] * size_rate), int(self.image.get_size()[1] * size_rate))
        self.image = pygame.transform.scale(self.image, self.new_size)
        self.rect = pygame.rect.Rect((pos_x * sq_size, pos_y * sq_size), self.image.get_size())

    def get_size(self):
        return self.new_size

    def moveto(self, new_x: int, new_y: int):
        self.rect.x = new_x * self.sq_size
        self.rect.y = new_y * self.sq_size
        # Keep visible
        self.dirty = 1

    def update(self, stub: client_stub.StubClient()):
        key = pygame.key.get_pressed()
        if self.number == 0:
            if key[pygame.K_a]:
                # pos = gm.execute(M_LEFT, "player", self.number)
                pos = stub.execute(M_LEFT, "player", self.number)
                if self.rect.x != pos[0]:
                    self.rect.x = pos[0] * self.sq_size
            if key[pygame.K_d]:
                # pos = gm.execute(M_RIGHT, "player", self.number)
                pos = stub.execute(M_RIGHT, "player", self.number)
                if self.rect.x != pos[0]:
                    self.rect.x = pos[0] * self.sq_size
            if key[pygame.K_w]:
                # pos = gm.execute(M_UP, "player", self.number)
                pos = stub.execute(M_UP, "player", self.number)
                if self.rect.y != pos[1]:
                    self.rect.y = pos[1] * self.sq_size
            if key[pygame.K_s]:
                # pos = gm.execute(M_DOWN, "player", self.number)
                pos = stub.execute(M_DOWN, "player", self.number)
                if self.rect.y != pos[1]:
                    self.rect.y = pos[1] * self.sq_size
        elif self.number == 1:
            if key[pygame.K_LEFT]:
                # pos = gm.execute(M_LEFT, "player", self.number)
                pos = stub.execute(M_LEFT, "player", self.number)
                if self.rect.x != pos[0]:
                    self.rect.x = pos[0] * self.sq_size
            if key[pygame.K_RIGHT]:
                # pos = gm.execute(M_RIGHT, "player", self.number)
                pos = stub.execute(M_RIGHT, "player", self.number)
                if self.rect.x != pos[0]:
                    self.rect.x = pos[0] * self.sq_size
            if key[pygame.K_UP]:
                # pos = gm.execute(M_UP, "player", self.number)
                pos = stub.execute(M_UP, "player", self.number)
                if self.rect.y != pos[1]:
                    self.rect.y = pos[1] * self.sq_size
            if key[pygame.K_DOWN]:
                # pos = gm.execute(M_DOWN, "player", self.number)
                pos = stub.execute(M_DOWN, "player", self.number)
                if self.rect.y != pos[1]:
                    self.rect.y = pos[1] * self.sq_size
        
        # Keep visible
        self.dirty = 1
