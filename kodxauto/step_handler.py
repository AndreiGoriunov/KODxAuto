import logging
import re
import os.path

from yaml import YAMLError, safe_load

# Holds a dictionary in for of { @kxa_step(regex) : function.__name__ }
regex_to_function_map = {}

types = {r"{string}": r'"(.*)"', r"{int}": r"(\d+)", r"{float}": r"(\d+|\d+.\d+)"}


class StepParser:
    """Reads and Parses the steps from macros.yaml file.

    Initialized with the path to the macros name directory.
    """

    def __init__(self, _path: str):
        self._path = _path
        self.macros_yaml_path = os.path.join(_path, "macros.yaml")
        self.macros_txt_path = os.path.join(_path, "macros.txt")
        logging.info(f"File macros.yaml read successfully.")
        self.parsed_steps = []  # A list of parsed steps

    def parse_steps(self) -> list:
        """Iterates through all the steps in macros.yaml.s

        Returns a list of functions with arguments.
        """
        self.yaml_steps = self.__read_macros_yaml_file(self._path)  # Read yaml file

        for step in self.yaml_steps:
            func = self.__step_matcher(step)
            if func:
                self.parsed_steps.append(func)
            else:
                _error = f'Step "{step}" is not defined.'
                logging.error(_error)
                raise Exception(_error)

        self.__write_parsed_steps_to_file()
        return self.parsed_steps

    def read_parsed_steps(self) -> list:
        self.parsed_steps.clear
        with open(self.macros_txt_path, "r", encoding="utf-8") as file:
            # Append each line of the file to the list.
            for line in file:
                self.parsed_steps.append(line)
        return self.parsed_steps

    def __read_macros_yaml_file(self, _path) -> list:
        """Reads macros.yaml file and returns a list of yaml_steps."""
        macros = None
        logging.info(f"Attempting to open: {self.macros_yaml_path}")
        try:
            # Opening the file with context manager and reading yaml to dict
            with open(self.macros_yaml_path, "r", encoding="utf-8") as file:
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

    def __write_parsed_steps_to_file(self) -> None:
        if self.parsed_steps:
            with open(self.macros_txt_path, "w", encoding="utf-8") as file:
                file.write("\n".join(self.parsed_steps))
        else:
            _error = "self.parsed_steps list is empty."
            logging.error(_error)
            raise ValueError(_error)

    def __step_matcher(self, step) -> str:
        """Matches the yaml_steps from macros.yaml with a regex key in `regex_to_function_map`.

        Return function with arguments as string or None if no match.
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
                return f"{func_name}{tuple(func_args)}"
        return None  # If no match was found with existing `regex_to_function_map` dict

    # TODO
    def __update_regex_types(self):
        """TBD. Changes type aliases in @kxa_step to their regex form."""
        for old_key in list(regex_to_function_map.keys()):
            new_key = old_key.replace()
            regex_to_function_map[new_key] = regex_to_function_map[old_key]
            del regex_to_function_map[old_key]


def get_step_map():
    """Remove later"""
    return regex_to_function_map


# Decorator
def kxa_step(regex: str):
    """Function decorator for KODxAuto macros steps.

    If a function is marked with `@kxa_step` decorator, adds the regex pattern
    passed to the decorator and function's name to the dictionary as
    { regex : func_name }.
    """

    def decorate(fn):
        def inner(*args):
            return fn(*args)

        regex_to_function_map[regex] = fn.__name__
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
