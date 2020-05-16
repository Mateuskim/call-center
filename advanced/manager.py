from call import Call
from calls import Calls
from ops import Operators
from callqueue import CallQueue
from message import getCommand, getID
from twisted.internet import reactor
import time


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
        time.sleep(10)
        answer_message = ''
        if self.online_calls_list.checkCallIgnored(call_id):
            answer_message += "Call " + call_id + " ignored by operator " + op_id + "\n"
            op = self.searchOperator("available")
            call = self.online_calls_list.searchCall(call_id)
            if op is not None:
                # Allocate call to operator
                answer_message += "Call " + call_id + " ringing for operator " + op.ID + "\n"

                reactor.callInThread(self.checkTimeOut, op.ID, call_id, protocol)
                self.operators.setCall(op.ID, call)

            protocol.sendData(answer_message)

    # -------------------- Input from server -------------------------

    def execute_Command(self, json_file, protocol):
        command = getCommand(json_file)
        ID = getID(json_file)
        print("Command received: " + command + " " + ID + "\n")
        error_message = self.validateCommand(command, ID)

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

    def validateCommand(self, command, ID):
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
                    answer_message += "Call " + call_id + " ringing for operator " + op.ID + "\n"
                    reactor.callInThread(self.checkTimeOut, op.ID, call_id, protocol)

                    # Allocate call to operator
                    self.operators.setCall(op.ID, call)
                    go_queue = False

            # If is going to queue
            if go_queue:
                answer_message += "Call " + call_id + " waiting in queue\n"
                call.setStatus("waiting")
                self.call_queue.enqueue(call)
        else:
            answer_message = 'Must specify a call id ( Call <call_id>)'

        return answer_message

    # ------------------- Operator commands --------------------

    def answer(self, op_id):

        answer_message = ''
        # Search for operator and answer his curCall
        call = self.searchOperator("searchCall", op_id)

        # If operator <op_id> has a call ringing
        if call is not None:
            answer_message = "Call " + call.ID + " answered by operator " + op_id + "\n"

        return answer_message

    def reject(self, op_id, protocol):

        answer_message = ''
        call = self.searchOperator("reject", op_id)

        # If operator <op_id> has a call ringing
        if call is not None:

            answer_message += "Call " + call.ID + " rejected by operator " + op_id + "\n"

            # While don't find a new operator or don't happen hangup command
            while call.getStatus() != 'ringing' and call.getStatus() != 'ended':
                op = self.searchOperator("available")
                if op is not None:
                    # Allocate call to operator
                    answer_message += "Call " + call.ID + " ringing for operator " + op.ID + "\n"

                    reactor.callInThread(self.checkTimeOut, op.ID, call.ID, protocol)
                    self.operators.setCall(op.ID, call)

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
                    answer_message += "Call " + call.ID + " finished and operator " + op.ID + " available\n"
                else:
                    answer_message += "Call " + call.ID + " missed and operator " + op.ID + " available\n"

                call.setStatus('ended')
                # unlink operator and call and delete from online calls
                self.operators.finishCall(call)
                self.online_calls_list.endCall(call)

                # Allocate a call in the queue to operator
                if not self.call_queue.isEmpty():

                    # Search for a call which is online
                    new_call = self.call_queue.dequeue()
                    while not self.call_queue.isEmpty():
                        new_call = self.call_queue.dequeue()

                    if new_call.status != 'ended':
                        self.operators.setCall(op.ID, new_call)
                        answer_message += "Call " + new_call.ID + " ringing for operator " + op.ID + '\n'
                        reactor.callInThread(self.checkTimeOut, op.ID, new_call.ID, protocol)
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
