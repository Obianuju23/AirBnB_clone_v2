#!/usr/bin/python3
"""
A Python Flask script that starts a web application with two routings
"""

from flask import Flask
app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello():
    """
    Function that returns “Hello HBNB!” from the root route
    """
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hello_hbnb():
    """
    Function that returns "HBNB when you navigate to /hbnb route
    """
    return "HBNB"


@app.route("/c/<text>/", strict_slashes=False)
def hello_c(text):
    """
    Function that accepts a parameter in the C route + the text"""
    return "C {}".format(text.replace("_", " "))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
