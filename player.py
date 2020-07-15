class Player:
    def __init__(self, fullscreen_command, quit_command):
        self.fullscreen_command = fullscreen_command
        self.quit_command = quit_command

    def play_trailer_and_film(self):
        pass

    def play_trailer_and_quit_player(self):
        pass


### ARCHIVED METHOD
    # def window_maximalization(self):
    #     mousePointer = mouse.Controller()
    #     mousePointer.position = (1000, 500)
    #     time.sleep(1)
    #     mousePointer.press(mouse.Button.left)
    #     mousePointer.release(mouse.Button.left)
    #     time.sleep(1)
    #     self.logger.debug("Window maximalization.")
    #     time.sleep(1)
    #     user32 = ctypes.WinDLL('user32')
    #     SW_MAXIMISE = 3
    #     hWnd = user32.GetForegroundWindow()
    #     user32.ShowWindow(hWnd, SW_MAXIMISE)
    #     key = keyboard.Controller()
    #     key.press('F')
    #     key.release('F')
    #     key.press(keyboard.Key.f11)
    #     key.release(keyboard.Key.f11)
    #     self.logger.debug('F na F11 keys pressed and released.')