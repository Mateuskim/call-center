import cmd
class Server(cmd.Cmd):
    prompt = '(Client)'

    # ------------------ Client commands -----------------------

    def do_call(self, call_id):
        print('Call ', call_id, 'received')