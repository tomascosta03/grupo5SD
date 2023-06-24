import pygame
import client_stub
import player10, wall10, game_mech

class Game(object):
    def __init__(self, stub: client_stub.StubClient, grid_size:int  = 20):
        print("Starting game...")
        xymax = stub.get_dim_game()
        #print(xymax)
        # Next step will be:
        # self.x_max = stub_obj.get_x_max()
        self.x_max = xymax[0]
        self.y_max = xymax[1]
        self.width, self.height = self.x_max * grid_size, self.y_max * grid_size
        self.screen = pygame.display.set_mode((self.width,self.height))
        pygame.display.set_caption("Jogo de Rally")
        self.clock = pygame.time.Clock()
        # RGB colours
        self.grey = (125,125,125)
        self.black = (0, 0, 0)
        # Grid
        self.grid_size = grid_size
        # Create The Backgound
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill(self.grey)
        self.screen.blit(self.background,(0,0))
        self.draw_grid(self.black)
        self.stub = stub
        pygame.display.update()


    # Drawing a square grid
    def draw_grid(self, colour:tuple):
        for x in range(0, self.x_max):
            pygame.draw.line(self.screen, colour, (x * self.grid_size,0), ( x * self.grid_size, self.height))
        for y in range(0,self.y_max):
            pygame.draw.line(self.screen, colour, (0, y * self.grid_size), (self.width, y * self.grid_size))



    def set_players(self):
        self.pl = self.stub.get_players()
        nr_players = self.stub.get_nr_players()
        self.players = pygame.sprite.LayeredDirty()
        # Test
        print("Game2, Nr. of players:", nr_players)
        print("Game2, Players:", self.pl)
        for nr in range(nr_players):
            if self.pl[str(nr)] != []:
                    # Test
                    print("Game2, Player added:", nr)
                    p_x, p_y  = self.pl[str(nr)][1][0], self.pl[str(nr)][1][1]
                    player = player10.Player(nr, self.pl[str(nr)][0], p_x, p_y, self.grid_size, self.players)
                    self.players.add(player)


    def set_walls(self, wall_size:int):
        # self.wl = self.gm.obstacles
        print("Pergunto por obstaculos")
        self.wl = self.stub.get_obstacles()
        print("Recebi msg do servidor sobre obstaculos")
        # Create Wall (sprites) around world
        self.walls = pygame.sprite.Group()
        # nr_obstacles = self.gm.nr_obstacles
        nr_obstacles = self.stub.get_nr_obstacles()
        for nr in range(nr_obstacles):
            if self.wl[str(nr)] != []:
                w_x, w_y = self.wl[str(nr)][1][0], self.wl[str(nr)][1][1]
                wall = wall10.Wall(w_x, w_y, self.grid_size, self.walls)
                self.walls.add(wall)

    def run(self):
        nome = input("Por favor, qual é o seu nome?")
        self.stub.add_player(nome)
        self.set_walls(self.grid_size)
        self.walls.draw(self.screen)

        self.set_players()
        end = False
        while end == False:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    end = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    end = True
            self.walls.update()
            self.players.update(self.stub)
            rects = self.players.draw(self.screen)
            self.draw_grid(self.black)
            pygame.display.update(rects)
            self.players.clear(self.screen, self.background)
        return True
