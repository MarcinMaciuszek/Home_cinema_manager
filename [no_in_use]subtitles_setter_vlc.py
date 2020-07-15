import time
from pynput import mouse, keyboard

PAUSE_TIME = 0.5
RATE = 1


def set_subtitles(rate=RATE):
    mouse_controller, keyborad_controller = mouse_and_keyboard_initialization(rate)
    make_video_window_as_main_window(mouse_controller)
    open_video_context_menu(mouse_controller)
    move_and_click_subtitles(mouse_controller)
    move_and_click_add_subtitles(mouse_controller)
    set_subtitles_in_subtitles_window(keyborad_controller)


def mouse_and_keyboard_initialization(rate):
    keyboard_controller = keyboard.Controller()
    mouse_controller = mouse.Controller()
    mouse_controller.position = (1000 * rate, 500 * rate)
    return mouse_controller, keyboard_controller


def make_video_window_as_main_window(mouse_controller):
    time.sleep(PAUSE_TIME)
    mouse_controller.press(mouse.Button.left)
    mouse_controller.release(mouse.Button.left)


def open_video_context_menu(mouse_controller):
    time.sleep(PAUSE_TIME)
    mouse_controller.press(mouse.Button.right)
    mouse_controller.release(mouse.Button.right)


def move_and_click_subtitles(mouse_controller):
    time.sleep(PAUSE_TIME)
    mouse_controller.move(40, 200)
    time.sleep(PAUSE_TIME)
    mouse_controller.press(mouse.Button.left)
    mouse_controller.release(mouse.Button.left)


def move_and_click_add_subtitles(mouse_controller):
    time.sleep(PAUSE_TIME)
    mouse_controller.move(250, 0)
    time.sleep(PAUSE_TIME)
    mouse_controller.press(mouse.Button.left)
    mouse_controller.release(mouse.Button.left)


def set_subtitles_in_subtitles_window(keyboard_controller):
    time.sleep(3 * PAUSE_TIME)
    keyboard_controller.press(keyboard.Key.shift)
    keyboard_controller.press(keyboard.Key.tab)
    keyboard_controller.release(keyboard.Key.shift)
    keyboard_controller.release(keyboard.Key.tab)
    time.sleep(PAUSE_TIME)
    keyboard_controller.press(keyboard.Key.shift)
    keyboard_controller.press(keyboard.Key.tab)
    keyboard_controller.release(keyboard.Key.shift)
    keyboard_controller.release(keyboard.Key.tab)
    time.sleep(PAUSE_TIME)
    keyboard_controller.press(keyboard.Key.down)
    keyboard_controller.release(keyboard.Key.down)
    time.sleep(PAUSE_TIME)
    keyboard_controller.press(keyboard.Key.enter)
    keyboard_controller.release(keyboard.Key.enter)
