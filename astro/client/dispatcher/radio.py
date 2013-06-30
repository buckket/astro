from .base import BaseDispatcher


class RadioDispatcher(BaseDispatcher):

    def __init__(self, system_code, host, port, key):
        super(RadioDispatcher, self).__init__(host=host, port=port, key=key)
        self.system_code = system_code

    def do(self, args):
        socket = self.generate_socket()

        devices = args.devices
        status = args.status

        if status == '1' or status == 'on':
            status = 'on'
        elif status == '0' or status == 'off':
            status = 'off'
        else:
            print "Invalid status"
            return False

        args_send = {'system_code': self.system_code, 'devices': devices, 'status': status}
        self.try_send(socket, self.wrap_data(args.command, 'send', args_send))

