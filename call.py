class Call(object):
    def __init__(self, ID):
        self.ID = ID
        self.status = None
        self.op = None

    def setStatus(self, status):
        self.status = status

    def getStatus(self):
        return self.status

    def setOp(self, op):
        self.op = op

    def getOp(self):
        return self.op