from flask import Flask, render_template
from flask import jsonify
import argparse

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


@app.route('/admin')
def admin():
    return render_template('admin.html')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run Flask server")
    parser.add_argument('-p', '--port', default=5000, help='Specify port')
    
    args = parser.parse_args()

    app.run(port=args.port)
