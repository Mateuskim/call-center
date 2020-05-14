import json
from sys import stdout
from cmd import Cmd
from twisted.internet import reactor
from twisted.internet.protocol import Protocol
from twisted.internet.endpoints import TCP4ClientEndpoint, connectProtocol
from server import Server



def createJSON(command):
    json_command = {}
    json_command["command"] = command[:-2]
    json_command["id"] = command[-1:]
    json_command["response"] = "mensagem default"
    return json_command


def packJson(json_message):
    return json.dumps(json_message).encode("utf-8")


def translateAnswer(message_answer):
    return json.loads(message_answer.decode("utf-8"))


def getAnswer(message_json):
    return message_json["response"]


class MyCmd(Cmd):
    def __init__(self, client):
        Cmd.__init__(self)
        self.prompt = ''
        self.client = client
    def default(self, answer):
        print("nao existe")

    def do_call(self, call_id):
        command = 'call ' + call_id
        json_command = createJSON(command)
        pack_json = packJson(json_command)
        self.client.sendData(pack_json)

    def do_answer(self, op_id):
        command = 'answer ' + op_id
        json_command = createJSON(command)
        pack_json = packJson(json_command)
        self.client.sendData(pack_json)

    def do_reject(self, op_id):
        command = 'reject ' + op_id
        json_command = createJSON(command)
        pack_json = packJson(json_command)
        self.client.sendData(pack_json)

    def do_hangup(self, call_id):
        command = 'hangup ' + call_id
        json_command = createJSON(command)
        pack_json = packJson(json_command)
        self.client.sendData(pack_json)

    def do_quit(self, line):
        if reactor.running:
            reactor.stop()
        stdout.write("\n")
        return True


class MyClient(Protocol):
    def __init__(self, myServer):
        self.myServer = myServer

    def dataReceived(self, data):
        answer_json = translateAnswer(data)
        answer = getAnswer(answer_json)
        self.myServer.execute_Command(answer)
        stdout.write(answer)
        stdout.flush()

    def sendData(self, data):
        self.transport.write(data)


# this connects the protocol to a server running on port 8000
def main():

    myServer = Server()
    point = TCP4ClientEndpoint(reactor, "34.95.167.27", 5678)
    client = MyClient(myServer)
    connectProtocol(point, client)
    reactor.callInThread(MyCmd(client).cmdloop)
    reactor.run()



# this only runs if the module was *not* imported
if __name__ == '__main__':
    main()
