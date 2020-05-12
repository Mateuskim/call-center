import cmd
from call import Call
from ops import Operators
from queue import Queue

class Server(cmd.Cmd):

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = '(Application)'
        self.operators = Operators()
        self.call_queue = Queue()

        #Criando operadores
        self.operators.addOp('A')
        self.operators.addOp('B')

    # ------------------ Client commands -----------------------

    def do_call(self, call_id):

        #If the call input is correct
        if call_id != '':

            call = Call(call_id)
            print("Call", call_id, "received")

            #Flag to see if call is going to queue or not
            go_queue = True

            if self.call_queue.isEmpty():
                #Look for operator available
                op = self.searchOperator()
                if op is not None:

                    #Operator op is available
                    print("Call " + call_id + " ringing for operator " + op.ID)
                    self.operators.setCall(op.ID, call)
                    go_queue = False

            #If is going to queue
            if go_queue:
                print("Call " + call_id + " waiting in queue")
                call.setStatus("waiting")
                self.call_queue.enqueue(call)
        else:
            print('Must specify a call id ( Call <call_id>)')

    def do_answer(self, op_id):
        print('Call 1 answered by operator ', op_id)

    def do_reject(self, op_id):
        print('Call 1 rejected by operator ', op_id)

    def do_hangup(self, call_id):
        print("Call "+ call_id+ " missed")


    def searchOperator(self):
        return self.operators.lookOpAvailable()
