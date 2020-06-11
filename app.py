from flask import Flask, render_template, url_for, redirect, request
from flask import jsonify
import argparse
import marshal
import json
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
        result = reader()
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

            obj = {'id': v}
        else:
            bracket_index = k.index('[')
            key = k[:bracket_index]
            obj[key] = v

    if len(obj) > 0:
        result.append(obj)

    writer(result)

    return redirect(url_for('admin'))


@app.route('/api/news/save_by_app', methods=['POST'])
def news_save_by_app():
    results = reader()

    if not results:
        last_id = 1
    else:
        last_id = int(results[-1]['id']) + 1

    json_data = json.loads(request.get_data())
    new_record = {'id': last_id, 'title': list(json_data.keys())[0], 'text': list(json_data.values())[0]}

    results.append(new_record)

    writer(results)

    return {'status_code': 201}


def reader():
    with open(NEWS_DUMP_FILE, 'rb') as f:
        results = marshal.load(f)

    return results


def writer(results):
    with open(NEWS_DUMP_FILE, 'wb') as f:
        marshal.dump(results, f)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run Flask server")
    parser.add_argument('-p', '--port', default=5000, help='Specify port')

    args = parser.parse_args()

    app.run(port=args.port)
