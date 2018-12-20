# Created by glendal at 20/12/18

import sys


def usage():
    print("TODO usage")


def main(argv):
    print("Hello")


if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(sys.argv[1:])
    else:
        usage()
        sys.exit(2)