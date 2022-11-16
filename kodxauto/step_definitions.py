"""KODxAuto built-in step definitions"""
import logging
import os.path
from time import sleep

import pyautogui as pag


from .step_handler import kxa_step, GlobalVars


@kxa_step(r"^Move mouse to (\d+),(\d+) over (\d+|\d+.\d+) sec$")
def move_mouse_to_over_seconds(x: int, y: int, sec: int) -> None:
    pag.moveTo(x, y, sec)


@kxa_step(r"^Move mouse to (\d+),(\d+)$")
def move_mouse_to(x: int, y: int) -> None:
    pag.moveTo(x, y)


@kxa_step(r"^Click \"(.*)\" element on sreen$")
def click_element_on_screen(element: str) -> None:
    element_path = os.path.join(GlobalVars.macros_resources_dir, element)
    # Wait until element appears
    location = pag.locateCenterOnScreen(
        image=element_path, confidence=0.9, minSearchTime=10
    )
    pag.click(location)


@kxa_step(r"^Click \"(.*)\" element on screen (\d+) times$")
def click_element_on_screen_times(element: str, times: int) -> None:
    region = GlobalVars.region
    # region = (466, 151, 970, 540)
    for _ in range(times):
        element_path = os.path.join(GlobalVars.macros_resources_dir, element)
        pag.click(
            pag.locateCenterOnScreen(
                image=element_path,
                confidence=0.8,
                minSearchTime=10,
                region=region,
                grayscale=True,
            )
        )


@kxa_step(r"^Select working region$")
def select_working_region():
    # TODO improve
    input(
        "\nPlace cursor at the top left of the region you want to capture, and then press enter\n"
    )
    pos1 = pag.position()
    input(
        "Now place your cursor at the bottom right of the region you want to capture, and press enter\n"
    )
    pos2 = pag.position()
    width = pos2[0] - pos1[0]
    height = pos2[1] - pos1[1]
    GlobalVars.region = (pos1[0], pos1[1], width, height)
    print(f"region=({pos1[0]},{pos1[1]},{width},{height})")
