import logging
import os.path
import re

from yaml import YAMLError, safe_load

# Holds a dictionary in for of { @kxa_step(regex) : function.__name__ }
regex_to_function_map = {}


class KXAContext:
    macro_resources_dir = None
    region = None


class StepParser:
    """Reads and Parses the steps from macros.yaml file.

    Initialized with the path to the macros name directory.
    """

    def __init__(self, _path: str):
        self._path = _path
        self.macro_yaml_path = os.path.join(_path, "macros.yaml")
        self.macro_txt_path = os.path.join(_path, "macros.txt")
        logging.info(f"File macros.yaml read successfully.")
        self.parsed_steps = []  # A list of parsed steps

    def parse_steps(self) -> list:
        """Iterates through all the steps in macros.yaml.

        Returns a list of functions with arguments.
        """
        self.yaml_steps = self.__read_macro_yaml_file(self._path)  # Read yaml file

        for step in self.yaml_steps:
            func = self.__match_steps(step)
            if func:
                self.parsed_steps.append(func)
            else:
                _error = f'Step "{step}" is not defined.'
                logging.error(_error)
                raise Exception(_error)

        return self.parsed_steps

    def __read_macro_yaml_file(self, _path) -> list:
        """Reads macros.yaml file and returns a list of yaml_steps."""
        macros = None
        logging.info(f"Attempting to open: {self.macro_yaml_path}")
        try:
            # Opening the file with context manager and reading yaml to dict
            with open(self.macro_yaml_path, "r", encoding="utf-8") as file:
                try:
                    macros = safe_load(file)
                except YAMLError as exc:
                    logging.error(exc)
                    raise YAMLError("Error opening yaml.")
        except FileNotFoundError:
            _error = f"Error when opening {_path}."
            logging.error(_error)
            raise FileNotFoundError(_error)
        return macros["steps"]

    def __match_steps(self, step) -> tuple:
        """Matches the yaml_steps from macros.yaml with a regex key in `regex_to_function_map`.

        Return a tuple where:
        - element [0] is function object and
        - element [1] is function arguments in a tuple.
        """
        # Loop throug regex to func map
        for regex, func_name in regex_to_function_map.items():
            func_match = re.search(regex, step)
            # Check if match is found with existing regex
            if func_match:
                groups = func_match.groups()
                func_args = []  # Stores a list of function arguments
                for _, gr in enumerate(groups):
                    func_args.append(type_conversion(gr))
                # return f"{func_name}{tuple(func_args)}"
                return (func_name, tuple(func_args))
        return None  # If no match was found with existing `regex_to_function_map` dict


# Decorator
def kxa_step(regex: str):
    """Function decorator for KODxAuto macros steps.

    If a function is marked with `@kxa_step` decorator, adds the regex pattern
    passed to the decorator and function's name to the dictionary as
    { regex : func_name }.
    """
    types = {r"{string}": r'"(.*)"', r"{int}": r"(\d+)", r"{float}": r"(\d+|\d+.\d+)"}

    def decorate(fn):
        def inner(*args):
            return fn(*args)

        _regex = regex
        # replacing type placeholders with regex str
        for k, v in types.items():
            _regex = _regex.replace(k, v)

        regex_to_function_map[_regex] = fn
        return inner

    return decorate


# Helper functions =========================================s
def type_conversion(element: str):
    """Helper function to convert a value to correct type."""
    if element.isdigit():
        return int(element)
    elif is_float(element):
        return float(element)
    else:
        return str(element)


def is_float(element) -> bool:
    """Helper function to check if string value is float."""
    try:
        float(element)
        return True
    except ValueError:
        return False
