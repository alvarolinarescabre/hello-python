from flask import Flask


app = Flask(__name__)


@app.route('/')
def index():
       return "(Version 01) - Use like this: https://hello.codigofacilito.local/hello/Chamo"


@app.route('/hello/<name>')
def hello(name):
       return "Hello {}".format(name)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
