from sys import stdout
from twisted.internet import reactor, protocol
from twisted.internet.stdio import StandardIO
from server import Server
import json

class Echo(protocol.Protocol):
    """This is just about the simplest possible protocol"""

    def dataReceived(self, data):
        json_response = json.loads(data.decode("utf-8"))
        command = json_response["command"]
        id = json_response["id"]
        command_string = command + " " + id
        # if command == "call":
        #     answer_json["response"] = "Call " + id + " received"
        # StandardIO(command_string)
        stdout.write(command_string)

        answer_json = {}
        answer = json.dumps(answer_json).encode("utf-8")
        "As soon as any data is received, write it back."
        self.transport.write(answer)



def main():
    """This runs the protocol on port 5678"""
    factory = protocol.ServerFactory()
    factory.protocol = Echo
    reactor.listenTCP(5678, factory)
    reactor.callInThread(Server().cmdloop())
    reactor.run()


# this only runs if the module was *not* imported
if __name__ == '__main__':
    main()
