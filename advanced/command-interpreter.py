from myclient import MyClient
from mycmd import MyCmd
from message import *
from twisted.internet import reactor
from twisted.internet.endpoints import TCP4ClientEndpoint, connectProtocol


# this connects the protocol to a server running on port 8000
def main():
    point = TCP4ClientEndpoint(reactor, "35.247.222.99", 5678)
    client = MyClient()
    connectProtocol(point, client)
    reactor.callInThread(MyCmd(client).cmdloop)
    reactor.run()


# this only runs if the module was *not* imported
if __name__ == '__main__':
    main()
