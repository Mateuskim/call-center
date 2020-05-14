from twisted.internet.protocol import Protocol, ServerFactory

from message import *


class MyProtocol(Protocol):
    """This is just about the simplest possible protocol"""

    def __init__(self, manager):
        self.manager = manager


    def dataReceived(self, data):
        command = translateCommand(data)
        answer_string = self.manager.execute_Command(command)
        answer_json = createJson(answer_string)
        self.transport.write(answer_json)
