from flask import Flask
from flask import jsonify

app = Flask(__name__)


@app.route('/')
def root():
    return jsonify([
        {
            "id": "1",
            "title": "First post",
            "text": "Some text",
        },
        {
            "id": "2",
            "title": "Second post",
            "text": "Some text",
        }])


if __name__ == '__main__':
    app.run()
