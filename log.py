import logging
import logging.handlers
import time
from conf import conf

class WxLog():
    def __init__(self, path):
        if conf.uselog == 1:
            logger = logging.getLogger()
            hdlr   = logging.handlers.TimedRotatingFileHandler(path, when=conf.interval_unit, interval=conf.interval, backupCount=40)
            fmt    = logging.Formatter('%(asctime)s %(message)s')
            hdlr.setFormatter(fmt)
            logger.addHandler(hdlr)
            logger.setLevel(logging.NOTSET)
            self.log = logger
        else:
            pass
    def Print(self, msg):
        if conf.uselog == 1:
            self.log.info('\3' + msg)
        else:
            pass

log = WxLog(conf.logloc)

if __name__ == '__main__':
    i = 1
    while True:
        log.Print(i)
        time.sleep(1)
        i = i+1
