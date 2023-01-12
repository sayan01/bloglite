#!/bin/env python3
import sys
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")
    

@app.route('/user/<id>', methods=['GET'])
def get_user(id):
    return render_template("user/index.html", 
    profileactive="active",
    user = {"username": "sayan", "fname": "Sayan", "lname": "Ghosh", "about": "I code stuff", "id": id})


# error pages
# invalid url
@app.errorhandler(404)
def error404(e):
    return render_template("error/404.html", error=e), 404



if __name__ == '__main__':
    app.run()
