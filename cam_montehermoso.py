import http.server
import os
import socketserver
import threading
import time

import requests

PORT = 8770
UPSTREAM = "https://live.noticiasmontehermoso.com.ar/camara2/"
CAM = "guardalavaca"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
HLS_JS_PATH = os.path.join(SCRIPT_DIR, "hls.min.js")

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/131.0 Safari/537.36"
})
lock = threading.Lock()


def warm():
    with lock:
        for _ in range(2):
            r = session.get(UPSTREAM + "index.m3u8", timeout=15)
            if "hlsSession" in session.cookies:
                return r
        return r


HTML = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
html,body{margin:0;padding:0;width:100%;height:100%;overflow:hidden;background:#000}
#v{position:fixed;top:0;left:0;width:100vw;height:100vh;object-fit:fill}
</style>
</head>
<body>
<video id="v" autoplay muted playsinline></video>
<script>
PLACEHOLDER_HLSJS
</script>
<script>
(function(){
var v=document.getElementById("v");
var u="/proxy/index.m3u8";
function play(){
  if(typeof Hls==="undefined"){console.log("Hls no definido");return;}
  if(Hls.isSupported()){
    var h=new Hls({liveSyncDurationCount:2,enableWorker:true,lowLatencyMode:false,maxBufferLength:10});
    h.loadSource(u);
    h.attachMedia(v);
    h.on(Hls.Events.MANIFEST_PARSED,function(){console.log("OK");});
    h.on(Hls.Events.ERROR,function(e,d){console.log("ERR",d.type,d.details);if(d.fatal){h.destroy();setTimeout(play,4000);}});
  }else{
    v.src=u;
  }
}
play();
})();
</script>
</body>
</html>"""


class Handler(http.server.BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def do_GET(self):
        if self.path.startswith("/proxy/"):
            self.proxy(self.path[len("/proxy/"):])
        elif self.path in ("/", "/index.html"):
            with open(HLS_JS_PATH, "r", encoding="utf-8") as f:
                js = f.read()
            page = HTML.replace("PLACEHOLDER_HLSJS", js)
            self.reply(200, page.encode("utf-8"), "text/html; charset=utf-8")
        else:
            self.reply(404, b"404", "text/plain")

    def proxy(self, rel):
        rel = rel.split("?")[0]
        if ".." in rel or not rel:
            return self.reply(400, b"bad path", "text/plain")
        try:
            r = session.get(UPSTREAM + rel, timeout=20)
        except Exception as e:
            return self.reply(502, str(e).encode(), "text/plain")
        if r.status_code != 200:
            warm()
            try:
                r = session.get(UPSTREAM + rel, timeout=20)
            except Exception:
                pass
        if r.status_code != 200:
            return self.reply(r.status_code, r.content, "application/json")
        ct = r.headers.get("Content-Type", "application/octet-stream")
        if "mpegurl" in ct:
            ct = "application/vnd.apple.mpegurl"
        self.reply(200, r.content, ct, extra=r.headers.get("Content-Length"))

    def reply(self, code, body, ctype, extra=None):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", extra or len(body))
        self.send_header("Cache-Control", "no-store")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        pass


class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


if __name__ == "__main__":
    warm()
    print(f"cookies: {dict(session.cookies)}", flush=True)
    srv = Server(("127.0.0.1", PORT), Handler)

    def loop():
        while True:
            time.sleep(60)
            try:
                warm()
            except Exception:
                pass

    threading.Thread(target=loop, daemon=True).start()
    print(f"Monte Hermoso / {CAM}: http://127.0.0.1:{PORT}", flush=True)
    srv.serve_forever()