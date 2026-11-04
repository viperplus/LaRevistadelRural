"""Servidor de pruebas: sirve la carpeta y guarda el resultado en _resultado_red.txt.
Permite que _test_red.html se ejecute en tiempo real (WebRTC necesita tiempo real)."""
import http.server
import os
import socketserver
import urllib.parse

DIR = os.path.dirname(os.path.abspath(__file__))
LOG = os.path.join(DIR, "_resultado_red.txt")


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=DIR, **kw)

    def log_message(self, *a):
        pass

    def do_GET(self):
        u = urllib.parse.urlparse(self.path)
        if u.path == "/resultado":
            q = u.query
            if q.startswith("d="):
                q = q[2:]
            with open(LOG, "w", encoding="utf-8") as f:
                f.write(urllib.parse.unquote(q))
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"ok")
            return
        return super().do_GET()

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()


class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


if __name__ == "__main__":
    with Server(("127.0.0.1", 8767), Handler) as httpd:
        httpd.serve_forever()
