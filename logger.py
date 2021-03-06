""" Class : Logger

Author: Peter Lee
Date created: 2016 Jan 27

The Logger class makes use of the queue.Queue() to pass module logs into the queue pipe, and a listener (works on a different thread) to display logging information to the User Interface.

Handlers
--------
    console_handler : StreamHander()
        Directs outputs to sys.stdout; Using curses wrapper method, the logging outputs will be viewable when quiting the UI.

    ui_handler : QueueHandler()
        Directs outputs to the queue.Queue() object (same queue within the FincLab engine).

"""


import queue
import logging
import logging.handlers
from config import config


def create_logger(log_queue):
    """
    Create a logger with multiple handles.

    Parameters
    ----------
        log_queue : queue.Queue()
            The queue for the QueueHandler.
    """

    # Load settings
    level = logging.getLevelName(config['log']['level'])
    log_in_user_interface = config.getboolean('log', 'log_in_user_interface')
    save_to_file = config.getboolean('log', 'save_to_file')
    log_filename = config['log']['log_filename']

    # create a logger
    logger = logging.getLogger("FincLab")
    logger.setLevel(level)

    # Formatter
    formatter = logging.Formatter(fmt="%(asctime)s %(name)-12s %(levelname)-8s %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    formatter = logging.Formatter(fmt="%(name)-18s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    # create consoleHandler
    # console_handler = logging.StreamHandler()
    # console_handler.setLevel(logging.DEBUG)
    # console_handler.setFormatter(formatter)
    # logger.addHandler(console_handler)

    # create queue handler for the user interface
    if log_in_user_interface:
        queue_handler = logging.handlers.QueueHandler(log_queue)
        queue_handler.setLevel(level)
        queue_handler.setFormatter(formatter)
        logger.addHandler(queue_handler)

    # create a file handler to save log
    if save_to_file:
        file_handler = logging.FileHandler(log_filename, mode='w')
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


if __name__ == '__main__':
    # Logging to a file
    # logging.basicConfig(filename='/Users/peter/Workspace/FincLab/src/example.log', level=logging.DEBUG)
    # logging.debug('This message should go to the log file.')
    # logging.info('So should this one')
    # logging.warning('And this too!')

    # Initialise the event_queue logger
    log_queue = queue.Queue()
    logger = create_logger(log_queue)

    # Testing the sys.stdout handler
    print("Testing the sys.stdout handler")
    logger.debug('Old: debug message')
    logger.info('Old: info msg')
    logger.warn('Old: warn msg')
    logger.error('Old: error msg')
    logger.critical('Old: critical msg')

    # Testing the queue handler
    print("Testing the queue handler")
    handler = logging.StreamHandler()
    listener = logging.handlers.QueueListener(log_queue, handler)
    listener.start()
    logger.warn('new: dwarn msg')
    logger.error('new: derror msg')
    logger.warn('new: warn msg')
    logger.error('new: error msg')
    logger.critical('new: critical msg')
    listener.stop()

    print("Tests complete.")
