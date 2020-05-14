import json
from twisted.internet import reactor
from twisted.internet.endpoints import TCP4ServerEndpoint, connectProtocol
from manager import Manager
from myserver import MyServer

def main():
    """Declare Server class"""
    myManager = Manager()
    endpoint = TCP4ServerEndpoint(reactor, 5678)
    server = MyServer(myManager)
    endpoint.listen()

    reactor.run()


# this only runs if the module was *not* imported
if __name__ == '__main__':
    main()
