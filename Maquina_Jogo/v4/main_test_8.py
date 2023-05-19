import pygame
import player8
import wall8
import game_mech

# ---------------------
# The grid now is built based on the number of squares in x and y.
# This allows us to associate the size of the space to a matrix or to a dictionary
# that will keep data about each position in the environment.
# Moreover, we now can control the movement of the objects.
class Game(object): 
    def __init__(self, x_nr_sq:int = 40, y_nr_sq:int = 40, grid_size:int  = 40):
        self.x_max = x_nr_sq
        self.y_max = y_nr_sq
        self.width, self.height = x_nr_sq * grid_size, y_nr_sq * grid_size
        self.screen = pygame.display.set_mode((self.width,self.height))
        pygame.display.set_caption("first game")
        self.clock = pygame.time.Clock()
        # RGB colours
        self.grey = (125, 125, 125)
        self.black = (0, 0, 0)
        # Grid
        self.grid_size = grid_size
        grid_colour = self.black
        # Create The Backgound
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill(self.grey)
        self.screen.blit(self.background,(0,0))
        self.draw_grid(self.black)
        # Atenção: O Game deveria pedir dimensões do jogo ao GameMech e
        # não o contrário. Portanto, GameMech deverá ser gerado fora do
        # Game.
        self.gm = game_mech.GameMech(self.x_max, self.y_max)
        pygame.display.update()


    # Drawing a square grid
    def draw_grid(self, colour:tuple):

        for x in range(0, self.x_max):
            pygame.draw.line(self.screen, colour, (x * self.grid_size,0), ( x * self.grid_size, self.height))
        for y in range(0,self.y_max):
            pygame.draw.line(self.screen, colour, (0, y * self.grid_size), (self.width, y * self.grid_size))

    def create_players(self,size:int) -> None:
        #self.players = pygame.sprite.Group()
        self.players = pygame.sprite.LayeredDirty()
        # Atenção, os jogadores têm de ser criados pelo GameMech e só depois
        # gerados aqui pelo Game
        self.playerA = player8.Player(0, 1,1,size,self.players)
        self.playerB = player8.Player(1, 2,2,size,self.players)
        self.players.add(self.playerA)
        self.players.add(self.playerB)

    def create_walls(self, wall_size:int):
        # Create Wall (sprites) around world
        self.walls = pygame.sprite.Group()
        for x in range(0,self.x_max):
            for y in range(0,self.y_max):
                if x in (0,self.x_max - 1) or y in (0, self.y_max - 1):
                    w = wall8.Wall(x,y,wall_size,self.walls)
                    self.walls.add(w)
        # More walls
        w = wall8.Wall(20,20,wall_size,self.walls)
        w = wall8.Wall(21,20,wall_size,self.walls)
        self.walls.add(w)

    def run(self):
        #Create Sprites
        self.create_walls(self.grid_size)
        self.walls.draw(self.screen)
        self.create_players(self.grid_size)
        end = False
        while end == False:
            dt = self.clock.tick(10)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    end = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    end = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                    self.playerB.moveto(1,1)
            self.players.update(self.gm)
            #self.walls.update(dt / 1000.)
            #self.screen.fill((200,200,200))
            rects = self.players.draw(self.screen)
            #self.walls.draw(self.screen)
            #pygame.display.flip()
            self.draw_grid(self.black)
            pygame.display.update(rects)
            self.players.clear(self.screen,self.background)

        return
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    pygame.init()
    gm = Game(40,40,25)
    gm.run()

