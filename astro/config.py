from ConfigParser import SafeConfigParser


def setup_config(config_file):
    config = SafeConfigParser()
    try:
        config.readfp(config_file)
    except IOError:
        return None
    return config

def server_config_helper(cfg):
    config = {'host': cfg.get('server', 'host'),
        'port': cfg.getint('server', 'port'),
        'key': cfg.get('server', 'key')}
    return config

def temp_config_helper(cfg):
    config = {'w1_device': cfg.get('temp', 'w1_device'),
        'xivley': {'apikey': cfg.get('temp', 'xivley_key'), 'url': cfg.get('temp', 'xivley_url')},
        'period': cfg.getfloat('temp', 'period')}
    return config

def light_config_helper(cfg):
    config = {'red': cfg.get('light', 'red'),
        'green': cfg.get('light', 'green'),
        'blue': cfg.get('light', 'blue'),
        'frequency': cfg.getint('light', 'frequency')}
    return config

def client_config_helper(cfg):
    config = {'host': cfg.get('client', 'target_host'),
        'port': cfg.getint('client', 'port'),
        'key': cfg.get('client', 'key')}
    return config
