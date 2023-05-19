import socket
from typing import Union
import constant
import json


# Stub do lado do cliente: como comunicar com o servidor...

class StubClient:

    def __init__(self):
        self.s: socket = socket.socket()
        self.s.connect((constant.SERVER_ADDRESS, constant.PORT))

    def get_players(self) -> dict:
        """
        Protocolo:
        -- Envia tipo de msg "get_players"
        -- Receber dimensão do objeto dicionario
        -- Recebe objeto com um dicionario com todos os jogadores
        :return:
        """
        msg = constant.GET_PLAYERS
        self.s.send((msg.encode(constant.STR_CODIFICATION)))
        data: bytes = self.s.recv(constant.N_BYTES)
        dim = int.from_bytes(data, byteorder='big', signed=True)
        rec: bytes = self.s.recv(dim)
        players = json.loads(rec)
        return players

    def get_nr_players(self):
        msg = constant.NR_PLAYERS
        self.s.send((msg.encode(constant.STR_CODIFICATION)))
        data: bytes = self.s.recv(constant.N_BYTES)
        nr = int.from_bytes(data, byteorder='big', signed=True)
        return nr

    def add_player(self, name:str) -> int:
        '''
        Protocolo:
        - enviar msg com o nome associado ao pedido 'add player'
        - enviar o nome do jogador
        - receber o numero do jogador
        :param name:
        :return:
        '''
        msg = constant.ADD_PLAYER
        self.s.send((msg.encode(constant.STR_CODIFICATION)))
        msg = name
        self.s.send(msg.encode(constant.STR_CODIFICATION))
        data: bytes = self.s.recv(constant.N_BYTES)
        number = int.from_bytes(data, byteorder='big', signed=True)
        return number

    def get_dim_game(self) -> tuple:
        """
        Protocolo: 
        - Enviar mensagem com o nome associado ao pedido max_x e max_y
        - Servidor retorna dois inteiros com essa informação
        :return:
        """
        msg = constant.X_MAX
        self.s.send(msg.encode(constant.STR_CODIFICATION))
        print("Client sent message:", msg)
        data: bytes = self.s.recv(constant.N_BYTES)
        print("DATA:", data)
        X_MAX = int.from_bytes(data, byteorder='big',signed=True)
        msg = constant.Y_MAX
        self.s.send(msg.encode(constant.STR_CODIFICATION))
        data: bytes = self.s.recv(constant.N_BYTES)
        Y_MAX = int.from_bytes(data, byteorder='big',signed=True)
        return (X_MAX, Y_MAX)

    def get_obstacles(self) -> dict:
        '''
        Protocolo:
        -- Envio tipo de msg "get obst"
        -- Recebe dimensao do objeto dicionario
        -- Recebe objeto dicionario com todos os obstaculos
        :return:
        '''
        msg = constant.GET_OBST
        self.s.send(msg.encode(constant.STR_CODIFICATION))
        data: bytes = self.s.recv(constant.N_BYTES)
        dim = int.from_bytes(data, byteorder='big', signed=True)
        rec: bytes = self.s.recv(dim)
        obst = json.loads(rec)
        return obst

    def get_nr_obstacles(self):
        msg = constant.NR_OBST
        self.s.send(msg.encode(constant.STR_CODIFICATION))
        data: bytes = self.s.recv(constant.N_BYTES)
        nr = int.from_bytes(data, byteorder='big', signed=True)
        return nr

    def execute(self, mov:int, type: str, player:int) -> tuple:
        '''
        Protocolo:
        -- Envia o tipo de msg "player mov"
        -- Envia o movimento
        -- Envia o nr do jogador
        -- Recebe a nova posição do jogador (tuple) que é estrutura de dados complexa
        ------ recebe primeiro a dimensao da estrutura de dados
        ------ recebe a estrutura (tuple)
        :param mov:
        :param type:
        :param player:
        :return:
        '''
        msg = constant.PLAYER_MOV
        self.s.send(msg.encode(constant.STR_CODIFICATION))
        self.s.send(mov.to_bytes(constant.N_BYTES, byteorder="big", signed=True))
        self.s.send(player.to_bytes(constant.N_BYTES, byteorder="big", signed=True))
        data: bytes = self.s.recv(constant.N_BYTES)
        dim = int.from_bytes(data, byteorder="big", signed=True)
        rec: bytes = self.s.recv(dim)
        tuple = json.loads(rec)
        return tuple

    '''
    def add(self, value1: int, value2: int) -> Union[int, None]:

        msg = constant.SOMA
        self.s.send(msg.encode(constant.CODIFICACAO_STR))
        self.s.send(value1.to_bytes(constant.N_BYTES, byteorder="big", signed=True))
        self.s.send(value2.to_bytes(constant.N_BYTES, byteorder="big", signed=True))
        dados_recebidos: bytes = self.s.recv(constant.N_BYTES)
        return int.from_bytes(dados_recebidos, byteorder='big', signed=True)
        #if msg != constante.FIM:
        #    dados_recebidos: bytes = self.s.recv(constante.TAMANHO_MENSAGEM)
        #    return dados_recebidos.decode(constante.CODIFICACAO_STR)
        #else:
        #    self.s.close()
    '''