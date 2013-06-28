import threading
import Queue

import logging


class BaseController(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

        self.logger = logging.getLogger('astro.BaseController')

        self.stop_requested = False
        self.queue = Queue.Queue()

    def shutdown(self):
        self.stop_requested = True

    def execute_task(self, command, args, answer):
        pass

    def run(self):
        while not self.stop_requested:
            try:
                ((command, args), answer) = self.queue.get(block=True, timeout=1.0)
                self.execute_task(command, args, answer)
                self.queue.task_done()
            except Queue.Empty:
                continue
        self.logger.debug('Received stop_requested')
