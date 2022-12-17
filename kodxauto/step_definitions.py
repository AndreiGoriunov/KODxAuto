"""KODxAuto built-in step definitions"""
import logging
import os.path
from time import sleep

import pyautogui as pag

from .step_handler import KXAContext, kxa_step


@kxa_step(r"^Move mouse to {int},{int} over {float} sec$")
def move_mouse_to_over_seconds(x: int, y: int, sec: int) -> None:
    pag.moveTo(x, y, sec)


@kxa_step(r"^Move mouse to {int},{int}$")
def move_mouse_to(x: int, y: int) -> None:
    pag.moveTo(x, y)


@kxa_step(r"^Click {string} mouse button$")
def click():
    button = button.upper()
    pag.click(button=button)


@kxa_step(r"^Click {string} mouse button at {int},{int}$")
def click_at(button: str, x: int, y: int) -> None:
    button = button.upper()
    pag.click(x, y, button=button)


@kxa_step(r"^Click {string} image on screen$")
def click_image_on_screen(element: str) -> None:
    region = KXAContext.region  # get region
    element_path = os.path.join(KXAContext.macro_resources_dir, element)
    # Wait until element appears
    location = pag.locateCenterOnScreen(
        image=element_path,
        confidence=0.8,
        minSearchTime=10,
        grayscale=True,
        region=region,
    )
    pag.click(location)


@kxa_step(r"^Click {string} image on screen {int} times$")
def click_image_on_screen_times(element: str, times: int) -> None:
    """Used for fast conseccutive clicking."""
    region = KXAContext.region  # get region
    element_path = os.path.join(KXAContext.macro_resources_dir, element)
    for _ in range(times):
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
def pag_select_working_region():
    # TODO improve
    input("Hover over region Point 1, press Enter\n")
    pos1 = pag.position()
    input("Hover over region Point 2, press Enter\n")
    pos2 = pag.position()
    width = pos2[0] - pos1[0]
    height = pos2[1] - pos1[1]
    KXAContext.region = (pos1[0], pos1[1], width, height)
    print(f"region=({pos1[0]},{pos1[1]},{width},{height})")


@kxa_step(r"^Set working region to \({int},{int},{int},{int}\)$")
def pag_set_working_region_to(x: int, y: int, w: int, h: int) -> None:
    KXAContext.region = (x, y, w, h)


@kxa_step(r"^Take screenshot of the region$")
def take_screenshot_of_the_region():
    image = pag.screenshot(region=KXAContext.region)
    KXAContext.image = image


@kxa_step(r"^Wait {int} sec$")
def wait_sec(sec: int):
    sleep(sec)


@kxa_step(r"^Wait for {string} image to appear$")
def wait_for_image_to_appear(element: str):
    region = KXAContext.region  # get region
    element_path = os.path.join(KXAContext.macro_resources_dir, element)
    pag.locateCenterOnScreen(
        image=element_path,
        confidence=0.8,
        minSearchTime=10,
        region=region,
        grayscale=True,
    )
