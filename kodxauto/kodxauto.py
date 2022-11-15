import logging
import os.path
from configparser import ConfigParser
from time import perf_counter

from .executor import Executor
from .step_handler import StepParser


class KODxAuto:
    """KODXAuto automation class."""

    def __init__(self):
        self.properties = {}
        self.root_abs_path = ""

    def __str__(self):
        return f"properties = {self.properties}, root_abs_path = {self.root_abs_path}"

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
        """Optional. Used to set or overwrite properties file properties.
        Available properties:
        - macros_folder_path (str)
        - log_file_path (str)
        - custom_step_definitions_paths (list of str)
        - macro_name (str)
        """
        for key, value in props.items():
            self.properties[key] = value

    def get_property(self, property_name: str) -> str | bool:
        """Getter for properies."""
        true_options = ("1", "true", "True")
        false_options = ("0", "false", "False")
        if not self.properties:
            _error = "self.properties is empty. No properties were set."
            logging.error(_error)
            raise Exception(_error)
        property_value = None
        try:
            property_value = self.properties[property_name]
        except KeyError:
            _error = f'There is no propery with the key "{property_name}" set.'
            logging.error(_error)
            raise KeyError(_error)

        if property_value in true_options:
            return True
        elif property_value in false_options:
            return False
        elif property_value == "":
            return None
        else:
            return str(property_value)

    def run(self, macro_name=None):
        macro_name = self.get_property("macro_name")

        # Path to the macros directory containing steps
        _path = os.path.join(
            self.root_abs_path, self.get_property("macros_folder_path"), macro_name
        )

        # Check "recompile" property
        recompile = self.get_property("recompile")

        # If property is set to true or not set at all then recompile
        bf_parse = perf_counter()  # timer before parse/read
        if recompile is None or recompile:
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
            _error = f"kodxauto.properties was not found on the given path: {self.config_path}"
            raise FileNotFoundError(_error)

        # get properties file and store it in self.properties dictionary
        _config_parser = ConfigParser()
        _config_parser.read(self.config_path)
        self.properties = dict(_config_parser.items("settings"))

    def __set_logger(self):
        """Initialize the logger"""
        logging.basicConfig(
            filename=self.get_property("log_file_path"),
            filemode="w",
            level=logging.INFO,
            encoding="utf-8",
            format="%(asctime)s [%(levelname)-5s] (%(module)-12s): %(message)s",
            datefmt="%H:%M:%S",
        )
        logging.info("Logging initialized.")
