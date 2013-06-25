import logging
import subprocess

from .base import BaseController


class RadioController(BaseController):

    def __init__(self):
        super(RadioController, self).__init__()
        self.logger = logging.getLogger('astro.radio')

    def execute_task(self, command, args, answer):
        if command == 'send':
            for device in args['devices']:
                self.logger.info('Calling radio helper: 433 %s %s %s', args['system_code'], device, args['status'])
                subprocess.call(['sudo', '433', args['system_code'], device, args['status']])
            answer(0)
        else:
            self.logger.warn('invalid command: %s', command)
            answer(1, 'invalid command')
