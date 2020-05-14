import cmd
from call import Call
from calls import Calls
from ops import Operators
from callqueue import CallQueue
from advanced.message import *

class Manager:

    def __init__(self):
        self.operators = Operators()
        self.call_queue = CallQueue()
        self.online_calls_list = Calls()


        #Criando operadores
        self.operators.addOp('A')
        self.operators.addOp('B')

    def execute_Command(self, json_file):
        command = json_file.getCommand(json_file)
        ID = json_file.getID(json_file)
        if command == 'call':
            return self.call(ID)
        elif command == 'answer':
            return self.answer(ID)
        elif command == 'reject':
            return self.reject(ID)
        elif command == 'hangup':
            return self.hangup(ID)

    # ------------------ Client commands -----------------------

    def call(self, call_id):
        answer_message = ''


        #If the call input is correct
        if call_id != '':

            call = Call(call_id)
            # print("Call " + call_id + " received\n")
            answer_message += "Call " + call_id + " received\n"

            #Adding call to the list of calls which are happening
            self.online_calls_list.addCall(call)

            #Flag to see if call is going to queue or not
            go_queue = True

            if self.call_queue.isEmpty():

                #Look for operator available
                op = self.searchOperator("available")
                if op is not None:

                    answer_message += "Call " + call_id + " ringing for operator " + op.ID + "\n"

                    #Allocate call to operator
                    # print("Call " + str(call_id) + " ringing for operator " + op.ID)
                    self.operators.setCall(op.ID, call)
                    go_queue = False

            #If is going to queue
            if go_queue:
                # print("Call " + call_id + " waiting in queue")
                answer_message += "Call " + call_id + " waiting in queue\n"
                call.setStatus("waiting")
                self.call_queue.enqueue(call)
        else:
            answer_message = 'Must specify a call id ( Call <call_id>)'

        return answer_message



    # ------------------- Operator commands --------------------

    def answer(self, op_id):

        answer_message = ''
        #Search for operator and answer his curCall
        call = self.searchOperator("searchCall", op_id)

        # If operator <op_id> has a call ringing
        if call is not None:
            answer_message = "Call " + call.ID + " answered by operator " + op_id + "\n"

        return answer_message

    def reject(self, op_id):

        answer_message = ''
        call = self.searchOperator("reject", op_id)


        # If operator <op_id> has a call ringing
        if call is not None:

            # print("Call " + call.ID + " rejected by operator " + op_id)
            answer_message += "Call " + call.ID + " rejected by operator " + op_id + "\n"

            #While don't find a new operator or don't happen hangup command
            while call.getStatus() != 'ringing' and call.getStatus() != 'ended':
                op = self.searchOperator("available")
                if op is not None:

                    # Allocate call to operator
                    # print("Call " + call.ID + " ringing for operator " + op.ID)
                    answer_message += "Call " + call.ID + " ringing for operator " + op.ID + "\n"
                    self.operators.setCall(op.ID, call)

        return answer_message


    def hangup(self, call_id):

        answer_message = ''
        #Search for the call
        call = self.online_calls_list.searchCall(call_id)
        if call is not None:

            #If call is in queue
            if call.getStatus() == 'waiting':

                #Set call status to ended and delete from the list of online calls
                call.setStatus('ended')
                self.online_calls_list.endCall(call)
                # print("Call " + call_id + " missed")
                answer_message += "Call " + call_id + " missed\n"

            #If call is answered
            elif call.getStatus() == 'answered' or call.getStatus() == 'ringing':
                op = call.getOp()

                # Messages different but the structure of
                # answered and ringing is the same

                if call.getStatus() == 'answered':
                    # print("Call " + call.ID + " finished and operator " + op.ID + " available")
                    answer_message += "Call " + call.ID + " finished and operator " + op.ID + " available\n"
                else:
                    print("Call " + call.ID + " missed")
                    answer_message += "Call " + call.ID + " missed\n"

                call.setStatus('ended')
                #unlink operator and call and delete from online calls
                self.operators.finishCall(call)
                self.online_calls_list.endCall(call)

                # Allocate a call in the queue to operator
                if not self.call_queue.isEmpty():

                    # Search for a call which is online
                    new_call = self.call_queue.dequeue()
                    while new_call.status == 'ended' and (not self.call_queue.isEmpty()):
                        new_call = self.call_queue.dequeue()


                    if new_call.status != 'ended':

                        self.operators.setCall(op.ID, new_call)
                        answer_message += "Call " + new_call.ID + " ringing for operator " + op.ID + '\n'
                        print("Call " + new_call.ID + " ringing for operator " + op.ID)
        return answer_message


    def searchOperator(self, command, op_id = None):

        # For call command the operator needs to be available without a
        # call ringing
        if command == 'available':
            return self.operators.lookOpAvailable()

        #For answer command the operator needs to be busy and with a
        #call ringing
        elif command == 'searchCall':
            return self.operators.lookOpAnswer(op_id)

        # For reject command the operator needs to be busy and with a
        # call ringing
        elif command == 'reject':
            return self.operators.lookOpReject(op_id)



