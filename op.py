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

    def answerCall(self, op_id):
        if self.ID == op_id:
            if self.status == 'available' and self.curCall is not None:
                self.status = 'busy'
                self.curCall.setStatus('answered')
                return self.curCall
        return None

    def isAvailable(self):
        if self.status == 'available' and self.curCall is None:
            return True
        return False
