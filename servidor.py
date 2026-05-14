from flask import Flask, send_from_directory, abort
import os

app = Flask(__name__)

# O Render roda de /opt/render/project/src/
# Os arquivos estão em /opt/render/project/src/ também
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def index():
    return send_from_directory(BASE_DIR, 'painel.html')

@app.route('/<path:filename>')
def serve_file(filename):
    filepath = os.path.join(BASE_DIR, filename)
    if os.path.exists(filepath):
        return send_from_directory(BASE_DIR, filename)
    abort(404)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
