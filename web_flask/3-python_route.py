#!/usr/bin/python3
"""
Starts Flask web application
Web app listens on 0.0.0.0 port 5000
Routes:
/hbnb page include
/c/<text> page included
/python/(<text>) page included
"""

from flask import Flask
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello():
    """Route must display Hello HBNB! when queried"""
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """Route must display HBNB when queried"""
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def hello_C(text):
    """so the route must display c + text"""
    return "C {}".format(text.replace("_", " "))


@app.route('/python', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_text(text="is cool"):
    """reformat text based on optional variable"""
    return "Python {}".format(text.replace("_", " "))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
