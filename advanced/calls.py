class Calls(object):
    def __init__(self):
        self.calls = []

    def addCall(self, call):
        self.calls.append(call)

    def endCall(self, call):
        for c in self.calls:
            if call.getID() == c.getID():
                if call in self.calls:
                    self.calls.remove(call)

    def searchCall(self, call_id):
        for call in self.calls:
            if call_id == call.getID():
                return call
        return None

    def checkCallIgnored(self, call_id):
        for call in self.calls:
            if call_id == call.getID():
                if call.getStatus() == 'ringing':
                    call.setStatus("ignored")
                    call.op.setStatus("available")
                    call.setOp(None)
                    return True
        return False

    def printaCalls(self):
        for i in self.calls:
            print(i.status)
