from twisted.internet.protocol import Protocol
from sys import stdout
from message import *

class MyClient(Protocol):

    def connectionMade(self):
        print("Connection made")

    def dataReceived(self, data):
        answer_json = translateMessage(data)
        answer = getAnswer(answer_json)
        print("========== ANSWER FROM SERVER ==============")
        print(answer, end='')
        print("============================================")
        stdout.flush()

    def sendData(self, data):
        self.transport.write(data)