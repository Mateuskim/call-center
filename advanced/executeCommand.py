from sys import stdout
from cmd import Cmd

from twisted.internet import reactor, protocol
from twisted.internet.protocol import Protocol

class MyCmd(Cmd):
    def __init__(self, client):
        Cmd.__init__(self)
        self.client = client

    def default(self, line):
        factory.sendData(line)

    def do_quit(self, line):
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


factory = protocol.ServerFactory()
factory.protocol = MyClient
reactor.listenTCP(5678, factory)
reactor.callInThread(MyCmd().cmdloop())
reactor.run()

