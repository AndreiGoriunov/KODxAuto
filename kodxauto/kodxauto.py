import logging
import os.path
from configparser import ConfigParser
from time import perf_counter

from .executor import Executor
from .step_handler import StepParser

true_options = ("1", "true", "True")


class KODxAuto:
    """KODXAuto automation class."""

    def __init__(self):
        self.config = {}
        self.root_abs_path = ""

    def __str__(self):
        return f"config = {self.config}, root_abs_path = {self.root_abs_path}"

    def set_root_dir(self, root_dir: str) -> None:
        """Required. Set a directory where the `kodxauto.properties` is located.
        Required before calling run() method.

        `kodxauto.properties` should be placed in the root directory of the project."""

        # Get the absolute path to the directory containing kodxauto.properties
        self.root_abs_path = os.path.abspath(root_dir)

        # Get abs path to the kodxauto.properties file
        self.config_path = os.path.join(self.root_abs_path, "kodxauto.properties")
        self.__set_config_file()
        self.__set_logger()

    def set_properties(self, **props) -> None:
        """Optional. Used to set or overwrite config file properties.
        Available properties:
        - macros_folder_path (str)
        - log_file_path (str)
        - custom_step_definitions_paths (list of str)
        - macro_name (str)
        """
        for key, value in props.items():
            self.config[key] = value

    def run(self, macro_name=None):
        if not macro_name:
            if ("macro_name" not in self.config) or (self.config["macro_name"] == ""):
                logging.error(
                    "macro_name is not defined. Define macro_name in kodxauto.properties or pass it as an argument."
                )
                raise Exception(
                    "macro_name is not defined. Define macro_name in kodxauto.properties or pass it as an argument."
                )
            else:
                macro_name = self.config["macro_name"]

        # Path to the macros directory containing steps
        _path = os.path.join(
            self.root_abs_path, self.config["macros_folder_path"], macro_name
        )

        # Check "recompile" config property
        bf_parse = perf_counter()  # timer before parse/read
        if (self.config["recompile"] != "") and self.config[
            "recompile"
        ] in true_options:
            steps = StepParser(_path).parse_steps()
            logging.info(f"Parsed steps: {steps}")
        else:
            steps = StepParser(_path).read_parsed_steps()
            logging.info(f"Read steps: {steps}")
        af_parse = perf_counter()  # timer after parse/read

        # Calling Executor
        bf_exec = perf_counter()  # timer before execution
        executor = Executor(steps)
        executor.execute()
        af_exec = perf_counter()  # timer after execution

        logging.info("Execution complete")
        logging.info(f"Parsing/reading took  : {af_parse - bf_parse:.4f}")
        logging.info(f"Execution took: {af_exec - bf_exec:.4f}")

    def __set_config_file(self):
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(
                f"kodxauto.properties was not found on the given path: {self.config_path}"
            )

        # get config file and store it in self.config dictionary
        _config_parser = ConfigParser()
        _config_parser.read(self.config_path)
        self.config = dict(_config_parser.items("settings"))

    def __set_logger(self):
        """Initialize the logger"""
        logging.basicConfig(
            filename=self.config["log_file_path"],
            filemode="w",
            level=logging.INFO,
            encoding="utf-8",
            format="%(asctime)s [%(levelname)-5s] (%(module)-12s): %(message)s",
            datefmt="%H:%M:%S",
        )
        logging.info("Logging initialized.")
