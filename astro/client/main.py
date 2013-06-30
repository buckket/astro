from astro.config import setup_config, client_config_helper

from astro.client.dispatcher.temp import TempDispatcher
from astro.client.dispatcher.light import LightDispatcher
from astro.client.dispatcher.radio import RadioDispatcher


class AstroClient(object):

    def __init__(self, config_file):
        cfg = setup_config(config_file)
        network_settings = client_config_helper(cfg)

        self.dispatcher = {}
        self.add_dispatcher(TempDispatcher(**network_settings), 'temp')
        self.add_dispatcher(LightDispatcher(**network_settings), 'light')
        self.add_dispatcher(RadioDispatcher(system_code=cfg.get('radio', 'system_code'), **network_settings), 'radio')

    def add_dispatcher(self, ref, name):
        self.dispatcher[name] = ref

    def dispatch(self, args):
        try:
            dispatcher = self.dispatcher[args.command]
            dispatcher.do(args)
        except KeyError:
            return False
