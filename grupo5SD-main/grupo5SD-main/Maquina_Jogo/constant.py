import logging

SERVER_ADDRESS = '127.0.0.1'
PORT = 8000

#Tipo de Mensagens
END = "fim"
X_MAX = "x max"
Y_MAX = "y max"
ADD_PLAYER =  "add player "
GET_PLAYERS = "get players"
GET_OBST =    "get obst   "
NR_PLAYERS =  "nr players "
NR_OBST =     "nr obst    "
PLAYER_MOV =  "player mov "
START_GAME =  "start game "
MESSAGE_SIZE = 40
N_BYTES = 10
STR_CODIFICATION = 'utf-8'
LOG_FILE_NAME = "game-server.log"
LOG_LEVEL = logging.DEBUG
ACCEPT_TIMEOUT = 1
NR_MAX_CLIENTS = 2