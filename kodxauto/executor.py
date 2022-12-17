import logging

import pyautogui as pag

from .step_definitions import *
from .step_handler import get_step_map


class Executor:
    """Class for executing the macros steps.

    Initialized with a list of steps.
    """

    def __init__(self, steps: list, step_defs: list = None):
        self.steps = steps
        # macros_resources_dir = os.path.join(macros_directory, "resources")
        logging.info("Executor initialized.")

    def execute(self):
        logging.info(f"regex_to_function_map = {get_step_map()}")
        for i, step in enumerate(self.steps):
            try:
                # Attempt to execute the step
                logging.info(f"Executing step: {step}{(arg for arg in step[1])}")
                step[0](*step[1])
            except Exception:
                logging.error(f"Step {i}: failed - {step}")
                raise Exception(f"Step {i}: failed - {step}")
