# Functions to threat message reading
import json


def translateCommand(str_json):
    return json.loads(str_json.decode("utf-8"))
    # command = json_response["command"]
    # id = json_response["id"]
    # command_string = command + " " + id
    # return command_string


def createJson(answer):
    answer_json = {}
    answer_json["response"] = answer
    return json.dumps(answer_json).encode("utf-8")


def getCommand(json_file):
    return json_file["command"]


def getID(json_file):
    return json_file["id"]
