from twisted.internet.protocol import Protocol
from message import *


class MyProtocol(Protocol):
    """This is just about the simplest possible protocol"""

    def __init__(self, manager):
        self.manager = manager

    def connectionMade(self):
        print("Connection made")

    def dataReceived(self, data):
        command = translateMessage(data)
        print("Command received: "+command + "\n")
        answer_string = self.manager.execute_Command(command, self)
        if answer_string is not None:
            answer_json = createResponse(answer_string)
        else:
            answer_json = createResponse("Command not executed")
        self.transport.write(answer_json)

    def sendData(self, data):
        answer_json = createResponse(data)
        self.transport.write(answer_json)
