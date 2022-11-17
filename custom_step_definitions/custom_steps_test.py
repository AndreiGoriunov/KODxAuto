import logging


from kodxauto.step_handler import kxa_step, GlobalVars


@kxa_step(r"Click on {string} element")
def click_on_element(xpath: str) -> None:
    print(f"Clicking on {xpath}")
