class Operator():

    def __init__(self, ID, status = 'Available'):
        self.ID = ID
        self.curCall = None
        self.status = status

    def setCall(self, call_id):
        self.curCall = call_id

    def setStatus(self, status):
        self.status = status

    def getID(self):
        return self.ID

    def getStatus(self):
        return self.status
