import logging
from messenger import config

FORMAT = '%(asctime)-15s::%(name)s::%(levelname)-6s %(message)s'
DATE_FORMAT = '%b %d %H:%M:%S'
logging.basicConfig(format=FORMAT, datefmt=DATE_FORMAT)

def get(name):
    conf = config.load()
    return _get_logger(name, conf['level'])

def get_default(name):
    return _get_logger(name, 'debug')

def _get_logger(name, level):
    logger = logging.getLogger(name)
    _set_access_level(logger, level)
    return logger

def _set_access_level(logger, level):
    logger.setLevel(_access_level(level))


def _access_level(level):
    return {'critical': logging.CRITICAL,
            'error': logging.ERROR,
            'warning': logging.WARNING,
            'info': logging.INFO,
            'debug': logging.DEBUG,
            'notset': logging.NOTSET
            }[level]
