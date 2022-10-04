from time import sleep

import pyautogui as pg

from lib import kblr, parser

running = False

def start(file_path: str):
    macro = parser.parse(file_path)
    macro_len = len(macro['steps'])

    # Debug
    print(f'Macros: {file_path}')
    print(f'Number of steps: {macro_len}')
    print('Ready. Press <Home> to start execution.')

    kblr.listen()

    while (kblr.bindPressed):
        print('Waiting.')
        sleep(1)

    steps = macro['steps']
    executor(steps)


def executor(steps: list):
    for step in steps:
        eval(f'pg.{step}')
