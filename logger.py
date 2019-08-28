import sys
import time
import logging

def init_logger(name, log_level=logging.INFO, propagate=False, **kwargs):
    logging.Formatter.converter = time.gmtime
    logger = logging.getLogger(name)
    formatter = logging.Formatter("%(name)s, %(asctime)s, %(message)s")
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.propagate = propagate
    logger.setLevel(log_level)

    return logger