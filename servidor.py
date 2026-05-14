from flask import Flask, send_from_directory, abort
import os

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def find_html():
    for name in ['painel.html', 'dashboard.html', 'index.html']:
        if os.path.exists(os.path.join(BASE_DIR, name)):
            return name
    return None

@app.route('/')
def index():
    html = find_html()
    if html:
        return send_from_directory(BASE_DIR, html)
    files = os.listdir(BASE_DIR)
    return '<h2>Arquivos encontrados:</h2><ul>' + ''.join(f'<li>{f}</li>' for f in sorted(files)) + '</ul>'

@app.route('/<path:filename>')
def serve_file(filename):
    filepath = os.path.join(BASE_DIR, filename)
    if os.path.exists(filepath):
        return send_from_directory(BASE_DIR, filename)
    abort(404)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
