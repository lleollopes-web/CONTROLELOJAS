const http = require('http');
const fs   = require('fs');
const path = require('path');

const PORT = process.env.PORT || 3000;
const TOKEN = process.env.GH_TOKEN || '';

const HTML_PATH = path.join(__dirname, 'dashboard.html');

http.createServer((req, res) => {
  // Serve only the dashboard (all routes → dashboard.html)
  fs.readFile(HTML_PATH, 'utf8', (err, html) => {
    if (err) { res.writeHead(500); res.end('Server error'); return; }

    // Inject the token as a JS variable before </head>
    const injected = html.replace(
      '</head>',
      `<script>window.__GH_TOKEN__="${TOKEN}";</script></head>`
    );

    res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
    res.end(injected);
  });
}).listen(PORT, () => console.log(`Server running on port ${PORT}`));
