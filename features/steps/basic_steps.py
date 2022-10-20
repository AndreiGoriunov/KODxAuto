from behave import given
import pyautogui as pg


@given("I click")
def step_given(context):
    pg.click()


@given("I click on ({x:d},{y:d})")
def step_given(context, x, y):
    pg.click(x, y)


@given("I move mouse to ({x:d},{y:d})")
def step_impl(context, x, y):
    pg.moveTo(x, y)


@given("I move mouse to ({x:d},{y:d}) over {sec:d} second(s)")
def step_impl(context, x, y, sec):
    pg.moveTo(x, y, duration=sec)

@given("I drag mouse to ({x:d},{y:d}) over {sec:d} second(s)")
def step_impl(context, x, y, sec):
    pg.dragTo(x, y, duration=sec)

@given("I drag mouse ({x:d},{y:d}) over {sec:d} second(s)")
def step_impl(context, x, y, sec):
    pg.drag(x, y, duration=sec)