import sys
import default_logger
from get_set_functions import *
from win32api import GetSystemMetrics
from singleton import GlobalSingletonDict
from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QPushButton, QLineEdit, QAction, QComboBox
from PyQt5.QtGui import QPixmap
from settings import Settings

TITLE = "Kino"
LEFT = 100
TOP = 100
WIDTH = 800
HEIGHT = 600
VIDEO_PLAYER = r"C:\Program Files\Windows Media Player\wmplayer.exe"
TRAILER = r"<your tailer path>"
CONFIG = {}
BACKGROUND_IMAGE = "<your background img>"


class Application(QMainWindow):
    def __init__(self, title=TITLE, left=LEFT, top=TOP, width=WIDTH, height=HEIGHT,
                 video_Player=VIDEO_PLAYER, trailer=TRAILER, config=CONFIG):
        super().__init__()
        application = GlobalSingletonDict()
        application['app'] = self
        self.logger = default_logger.logger_creation(name='application')
        self.title = title
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.config = config
        self.central_widget = QWidget()
        self.main_menu = self.menuBar()
        self.resolution = ()
        self.text_bar_browse = ""
        self.list_netflix = ""
        self.video_player = self.config.get('video_player', video_Player)
        self.trailer = trailer
        self.user_interface_initialization()
        self.settings = Settings()
        self.show()

    def user_interface_initialization(self):
        self.logger.debug("Application creation started.")
        try:
            self.central_widget_initialization()
            self.title_and_geometry_initialization()
            self.image_initialization()
            self.menu_bar_initialization()
            self.buttons_initialization()
            self.bars_initialization()
            self.setting_monitor_resolution()
        except Exception as Error:
            self.logger.error("Exception during application creation: {}.".format(Error))
            sys.exit(1)
        self.logger.info('Application created.')

    def central_widget_initialization(self):
        self.setCentralWidget(self.central_widget)
        self.logger.debug('Central Widget created.')

    def title_and_geometry_initialization(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setFixedSize(self.width, self.height)
        self.logger.debug('Set title: {}, and window geometry, left: {}, top: {}, width: {}, height: {}.'
                          .format(self.title, self.left, self.top, self.width, self.height))

    def image_initialization(self):
        photo_container = QLabel(self.central_widget)
        background_photo = QPixmap(BACKGROUND_IMAGE)
        photo_container.setPixmap(background_photo)
        self.resize(background_photo.width(), background_photo.height())
        self.logger.debug('Set background image: {}.'.format(BACKGROUND_IMAGE))

    def menu_bar_initialization(self):
        self.file_menu_into_menu_bar_initialization()
        self.help_menu_into_menu_bar_initialization()
        self.logger.debug('Menu bar created.')

    def file_menu_into_menu_bar_initialization(self):
        file_menu = self.main_menu.addMenu("File")
        open_button = self.menu_button_initialization('Open', 'Ctrl+O', get_event_method('on_click_browse'))
        netflix_button = self.menu_button_initialization('Netflix', 'Ctrl+N',
                                                         get_event_method('on_click_netflix'))
        settings_button = self.menu_button_initialization('Settings', 'Ctrl+S',
                                                          get_event_method('on_click_settings'))
        exit_button = self.menu_button_initialization('Exit', 'Ctrl+Q', self.close)
        file_menu.addAction(open_button)
        file_menu.addAction(netflix_button)
        file_menu.addAction(settings_button)
        file_menu.addAction(exit_button)
        self.logger.debug('File menu created.')

    def help_menu_into_menu_bar_initialization(self):
        help_menu = self.main_menu.addMenu("Help")
        about_button = self.menu_button_initialization('About', trigger=get_event_method('on_click_about'))
        help_menu.addAction(about_button)
        self.logger.debug('Help menu created.')

    def menu_button_initialization(self, name, shortcut=None, trigger=None):
        button = QAction(name, self)
        if shortcut:
            button.setShortcut(shortcut)
        if trigger:
            button.triggered.connect(trigger)
        self.logger.debug("Buttton: {} created.".format(name))
        return button

    def buttons_initialization(self):
        self.single_button_initialization("Browse", 550, 300, 'on_click_browse')
        self.single_button_initialization("Clear", 600, 300, 'on_click_clear_browse')
        self.single_button_initialization("Netflix", 550, 350, 'on_click_netflix')
        self.single_button_initialization("Clear", 600, 350, 'on_click_clear_netflix')
        self.single_button_initialization("Myyyyk", 300, 400, 'on_click_start', 100, 50)

    def single_button_initialization(self, name, top, left, event, size_x=50, size_y=25):
        button = QPushButton(name, self.central_widget)
        button.resize(size_x, size_y)
        button.move(top, left)
        on_click_event = get_event_method(event)
        button.clicked.connect(on_click_event)
        self.logger.debug('Button created with name: {}, top: {}, left: {}, event: {}, size_x: {}, size_y: {}.'
                          .format(name, top, left, event, size_x, size_y))
        return button

    def bars_initialization(self):
        self.text_bar_browse = self.text_bar_initialization(150, 300, 400, 20)
        self.list_netflix = self.list_initialization(150, 350, 400, 20, False)

    def text_bar_initialization(self, top, left, size_x, size_y):
        textbox = QLineEdit(self.central_widget)
        textbox.move(top, left)
        textbox.resize(size_x, size_y)
        self.logger.debug('Text bar created with top: {}, left: {}, size_x: {}, size_y: {}.'
                          .format(top, left, size_x, size_y))
        return textbox

    def list_initialization(self, top, left, size_x, size_y, state):
        text_list = QComboBox(self.central_widget)
        text_list.move(top, left)
        text_list.setFixedSize(size_x, size_y)
        text_list.setEnabled(state)
        self.logger.debug('List created with top: {}, left: {}, size_x: {}, size_y: {}, state: {}.'
                          .format(top, left, size_x, size_y, state))
        return text_list

    def setting_monitor_resolution(self):
        self.resolution = (GetSystemMetrics(0), GetSystemMetrics(1))
        self.logger.debug("Resolution is {}.".format(self.resolution))

    def closeEvent(self, *args, **kwargs):
        self.logger.info("Application closing.")
        self.close()

