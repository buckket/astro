import threading
import Queue

import logging

import requests
import json


class TempController(threading.Thread):

    def __init__(self, w1_device=None, xivley=None, period=60.0):
        threading.Thread.__init__(self)

        self.logger = logging.getLogger('astro.temp')
        requests_log = logging.getLogger('requests')
        requests_log.setLevel(logging.WARNING)

        self.stop_requested = False
        self.queue = Queue.Queue()

        self.w1_device = w1_device
        self.xivley = xivley
        self.period = period

        self.timer = None
        self.temp = 0

    def shutdown(self):
        self.stop_requested = True

    def read_temp(self):
        try:
            with open(self.w1_device, 'r') as f:
               lines = f.readlines()
            temp = int(lines[1][lines[1].find('t=')+2:])
        except (IOError, ValueError):
            self.logger.error('Error while fetching data')
            return None
        else:
            self.logger.debug('Fetched new data: %s)', temp)
            return temp

    def push_temp(self, temp):

        if temp:

            # xivley
            if self.xivley:
                headers = {'X-ApiKey': self.xivley['apikey']}
                payload = {'current_value': self.format_temp(temp)}
                try:
                    r = requests.put(self.xivley['url'], data=json.dumps(payload), headers=headers)
                except:
                    self.logger.error('Network error while pushing to xivley')
                else:
                    if r.status_code == requests.codes.ok:
                        self.logger.info('xivley accepted push_temp request (temp: %s)', temp)
                    else:
                        self.logger.warn('xivley declined push_temp request (temp: %s)', temp)

        else:
            self.logger.warn('temp is not set or invalid, skipping push_temp')

    def format_temp(self, temp):
        return '%.2f' % (temp / 1000.0)

    def periodic_task(self):
        self.logger.debug('periodic_task was called')
        self.timer = threading.Timer(self.period, self.periodic_task)
        self.timer.start()

        self.temp = self.read_temp()
        self.push_temp(self.temp)

    def execute_task(self, command, args, answer):
        if command == 'get_temp':
            answer(0, self.temp)
        else:
            self.logger.warn('invalid command: %s', command)
            answer(1, 'invalid command')

    def run(self):
        self.periodic_task()
        while not self.stop_requested:
            try:
                ((command, args), answer) = self.queue.get(block=True, timeout=1.0)
                self.execute_task(command, args, answer)
                self.queue.task_done()
            except Queue.Empty:
                continue
        self.timer.cancel()
        self.logger.debug('Received stop_requested')
