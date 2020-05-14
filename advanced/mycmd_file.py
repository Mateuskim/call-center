from sys import stdout
from cmd import Cmd

from twisted.internet import reactor
from twisted.internet.protocol import Protocol
from twisted.internet.endpoints import TCP4ClientEndpoint, connectProtocol

class MyCmd(Cmd):
    def __init__(self, client):
        Cmd.__init__(self)
        self.client = client

    def default(self, line):
        client.sendData(line)

    def do_ola(self, line):
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

point = TCP4ClientEndpoint(reactor, "localhost", 5678)
client = MyClient()
connectProtocol(point, client)
reactor.callInThread(MyCmd(client).cmdloop)
reactor.run()