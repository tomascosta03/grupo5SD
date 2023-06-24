import threading
import constant
from game_mech import GameMech
from socket import socket

class Shared():
    def __init__(self, game_mech: GameMech):
        self.gm: GameMech = game_mech
        # Um conjunto nao permite ter clientes iguais. No conjunto iremos guardar os socket dos clientes.
        self._clients: set[socket] = set()
        self._clients_lock = threading.Lock()
        # Semaforo impedindd os clientes de passar
        self._clients_control = threading.Semaphore()

    def add_client(self, client: socket) -> None:
        '''
        Adiciona um cliente à lista de clientes de forma protegida
        :param client:
        :return:
        '''
        self._clients_lock.acquire()
        self._clients.add(client)
        self._clients_lock.release()

    def remove_client(self, client_socket: socket) -> None:
        '''

        :param client_socket:
        :return:
        '''
        self._clients_lock.acquire()
        self._clients.remove(client_socket)
        if len(self._clients) < constant.NR_MAX_CLIENTS:
            self._clients_control.release()
        self._clients_lock.release()


    def control_nr_clients(self):
        if len(self._clients) >= constant.NR_MAX_CLIENTS:
            print("Nr client is", len(self._clients))
            for i in range(len(self._clients)):
                self._clients_control.release()

