import logging
import os.path
import sys

import pyautogui as pg
from yaml import YAMLError, safe_load

# Static
DIRNAME = os.path.dirname(os.path.abspath(__file__))
STATUSES = {0: 'running', 1: 'complete', 2: 'error'}

# Configure logging
logging.basicConfig(filename=os.path.join(DIRNAME, '..\\run.log'), filemode='w', level=logging.DEBUG, encoding='utf-8',
                    format='%(asctime)s [%(levelname)s]: %(message)s', datefmt='%H:%M:%S')


class KODxAuto:
    """Main framework automation class"""

    def __init__(self, file_path):
        logging.info('KODxAuto Started.')
        self.file_path = file_path
        self._steps = None
        self._config = None
        self.__path = None
        self.__parse()
        logging.info('KodXAuto Initialized.')

    def start(self):
        # Print box
        text = f'Macro: {self.file_path}\nNumber of steps: {len(self._steps)}'
        print_msg_box(msg=text, title='KODXAuto')
        executor = self.Executor(self._steps)
        executor.execute_all()

    def __parse(self):
        macro = None
        if (os.path.exists(f'{self.file_path}\\macro.yaml')):
            logging.info('Using absolute macros path.')
            self.__path = f'{self.file_path}'
        elif (os.path.exists(os.path.join(DIRNAME, f'..\\macros\\{self.file_path}\\macro.yaml'))):
            logging.info('Using relative macros path.')
            self.__path = os.path.join(
                DIRNAME, f'..\\macros\\{self.file_path}')
        else:
            raise FileNotFoundError(
                'The specified folder does not contain macro.yaml file')

        # Read macro.yaml file
        if self.__path:
            with open(f'{self.__path}\\macro.yaml', 'r', encoding='utf-8') as stream:
                try:
                    macro = safe_load(stream)
                except YAMLError as exc:
                    logging.error(exc)

        # Set variables
        self._steps = macro['steps']
        self._config = macro['config']

    class Executor:
        """A class for executing steps from a list"""

        def __init__(self, steps: list):
            self.steps = steps
            self.step = None
            self.__SENTINEL = str(object())
            self.TOTAL_STEPS = len(self.steps)
            self.step_iter = 0
            self.__status = 0
            logging.info('Executor Initialized.')

        @property
        def status(self):
            return STATUSES.get(self.__status)

        def __repr__(self) -> str:
            return f'Executor({self.steps!r})'

        def __str__(self, all=False) -> str:
            if (all):
                return f'''Executor:
                Steps: {self.steps}
                Current Step: {self.step}
                Status: {self.status}
                '''
            else:
                return f'''Executor:
                Current Step: {self.step}
                Status: {self.status}
                '''

        def next_step(self) -> bool:
            '''Sets self.step with the next step from self.steps'''
            if (self.step_iter < self.TOTAL_STEPS):
                self.step = self.steps[self.step_iter]
                self.step_iter += 1
                return True
            else:
                self.step = self.__SENTINEL
                return False

        def execute_all(self):
            logging.info('Execution started.')
            print('Steps:')
            while (self.next_step()):
                # Visual execution step information
                print(self.step, end='')
                sys.stdout.flush()
                try:
                    # Executing step action
                    eval(f'pg.{self.step}')
                    logging.info(
                        f'Step [{self.step_iter:}]: {self.step}. Success.')
                    print(' - Success.')
                except Exception as exc:
                    logging.error(
                        f'Step [{self.step_iter}]: {self.step}. Error: {exc}.')
                    print(f' - Failure.\nError: {exc}')
                    self.__status = 2

                if (self.__status != 0):
                    logging.error('Execution aborted.')
                    return

            self.__status = 1
            logging.info('Execution complete.')


class KB_Listener():
    def __init__():
        pass


def print_msg_box(msg, indent=1, width=None, title=None):
    """Print message-box with optional title."""
    lines = msg.split('\n')
    space = " " * indent
    if not width:
        width = max(map(len, lines))
    box = f'╔{"═" * (width + indent * 2)}╗\n'  # upper_border
    if title:
        box += f'║{space}{title:<{width}}{space}║\n'  # title
        box += f'║{space}{"-" * len(title):<{width}}{space}║\n'  # underscore
    box += ''.join([f'║{space}{line:<{width}}{space}║\n' for line in lines])
    box += f'╚{"═" * (width + indent * 2)}╝'  # lower_border
    print(box)
