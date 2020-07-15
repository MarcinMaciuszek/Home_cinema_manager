import webbrowser
import time
from pynput import keyboard

NETFLIX_SLEEP_TIME_BETWEEN_OPERATIONS = 2


def netflix_handling(netflix_link):
    webbrowser.open(netflix_link)
    key_Controller = keyboard.Controller()
    clicking_netflix_mark(key_Controller)
    going_to_site_bar(key_Controller)
    return_one_site_and_refresh(key_Controller)
    film_start(key_Controller)
    window_maximalization(key_Controller)


def clicking_netflix_mark(key_controller):
    time.sleep(3 * NETFLIX_SLEEP_TIME_BETWEEN_OPERATIONS)
    key_controller.press(keyboard.Key.tab)
    key_controller.release(keyboard.Key.tab)
    key_controller.press(keyboard.Key.enter)
    key_controller.release(keyboard.Key.enter)


def going_to_site_bar(key_controller):
    time.sleep(NETFLIX_SLEEP_TIME_BETWEEN_OPERATIONS)
    key_controller.press(keyboard.Key.shift)
    key_controller.press(keyboard.Key.tab)
    key_controller.release(keyboard.Key.tab)
    key_controller.release(keyboard.Key.shift)


def return_one_site_and_refresh(key_controller):
    time.sleep(0.5 * NETFLIX_SLEEP_TIME_BETWEEN_OPERATIONS)
    key_controller.press(keyboard.Key.alt)
    key_controller.press(keyboard.Key.left)
    key_controller.release(keyboard.Key.alt)
    key_controller.release(keyboard.Key.left)
    time.sleep(NETFLIX_SLEEP_TIME_BETWEEN_OPERATIONS)
    key_controller.press(keyboard.Key.f5)
    key_controller.release(keyboard.Key.f5)


def film_start(key_controller):
    time.sleep(2 * NETFLIX_SLEEP_TIME_BETWEEN_OPERATIONS)
    key_controller.press(keyboard.Key.tab)
    key_controller.release(keyboard.Key.tab)
    key_controller.press(keyboard.Key.enter)
    key_controller.release(keyboard.Key.enter)


def window_maximalization(key_controller):
    time.sleep(NETFLIX_SLEEP_TIME_BETWEEN_OPERATIONS)
    key_controller.press(keyboard.Key.f11)
    key_controller.release(keyboard.Key.f11)
