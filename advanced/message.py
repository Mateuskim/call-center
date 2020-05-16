# Functions to threat message reading

import json


def createResponse(answer):
    answer_json = {}
    answer_json["response"] = answer
    return json.dumps(answer_json).encode("utf-8")


def createCommand(command):
    json_command = {}
    data = command.split()
    json_command["command"] = data[0]
    if len(data) > 1:
        json_command["id"] = data[1]
    else:
        json_command["id"] = -1
    return json_command


def packJson(json_message):
    return json.dumps(json_message).encode("utf-8")


def translateMessage(message_answer):
    return json.loads(message_answer.decode("utf-8"))


def getCommand(json_file):
    return json_file["command"]


def getID(json_file):
    return json_file["id"]


def getAnswer(message_json):
    return message_json["response"]
