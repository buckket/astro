import logging


def setup_logger():
    logger = logging.getLogger('astro')
    logger.setLevel(logging.DEBUG)

    fh = logging.FileHandler('astro.log')
    fh.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s : %(name)-11s : %(levelname)-8s : %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger
