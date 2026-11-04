import http.server
import json
import os
import re
import threading
import time
import requests
from datetime import datetime

PORT = 8765
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
HLS_JS_PATH = os.path.join(SCRIPT_DIR, "hls.min.js")
PAGE_URL = "https://www.skylinewebcams.com/es/webcam/argentina/tierra-del-fuego/ushuaia/tren-del-fin-del-mundo.html"

stream_url = ""

def fetch_stream():
    global stream_url
    s = requests.Session()
    s.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"})
    r = s.get(PAGE_URL, timeout=15)
    if len(r.text) < 100:
        return None
    m = re.search(r"source\s*:\s*'([^']+\.m3u8[^']*)'", r.text)
    if not m:
        return None
    source = m.group(1)
    return "https://hd-auth.skylinewebcams.com/" + source.replace("livee.", "live.")

def refresh_loop():
    while True:
        try:
            new_url = fetch_stream()
            if new_url:
                stream_url = new_url
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Stream OK", flush=True)
        except Exception as e:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Error: {e}", flush=True)
        time.sleep(7200)

# Load hls.js once at startup
hls_js_code = ""
try:
    with open(HLS_JS_PATH, "r", encoding="utf-8") as f:
        hls_js_code = f.read()
    print(f"hls.js cargado: {len(hls_js_code)} bytes", flush=True)
except Exception as e:
    print(f"Error cargando hls.js: {e}", flush=True)

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
function play(u){
  if(!u)return;
  if(typeof Hls==="undefined"){console.log("Hls no definido");return;}
  if(Hls.isSupported()){
    var h=new Hls({liveSyncDurationCount:2,enableWorker:true,maxBufferLength:10});
    h.loadSource(u);
    h.attachMedia(v);
    h.on(Hls.Events.ERROR,function(e,d){console.log("ERR",d.type,d.details);if(d.fatal)setTimeout(function(){play(u)},5000);});
    h.on(Hls.Events.MANIFEST_PARSED,function(e,d){console.log("OK levels="+d.levels.length);});
  }else{
    v.src=u;
  }
}
fetch("/api/stream").then(function(r){return r.json()}).then(function(d){
  console.log("URL:",d.url);
  if(d.url)play(d.url);
});
})();
</script>
</body>
</html>"""

class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            page = HTML.replace("PLACEHOLDER_HLSJS", hls_js_code)
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(page.encode("utf-8"))
        elif self.path.startswith("/api/stream"):
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps({"url": stream_url}).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        pass

if __name__ == "__main__":
    print("Obteniendo stream...", flush=True)
    try:
        stream_url = fetch_stream()
        if stream_url:
            print(f"Stream: {stream_url}", flush=True)
    except Exception as e:
        print(f"Error: {e}", flush=True)

    t = threading.Thread(target=refresh_loop, daemon=True)
    t.start()

    server = http.server.HTTPServer(("127.0.0.1", PORT), Handler)
    print(f"\nServer: http://127.0.0.1:{PORT}", flush=True)
    print("OBS Navegador -> http://127.0.0.1:8765", flush=True)
    print("1920x1080\n", flush=True)
    server.serve_forever()
