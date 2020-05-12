class Operator(object):

    def __init__(self, ID, status = 'available'):
        self.ID = ID
        self.curCall = None
        self.status = status

    def setCall(self, call_id):
        self.status = 'busy'
        self.curCall = call_id
        self.curCall.setStatus('ringing')


    def setStatus(self, status):
        self.status = status

    def getID(self):
        return self.ID

    def getStatus(self):
        return self.status

    def answerCall(self, op_id):
        if self.ID == op_id:
            if self.status == 'busy' and self.curCall.getStatus() == 'ringing':
                self.curCall.setStatus('answered')
                return True
        return False

    def rejectCall(self, op_id):
        if self.ID == op_id:
            if self.status == 'busy' and self.curCall.getStatus() == 'ringing':
                self.curCall.setStatus('rejected')
                return True
        return False

    def isAvailable(self):
        if self.status == 'available':
            return True
        return False
