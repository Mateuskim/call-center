import cmd
from call import Call
from calls import Calls
from ops import Operators
from queue import Queue

class Server(cmd.Cmd):

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = '(Application)'
        self.operators = Operators()
        self.call_queue = Queue()
        self.online_calls_list = Calls()

        #Criando operadores
        self.operators.addOp('A')
        self.operators.addOp('B')

    # ------------------ Client commands -----------------------

    def do_call(self, call_id):

        #If the call input is correct
        if call_id != '':

            call = Call(call_id)
            print("Call " + call_id + " received")

            #Adding call to the list of calls which are happening
            self.online_calls_list.addCall(call)

            #Flag to see if call is going to queue or not
            go_queue = True

            if self.call_queue.isEmpty():

                #Look for operator available
                op = self.searchOperator("call")
                if op is not None:

                    #Allocate call to operator
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



    # ------------------- Operator commands --------------------

    def do_answer(self, op_id):

        #Search for operator and answer his curCall
        call = self.searchOperator("answer", op_id)

        # If operator <op_id> has a call ringing
        if call is not None:
            print("Call " + call.ID + " answered by operator " + op_id)


    def do_reject(self, op_id):
        print('Call 1 rejected by operator ', op_id)



    def do_hangup(self, call_id):
        #Search for the call
        call = self.online_calls_list.searchCall(call_id)
        if call is not None:

            #If call is in queue
            if call.getStatus() == 'waiting':

                #Set call status to ended and delete from the list of online calls
                call.setStatus('ended')
                self.online_calls_list.endCall(call)
                print("Call " + call_id + " missed")

            elif call.getStatus() == 'answered':
                call.setStatus('ended')

                #unlink operator and call and delete from online calls
                self.operators.finishCall(call)
                self.online_calls_list.endCall(call)
                op = call.getOp()

                # Allocate a call in the queue to operator
                if not self.call_queue.isEmpty():

                    new_call = self.call_queue.dequeue()
                    self.operators.setCall(op.ID, new_call)
                    print("Call " + call.ID + " finished and operator " + op.ID + " available")
                    print("Call " + new_call.ID + " ringing for operator " + op.ID)
                else:
                    print("Call " + call.ID + " finished and operator " + op.ID + " available")



    def searchOperator(self, command, op_id = None):

        # For call command the operator needs to be available without a
        # call ringing
        if command == 'call':
            return self.operators.lookOpAvailable()

        #For answer command the operator needs to be available and with a
        #call ringing
        elif command == 'answer':
            return self.operators.lookOpAnswer(op_id)

