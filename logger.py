import logging as log
from logging import handlers
from config import basic_config as conf
import time
import os

def get_level(level: str):
    if level.lower() == "debug":
        return log.DEBUG
    elif level.lower() == "info":
        return log.INFO
    elif level.lower() == "warning":
        return log.WARNING
    elif level.lower() == "error":
        return log.ERROR
    elif level.lower() == "fatal":
        return log.FATAL
    elif level.lower() == "critical":
        return log.CRITICAL
    else:
        return log.INFO

def _logging(**kwargs):
    level = kwargs.pop('level', None)
    filename = kwargs.pop('filename', None)
    datefmt = kwargs.pop('datefmt', None)
    format = kwargs.pop('format', None)
    if level is None:
        level = log.DEBUG
    if filename is None:
        filename = 'default.log'
    if datefmt is None:
        datefmt = '(%H:%M:%S %a)'
    if format is None:
        format = 'T:(%(thread)s)%(asctime)s[%(name)s-%(levelname)s] %(message)s'

    _log = log.getLogger()
    format_str = log.Formatter(format, datefmt)
    # backupCount 保存日志的数量，过期自动删除
    # when 按什么日期格式切分(使用date)
    th = handlers.TimedRotatingFileHandler(filename=filename, when='d', backupCount=5, encoding='utf-8')
    th.setFormatter(format_str)
    th.setLevel(get_level(conf.loggingLevel))
    # stdout
    ch = log.StreamHandler()
    ch.setFormatter(format_str)
    ch.setLevel(get_level(conf.loggingLevel))
    _log.addHandler(ch)
    _log.addHandler(th)
    _log.setLevel(level)
    return _log


os.makedirs(conf.loggingPath, exist_ok=True)
file_logger = _logging(filename=os.path.join(conf.loggingPath, "server.log.{date}".format(
    date=time.strftime("%Y-%m-%d", time.localtime()))))
if __name__ == '__main__':
    cnt = 1
    while True:
        time.sleep(1)
        file_logger.debug('hhh')
        file_logger.info('hhh')
        file_logger.warning('hhh')
        file_logger.critical('asdad')
        cnt += 1
        if cnt == 10:
            break
