'''
Logging setup for bcpp tests
'''

import logging
import os


class ShyLogHandler(logging.StreamHandler):
    '''Emit messages only if root logger has no other handlers'''
    root = logging.getLogger()
    def emit(self, record):
        if not self.root.hasHandlers():
            super().emit(record)


def setup():
    log_file = os.environ.get('BCPP_TEST_LOG_FILE')
    log_stdout = os.environ.get('BCPP_TEST_LOG_STDOUT')

    log = logging.getLogger('bcpp_tests')
    log.level = logging.DEBUG

    if log_file:
        handler = logging.FileHandler(log_file, encoding='utf-8')
        handler.level = logging.DEBUG
        handler.formatter = logging.Formatter('%(asctime)s - %(message)s')
        log.addHandler(handler)

    if log_stdout:
        handler = ShyLogHandler()
        handler.level = logging.DEBUG
        log.addHandler(handler)

    return log
