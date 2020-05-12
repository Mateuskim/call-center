class Operator():

    def __init__(self, ID, status = 'Available'):
        self.ID = ID
        self.curCall = None
        self.status = status

    def set_Call(self, call_id):
        self.curCall = call_id

    def set_Status(self, status):
        self.status = status

    def get_ID(self):
        return self.ID

    def get_Status(self):
        return self.status
