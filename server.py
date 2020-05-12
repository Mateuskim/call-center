import cmd
from call import Call
from ops import Operators

class Server(cmd.Cmd):

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = '(Application)'
        self.operators = Operators()

        #Criando operadores
        self.operators.addOp('A')
        self.operators.addOp('B')

    # ------------------ Client commands -----------------------

    def do_call(self, call_id):

        #If the call input is correct
        if call_id != '':

            call = Call(call_id)
            print("Call", call_id, "received")

            #Look for operator available
            op = self.searchOperator()
            if op is not None:

                #Operator op is available
                print("Call " + call_id + " ringing for operator " + op.ID)
                self.operators.setCall(op.ID, call)
                # self.operators.printa()
            else:
                print("Coloca na pilha")
        else:
            print('Must specify a call id')

    def do_answer(self, op_id):
        print('Call 1 answered by operator ', op_id)

    def do_reject(self, op_id):
        print('Call 1 rejected by operator ', op_id)

    def do_hangup(self, call_id):
        print("Call "+ call_id+ " missed")


    def searchOperator(self):
        return self.operators.lookOpAvailable()
