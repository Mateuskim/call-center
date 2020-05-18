from cmd import Cmd
from message import *
from twisted.internet import reactor


class MyCmd(Cmd):
    def __init__(self, client):
        Cmd.__init__(self)
        self.prompt = ''
        self.client = client

    def default(self, answer):
        print("comando nao executado")

    def do_call(self, call_id):
        command = 'call ' + call_id
        json_command = createCommand(command)
        pack_json = packJson(json_command)
        self.client.sendData(pack_json)

    def do_answer(self, op_id):
        command = 'answer ' + op_id
        json_command = createCommand(command)
        pack_json = packJson(json_command)
        self.client.sendData(pack_json)

    def do_reject(self, op_id):
        command = 'reject ' + op_id
        json_command = createCommand(command)
        pack_json = packJson(json_command)
        self.client.sendData(pack_json)

    def do_hangup(self, call_id):
        command = 'hangup ' + call_id
        json_command = createCommand(command)
        pack_json = packJson(json_command)
        self.client.sendData(pack_json)

    def do_quit(self, *args):
        if reactor.running:
            reactor.stop()
        return True