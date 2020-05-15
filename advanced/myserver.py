from twisted.internet.protocol import Protocol
from sys import stdout

from message import *

class MyProtocol(Protocol):
    """This is just about the simplest possible protocol"""

    def __init__(self, manager):
        self.manager = manager

    def connectionMade(self):
        print("Connection made")


    def dataReceived(self, data):
        command = translateMessage(data)
        answer_string = self.manager.execute_Command(command)
        if answer_string is not None:
            answer_json = createResponse(answer_string)
        else :
            answer_json = createResponse("Command not executed")
        self.transport.write(answer_json)
