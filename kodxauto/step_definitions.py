"""KODxAuto built-in step definitions"""
import logging
from sys import stdout
from time import sleep

import pyautogui as pag

from .step_handler import kxa_step


@kxa_step(r"^Move mouse to (\d+),(\d+) over (\d+|\d+.\d+) sec$")
def move_mouse_to_over_seconds(x: int, y: int, sec: int):
    pag.moveTo(x, y, sec)


@kxa_step(r"^Move mouse to (\d+),(\d+)$")
def move_mouse_to(x: int, y: int):
    pag.moveTo(x, y)


@kxa_step(r"^$")
def meh():
    pass


def wait_for_element(
    _element: str, seconds: int = 10, polling_rate: float = 0.2
) -> pag.Point | None:
    maxs_tries = seconds / polling_rate
    try_number = 0
    logging.info(f"Waiting for element: {_element}")
    while try_number < maxs_tries:
        _location = pag.locateCenterOnScreen(image=_element, confidence=0.9)
        if _location is not None:
            logging.info(f"Element found.")
            break
        try_number += 1
        sleep(polling_rate)
    if not _location:
        logging.error(
            f"Element {_element}  was not found for the duration of {seconds} with polling rate of {polling_rate}"
        )
    return _location
