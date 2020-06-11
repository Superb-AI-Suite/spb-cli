import os
import logging
import logging.config
from logging.handlers import TimedRotatingFileHandler



class LoggerConfig():
  def __init__(self, logtype='STREAM', loglevel=logging.ERROR, filename='temp.log', rollover='m', interval=10, backupcount=10, format=None):
    self.logtype = logtype
    self.loglevel = loglevel
    self.filename = filename
    self.rollover = rollover
    self.interval = interval
    self.backupcount = backupcount

    if format is None:
        self.format = logging.Formatter('[%(asctime)s] %(process)d %(levelname)s in %(module)s: %(message)s')
    else:
        self.format = format

def _file_log_handler(config):
    logpath = os.path.dirname(__file__) + '/logs/' + config.filename
    logdir = os.path.dirname(logpath)
    if not os.path.exists(logdir):
        os.makedirs(logdir)
    fhandler = TimedRotatingFileHandler(logpath, when=config.rollover, interval=config.interval, backupCount=config.backupcount)
    fhandler.setFormatter(config.format)
    return fhandler

def _stream_log_handler(config):
    shandler = logging.StreamHandler()
    shandler.setFormatter(config.format)
    return shandler

def create_logger(config=LoggerConfig(), logger=None):
    if logger is not None:
        logger = logging.getLogger()
        logger.propagate = True
        logger.setLevel(config.loglevel)
        if config.logtype == 'FILE':
            handler = _file_log_handler(config)
            logger.addHandler(handler)
        elif config.logtype == 'STREAM':
            handler = _stream_log_handler(config)
            logger.addHandler(handler)
        else:
            shandler = _stream_log_handler(config)
            fhandler = _file_log_handler(config)
            logger.addHandler(shandler)
            logger.addHandler(fhandler)
    else:
        pass