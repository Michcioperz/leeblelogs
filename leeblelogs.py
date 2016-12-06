#!/usr/bin/env python3
import os
from logging.handlers import SysLogHandler
from flask import Flask, render_template

chatlogs = "/home/znc/.znc/moddata/log/michcioperz/mibbit/#leebleforest"

app = Flask(__name__)


def logs_registry():
    return sorted(os.listdir(chatlogs))

def parse(line):
    x = {}
    x["time"], x["message"] = line.split(" ", 1)
    if x["message"].startswith("*** Joins: "):
        x["type"] = "join"
        x["object"] = x["message"][11:].split(" ", 1)[0]
    elif x["message"].startswith("*** Quits: "):
        x["type"] = "quit"
        x["object"] = x["message"][11:].split(" ", 1)[0]
    elif x["message"].startswith("* "):
        x["type"] = "action"
        x["object"], x["action"] = x["message"][2:].split(" ", 1)
    elif x["message"].startswith("*** ") and " is now known as " in x["message"]:
        x["type"] = "nickchange"
        x["object"], x["target"] = x["message"][4:].split(" is now known as ", 1)
    elif x["message"].startswith("<"):
        x["type"] = "message"
        x["object"] = x["message"][1:].split(">", 1)[0]
        x["content"] = x["message"].split(">", 1)[1]
    return x

@app.route("/")
def forest():
    return render_template("forest.html", forest=logs_registry()[::-1])

@app.route("/log/<day>")
def log(day):
    logs = logs_registry()
    if day not in logs:
        return render_template("not_found.html", forest=logs_registry()[::-1])
    with open(os.path.join(chatlogs, day)) as f:
        data = f.read()
    parsed_data = [parse(line) for line in data]
    return render_template("log.html", data=data, parsed_data=parsed_data, forest=logs_registry()[::-1], p=logs[logs.index(day)-1] if logs[0] != day else None, n=logs[logs.index(day)+1] if logs[-1] != day else None)
