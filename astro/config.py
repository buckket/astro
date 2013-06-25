from ConfigParser import SafeConfigParser


def setup_config():
    config = SafeConfigParser()
    try:
        config.readfp(open('astro.cfg'))
    except IOError:
        return None
    return config
