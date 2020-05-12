class Call(object):
    def __init__(self, ID):
        self.ID = ID
        self.status = None

    def setStatus(self, status):
        self.status = status

    def getStatus(self):
        return self.status
