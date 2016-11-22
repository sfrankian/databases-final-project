#!/usr/local/bin/python2.7

''' Stephanie Frankian and Elizabeth Kuszmaul
    November 20, 2016
    main.py
'''

import db_functions
from flask import Flask, request,render_template, redirect, url_for


app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")

if __name__ == '__main__':
    app.debug = True
    app.run('0.0.0.0', 9874)
