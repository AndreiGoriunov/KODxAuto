from pynput import keyboard as kb

from lib import kodxauto

bind = kb.Key.insert
pressed = False

def listen():
    listener = kb.Listener(on_release=on_release)

    # def __init__(self, bind):
    #     self.bind = bind

def on_press(key):
    try:
        print(f'Key {key.char} pressed')
    except AttributeError:
        print(f'Key {key} pressed')

def on_release(key):
    print(f'{key} released')
    if key == bind:
        pressed = True
    if key == kb.Key.esc:
        return False

def bindPressed():
    return pressed