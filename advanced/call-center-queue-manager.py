from twisted.internet import reactor
from twisted.internet.protocol import ServerFactory
from manager import Manager
from myserver import MyServer

def main():
    
    manager = Manager()
    """This runs the protocol on port 5678"""
    factory = ServerFactory()
    factory.protocol = MyServer(manager)
    reactor.listenTCP(5678, factory)
    reactor.run()

# this only runs if the module was *not* imported
if __name__ == '__main__':
    main()
