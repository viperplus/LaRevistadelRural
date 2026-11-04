import re
import os
import sys
import json
import urllib.request
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
HTML_FILE = os.path.join(SCRIPT_DIR, "cam.html")
JSON_FILE = os.path.join(SCRIPT_DIR, "stream.json")
PAGE_URL = "https://www.skylinewebcams.com/es/webcam/argentina/tierra-del-fuego/ushuaia/ushuaia.html"

HTML_TEMPLATE = '''<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
* {{ margin: 0; padding: 0; }}
html, body {{ width: 100%; height: 100%; overflow: hidden; background: #000; }}
video {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
</style>
</head>
<body>
<video id="video" autoplay muted></video>
<script>
var defined_hls = null;
var video = document.getElementById('video');
var streamUrl = '{stream_url}';
var defined_Hls = null;

function loadScript(cb) {{
    if (window.Hls) {{ defined_Hls = window.Hls; cb(); return; }}
    var s = document.createElement('script');
    s.src = 'https://cdn.jsdelivr.net/npm/hls.js@latest';
    s.onload = function() {{ defined_Hls = window.Hls; cb(); }};
    document.head.appendChild(s);
}}

function playStream(url) {{
    if (defined_Hls && defined_Hls.isSupported()) {{
        if (defined_hls) {{ defined_hls.destroy(); }}
        defined_hls = new defined_Hls({{
            liveSyncDurationCount: 2,
            enableWorker: true,
            lowLatencyMode: false,
            maxBufferLength: 10
        }});
        defined_hls.loadSource(url);
        defined_hls.attachMedia(video);
        defined_hls.on(defined_Hls.Events.ERROR, function(e, data) {{
            if (data.fatal) {{
                setTimeout(function() {{ playStream(url); }}, 5000);
            }}
        }});
    }} else if (video.canPlayType('application/vnd.apple.mpegurl')) {{
        video.src = url;
    }}
}}

loadScript(function() {{ playStream(streamUrl); }});
</script>
</body>
</html>'''

def fetch_stream():
    req = urllib.request.Request(PAGE_URL, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        html = resp.read().decode("utf-8", errors="ignore")
    match = re.search(r"source\s*:\s*'([^']+\.m3u8[^']*)'", html)
    if not match:
        return None
    source = match.group(1)
    return "https://hd-auth.skylinewebcams.com/" + source.replace("livee.", "live.")

def update():
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] Buscando stream de Ushuaia...")
    try:
        stream = fetch_stream()
        if not stream:
            print(f"[{ts}] ERROR: stream no encontrado")
            return False

        print(f"[{ts}] OK: {stream[:70]}...")

        html = HTML_TEMPLATE.format(stream_url=stream)
        with open(HTML_FILE, "w", encoding="utf-8") as f:
            f.write(html)

        data = {"url": stream, "actualizado": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        with open(JSON_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f)

        print(f"[{ts}] HTML y JSON actualizados")
        return True
    except Exception as e:
        print(f"[{ts}] ERROR: {e}")
        return False

if __name__ == "__main__":
    update()
