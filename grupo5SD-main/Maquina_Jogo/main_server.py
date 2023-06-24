from game_mech import GameMech
from server_skeleton import SkeletonServer


def main():
    gmech = GameMech()
    skeleton = SkeletonServer(gmech)
    skeleton.run()


main()