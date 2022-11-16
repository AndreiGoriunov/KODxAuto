import logging

import pyautogui as pag

from .step_definitions import *
from .step_handler import get_step_map

macros_resources_dir = ""


class Executor:
    """Class for executing the macros steps.

    Initialized with a list of steps.
    """

    def __init__(self, steps: list, step_defs: list = None):
        self.steps = steps
        # macros_resources_dir = os.path.join(macros_directory, "resources")
        logging.info("Executor initialized.")

    # def __import_step_definitions(self):
    #     if self.step_defs:
    #         for step_def in self.step_defs:
    #             __import__(step_def)

    def execute(self):
        logging.info(f"regex_to_function_map = {get_step_map()}")
        for i, step in enumerate(self.steps):
            try:
                eval(step)
            except Exception:
                logging.error(f"Step {i}: failed - {step}")
                raise Exception(f"Step {i}: failed - {step}")
