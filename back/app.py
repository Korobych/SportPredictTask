#!/usr/bin/python3
from flask import Flask, render_template, json, jsonify
from flask import request
import os
import asyncio
import subprocess
import sparser

app = Flask(__name__,
            static_folder = "../vue/dist/static",
            template_folder = "../vue/dist")
@app.route('/')
def Index():
    return render_template("index.html")

@app.route("/today",methods=["POST"])
def SportTd():
    data = request.get_json()
    print(data)
    check = sparser.Parser()
    f = check.SportToday(data["sport"])
    print(f)
    return jsonify(start_time=f["start_time"],game_status=f["game_status"],home_team=f["home_team"],score=f["score"],away_team=f["away_team"])
    # return str(f)

if __name__ == "__main__":
    app.run(threaded=True)
