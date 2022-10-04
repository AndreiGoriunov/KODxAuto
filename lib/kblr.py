from pynput import keyboard

# def on_press(key):
#     try:
#         print(f'Key {key.char} pressed')
#     except AttributeError:
#         print(f'Key {key} pressed')

def on_release(key):
    print(f'{key} released')
    if key == keyboard.Key.home:
        return False
    if key == keyboard.Key.insert:
        return False
    if key == keyboard.Key.esc:
        return False

# Collect events until released
with keyboard.Listener(
        on_press=None,
        on_release=on_release) as listener:
    listener.join()

# # ...or, in a non-blocking fashion:
# listener = keyboard.Listener(
#     on_press=on_press,
#     on_release=on_release)