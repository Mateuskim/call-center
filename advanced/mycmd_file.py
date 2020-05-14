from sys import stdout
from cmd import Cmd

from twisted.internet import reactor
from twisted.internet.protocol import Protocol, ServerFactory

class MyCmd(Cmd):
    def __init__(self, client):
        Cmd.__init__(self)
        self.client = client

    def default(self, line):
        client.sendData(line)

    def do_greeting(self, line):
        print("ola")

    def do_EOF(self, line):
        if reactor.running:
            reactor.stop()
        stdout.write("\n")
        return True


class MyClient(Protocol):
    def dataReceived(self, data):
        stdout.write(data)

    def sendData(self, data):
        self.transport.write(data)
        self.transport.write("\n")

factory = ServerFactory()
factory.protocol = MyClient()
reactor.listenTCP(5678, factory)
reactor.callInThread(MyCmd(factory.protocol).cmdloop)
reactor.run()