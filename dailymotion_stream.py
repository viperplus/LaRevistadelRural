import http.server
import json
import os
import re
import socket
import socketserver
import threading
import time
import urllib.parse

import requests

PORT = 8771
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
HLS_JS_PATH = os.path.join(SCRIPT_DIR, "hls.min.js")
VIDEO_ID = "x9x6vqm"
META = "https://www.dailymotion.com/player/metadata/video/"
REFRESH = 300

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/131.0 Safari/537.36",
    "Referer": "https://www.dailymotion.com/",
})

state = {"id": VIDEO_ID, "title": "", "url": "", "levels": [], "audio": []}
lock = threading.Lock()

MEDIA_RE = r'#EXT-X-MEDIA:[^\n]*URI="([^"]+)"'


def parse_master(text, base):
    levels, audio = [], []
    attrs = None
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("#EXT-X-MEDIA:"):
            if "TYPE=AUDIO" in s:
                m = re.search(MEDIA_RE, s)
                if m:
                    audio.append(urllib.parse.urljoin(base, m.group(1).split("#")[0]))
        elif s.startswith("#EXT-X-STREAM-INF:"):
            attrs = s
        elif attrs and s and not s.startswith("#"):
            res = (re.search(r"RESOLUTION=([0-9]+x[0-9]+)", attrs) or [None, "?"])[1]
            bw = int((re.search(r"BANDWIDTH=(\d+)", attrs) or [0, 0])[1])
            levels.append({"res": res, "bw": bw, "url": urllib.parse.urljoin(base, s)})
            attrs = None
    return levels, audio


def extract(video_id):
    d = session.get(META + video_id, timeout=20).json()
    url = ""
    for entries in (d.get("qualities") or {}).values():
        for e in entries:
            if e.get("type") == "application/x-mpegURL":
                url = e["url"]
    if not url:
        raise RuntimeError("sin stream: " + json.dumps(d.get("error"))[:120])

    levels, audio = parse_master(session.get(url.split("#")[0], timeout=20).text, url)
    if not levels:
        levels = [{"res": "media", "bw": 0, "url": url}]

    with lock:
        state["id"] = video_id
        state["title"] = d.get("title") or video_id
        state["url"] = url
        state["levels"] = levels
        state["audio"] = audio
    return url


