#!/usr/bin/python3
from flask import Flask, render_template, json, jsonify
from flask import request
import os
import parser
import asyncio


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
    # asyncio.set_event_loop().run_until_complete()
    r = parser.Parser()
    o = r.Today()
    # return "check"
    return(str("2"))


app.run(host="0.0.0.0")