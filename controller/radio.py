import threading
import Queue

import logging

import subprocess


class RadioController(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

        self.logger = logging.getLogger('astro.radio')

        self.stop_requested = False
        self.queue = Queue.Queue()

    def shutdown(self):
        self.stop_requested = True

    def execute_task(self, command, args, answer):
        if command == 'send':
            for device in args['devices']:
                self.logger.info('Calling radio helper: 433 %s %s %s', args['system_code'], device, args['status'])
                subprocess.call(['sudo', '433', args['system_code'], device, args['status']])
            answer(0)
        else:
            self.logger.warn('invalid command: %s', command)
            answer(1, 'invalid command')

    def run(self):
        while not self.stop_requested:
            try:
                ((command, args), answer) = self.queue.get(block=True, timeout=1.0)
                self.execute_task(command, args, answer)
                self.queue.task_done()
            except Queue.Empty:
                continue
        self.logger.debug('Received stop_requested')
