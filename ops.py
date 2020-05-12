from op import Operator


class Operators(object):

    def __init__(self):
        self.operators = []

    def addOp(self, id):
        operator = Operator(id)
        operator.status = 'Available'
        self.operators.append(operator)

    def lookOpAvailable(self):
        # Look for operator available
        for op in self.operators:
            if op.status == 'Available' and op.curCall is None:
                return op

        # All operators are busy
        return None

    def lookOpAnwers(self, op_id):
        for op in self.operators:

            #The telephone is calling
            if op.status == 'Available' and op.curCall is not None:
                return op

    def printa(self):
        for op in self.operators:
            print(op)

    #Can be optmized
    def setCall(self, op_id, call):
        for op in self.operators:
            if op.ID == op_id:
                op.setCall(call)