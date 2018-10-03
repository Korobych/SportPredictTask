#!/usr/bin/python3
from flask import Flask, render_template, json, jsonify
from flask import request
import os
import asyncio
import subprocess


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
    a = subprocess.check_output("python3.6 parser.py "+data["sport"],shell=True)
    return(a)


if __name__ == "__main__":
    app.run(threaded=True)
