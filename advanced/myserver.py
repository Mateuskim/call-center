from twisted.internet.protocol import Protocol
from sys import stdout

from message import *

class MyProtocol(Protocol):
    """This is just about the simplest possible protocol"""

    def __init__(self, manager):
        self.manager = manager

    def connectionMade(self):
        stdout.write("Connection made")


    def dataReceived(self, data):
        command = translateMessage(data)
        answer_string = self.manager.execute_Command(command)
        answer_json = createResponse(answer_string)
        self.transport.write(answer_json)
