#!/usr/bin/env python3
"""Situational Geometry V14 — local iOS Pyto launcher.
Place this file and index.html in the same directory, run from Pyto,
then open http://localhost:8765 in Safari and grant camera permission.
No external Python packages or server connections are required.
"""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import webbrowser

HOST, PORT = '127.0.0.1', 8765
HTML = Path(__file__).resolve().with_name('index.html')

class LocalHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        name = self.path.split('?')[0].lstrip('/') or 'index.html'
        allowed = {'index.html', 'puzzle_solutions.json', 'solution_audit.json', 'puzzles.json', 'activity_reference.json', 'country_borders.json'}
        if name not in allowed:
            self.send_error(404)
            return
        target = HTML.parent / name
        if not target.is_file():
            self.send_error(404)
            return
        body = target.read_bytes()
        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8' if name.endswith('.json') else 'text/html; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Cache-Control', 'no-store')
        self.send_header('Permissions-Policy', 'camera=(self), gyroscope=(self), accelerometer=(self)')
        self.end_headers()
        self.wfile.write(body)
    def log_message(self, *args):
        pass

if __name__ == '__main__':
    if not HTML.is_file():
        raise SystemExit('index.html must be in the same folder as pyto_launcher.py')
    server = ThreadingHTTPServer((HOST, PORT), LocalHandler)
    url = f'http://localhost:{PORT}'
    print('Situational Geometry V14 — open in Safari:', url)
    try:
        webbrowser.open(url)
    except Exception:
        pass
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
