import pygame
import game_mech

# Constantes
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

class Player(pygame.sprite.DirtySprite):
    def __init__(self, number: int, pos_x: int, pos_y: int, sq_size: int, *groups):
        super().__init__(*groups)
        self.image = pygame.image.load('carro1.png')
        initial_size = self.image.get_size()
        self.sq_size = sq_size
        size_rate = sq_size / initial_size[0]
        self.new_size = (int(self.image.get_size()[0] * size_rate), int(self.image.get_size()[1] * size_rate))
        self.image = pygame.transform.scale(self.image, self.new_size)
        self.rect = pygame.rect.Rect((pos_x * sq_size, pos_y * sq_size), self.image.get_size())
        self.number = number

    def get_size(self):
        return self.new_size

    def moveto(self, new_x: int, new_y: int):
        self.rect.x = new_x * self.sq_size
        self.rect.y = new_y * self.sq_size
        # Keep visible
        self.dirty = 1

    def update(self, gm: game_mech.GameMech):
        last = self.rect.copy()
        keys = pygame.key.get_pressed()

        # Para qualquer tecla, há que pedir ao Game Mech que nova posição
        # o jogador ocupa
        # Movimento do jogador com as teclas AWSD
        if self.number == 0:
            if keys[pygame.K_a]:
                new_x, new_y = gm.execute(self.number, gm.LEFT)
                self.rect.x = new_x * self.sq_size
                self.rect.y = new_y * self.sq_size
            elif keys[pygame.K_d]:
                new_x, new_y = gm.execute(self.number, gm.RIGHT)
                self.rect.x = new_x * self.sq_size
                self.rect.y = new_y * self.sq_size
            elif keys[pygame.K_w]:
                new_x, new_y = gm.execute(self.number, gm.UP)
                self.rect.x = new_x * self.sq_size
                self.rect.y = new_y * self.sq_size
            elif keys[pygame.K_s]:
                new_x, new_y = gm.execute(self.number, gm.DOWN)
                self.rect.x = new_x * self.sq_size
                self.rect.y = new_y * self.sq_size

        # Movimento do jogador com as setas
        if self.number == 1:
            if keys[pygame.K_LEFT]:
                new_x, new_y = gm.execute(self.number, gm.LEFT)
                self.rect.x = new_x * self.sq_size
                self.rect.y = new_y * self.sq_size
            elif keys[pygame.K_RIGHT]:
                new_x, new_y = gm.execute(self.number, gm.RIGHT)
                self.rect.x = new_x * self.sq_size
                self.rect.y = new_y * self.sq_size
            elif keys[pygame.K_UP]:
                new_x, new_y = gm.execute(self.number, gm.UP)
                self.rect.x = new_x * self.sq_size
                self.rect.y = new_y * self.sq_size
            elif keys[pygame.K_DOWN]:
                new_x,new_y = gm.execute(self.number, gm.DOWN)
                self.rect.x = new_x * self.sq_size
                self.rect.y = new_y * self.sq_size

            # Verificar colisão com outros jogadores
        for player in gm.players:
            if player.number != self.number and self.rect.colliderect(player.rect):
                self.rect = last
                break
