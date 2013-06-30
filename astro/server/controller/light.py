import logging
import time

import Queue

from .base import BaseController


class LightController(BaseController):

    def __init__(self, red, green, blue, frequency):
        super(LightController, self).__init__()

        self.logger = logging.getLogger('astro.light')

        self.red = red
        self.green = green
        self.blue = blue
        self.frequency = frequency

        self.mode = None

    def get_color(self):
        def get_duty(color):
            try:
                with open('/sys/class/pwm/%s/duty_ns' % color, 'r') as fw:
                    duty = 255 - int(int(fw.read()) * 255 / self.frequency)
                    return duty
            except (IOError, ValueError):
                self.logger.error('PWM error while getting values')
                return 0
        return (get_duty(self.red), get_duty(self.green), get_duty(self.blue))

    def set_color(self, color):
        def set_duty(color, value):
            try:
                with open('/sys/class/pwm/%s/duty_ns' % color, 'w') as fw:
                    fw.write('%d' % (value))
            except (IOError, ValueError):
                self.logger.error('PWM error while writting values')
        set_duty(self.red, self.frequency - (color[0] * self.frequency / 255))
        set_duty(self.green, self.frequency - (color[1] * self.frequency / 255))
        set_duty(self.blue, self.frequency - (color[2] * self.frequency / 255))

    def avg_color(self, color1, color2, weight=1):
        return ((color1[0]*weight+color2[0])/(1+weight), (color1[1]*weight+color2[1])/(1+weight), (color1[2]*weight+color2[2])/(1+weight))

    def fade(self, color, steps=50, sleep_time=0.0005):
        for s in range(0, steps):
            self.set_color(self.avg_color(self.get_color(), color, steps-s))
            time.sleep(sleep_time)
        self.set_color(color)

    def flash(self, count=1):
        old_color = self.get_color()
        if old_color == (0, 0, 0):
            color = (255, 255, 255)
        else:
            color = (0, 0, 0)
        for i in range(0, count):
            self.fade(color)
            self.fade(old_color)

    def strobo(self):
        self.logger.info('Entering strobo mode')
        old_color = self.get_color()
        while self.queue.empty() and not self.stop_requested:
            self.set_color((0, 0, 0))
            time.sleep(0.15)
            self.set_color((255, 255, 255))
            time.sleep(0.04)
        self.set_color(old_color)
        self.logger.info('Stopping strobo mode')

    def execute_task(self, command, args, answer):
        if command == 'set_color':
            self.logger.info('Setting color (R: %s G: %s B: %s)' % args['color'])
            self.set_color(args['color'])
            answer(0)

        elif command == 'get_color':
            color = self.get_color()
            self.logger.info('Reading current color (R: %s G: %s B: %s)' % color)
            answer(0, color)

        elif command == 'fade':
            self.logger.info('Fading color (R: %s G: %s B: %s)' % args['color'])
            self.fade(args['color'])
            answer(0)

        elif command == 'flash':
            self.logger.info('Flashing lights')
            if 'count' in args:
                self.flash(count=args['count'])
            else:
                self.flash()
            answer(0)

        elif command == 'strobo':
            self.mode = self.strobo
            answer(0)

        elif command == 'stop':
            self.mode = None
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
                if self.mode:
                    self.mode()
            except Queue.Empty:
                continue
        self.logger.debug('Received stop_requested')
