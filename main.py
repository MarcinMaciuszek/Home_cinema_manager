import yaml
import sys
import default_logger
import logging
from application import Application
from event import Event
from PyQt5.QtWidgets import QApplication


LOG_LEVEL = logging.DEBUG


def config():
    try:
        with open('config.yaml', 'r') as yaml_file:
            config_file = yaml.safe_load(yaml_file)['settings']
        if config_file:
            logger.debug("Config file: {} found.".format(config_file))
            return Application(config=config_file)
        else:
            return Application()
    except IOError:
        logger.info('Config file not found.')
        return Application()


if __name__ == '__main__':
    try:
        logger = default_logger.logger_creation(name='main')
        logger.info('########## Start logger ##########')
        app = QApplication(sys.argv)
        event = Event()
        logger.debug('Event object created.')
        config()
        sys.exit(app.exec_())
    except Exception as Error:
        print("Error during application start: {}.".format(Error))
        sys.exit()
