from op import Operator


class Operators(object):

    def __init__(self):
        self.operators = []

    def addOp(self, id):
        operator = Operator(id)
        operator.status = 'available'
        self.operators.append(operator)

    def lookOpAvailable(self):
        # Look for operator available
        for op in self.operators:
            if op.isAvailable():
                return op

        # All operators are busy
        return None

    def lookOpAnswer(self, op_id):
        for op in self.operators:
            if op.answerCall(op_id):
                return op.curCall
        return None

    def lookOpReject(self,op_id):
        for op in self.operators:
            if op.rejectCall(op_id):
                return op.curCall
        return None

    def printa(self):
        for op in self.operators:
            print(op)

    #Can be optmized
    def setCall(self, op_id, call):
        for op in self.operators:
            if op.ID == op_id:
                op.setCall(call)