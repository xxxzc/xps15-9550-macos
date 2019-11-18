from platform import system
from utils.path import Dst
import os
from pathlib import Path

iswin = system() == 'Windows'

colors = {
    'idx': 172, 'path': 39, 'lv': 204, 'rv': 70, 'info': 245
}


def fg(text, color):
    # Q: How do I print colored output with Python 3?
    # A: https://stackoverflow.com/a/56774969
    if type(color) == str:
        color = colors[color]
    return "\33[38;5;{}m{}\33[0m".format(color, text)


PREFIX = fg('::', 75)
ARROW = fg('==>', 40)


def executable(program):
    '''Make program executable
    '''
    if iswin:
        program = str(program)
        if program.endswith('macserial'):
            program += '32'
        program += '.exe'

    if not Path(program).exists():
        print(program, 'not found, downloading...')
        os.system('python {} {}'.format(
            Dst('Script', 'update_package.py'),
            program))

    if not iswin:
        os.system('chmod +x {}'.format(program))

    return program


def Confirm(msg):
    r = input(ARROW + ' ' + msg + '(Y/n)')
    return 'n' not in r.lower()


def Title(*args):
    print(PREFIX, *args)


def Input(msg):
    return input(ARROW + ' ' + msg)


def Exit(*args):
    print(PREFIX, *args)
    exit(0)
