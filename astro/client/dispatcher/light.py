from .base import BaseDispatcher


class LightDispatcher(BaseDispatcher):

    def do(self, args):
        socket = self.generate_socket()

        if args.command_light == 'set_color':
            args_send = {'color': (args.r, args.g, args.b)}
            self.try_send(socket, self.wrap_data(args.command, args.command_light, args_send))

        elif args.command_light == 'get_color':
            if self.try_send(socket, self.wrap_data(args.command, args.command_light, {})):
                response = self.try_catch_response(socket)
                if response:
                    print "Current color: R: %s G: %s B: %s" % response['message']

        elif args.command_light == 'fade':
            args_send = {'color': (args.r, args.g, args.b)}
            self.try_send(socket, self.wrap_data(args.command, args.command_light, args_send))

        elif args.command_light == 'flash':
            args_send = {'count': 1}
            self.try_send(socket, self.wrap_data(args.command, args.command_light, args_send))

        elif args.command_light == 'strobo':
            self.try_send(socket, self.wrap_data(args.command, args.command_light, {}))

        elif args.command_light == 'stop':
            self.try_send(socket, self.wrap_data(args.command, args.command_light, {}))

        else:
            print "Unknown command: %s" % args.command_light
