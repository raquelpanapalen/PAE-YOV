# Utils file for python scripts
import sys


# Some ANSI escape sequences for colors, and end
CC_RED = '\033[0;31m'
CC_GREEN = '\033[0;32m'
CC_YELLOW = '\033[0;33m'
CC_END = '\033[0m'

EC_ERROR = 1


# Basic logging
def info(m: str) -> None:
    print(f'{CC_GREEN}[I]{CC_END} {m}')

def warn(m: str) -> None:
    print(f'{CC_YELLOW}[W]{CC_END} {m}')


def error(m: str) -> None:
    print(f'{CC_RED}[E]{CC_END} {m}')
    sys.exit(EC_ERROR)

