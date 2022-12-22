#!/bin/env python3
import sys
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return "hello world"
    

@app.route('/user/<id>', methods=['GET'])
def get_user(id):
    return render_template("user/index.html", 
    user = {"username": "sayan", "fname": "Sayan", "lname": "Ghosh", "about": "I code stuff", "id": id})




if __name__ == '__main__':
    app.run()
