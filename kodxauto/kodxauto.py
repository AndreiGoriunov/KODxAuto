import logging
import os.path
from configparser import ConfigParser
from time import perf_counter

from .executor import Executor
from .step_handler import KXAContext, StepParser


class KODxAuto:
    """KODXAuto automation class."""

    def __init__(self):
        self.properties = {}
        self.__set_config_file()
        self.__set_logger()

    def __str__(self):
        return f"properties = {self.properties}"

    @PendingDeprecationWarning
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
        if not macro_name:
            macro_name = self.get_property("macro_name")

        # Path to the macros directory containing steps
        macro_directory = os.path.join(
            self.get_property("macros_folder_path"), macro_name
        )

        _macro_resources_dir = os.path.join(macro_directory, "resources")
        KXAContext.macro_resources_dir = _macro_resources_dir

        # If property is set to true or not set at all then recompile
        bf_parse = perf_counter()  # timer before parse/read
        steps = StepParser(macro_directory).parse_steps()
        logging.info(f"Parsed steps: {steps}")
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
        config_path = "kodxauto.properties"
        # Check if kodxauto.properties exists
        if not os.path.exists(config_path):
            _error = f"{config_path} was not found. Create the file in the same directory as your main program."
            raise FileNotFoundError(_error)

        # Get properties file and store it in self.properties dictionary
        _config_parser = ConfigParser()
        _config_parser.read(config_path)
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
