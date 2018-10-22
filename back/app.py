#!/usr/bin/python3
from flask import Flask, render_template, json, jsonify,send_file
from flask import request
import os
import asyncio
import subprocess
import sparser

One = ""

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
    return jsonify(start_time=f["start_time"],game_status=f["game_status"],home_team=f["home_team"],score=f["score"],
    away_team=f["away_team"],league=f["league"])
    # return str(f)


@app.route("/teams",methods=["POST"])
def Teams():
    data = request.get_json()
    print(data)
    print(data["sport"],data["second"],data["first"])
    parser = sparser.Parser()
    response = parser.SportToday(data["sport"],data["first"], data["second"])
    global One
    One = parser
    # parser.team_detailed_info(data["sport"])
    return jsonify({"info":response})

@app.route("/efw",methods=["POST"])
def Excel():
    data = request.get_json()
    print(data)
    # parser = sparser.Parser()
    response = One.team_detailed_info(data["sport"])
    return jsonify({"info":response})


@app.route("/downloadfile/<name>")
def Download(name = None):
    try:
        return send_file(name, as_attachment=True)
    except Exception as e:
        log.exception(e)
        Error(400)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
