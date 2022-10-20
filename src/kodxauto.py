from asyncio.log import logger
import logging
from threading import Thread
import os
import time

from behave.__main__ import main as behave_main

STATUSES = {0: "running", 1: "complete", 2: "error"}


class KODXAuto:
    """KODXAuto automation class.
    Initialized with abs directory path to the runner.py
    set other required parameters with"""

    def __init__(self, dir_name: str):
        self.dir_name = dir_name
        self.macros_name = None
        self.args = None

    def set_macros_name(self, macros_name: str):
        self.macros_name = macros_name

    def set_args(self, args: list):
        """Set additional arguments for behave"""
        self.args = args

    def run(self):
        if not self.macros_name:
            logger.error("Missing required macros_name argument")

        logging.info(
            f"Framework Home: {self.dir_name} macros_name: {self.macros_name} args: {self.args}"
        )
        _path = f"features/{self.macros_name}.feature"
        macros = Thread(target=self.executor, args=(_path,))
        macros.start()

    def executor(self, _path: str):
        logging.info("Execution thread started")
        behave_main(_path)
        logging.info("Execution thread finished")
