from call import Call
from calls import Calls
from ops import Operators
from callqueue import CallQueue
from message import getCommand, getID
from twisted.internet import reactor


class Manager:

    def __init__(self):
        self.operators = Operators()
        self.call_queue = CallQueue()

        # Store all the calls which hasn't been hung up
        self.online_calls_list = Calls()

        # Creating operators
        self.operators.addOp('A')
        self.operators.addOp('B')

    def checkTimeOut(self, op_id, call_id, protocol):

        answer_message = ''
        if self.online_calls_list.checkCallIgnored(call_id):
            answer_message += "Call " + call_id + " ignored by operator " + op_id + "\n"
            op = self.searchOperator("available")
            call = self.online_calls_list.searchCall(call_id)
            if op is not None:
                # Allocate call to operator
                answer_message += "Call " + call_id + " ringing for operator " + op.getID() + "\n"

                self.call_Check(op.getID(), call_id, protocol)
                self.operators.setCall(op.getID(), call)

            protocol.sendData(answer_message)

    def call_Check(self, op_id, call_id, protocol):
        reactor.callLater(10, self.checkTimeOut, op_id, call_id, protocol)


    # -------------------- Input from server -------------------------

    def execute_Command(self, json_file, protocol):
        command = getCommand(json_file)
        ID = getID(json_file)
        print("Command received: " + str(command) + " " + str(ID) + "\n")
        error_message = self.validate_Command(command, ID)

        if error_message:
            return error_message
        else:
            if command == 'call':
                return self.call(ID, protocol)
            elif command == 'answer':
                return self.answer(ID)
            elif command == 'reject':
                return self.reject(ID, protocol)
            elif command == 'hangup':
                return self.hangup(ID, protocol)

    def validate_Command(self, command, ID):
        message_error = None

        # Verify if call_id already exists
        if command == 'call':
            if self.online_calls_list.searchCall(ID):
                message_error = "call_id already exists\n"
        elif command == 'answer' or command == 'reject':
            if self.operators.searchOp(ID) is None:
                message_error = "Operator doesn't exists\n"
        elif command == 'hangup':
            if self.online_calls_list.searchCall(ID) is None:
                message_error = "call_id doesn't exists\n"
        return message_error

    # ------------------ Client commands -----------------------

    def call(self, call_id, protocol):
        answer_message = ''

        # If the call input is correct
        if call_id != '':

            call = Call(call_id)
            answer_message += "Call " + call_id + " received\n"

            # Adding call to the list of calls which are happening
            self.online_calls_list.addCall(call)

            # Flag to see if call is going to queue or not
            go_queue = True

            # Check if the is going to the queue
            if self.call_queue.isEmpty():

                # Look for operator available
                op = self.searchOperator("available")
                if op is not None:
                    answer_message += "Call " + call_id + " ringing for operator " + op.getID() + "\n"
                    # Allocate call to operator
                    self.operators.setCall(op.getID(), call)
                    go_queue = False

                    self.call_Check(op.getID(), call_id, protocol)
                    # reactor.callLater(10, self.checkTimeOut, op.getID(), call_id, protocol)

            # If is going to queue
            if go_queue:
                answer_message += "Call " + call_id + " waiting in queue\n"
                call.setStatus("waiting")
                self.call_queue.enqueue(call)
        else:
            answer_message = 'Must specify a call id ( Call <call_id>)\n'

        return answer_message

    # ------------------- Operator commands --------------------

    def answer(self, op_id):

        answer_message = ''
        # Search for operator and answer his curCall
        call = self.searchOperator("searchCall", op_id)

        # If operator <op_id> has a call ringing
        if call is not None:
            answer_message = "Call " + call.getID() + " answered by operator " + op_id + "\n"

        return answer_message

    def reject(self, op_id, protocol):

        answer_message = ''
        call = self.searchOperator("reject", op_id)

        # If operator <op_id> has a call ringing
        if call is not None:

            answer_message += "Call " + call.getID() + " rejected by operator " + op_id + "\n"

            # While don't find a new operator or don't happen hangup command
            while call.getStatus() != 'ringing' and call.getStatus() != 'ended':
                op = self.searchOperator("available")
                if op is not None:
                    # Allocate call to operator
                    answer_message += "Call " + call.getID() + " ringing for operator " + op.getID() + "\n"
                    self.call_Check(op.getID(), call.getID(), protocol)
                    # reactor.callLater(10, self.checkTimeOut, op.getID(), call.getID(), protocol)
                    self.operators.setCall(op.getID(), call)

        return answer_message

    def hangup(self, call_id, protocol):

        answer_message = ''
        # Search for the call
        call = self.online_calls_list.searchCall(call_id)
        if call is not None:

            # If call is in queue
            if call.getStatus() == 'waiting':

                # Set call status to ended and delete from the list of online calls
                call.setStatus('ended')
                self.online_calls_list.endCall(call)
                answer_message += "Call " + call_id + " missed\n"

            # If call is answered
            elif call.getStatus() == 'answered' or call.getStatus() == 'ringing':
                op = call.getOp()

                # Messages different but the structure of
                # answered and ringing is the same

                if call.getStatus() == 'answered':
                    answer_message += "Call " + call.getID() + " finished and operator " + op.getID() + " available\n"
                else:
                    answer_message += "Call " + call.getID() + " missed\n"


                # unlink operator and call and delete from online calls
                self.operators.finishCall(call)
                self.online_calls_list.endCall(call)

                # Allocate a call in the queue to operator
                if not self.call_queue.isEmpty():

                    # Search for a call which is online
                    new_call = self.call_queue.dequeue()
                    while new_call.status == 'ended' and (not self.call_queue.isEmpty()):
                        new_call = self.call_queue.dequeue()

                    if new_call.status != 'ended':
                        self.operators.setCall(op.getID(), new_call)
                        answer_message += "Call " + new_call.getID() + " ringing for operator " + op.getID() + '\n'

                        self.call_Check(op.getID(), new_call.getID(), protocol)
                        # reactor.callLater(10, self.checkTimeOut, op.getID(), new_call.getID(), protocol)
        return answer_message

    def searchOperator(self, command, op_id=None):

        # For call command the operator needs to be available without a
        # call ringing
        if command == 'available':
            return self.operators.lookOpAvailable()

        # For answer command the operator needs to be busy and with a
        # call ringing
        elif command == 'searchCall':
            return self.operators.lookOpAnswer(op_id)

        # For reject command the operator needs to be busy and with a
        # call ringing
        elif command == 'reject':
            return self.operators.lookOpReject(op_id)
