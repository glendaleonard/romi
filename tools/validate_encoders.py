# Project: romi 
# File: validate_encoders.py
# Created by glendal at 2018-12-20 4:45 PM

import sys
from a_star import AStar


def usage():
    print("TODO usage")


def main(argv):
    a_star = AStar()

    encoders = a_star.read_encoders()
    print(encoders)


if __name__ == '__main__':
    # if len(sys.argv) > 1:
    main(sys.argv[1:])
    # else:
    #    usage()
    #    sys.exit(2)
