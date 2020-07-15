import sys
import default_logger
import subtitles_downloader
import os.path
import filmweb_films_gatherer
import netflix_handler
from vlc import VLC
from get_set_functions import *
from mover import Mover
from pymediainfo import MediaInfo
from singleton import GlobalSingletonDict
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QMainWindow, QInputDialog, QWidget

TRAILER_TIME = 24
DEFAULT_PATH_TO_FILM = "C:\\"
PLAYERS_SUPPORTED = ['vlc.exe']


class Event(QMainWindow):
    def __init__(self):
        super().__init__()
        event = GlobalSingletonDict()
        event['event'] = self
        self.logger = default_logger.logger_creation(name='event')
        self.path_to_dir_with_film = r"{}".format(DEFAULT_PATH_TO_FILM)
        self.film_file_name = ""
        self.film_base = {}
        self.absolute_path_to_film = ""
        self.text_bar_browse = None
        self.list_netflix = None
        self.infobox = QWidget()

    def information_box(self):
        self.infobox.setWindowTitle('Window initilatization.')
        self.infobox.setGeometry(500, 500, 500, 10)
        self.infobox.show()
        self.logger.debug("Infobox showed.")

    @pyqtSlot()
    def on_click_browse(self):
        try:
            self.logger.debug('Browse clicked.')
            self.open_file_name_dialog_for_film()
        except Exception as Error:
            self.logger.error("Error during browse operation: {}.".format(Error))
            sys.exit(1)

    @pyqtSlot()
    def on_click_browse_player(self):
        try:
            self.logger.debug('Browse Player clicked.')
            self.open_file_name_dialog_for_player()
        except Exception as Error:
            self.logger.error("Error during browse player operation: {}.".format(Error))
            sys.exit(1)

    @pyqtSlot()
    def on_click_about(self):
        try:
            self.logger.debug('About clicked.')
            message = "Klikaj i ogladaj\n" \
                      "Supported browser: Google Chrome\n" \
                      "Supported player: VLC"
            QMessageBox.question(self, "About", message, QMessageBox.Ok, QMessageBox.Ok)
        except Exception as Error:
            self.logger.warning("Error during about operation: {}.".format(Error))

    @pyqtSlot()
    def on_click_settings(self):
        try:
            self.logger.debug('Settings clicked.')
            instance = GlobalSingletonDict()
            instance['app'].settings.show()
        except Exception as Error:
            self.logger.warning("Error during showing settings window: {}.".format(Error))

    @pyqtSlot()
    def on_click_clear_browse(self):
        try:
            self.logger.debug("Clear Browse clicked.")
            self.text_bar_browse = get_application_variable('text_bar_browse')
            self.text_bar_browse.setText("")
        except Exception as Error:
            self.logger.warning("Error during clearing film text bar: {}.".format(Error))

    @pyqtSlot()
    def on_click_clear_netflix(self):
        try:
            self.logger.debug("Clear Netflix clicked.")
            self.list_netflix = get_application_variable('list_netflix')
            self.list_netflix.clear()
            self.list_netflix.setEnabled(False)
        except Exception as Error:
            self.logger.warning("Error during clearing netflix_handling list: {}.".format(Error))

    @pyqtSlot()
    def on_click_netflix(self):
        try:
            self.logger.debug("Netflix clicked.")
            netflix_box, approval = QInputDialog.getText(self, "Netflix films finder", 'Type film name')
            if approval and netflix_box != "":
                self.logger.debug("netflix_box set to: {}.".format(netflix_box))
                films = filmweb_films_gatherer.netflix_finder(netflix_box)
                self.list_netflix = get_application_variable('list_netflix')
                self.list_netflix.clear()
                self.logger.debug("list_netflix cleared.")
                self.filling_netflix_list(films)
        except Exception as Error:
            self.logger.error("Error during gathering information about netflix_handling films: {}.".format(Error))
            sys.exit(1)

    def filling_netflix_list(self, films):
        if films:
            self.list_netflix.setEnabled(True)
            self.logger.debug("list_netflix state set to True.")
            for film in films:
                self.film_base[film['title']] = film['netflix_handling']
                film_info = "{}, {}, {}, {}, {}, {}".format(film['title'], film['year'], film['duration'],
                                                            film['director'], film['genre'], film['country'])
                self.list_netflix.addItem(film_info)
                self.logger.debug("{} added to filmBase.".format(film_info))
            self.logger.debug("Filmbase: {}".format(self.film_base))
        else:
            self.list_netflix.setEnabled(False)
            self.logger.debug("list_netflix state set to False.")

    @pyqtSlot()
    def on_click_start(self):
        try:
            self.logger.debug('Start clicked.')
            self.list_netflix = get_application_variable('list_netflix')
            self.text_bar_browse = get_application_variable('text_bar_browse')
            if os.path.basename(get_application_variable('video_player')) not in PLAYERS_SUPPORTED:
                self.player_check()
            elif self.text_bar_browse.text() == "" and not self.list_netflix.isEnabled():
                self.no_film_selected()
            elif self.text_bar_browse.text() != "" and self.list_netflix.isEnabled():
                self.too_many_films_selected()
            elif self.text_bar_browse.text() != "":
                self.film_from_drive_starting()
            elif self.list_netflix.isEnabled():
                self.film_from_netflix_starting()
        except Exception as Error:
            message = 'Error during starting film: {}.'.format(Error)
            self.logger.warning(message)
            QMessageBox.question(self, message, QMessageBox.Ok, QMessageBox.Ok)
            sys.exit(1)

    def player_check(self):
        message = "Please download and install VLC:\n" \
                  "https://www.videolan.org/vlc/download-windows.pl.html\n" \
                  "then set path to it in: File --> Settings --> Video Player"
        QMessageBox.question(self, "Player not supported", message, QMessageBox.Ok, QMessageBox.Ok)

    def no_film_selected(self):
        self.logger.warning('Film was not selected, textbox is empty.')
        QMessageBox.question(self, "error", "Wybierz film", QMessageBox.Ok, QMessageBox.Ok)

    def too_many_films_selected(self):
        self.logger.warning('Film was not selected, textbox is empty.')
        QMessageBox.question(self, "Error", "Za duzo wybranych filmow", QMessageBox.Ok, QMessageBox.Ok)

    def film_from_drive_starting(self):
        if get_settings_variable('download_subtitles'):
            self.move_old_files_to_archive_dir()
            if '.mkv' in self.film_file_name and get_settings_variable('subtitles_no_for_mkv') is True:
                pass
            else:
                self.information_box()
                self.download_subtitles()
        player = self.player_initialization()
        player.play_trailer_and_film()
        self.logger.info('Seance started.')

    def move_old_files_to_archive_dir(self):
        move_files = Mover()
        self.logger.debug("Mover object created.")
        move_files.move()
        self.logger.debug("Files moved.")

    def download_subtitles(self):
        subtitle = subtitles_downloader.SubtitlesDownloader(self.absolute_path_to_film,
                                                            get_settings_variable('main_language'),
                                                            get_settings_variable('backup_language'))
        subtitle_downloading_result = subtitle.download()
        return subtitle_downloading_result

    def film_from_netflix_starting(self):
        video_player = os.path.abspath(get_application_variable('video_player'))
        trailer = os.path.abspath(get_application_variable('trailer'))

        self.logger.info("Opening {} with {}.".format(video_player, trailer))
        player = self.player_initialization()
        player.play_trailer_and_quit_player()
        netflixLink = self.film_base[self.list_netflix.currentText().split(", ")[0]]
        netflix_handler.netflix_handling(netflixLink)
        self.logger.info('Seance started.')

    def player_initialization(self):
        if os.path.basename(get_application_variable('video_player')) == 'vlc.exe':
            player = VLC()
            return player

    def open_file_name_dialog_for_film(self):
        selected_film, _ = QFileDialog.getOpenFileName(self, "Select film", self.path_to_dir_with_film)
        if selected_film:
            self.logger.debug("Setting film...")
            try:
                media_info = MediaInfo.parse(selected_film)
                list_of_track_types = []
                for track in media_info.tracks:
                    list_of_track_types.append(track.track_type)
                if "Video" not in list_of_track_types:
                    raise Exception
                self.text_bar_browse = get_application_variable('text_bar_browse')
                self.text_bar_browse.setText(selected_film)
                self.absolute_path_to_film = os.path.abspath(r'{}'.format(selected_film))
                self.film_file_name = self.absolute_path_to_film.split('\\')[-1]
                self.path_to_dir_with_film = os.path.dirname(self.absolute_path_to_film)
                self.logger.debug("Selected film:\n"
                                  "Absolute path: {}\n"
                                  "Path to dir with film: {}\n"
                                  "Film file name: {}."
                                  .format(self.absolute_path_to_film, self.path_to_dir_with_film, self.film_file_name))
            except Exception as Error:
                self.logger.warning("Error during film selection: {}.".format(Error))
                QMessageBox.question(self, "Error", "Nie wybrano filmu", QMessageBox.Ok, QMessageBox.Ok)
                sys.exit(1)

    def open_file_name_dialog_for_player(self):
        selected_player, _ = QFileDialog.getOpenFileName(self, "Select video player", self.path_to_dir_with_film)
        if selected_player:
            self.logger.debug("Setting video_player...")
            textbox_player = get_settings_variable('textbox_player')
            textbox_player.setText(selected_player)
            set_application_variable('video_player', selected_player)
            self.logger.debug("video_player set to {}.".format(selected_player))


    ### ARCHIVED METHOD
    # def subtitles_setter(self):
    #     self.logger.info("Film will be played on {} with resolution {}."
    #                      .format(os.path.basename(get_application_variable('video_player')),
    #                              (GetSystemMetrics(0), GetSystemMetrics(1))))
    #     if os.path.basename(get_application_variable('video_player')) == 'vlc.exe':
    #         if GetSystemMetrics(0) > 1400:
    #             subtitles_setter_vlc.set_subtitles()
    #         else:
    #             subtitles_setter_vlc.set_subtitles(0.7)
    #     else:
    #         self.logger.error("Not supported player.")