from threading import Thread
from game_mech import GameMech
import constant
import json
import logging

import shared

# shr: shared.SharedServerState
class ClientSession(Thread):
    def __init__(self, socket_client: int, game_mech: GameMech, shr: shared.Shared):
        Thread.__init__(self)
        self._shared = shr
        self.socket_client = socket_client
        self._game_mech = game_mech

    def process_x_max(self,s_c):
        x = self._game_mech.x_max
        s_c.send(x.to_bytes(constant.N_BYTES, byteorder="big", signed=True))

    
    def process_y_max(self,s_c):
        y = self._game_mech.y_max
        s_c.send(y.to_bytes(constant.N_BYTES, byteorder="big", signed=True))

    def process_add_player(self, s_c):
        dados_rcv: bytes = s_c.recv(constant.MESSAGE_SIZE)
        name = dados_rcv.decode(constant.STR_CODIFICATION)
        number = self._game_mech.add_player(name, 1, 1)
        s_c.send(number.to_bytes(constant.N_BYTES, byteorder="big", signed=True))

    def process_get_players(self, s_c):
        pl = self._game_mech.players
        msg = json.dumps(pl)
        dim = len(msg)
        s_c.send(dim.to_bytes(constant.N_BYTES, byteorder="big", signed=True))
        s_c.send(msg.encode(constant.STR_CODIFICATION))

    def process_get_nr_players(self, s_c):
        nr_pl = self._game_mech.nr_players
        s_c.send(nr_pl.to_bytes(constant.N_BYTES, byteorder="big", signed=True))

    def process_get_obst(self, s_c):
        print("Get Obst")
        ob = self._game_mech.obstacles
        msg = json.dumps(ob)
        dim = len(msg)
        s_c.send(dim.to_bytes(constant.N_BYTES, byteorder="big", signed=True))
        s_c.send(msg.encode(constant.STR_CODIFICATION))

    def process_get_nr_obst(self, s_c):
        nr_ob = self._game_mech.nr_obstacles
        s_c.send(nr_ob.to_bytes(constant.N_BYTES, byteorder="big", signed=True))

    def process_player_mov(self, s_c):
        data: bytes = s_c.recv(constant.N_BYTES)
        mov = int.from_bytes(data, byteorder="big", signed= True)
        data: bytes = s_c.recv(constant.N_BYTES)
        nr_player = int.from_bytes(data, byteorder="big", signed=True)
        pos = self._game_mech.execute(mov, "player", nr_player)
        msg = json.dumps(pos)
        dim = len(msg)
        s_c.send(dim.to_bytes(constant.N_BYTES, byteorder="big", signed=True))
        s_c.send(msg.encode(constant.STR_CODIFICATION))

    def start_game(self, s_c):
        s_c.send()
        logging.debug("O cliente pretende iniciar o jogo")
        self._shared_clients_conn.acquire()
        logging.debug("O cliente vai iniciar o jogo")

        #returning "YES"
        value = constant.TRUE
        s_c.send(value.encode(constant.STR_CODE))

    def dispatch_request(self, socket_client) -> bool:
            lr = False
            #print("Inicio do ciclo...")
            dados_rcv = socket_client.recv(constant.MESSAGE_SIZE)
            data_str = dados_rcv.decode(constant.STR_CODIFICATION)
            if data_str == constant.X_MAX:
                self.process_x_max(socket_client)
            elif data_str == constant.Y_MAX:
                self.process_y_max(socket_client)
            elif data_str == constant.ADD_PLAYER:
                self.process_add_player(socket_client)
            elif data_str == constant.GET_PLAYERS:
                self.process_get_players(socket_client)
            elif data_str == constant.NR_PLAYERS:
                self.process_get_nr_players(socket_client)
            elif data_str == constant.GET_OBST:
                self.process_get_obst(socket_client)
            elif data_str == constant.NR_OBST:
                self.process_get_nr_obst(socket_client)
            elif data_str == constant.PLAYER_MOV:
                self.process_player_mov(socket_client)
            #Start the game...
            elif data_str == constant.START_GAME:
                self.process_start_game(self.client_connection)

            elif data_str == constant.END:
                lr = True
            return lr

    def run(self):
        with self.socket_client as client:
            last_request = False
            while not last_request:
                last_request = self.dispatch_request(self.socket_client)
            logging.debug("Client " + str(self.socket_client.peer_addr) + " disconnected")