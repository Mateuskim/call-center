class Call(object):
    def __init__(self, ID):
        self.ID = ID

        # status = ringing, waiting, rejected, answered, ended
        self.status = None
        self.op = None
    def getID(self):
        return self.ID

    def setStatus(self, status):
        self.status = status

    def getStatus(self):
        return self.status

    def setOp(self, op):
        self.op = op

    def getOp(self):
        return self.op
