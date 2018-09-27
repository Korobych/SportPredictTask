#!/usr/bin/python3
from flask import Flask, render_template, json, jsonify
from flask import request
import os


app = Flask(__name__,
            static_folder = "../vue/dist/static",
            template_folder = "../vue/dist")
@app.route('/')
def Index():
    return render_template("index.html")

app.run(host="0.0.0.0")