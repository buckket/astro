import logging


def setup_logger(logfile=True):
    logger = logging.getLogger('astro')
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s : %(name)-12s : %(levelname)-8s : %(message)s')

    if logfile:
        fh = logging.FileHandler('astro.log')
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    return logger
