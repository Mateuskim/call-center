from twisted.internet import reactor, protocol
import json

class Echo(protocol.Protocol):
    """This is just about the simplest possible protocol"""

    def dataReceived(self, data):
        json_response = {}
        command = data["command"]
        id = data["id"]
        if command == "call":
            json_response["response"] = "Call " + id + "received"

        "As soon as any data is received, write it back."
        self.transport.write(json_response)


def main():
    """This runs the protocol on port 8000"""
    factory = protocol.ServerFactory()
    factory.protocol = Echo
    reactor.listenTCP(5678, factory)
    reactor.run()


# this only runs if the module was *not* imported
if __name__ == '__main__':
    main()
