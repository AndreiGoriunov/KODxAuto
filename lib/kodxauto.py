import pyautogui as pg

from lib import parser
from lib import kblr

def start(file_path: str):
    macro = parser.parse(file_path)
    macro_len = len(macro['steps'])
    print(f'Macros: {file_path}')
    print(f'Number of steps: {macro_len}')
    print('Ready. Press <Home> to start execution.')
    steps = macro['steps']
    executor(steps)
    
def executor(steps: list):
    for step in steps:
        execute(step)

def execute(step: str) -> bool:
    eval(f'pg.{step}')
    return True
