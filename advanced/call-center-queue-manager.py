from twisted.internet import reactor, protocol
import json

def translateCommand(str_json):
    json_response = json.loads(str_json.decode("utf-8"))
    command = json_response["command"]
    id = json_response["id"]
    command_string = command + " " + id
    return command_string


def executeCommand(command):
    return command + "\n"


def createJson(answer):
    answer_json = {}
    answer_json["response"] = answer
    return json.dumps(answer_json).encode("utf-8")


class Echo(protocol.Protocol):
    """This is just about the simplest possible protocol"""


    def dataReceived(self, data):
        command = translateCommand(data)
        answer_string = executeCommand(command)
        answer_json = createJson(answer_string)
        self.transport.write(answer_json)



def main():
    """This runs the protocol on port 5678"""
    factory = protocol.ServerFactory()
    factory.protocol = Echo
    reactor.listenTCP(5678, factory)
    reactor.run()


# this only runs if the module was *not* imported
if __name__ == '__main__':
    main()
