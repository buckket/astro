from ConfigParser import SafeConfigParser


def setup_config():
    parser = SafeConfigParser()
    parser.read('astro.cfg')
    return parser