HTML = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
html,body{margin:0;padding:0;width:100%;height:100%;overflow:hidden;background:#000}
#v{position:fixed;top:0;left:0;width:100vw;height:100vh;object-fit:fill}
#i{position:fixed;bottom:6px;left:8px;color:#eee;font:12px monospace;text-shadow:0 0 4px #000;z-index:9}
</style>
</head>
<body>
<video id="v" autoplay muted playsinline></video>
<div id="i"></div>
<script>
PLACEHOLDER_HLSJS
</script>
<script>
(function(){
var v=document.getElementById("v"), i=document.getElementById("i"), h=null;
function play(){
  if(typeof Hls==="undefined"){i.textContent="Hls no definido";return;}
  if(h)try{h.destroy()}catch(e){}
  if(Hls.isSupported()){
    h=new Hls({liveSyncDurationCount:3,enableWorker:true,lowLatencyMode:false,maxBufferLength:10});
    h.loadSource("/proxy/m.m3u8");
    h.attachMedia(v);
    h.on(Hls.Events.MANIFEST_PARSED,function(){i.textContent=""});
    h.on(Hls.Events.ERROR,function(e,d){
      console.log("ERR",d.type,d.details);
      if(d.fatal){i.textContent=d.type+" "+d.details;h.destroy();setTimeout(play,4000);}
    });
  }else{
    v.src="/proxy/m.m3u8";
  }
}
play();
})();
</script>
</body>
</html>"""


def local_name(uri):
    return uri.split("?")[0].split("#")[0].split("/")[-1]


def rewrite_playlist(text, prefix):
    out = []
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("#EXT-X-MAP") or s.startswith("#EXT-X-KEY"):
            m = re.search(r'URI="([^"]+)"', s)
            if m:
                line = line[:m.start(1)] + prefix + local_name(m.group(1)) + line[m.end(1):]
            out.append(line)
        elif s and not s.startswith("#"):
            out.append(prefix + local_name(s))
        else:
            out.append(line)
    return "\n".join(out) + "\n"


class Handler(http.server.BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def do_GET(self):
        path = self.path.split("?")[0]
        if path == "/proxy/m.m3u8":
            return self.master()
        m = re.fullmatch(r"/proxy/v/(\d+)\.m3u8", path)
        if m:
            return self.variant(int(m.group(1)))
        m = re.fullmatch(r"/proxy/a/(\d+)\.m3u8", path)
        if m:
            return self.audio_playlist(int(m.group(1)))
        m = re.fullmatch(r"/proxy/(?:s|as)/(\d+)/([^/]+)", path)
        if m:
            return self.segment(int(m.group(1)), m.group(2), path.startswith("/proxy/as/"))
        if path == "/api/info":
            return self.reply(200, json.dumps({
                "id": state["id"], "title": state["title"],
                "url": state["url"].split("?")[0],
                "levels": [{"res": l["res"], "bw": l["bw"]} for l in state["levels"]],
            }, ensure_ascii=False).encode(), "application/json")
        if path in ("/", "/index.html"):
            try:
                with open(HLS_JS_PATH, "r", encoding="utf-8") as f:
                    js = f.read()
            except OSError:
                return self.reply(500, b"falta hls.min.js", "text/plain")
            page = HTML.replace("PLACEHOLDER_HLSJS", js).encode("utf-8")
            return self.reply(200, page, "text/html; charset=utf-8")
        self.reply(404, b"404", "text/plain")

    def master(self):
        with lock:
            url = state["url"]
        try:
            r = session.get(url.split("#")[0], timeout=20)
        except Exception as e:
            return self.reply(502, str(e).encode(), "text/plain")
        text = r.text
        lv, fresh = parse_master(text, url)
        with lock:
            if lv:
                state["levels"] = lv
            state["audio"] = fresh
        if "EXT-X-STREAM-INF" not in text:
            return self.reply(200, rewrite_playlist(text, "/proxy/s/0/").encode(),
                              "application/vnd.apple.mpegurl")
        lines = []
        n = 0
        a = 0
        for line in text.splitlines():
            s = line.strip()
            if s.startswith("#EXT-X-MEDIA:") and "TYPE=AUDIO" in s and 'URI="' in s:
                m = re.search(MEDIA_RE, s)
                if m and a < len(fresh):
                    line = line[:m.start(1)] + f"/proxy/a/{a}.m3u8" + line[m.end(1):]
                    a += 1
                lines.append(line)
            elif s and not s.startswith("#"):
                lines.append(f"/proxy/v/{n}.m3u8")
                n += 1
            else:
                lines.append(line)
        return self.reply(200, ("\n".join(lines) + "\n").encode(),
                          "application/vnd.apple.mpegurl")

    def variant(self, n):
        with lock:
            levels = list(state["levels"])
        if n >= len(levels):
            return self.reply(404, b"nivel inexistente", "text/plain")
        try:
            r = session.get(levels[n]["url"].split("#")[0], timeout=20)
        except Exception as e:
            return self.reply(502, str(e).encode(), "text/plain")
        body = rewrite_playlist(r.text, f"/proxy/s/{n}/").encode()
        return self.reply(200, body, "application/vnd.apple.mpegurl")

    def audio_playlist(self, n):
        with lock:
            audio = list(state["audio"])
        if n >= len(audio):
            return self.reply(404, b"pista de audio inexistente", "text/plain")
        try:
            r = session.get(audio[n], timeout=20)
        except Exception as e:
            return self.reply(502, str(e).encode(), "text/plain")
        body = rewrite_playlist(r.text, f"/proxy/as/{n}/").encode()
        return self.reply(200, body, "application/vnd.apple.mpegurl")

    def segment(self, n, name, is_audio=False):
        with lock:
            pool = list(state["audio" if is_audio else "levels"])
        if n >= len(pool):
            return self.reply(404, b"recurso inexistente", "text/plain")
        base = pool[n] if is_audio else pool[n]["url"]
        target = urllib.parse.urljoin(base, name)
        try:
            r = session.get(target, timeout=25)
        except Exception as e:
            return self.reply(502, str(e).encode(), "text/plain")
        ct = r.headers.get("Content-Type", "video/mp2t")
        return self.reply(r.status_code, r.content, ct)

    def reply(self, code, body, ctype):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", len(body))
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
    probe = socket.socket()
    probe.settimeout(0.5)
    try:
        probe.connect(("127.0.0.1", PORT))
        print(f"ya hay una instancia en el puerto {PORT}; cierro esta.", flush=True)
        raise SystemExit(0)
    except OSError:
        pass
    finally:
        probe.close()

    extract(VIDEO_ID)
    print(f"{state['title']} | niveles: {[l['res'] for l in state['levels']]}", flush=True)
    print(f"stream: {state['url'].split('?')[0]}", flush=True)
    srv = Server(("127.0.0.1", PORT), Handler)

    def loop():
        while True:
            time.sleep(REFRESH)
            try:
                extract(state["id"])
                print(f"[{time.strftime('%H:%M:%S')}] token renovado", flush=True)
            except Exception as e:
                print(f"[{time.strftime('%H:%M:%S')}] error: {e}", flush=True)

    threading.Thread(target=loop, daemon=True).start()
    print(f"\nhttp://127.0.0.1:{PORT}", flush=True)
    srv.serve_forever()