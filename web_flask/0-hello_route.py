#!/usr/bin/python3
""" 
This Scripts starts Flask web application on 0.0.0.0, port 5000
"""

from flask import Flask
app = Flask(__name__)


@app.route('/')
def hello_hbnb():
    """Shows the route what to display"""
    return "Hello HBNB!"

if __name__ == '__main__':
    app.url_map.strict_slashes = False
    app.run(host='0.0.0.0', port=5000)
