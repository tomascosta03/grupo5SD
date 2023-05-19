import pygame
import player8

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

class GameMech:

    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    def __init__(self, nr_max_x: int, nr_max_y: int):
        self.world = dict()
        self.players = pygame.sprite.LayeredDirty()
        self.walls = dict()
        self.x_max = nr_max_x
        self.y_max = nr_max_y
        for x in range(nr_max_x):
            for y in range(nr_max_y):
                self.world[(x, y)] = []
        # Criar paredes à volta do mundo
        nr_walls = 0
        for x in range(0, self.x_max):
            for y in range(0, self.y_max):
                if x in (0, self.x_max - 1) or y in (0, self.y_max - 1):
                    self.walls[nr_walls] = ["wall", (x, y)]
                    self.world[(x, y)].append(["obst", "wall", nr_walls])
                    nr_walls += 1
        # Criar jogador
        self.players.add(player8.Player(0, 1, 1, 32))
        self.world[(1, 1)].append(["player", "jose", 0])
        self.players.add(player8.Player(1, 2, 2, 32))
        self.world[(2, 2)].append(["player", "manuel", 1])

    def execute(self, nr_player: int, direction: int) -> tuple:
        player_list = list(self.players.sprites())  # Obter a lista de jogadores
        player = player_list[nr_player]  # Obter o jogador específico pelo índice
        x, y = player.rect.x, player.rect.y
        name = player.name
        if direction == UP:
            new_x = x
            new_y = y - 1
        elif direction == DOWN:
            new_x = x
            new_y = y + 1
        elif direction == LEFT:
            new_x = x - 1
            new_y = y
        elif direction == RIGHT:
            new_x = x + 1
            new_y = y

        if self.is_wall_at_position(new_x, new_y):
            return (x, y)

        if ["player", name, nr_player] in self.world[(x, y)]:
            self.world[(x, y)].remove(["player", name, nr_player])

        self.world[(new_x, new_y)].append(["player", name, nr_player])
        self.players[nr_player] = [name, (new_x, new_y)]
        return (new_x, new_y)


    def is_wall_at_position(self, x: int, y: int) -> bool:
        return any(cell[1] == (x, y) for cell in self.walls.values())

    def is_player_at_position(self, x: int, y: int) -> bool:
        return any(player.rect.x // 32 == x and player.rect.y // 32 == y for player in self.players.sprites())

    def print_position(self, x: int, y: int):
        print("Position (", x, ",", y, "):", self.world[(x, y)])

    def print_world(self):
        for x in range(0, self.x_max):
            for y in range (0, self.y_max):
                print("(", x, ",", y, ")=", self.world[(x, y)])
