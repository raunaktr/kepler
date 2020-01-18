from flask import Flask


app = Flask(__name__)


@app.route('/')
def kepler():
    return 'Kepler!'


if __name__ == '__main__':
    app.run()
