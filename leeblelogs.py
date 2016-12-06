#!/usr/bin/env python3
import os
from flask import Flask, render_template

chatlogs = "/home/znc/.znc/moddata/log/michcioperz/mibbit/#leebleforest"

app = Flask(__name__)

def logs_registry():
    return sorted(os.listdir(chatlogs))

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
    return render_template("log.html", data=data, forest=logs_registry()[::-1], p=logs[logs.index(day)-1] if logs[0] != day else None, n=logs[logs.index(day)+1] if logs[-1] != day else None)
