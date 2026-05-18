from flask import Flask, send_from_directory, abort, Response
import os

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
GH_TOKEN = os.environ.get('GH_TOKEN', '')

def find_html():
    for name in ['painel.html', 'dashboard.html', 'index.html']:
        if os.path.exists(os.path.join(BASE_DIR, name)):
            return name
    return None

@app.route('/')
def index():
    html_name = find_html()
    if not html_name:
        files = os.listdir(BASE_DIR)
        return '<h2>Arquivos encontrados:</h2><ul>' + ''.join(f'<li>{f}</li>' for f in sorted(files)) + '</ul>'

    with open(os.path.join(BASE_DIR, html_name), 'r', encoding='utf-8') as f:
        html = f.read()

    # Injeta o token como variável JS antes do </head>
    inject = f'<script>window.__GH_TOKEN__="{GH_TOKEN}";</script>'
    html = html.replace('</head>', inject + '</head>', 1)

    return Response(html, mimetype='text/html')

@app.route('/<path:filename>')
def serve_file(filename):
    filepath = os.path.join(BASE_DIR, filename)
    if os.path.exists(filepath):
        return send_from_directory(BASE_DIR, filename)
    abort(404)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
