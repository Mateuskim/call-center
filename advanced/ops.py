from op import Operator


class Operators(object):

    def __init__(self):
        self.operators = []

    def addOp(self, id):
        operator = Operator(id)
        operator.status = 'available'
        self.operators.append(operator)

    def searchOp(self, id):
        for op in self.operators:
            if op.ID == id:
                return op
        return None

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
                cur_call = op.curCall
                op.curCall = None
                return cur_call
        return None

    def printID(self):
        for op in self.operators:
            print(op.ID+" ", end='')

    #Can be optmized
    def setCall(self, op_id, call):
        for op in self.operators:
            if op.ID == op_id:
                op.setCall(call)
                call.setOp(op)

    def finishCall(self, call):
        call.setStatus('ended')
        op = call.getOp()
        op.curCall = None
        op.setStatus('available')

    def clear_Ops(self):
        for op in self.operators:
            op.curCall = None
            op.setStatus('available')
