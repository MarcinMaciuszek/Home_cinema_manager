import os
import re
import default_logger
from get_set_functions import *
from singleton import GlobalSingletonDict

ARCHIVE_DIR = "Old"


class Mover:
    def __init__(self, archive_dir=ARCHIVE_DIR):
        mover = GlobalSingletonDict()
        mover['mover'] = self
        self.logger = default_logger.logger_creation(name='mover')
        self.archive_dir = archive_dir
        self.path_to_dir_with_film = os.path.abspath(get_event_variable('path_to_dir_with_film'))
        self.film_file_name = get_event_variable('film_file_name')
        self.archive_path = r"{}\{}".format(self.path_to_dir_with_film, self.archive_dir)
        self.files_list_in_dir_with_film = os.listdir(self.path_to_dir_with_film)
        self.biggest_size_of_file = 0
        self.biggest_file_name = ""
        self.list_of_files_of_old_subtitles = []

    def move(self):
        # TODO regex
        # print(self.film_file_name)
        # print(self.files_list_in_dir_with_film)
        # for film in self.files_list_in_dir_with_film:
        #     if '.srt' in film or '.txt' in film:
        #         print("{} uuuu".format(film))
        self.archive_dir_initialization()
        self.finding_old_subtitles()
        self.moving_to_archive_dir_old_subtitles()

        # self.finding_biggest_file_in_dir_with_film()
        # self.moving_to_archive_dir_each_files_excluding_biggest()

    def archive_dir_initialization(self):
        if os.path.isdir(self.archive_path):
            self.logger.debug("Dir {} already exist.".format(self.archive_path))
        else:
            os.mkdir(self.archive_path)
            self.logger.debug("{} created.".format(self.archive_path))

    def finding_old_subtitles(self):
        pattern = re.compile(r'.*.(srt|txt)$')
        for file in self.files_list_in_dir_with_film:
            result = pattern.search(file)
            if result:
                self.list_of_files_of_old_subtitles.append(file)

    def moving_to_archive_dir_old_subtitles(self):
        for file in self.list_of_files_of_old_subtitles:
            path_to_file = r"{}\{}".format(self.path_to_dir_with_film, file)
            destination_path_to_file_in_archive = r"{}\{}".format(self.archive_path, file)
            self.logger.debug("Moving {} to {}.".format(path_to_file, destination_path_to_file_in_archive))
            try:
                os.rename(path_to_file, destination_path_to_file_in_archive)
            except FileExistsError:
                os.remove(destination_path_to_file_in_archive)
                os.rename(path_to_file, destination_path_to_file_in_archive)
                self.logger.debug("Replacing old file.")

    def finding_biggest_file_in_dir_with_film(self):
        self.logger.debug("List of files in {} : {}.".format(self.path_to_dir_with_film,
                                                             self.files_list_in_dir_with_film))
        self.logger.info("Finding biggest file...")
        for file in self.files_list_in_dir_with_film:
            path_to_file = r"{}\{}".format(self.path_to_dir_with_film, file)
            if os.path.isdir(path_to_file):
                self.logger.debug("{} is dir.".format(path_to_file))
            elif os.path.getsize(path_to_file) > self.biggest_size_of_file:
                self.biggest_size_of_file = os.path.getsize(path_to_file)
                self.biggest_file_name = path_to_file
                self.logger.debug("Finded new biggest file: {} about size: {}."
                                  .format(path_to_file, self.biggest_size_of_file))
            else:
                continue
        self.logger.info("Moving files to {} excluding {}.".format(self.archive_path, self.biggest_file_name))

    def moving_to_archive_dir_each_files_excluding_biggest(self):
        for file in self.files_list_in_dir_with_film:
            path_to_file = r"{}\{}".format(self.path_to_dir_with_film, file)
            if path_to_file != self.biggest_file_name and path_to_file != self.archive_path:
                destination_path_to_file_in_archive = r"{}\{}".format(self.archive_path, file)
                self.logger.debug("Moving {} to {}.".format(path_to_file, destination_path_to_file_in_archive))
                try:
                    os.rename(path_to_file, destination_path_to_file_in_archive)
                except FileExistsError:
                    os.remove(destination_path_to_file_in_archive)
                    os.rename(path_to_file, destination_path_to_file_in_archive)
                    self.logger.debug("Replacing old file.")
