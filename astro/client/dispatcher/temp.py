from .base import BaseDispatcher


class TempDispatcher(BaseDispatcher):

    def format_temp(self, temp):
        return '%.2f' % (temp / 1000.0)

    def do(self, args):
        socket = self.generate_socket()

        if args.command_temp == 'get_temp' or args.command_temp is None:
            if self.try_send(socket, self.wrap_data(args.command, 'get_temp', {})):
                response = self.try_catch_response(socket)
                if response:
                    print "Temp: %s C" % self.format_temp(response['message'])
        else:
            print "Unknown command: %s" % args.command_temp

