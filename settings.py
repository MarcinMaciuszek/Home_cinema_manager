import sys
import default_logger
from get_set_functions import *
from singleton import GlobalSingletonDict
from PyQt5.QtWidgets import QWidget, QDialog, QDialogButtonBox, QGroupBox, QLineEdit, QPushButton, QVBoxLayout, \
    QHBoxLayout, QCheckBox, QComboBox, QGridLayout
from PyQt5.QtCore import Qt

LANGUAGES_CONVERT_DICT = {'Polski': 'pol',
                          'pol': 'pol',
                          'English': 'eng',
                          'eng': 'eng'}
LANGUAGES = ["Polski", "English"]


class Settings(QDialog, QWidget):
    def __init__(self, title="Settings", width=550, height=250):
        super().__init__()
        settings = GlobalSingletonDict()
        settings['settings'] = self
        self.logger = default_logger.logger_creation(name='settings')
        self.download_subtitles = False
        self.main_language = None
        self.backup_language = None
        self.set_subtitles = False
        self.subtitles_no_for_mkv = False
        self.load_config()
        self.title = title
        self.width = width
        self.height = height
        self.groupbox_video_player = None
        self.checkbox_mkv_option = None
        self.checkbox_download = None
        self.checkbox_set_subtitles = None
        self.textbox_player = None
        self.list_languages = None
        self.shortcut_dict = LANGUAGES_CONVERT_DICT
        self.user_interface_initialization()

    def load_config(self):
        self.download_subtitles = get_application_variable('config').get('download_subtitles', False)
        self.main_language = get_application_variable('config').get('main_language', None)
        self.set_subtitles = get_application_variable('config').get('set_subtitles', False)
        self.subtitles_no_for_mkv = get_application_variable('config').get('no_download_subtitles_for_mkv', False)
        self.status_logger()

    def status_logger(self):
        self.logger.debug("download subtitles value: {}".format(self.download_subtitles))
        self.logger.debug("subtitles language value: {}".format(self.main_language))
        self.logger.debug("set subtitles value: {}".format(self.set_subtitles))
        self.logger.debug("subtitles no for mkv: {}".format(self.subtitles_no_for_mkv))

    def user_interface_initialization(self):
        self.logger.debug("Settings creation started.")
        try:
            self.title_and_geometry_initialization()
            self.video_player_group_box_initialization()
            self.subtitles_groupbox_initialization()
            self.window_initialization()
        except Exception as e:
            self.logger.error("Exception during application creation: {}.".format(e))
            sys.exit(1)
        self.logger.info("Settings created.")

    def title_and_geometry_initialization(self):
        self.setFixedSize(self.width, self.height)
        self.setWindowTitle(self.title)

    def video_player_group_box_initialization(self):
        self.groupbox_video_player = QGroupBox('Video player')
        layout_video_player = QHBoxLayout(self)
        self.textbox_player = self.textbox_player_initialization(400, 20)
        browse_button = self.button_initialization("Browse", self.groupbox_video_player, 75, 25,
                                                   get_event_method('on_click_browse_player'))
        layout_video_player.addWidget(self.textbox_player)
        layout_video_player.addWidget(browse_button)
        self.groupbox_video_player.setLayout(layout_video_player)

    def textbox_player_initialization(self, width, height):
        textbox_player = QLineEdit()
        textbox_player.resize(width, height)
        textbox_player.setFixedSize(width, height)
        self.logger.debug("Textbox_player with width: {} and height: {} created.".format(width, height))
        return textbox_player

    def button_initialization(self, name, groupbox, width, height, trigger):
        button = QPushButton(name, groupbox)
        button.setFixedSize(width, height)
        button.clicked.connect(trigger)
        self.logger.debug("Button with name: {}, groupbox: {}, width: {}, height: {} and trigger: {} created.".format(
            name, groupbox, width, height, trigger))
        return button

    def subtitles_groupbox_initialization(self):
        self.groupbox_subtitles = QGroupBox('Subtitles')
        layout_subtitles = QGridLayout(self)
        self.checkbox_mkv_option = self.checkbox_no_subtitles_download_for_mkv('No download subtitles for mkv files',
                                                                               self.change_checkbox_mkv)
        self.checkbox_download = self.checkbox_download_subtitles_initialization('Download subtitles in language: ',
                                                                                 self.change_checkbox_download)
        self.list_languages = self.combobox_initialization(LANGUAGES, 300, 20, False)
        self.checkbox_set_subtitles = self.checkbox_set_subtitles_initialization('Set downloaded subtitles',
                                                                                 self.change_checkbox_subtitles)
        if self.main_language:
            self.main_language, self.backup_language = self.translate_language_to_shortcut()
        layout_subtitles.addWidget(self.checkbox_mkv_option, 1, 0)
        layout_subtitles.addWidget(self.checkbox_download, 2, 0)
        layout_subtitles.addWidget(self.list_languages, 2, 1)
        layout_subtitles.addWidget(self.checkbox_set_subtitles, 3, 0)
        self.groupbox_subtitles.setLayout(layout_subtitles)

    def window_initialization(self):
        buttonbox = self.dialog_buttonbox_initialization()
        main_groupbox = QVBoxLayout(self)
        main_groupbox.addWidget(self.groupbox_video_player)
        main_groupbox.addWidget(self.groupbox_subtitles)
        main_groupbox.addWidget(buttonbox)
        self.setLayout(main_groupbox)
        video_player = get_application_variable('video_player')
        self.textbox_player.setText(video_player)
        self.logger.debug("mainGroupBox created.")

    def checkbox_no_subtitles_download_for_mkv(self, title, trigger):
        checkbox = QCheckBox(title)
        if self.subtitles_no_for_mkv:
            checkbox.setChecked(True)
        checkbox.stateChanged.connect(trigger)
        self.logger.debug("Checkbox with title: {} trigger: {} created.".format(title, trigger))
        return checkbox

    def checkbox_download_subtitles_initialization(self, title, trigger):
        checkbox = QCheckBox(title)
        if self.download_subtitles:
            checkbox.setChecked(True)
        checkbox.stateChanged.connect(trigger)
        self.logger.debug("Checkbox with title: {} trigger: {} created.".format(title, trigger))
        return checkbox

    def checkbox_set_subtitles_initialization(self, title, trigger):
        checkbox_set_subtitles = QCheckBox(title)
        checkbox_set_subtitles.setEnabled(False)
        if self.download_subtitles:
            checkbox_set_subtitles.setEnabled(True)
            if self.set_subtitles:
                checkbox_set_subtitles.setChecked(True)
        checkbox_set_subtitles.stateChanged.connect(trigger)
        self.logger.debug("Checkbox w title: {} trigger: {} created.".format(title, trigger))
        return checkbox_set_subtitles

    def combobox_initialization(self, language_list, width, height, status):
        combobox = QComboBox()
        combobox.addItems(language_list)
        combobox.setFixedSize(width, height)
        combobox.setEnabled(status)
        if self.download_subtitles:
            combobox.setEnabled(True)
            combobox.setCurrentText(self.main_language)
        combobox.activated.connect(self.language_setter)
        self.logger.debug("Combobox with language_list: {}, width: {}, height: {}, status: {} created.".format(
            language_list, width, height, status))
        return combobox

    def dialog_buttonbox_initialization(self):
        buttonbox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonbox.accepted.connect(self.accept)
        buttonbox.accepted.connect(self.status_logger)
        buttonbox.rejected.connect(self.reject)
        buttonbox.rejected.connect(self.status_logger)
        self.logger.debug("Dialog button groupbox created.")
        return buttonbox

    def language_setter(self):
        self.main_language, self.backup_language = self.translate_language_to_shortcut()
        self.logger.debug("subtitlesLanguage value: {}".format(self.main_language))

    def change_checkbox_download(self, state):
        if state == Qt.Checked:
            self.download_subtitles = True
            self.main_language, self.backup_language = self.translate_language_to_shortcut()
            self.list_languages.setEnabled(True)
            self.checkbox_set_subtitles.setEnabled(True)
        else:
            self.download_subtitles = False
            self.main_language = None
            self.set_subtitles = False
            self.list_languages.setEnabled(False)
            self.checkbox_set_subtitles.setChecked(False)
            self.checkbox_set_subtitles.setEnabled(False)
        self.status_logger()

    def translate_language_to_shortcut(self):
        current_language = self.list_languages.currentText()
        main_language_tag = ""
        backup_language_tag = ""
        for shortcut in self.shortcut_dict:
            if shortcut == current_language:
                main_language_tag = self.shortcut_dict[shortcut]
                break
        for shortcut in self.shortcut_dict:
            if shortcut != current_language and self.shortcut_dict[shortcut] != main_language_tag:
                backup_language_tag = self.shortcut_dict[shortcut]
                break
        self.logger.debug("Main language: {}, backup language: {}.".format(
            main_language_tag, backup_language_tag))
        return main_language_tag, backup_language_tag

    def change_checkbox_subtitles(self, state):
        if state == Qt.Checked:
            self.set_subtitles = True
        else:
            self.set_subtitles = False
        self.logger.debug("set_subtiles value: {}".format(self.set_subtitles))

    def change_checkbox_mkv(self, state):
        if state == Qt.Checked:
            self.subtitles_no_for_mkv = True
        else:
            self.subtitles_no_for_mkv = False
        self.logger.debug("subtitles no for mkv value: {}".format(self.subtitles_no_for_mkv))