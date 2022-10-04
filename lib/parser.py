import json
from os.path import exists

import yaml


def parse(file_path: str) -> dict:
    macro_steps = None
    _path = None

    if (exists(f'{file_path}/macro.yaml')):
        _path = f'{file_path}'
    elif (exists(f'macros/{file_path}/macro.yaml')):
        _path = f'macros/{file_path}'
    else:
        raise FileNotFoundError(
            'The specified folder does not contain macro.yaml file')

    with open(f'{_path}/macro.yaml', 'r', encoding='utf-8') as stream:
        try:
            macro_steps = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    return macro_steps


def prettyPrint(_dict: dict) -> None:
    print(json.dumps(_dict, indent=3))
