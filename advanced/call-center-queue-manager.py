from twisted.internet import reactor, protocol
from server import Server
import json

class Echo(protocol.Protocol):
    """This is just about the simplest possible protocol"""

    def dataReceived(self, data):
        json_response = json.loads(data.decode("utf-8"))
        command = json_response["command"]
        id = json_response["id"]
        answer_json = {}
        if command == "call":
            answer_json["response"] = "Call " + id + " received"


        answer = json.dumps(answer_json).encode("utf-8")

        "As soon as any data is received, write it back."
        self.transport.write(answer)


def main():
    """This runs the protocol on port 8000"""
    factory = protocol.ServerFactory()
    factory.protocol = Echo
    reactor.listenTCP(5678, factory)
    reactor.callInThread(Server.cmdloop())
    reactor.run()


# this only runs if the module was *not* imported
if __name__ == '__main__':
    main()
