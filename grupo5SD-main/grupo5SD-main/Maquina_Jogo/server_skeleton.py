import socket
import logging
from game_mech import GameMech
import constant
import client_session_management
from typing import Union


# Está no lado do servidor: Skeleton to user interface (permite ter informação
# de como comunicar com o cliente)
class SkeletonServer:

    def __init__(self, gm: GameMech):
        self.gm = gm
        self.s = socket.socket()
        self.s.bind((constant.SERVER_ADDRESS, constant.PORT))
        self.s.listen()
        #------------------------
        # Added timeout
        self.s.settimeout(constant.ACCEPT_TIMEOUT)
        #------------------------
        self.keep_running = True


    def accept(self) -> Union['Socket', None] :
        try:
            client_connection, address = self.s.accept()
            logging.info("O cliente com endereço " + str(address) + "ligou-se!")

            return client_connection
        except socket.timeout:
            return None

    def run(self):
        logging.info("a escutar no porto " + str(constant.PORT))
        while self.keep_running:
            socket_client = self.accept()
            if socket_client is not None:
               client_session_management.ClientSession (socket_client, self.gm).start()
            
        self.s.close()

        


logging.basicConfig(filename=constant.LOG_FILE_NAME,
                    level=constant.LOG_LEVEL,
                    format='%(asctime)s (%(levelname)s): %(message)s')
