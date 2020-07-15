import time
import default_logger
from get_set_functions import *
from singleton import GlobalSingletonDict
from babelfish import Language
from subliminal import download_best_subtitles, save_subtitles, scan_video
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QMessageBox


class SubtitlesDownloader(QMainWindow):
    def __init__(self, absolute_path_to_film, main_language, backup_language):
        super().__init__()
        subtitles_downloader = GlobalSingletonDict()
        subtitles_downloader['subtitles_dowloader'] = self
        self.logger = default_logger.logger_creation(name='subtitles_downloader')
        self.absolute_path_to_film = absolute_path_to_film
        self.video = scan_video(self.absolute_path_to_film)
        self.main_language = main_language
        self.backup_language = backup_language
        self.subtitles = None
        self.infobox = get_event_variable('infobox')

    def download(self):
        self.logger.info("Subtitle {} downloading for {} ...".format(self.main_language, self.absolute_path_to_film))
        self.infobox.setWindowTitle("Searching for {} subtitles...".format(self.main_language))
        self.logger.info("Searching for {} subtitles...".format(self.main_language))
        self.subtitles = download_best_subtitles([self.video], {Language(self.main_language)}, only_one=True)
        result = self.searching_subtitles_in_main_language()
        if not result:
            result = self.searching_subtitles_in_backup_language()
            if not result:
                result = self.manual_subtitles_download()
        return result

    def searching_subtitles_in_main_language(self):
        if self.subtitles[self.video]:
            save_subtitles(self.video, self.subtitles[self.video])
            self.logger.info("Subtitles {} downloaded.".format(self.main_language))
            self.infobox.setWindowTitle("Subtitles {} downloaded.".format(self.main_language))
            time.sleep(1)
            self.infobox.hide()
            return 1
        else:
            self.logger.warning(
                "No {} subtitles, try to download {} subtitles.".format(self.main_language, self.backup_language))
            self.infobox.setWindowTitle(
                "No {} subtitles, try to download {} subtitles.".format(self.main_language, self.backup_language))

    def searching_subtitles_in_backup_language(self):
        if self.subtitles[self.video]:
            save_subtitles(self.video, self.subtitles[self.video])
            self.logger.info("Subtitles {} downloaded.".format(self.backup_language))
            self.infobox.setWindowTitle("Subtitles {} downloaded.".format(self.backup_language))
            time.sleep(1)
            self.infobox.hide()
            return 1
        else:
            self.logger.warning("No {} subtitles.".format(self.backup_language))
            self.infobox.setWindowTitle("No {} subtitles.".format(self.backup_language))
            return 0

    def manual_subtitles_download(self):
        message = "Ściągnij napisy za pomocą QNapi.\n" \
                   "Okno dialogowe pojawi się po zamknięciu tego.\n" \
                  "Przy wyborze napisów kieruj się rozszerzeniem .srt.\n" \
                  "Po zamknięciu okna do wyszukania napisów rozpocznie się projekcja."
        QMessageBox.question(self, "Manualne ściaganie napisów", message, QMessageBox.Ok, QMessageBox.Ok)
        self.infobox.close()
        selected_film, _ = QFileDialog.getOpenFileName(self, "Select film", get_event_variable("path_to_dir_with_film"))
        return 0
