__author__ = 'naren'
from flask import Flask
app = Flask(__name__)

@app.route('/hello')
def hello_world():
    return "Hello Mundo"

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
