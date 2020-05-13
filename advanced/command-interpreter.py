from twisted.internet import reactor, protocol
import json

def createJSON(command):
    json_command = {}
    json_command["command"] = command[:-2]
    json_command["id"] =command[-1:]
    return json_command
def packJson(json_message):
    return json.dumps(json_message).encode("utf-8")

def translateAnswer(message_answer):
    return json.loads(message_answer.decode("utf-8"))


class EchoClient(protocol.Protocol):
    """Once connected, send a message, then print the result."""

    def connectionMade(self):

        command = createJSON('reject 1')
        json_message = packJson(command)
        self.transport.write(json_message)

    def dataReceived(self, answer):
        "As soon as any data is received, write it back."
        answer_json = translateAnswer(answer)
        print(answer_json["response"])
        self.transport.loseConnection()

    def connectionLost(self, reason):
        print("connection lost")


class EchoFactory(protocol.ClientFactory):
    protocol = EchoClient

    def clientConnectionFailed(self, connector, reason):
        print("Connection failed - goodbye!")
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        print("Connection lost - goodbye!")
        reactor.stop()

# this connects the protocol to a server running on port 8000
def main():
    f = EchoFactory()
    reactor.connectTCP("34.95.167.27", 5678, f)
    reactor.run()

# this only runs if the module was *not* imported
if __name__ == '__main__':
    main()
