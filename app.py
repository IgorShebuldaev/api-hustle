from flask import Flask, render_template, url_for, redirect, request
from flask import jsonify
import argparse
import marshal
from pathlib import Path

app = Flask(__name__)

NEWS_DUMP_FILE = 'news.dump'

@app.route('/')
def admin():
    return render_template('admin.html', 
                           save_url=url_for('news_save'),
                           news_url=url_for('news'))


@app.route('/api/news')
def news():
    dump_file = Path(NEWS_DUMP_FILE)
    if dump_file.is_file():
        with open(NEWS_DUMP_FILE, 'rb') as f:
            result = marshal.load(f)
    else:
        result = []

    return jsonify(result)


@app.route('/api/news/save', methods=['POST'])
def news_save():
    result = []
    obj = {}
    
    for k, v in request.form.items():
        if k.startswith('node_id'):
            if len(obj) > 0:
                result.append(obj)

            obj = { 'id': v }
        else:
            braket_index = k.index('[')
            key = k[:braket_index]
            obj[key] = v

    if len(obj) > 0:
        result.append(obj)

    with open(NEWS_DUMP_FILE, 'wb') as f:
        marshal.dump(result, f)

    return redirect(url_for('admin'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run Flask server")
    parser.add_argument('-p', '--port', default=5000, help='Specify port')
    
    args = parser.parse_args()

    app.run(port=args.port)
