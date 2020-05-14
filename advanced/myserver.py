from twisted.internet.protocol import Protocol, ServerFactory

from message import *


class MyProtocol(Protocol):
    """This is just about the simplest possible protocol"""

    def __init__(self, factory,  manager):
        self.manager = manager
        self.factory = factory

    def connectionMade(self):
        self.factory.numProtocols = self.factory.numProtocols + 1

    def connectionLost(self, reason):
        self.factory.numProtocols = self.factory.numProtocols - 1

    def dataReceived(self, data):
        command = translateCommand(data)
        answer_string = self.manager.executeCommand(command)
        answer_json = createJson(answer_string)
        self.transport.write(answer_json)
