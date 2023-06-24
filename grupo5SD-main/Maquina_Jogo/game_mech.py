# GameMech
# GameMech

import time
import copy


# Defining constants for the moves
M_UP = 0
M_RIGHT = 1
M_DOWN = 2
M_LEFT = 3
TIME_STEP = 200 #in milliseconds

class GameMech :
    def __init__(self, x_max:int= 20, y_max:int = 20) -> None:
        '''
        Create a dictionary where each position will keep the elements that are in each position and
        a dictionary with player information (name, nr. of points, etc.)
        :param x_max:
        :param y_max:
        '''
        self._x_max = x_max
        self._y_max = y_max
        # List of players
        self._players = dict()
        # List of obstacles
        self._obstacles = dict()
        # Number of players and obstacles in the game

        self._nr_players = 0
        self._nr_obstacles = 0
        # Initializing each world's position with a list
        self._world = dict()
        for i in range(x_max):
            for j in range(y_max):
                self._world[(i, j)] = []
        # Add the obstacles to the world
        self.create_world()

    def add_obstacle(self, type:str, x_pos:int, y_pos:int) -> bool:
        '''
        Add obstacles to world
        :param name:
        :param x_pos:
        :param y_pos:
        :return:
        '''
        nr_obstacle = self._nr_obstacles
        self._obstacles[nr_obstacle] = [type, (x_pos, y_pos)]
        self._world[(x_pos, y_pos)].append(['obstacle', type, nr_obstacle, (x_pos, y_pos)])
        self._nr_obstacles += 1
        return True


    def create_world(self):
        '''
        Define the initial world with the position of the obstacles
        '''
        for x in range(0,self._x_max):
            for y in range(0,self._y_max):
                if x in (0,self._x_max - 1) or y in (0, self._y_max - 1):
                    self.add_obstacle("wall", x, y)
            obstacles = [(3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (3, 8), (3, 9), (3, 10), (3, 11),
                         (3, 12), (3, 13), (3, 14), (3, 15), (4, 15), (5, 15), (6, 15), (7, 15), (8, 15), (9, 15), (10, 15), (11, 15),
                         (12, 15), (13, 15), (14, 15), (15, 15), (16, 15), (3, 16), (4, 16), (5, 16), (6, 16), (7, 16),
                         (8, 16), (9, 16), (10, 16), (11, 16), (12, 16), (13, 16), (14, 16), (15, 16), (16, 16), (4, 3), (4, 4), (4, 5), (4, 6), (4, 7), (4, 8),
                         (4, 9), (4, 10), (4, 11), (4, 12), (4, 13), (4, 14), (4, 15), (4, 16), (5, 3), (5, 4),
                         (5, 5), (5, 6), (5, 7), (5, 8),(5, 9), (5, 10),(5, 11), (5, 12), (5, 13), (5, 14), (5, 15),
                         (5, 16), (16, 14), (16, 13), (16, 12), (16, 11), (15, 14), (15, 13), (15, 12), (15, 11), (14, 11),
                         (13, 11), (12, 11), (11, 11), (10, 11), (9, 11), (8, 11), (14, 12), (13, 12), (12, 12), (11, 12),
                         (10, 12), (9, 12), (8, 12), (8, 11), (8, 10), (8, 9), (8, 8), (8, 7), (8, 6), (8, 5), (8, 4), (8, 3),
                         (9, 11), (9, 10), (9, 9), (9, 8), (9, 7), (9, 6), (9, 5), (9, 4), (9, 3), (10, 3), (11, 3), (12, 3),
                         (13, 3), (14, 3), (15, 3), (16, 3), (10, 4), (11, 4), (12, 4), (13, 4), (14, 4), (15, 4), (16, 4),
                         (16, 7), (16, 8), (17, 7), (17, 8), (18, 7), (18, 8), (15, 8), (14, 8), (13, 8), (12, 8),
                         (15, 7), (14, 7), (13, 7), (12, 7), (6, 3), (6, 4), (6, 5), (6, 6), (6, 7), (6, 8), (6, 9),
                         (6, 10), (6, 11), (6, 12), (6, 13),(6, 14),(7,3), (7,4), (7,5), (7,6), (7,7), (7,8), (7,9),
                         (7,10), (7,11), (7,12), (7,13), (7,14),(8,13),(8,14) ,(9,13),(9,14) ,(10,13),(10,14),(11,13),(11,14) ,(12,13),(12,14),
                         (13,13),(13,14),(14,13),(14,14)]


        for obstacle in obstacles:
            self.add_obstacle("wall", obstacle[0], obstacle[1])


    def is_obstacle(self,type, x,y) -> bool:
        """
        Test if there is an obstacle of type in x,y
        :param type:
        :param x:
        :param y:
        :return:
        """
        for e in self._world[(x,y)]:
            if e[0] == 'obstacle' and e[1]==type:
                return True
        return False
    
    def colission(self,type, x,y) -> bool:
        for e in self._world[(x,y)]:
            if e[0] == 'player' and e[1]==type:
                return True
        return False

    def remove_player(self, nr_player) -> int:
        """
        Remove a player from players and world dictionary
        :param nr_player:
        :return:
        """
        if nr_player <= self._nr_players:
            name = self._players[nr_player][0]
            x_pos, y_pos = self._players[nr_player][1][0], self._players[nr_player][1][1]
            self._world[(x_pos, y_pos)].remove(['player',name,nr_player,(x_pos, y_pos)])
            self._players[nr_player]=[]
        return nr_player


    #
    # Each player has a specific time.
    #
    def add_player(self,name, x_pos:int, y_pos:int ) -> int:
        '''
        :param name: the name of the player
        :param x_pos:
        :param y_pos:
        :return: return the number of player
        '''
        nr_player = self._nr_players
        # Tick implementation
        # -------------------
        # We collect the actual time and keep it inside player definition.
        # Each player has its own tick because we are using the tick increment
        #
        tick = int( 1000 * time.time() ) # Milliseconds

        self.players[nr_player]=[ name, (x_pos, y_pos),tick]
        self._world[(x_pos, y_pos)].append(['player',name, nr_player,(x_pos, y_pos)])
        self._nr_players += 1
        return nr_player

    def execute(self,move: int, type:str, nr_player:int ) -> tuple:
        '''
        Execute the actions. Each new tic, the world execute the actions. The players must ask
        to print the actual world.
        :return:
        '''
        if type == "player":
            name = self._players[nr_player][0]
            pos_x, pos_y = self._players[nr_player][1][0], self._players[nr_player][1][1]
            # Collect previous player's tick.
            tick = self._players[nr_player][2]
            if move == M_LEFT:
                # New position
                new_pos_x = pos_x - 1
                new_pos_y = pos_y
                # if there is an obstacle
                if self.is_obstacle('wall', new_pos_x, new_pos_y):
                    new_pos_x = pos_x
                if self.colission('jose', new_pos_x, new_pos_y) or self.colission('joao', new_pos_x, new_pos_y) :
                    new_pos_x = pos_x
            elif move == M_RIGHT:
                # New position
                new_pos_x = pos_x + 1
                new_pos_y = pos_y
                if self.is_obstacle('wall', new_pos_x, new_pos_y):
                    new_pos_x = pos_x
                if self.colission('jose', new_pos_x, new_pos_y) or self.colission('joao', new_pos_x, new_pos_y):
                    new_pos_x = pos_x
            elif move == M_UP:
                # New position
                new_pos_y = pos_y - 1
                new_pos_x = pos_x
                if self.is_obstacle('wall', new_pos_x, new_pos_y):
                    new_pos_y = pos_y
                if self.colission('jose', new_pos_x, new_pos_y) or self.colission('joao', new_pos_x, new_pos_y):
                    new_pos_y = pos_y
            elif move == M_DOWN:
                # New position
                new_pos_y = pos_y + 1
                new_pos_x = pos_x
                if self.is_obstacle('wall', new_pos_x, new_pos_y):
                    new_pos_y = pos_y
                if self.colission('jose', new_pos_x, new_pos_y) or self.colission('joao', new_pos_x, new_pos_y):
                    new_pos_y = pos_y
            next_tick = int(time.time() * 1000 )
            # Test
            #print("Tick:",self.tick)
            #print("Next tick:",next_tick)
            # End test
            # If actual time plus TIME STEP value is bigger than last player's tick
            if (next_tick - tick) > TIME_STEP:
                tick = next_tick
                # Update world:
                self.players[nr_player] =[name, (new_pos_x, new_pos_y), tick]
                # Previous objects in the initial position before phanton moves
                world_pos = self._world[(pos_x, pos_y)]
                # Test
                #print("Removing player in the position ", pos_x, ",", pos_y,":",world_pos)
                #print("Name:",name)
                #print("Nr_player:",nr_player)
                # Removing object player in the previous position
                world_pos.remove(['player',name,nr_player, (pos_x,pos_y)])
                # Update the world with objects remaining in the position
                self._world[(pos_x, pos_y)] = world_pos
                self._world[(new_pos_x, new_pos_y)].append(['player',name,nr_player,(new_pos_x, new_pos_y)])
            else:
                # Revert the changes because there was no movement...
                new_pos_x = pos_x
                new_pos_y = pos_y
            return (new_pos_x, new_pos_y)

    #
    # setters & getters
    #
    @property
    def x_max(self) -> int:
        return self._x_max

    @property
    def y_max(self) -> int:
        return self._y_max

    @property
    def players(self) -> dict:
        return self._players

    @property
    def obstacles(self) -> dict:
        return self._obstacles

    @property
    def nr_obstacles(self) -> int:
        return self._nr_obstacles

    @property
    def nr_players(self):
        return self._nr_players


    #
    # Support and Test
    #
    def print_players(self):
        for p in self.players:
            print("Nr. ",p)
            print("Value:",self.players[p])

    def print_pos(self, x: int, y:int):
        print("(x= ",x,", y=", y, ") =", self._world[(x, y)])

    def print_world(self):
        for i in range(self._x_max):
            for j in range(self._y_max):
                print("(", i, ",", j, ") =", self._world[(i, j)])


# Testing the class
if __name__ == '__main__':
    gm = GameMech()
    gm.create_world()
    nr_player = gm.add_player('jose',2,2)
    print("Player jose has the number ",nr_player )
    # gm.add_player('maria',10,15)
    # gm.print_world()
    print("Before execution:")
    gm.print_pos(2,2)
    gm.print_pos(3,2)
    gm.print_pos(4,2)
    print("Execution to right...")
    gm.execute(M_RIGHT,"player",0)
    print("After first execution:")
    gm.print_pos(2,2)
    gm.print_pos(3,2)
    gm.print_pos(4,2)
    print("Execution to right...")
    gm.execute(M_RIGHT,"player",0)
    print("After second execution:")
    gm.print_pos(2,2)
    gm.print_pos(3,2)
    gm.print_pos(4,2)
    print("Sleep...")
    time.sleep(1)
    print("Execution to right twice...")
    gm.execute(M_RIGHT,"player",0)
    time.sleep(1)
    gm.execute(M_RIGHT,"player",0)
    print("After third execution:")
    gm.print_pos(2,2)
    gm.print_pos(3,2)
    gm.print_pos(4,2)
    gm.print_pos(5,2)
    gm.print_pos(6,2)

    #gm.print_players()
