class Calls(object):
    def __init__(self):
        self.calls = []

    def addCall(self, call):
        self.calls.append(call)

    def endCall(self, call):
        for c in self.calls:
            if call.ID == c.ID:
                self.calls.remove(call)

    def searchCall(self, call_id):
        for c in self.calls:
            if call_id == c.ID:
                return c
        return None
    def printaCalls(self):
        for i in self.calls:
            print(i.status)