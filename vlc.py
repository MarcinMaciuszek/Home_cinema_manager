import time
import subprocess
import default_logger
from get_set_functions import *
from player import *


VLC_FULLSCREEN = "--fullscreen"
VLC_QUIT = "vlc://quit"
SUBTITLE_FLAG = "--sub-file="
TRAILER_TIME = 26 + 10


class VLC(Player):
    def __init__(self):
        super().__init__(fullscreen_command=VLC_FULLSCREEN, quit_command=VLC_QUIT)
        self.logger = default_logger.logger_creation(name='vlc')

    def play_trailer_and_film(self):
        video_player = get_application_variable('video_player')
        film = get_event_variable('absolute_path_to_film')
        trailer = get_application_variable('trailer')
        self.logger.debug("Started {} with {} then {}.".format(video_player, trailer, film))
        subprocess.Popen([video_player, trailer, film, self.quit_command, self.fullscreen_command])
        if '.mkv' in get_event_variable('film_file_name'):
            time.sleep(TRAILER_TIME)
            from pynput import keyboard
            keyboard_controller = keyboard.Controller()
            keyboard_controller.press('v')
            keyboard_controller.release('v')

    def play_trailer_and_quit_player(self):
        video_player = get_application_variable('video_player')
        trailer = get_application_variable('trailer')
        trailer_process = subprocess.Popen([video_player, trailer, self.quit_command, self.fullscreen_command])
        self.logger.debug("Started {} with {}.".format(video_player, trailer))
        trailer_process.communicate()
        self.logger.debug("Trailer finished.")