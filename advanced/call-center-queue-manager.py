from twisted.internet import reactor
from twisted.internet.protocol import Factory
from twisted.internet.endpoints import TCP4ServerEndpoint
from manager import Manager
from myserver import MyProtocol
import time as timer


class MyFactory(Factory):
    def __init__(self, manager):
        self.manager = manager

    def buildProtocol(self, addr):
        return MyProtocol(manager=self.manager)


def main():
    manager = Manager()
    factory = MyFactory(manager)
    endpoint = TCP4ServerEndpoint(reactor, 5678)
    endpoint.listen(factory)
    reactor.run()

# this only runs if the module was *not* imported
if __name__ == '__main__':
    main()
