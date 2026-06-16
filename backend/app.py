from flask import Flask, jsonify, request


def create_app():

    app = Flask(__name__)
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

       