import re
import os
import sys
import urllib.request
import time
import json
from datetime import datetime

CAMARAS = {
    "Ushuaia - Puerto": "https://www.skylinewebcams.com/es/webcam/argentina/tierra-del-fuego/ushuaia/ushuaia.html",
}

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PLAYLIST_DIR = os.path.join(SCRIPT_DIR, "playlists")
LOG_FILE = os.path.join(SCRIPT_DIR, "refresh.log")

def log(msg):
    ts = datetime.now().strftime("%H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")

def fetch_stream(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        html = resp.read().decode("utf-8", errors="ignore")
    match = re.search(r"source\s*:\s*'([^']+\.m3u8[^']*)'", html)
    if not match:
        return None
    source = match.group(1)
    if not source.startswith("http"):
        source = "https://www.skylinewebcams.com/" + source
    return source

def generate_playlists():
    os.makedirs(PLAYLIST_DIR, exist_ok=True)
    urls = []
    for nombre, page_url in CAMARAS.items():
        log(f"Buscando stream: {nombre}")
        try:
            stream = fetch_stream(page_url)
            if stream:
                log(f"  OK -> {stream[:80]}...")
                urls.append((nombre, stream))
            else:
                log(f"  ERROR: stream no encontrado")
        except Exception as e:
            log(f"  ERROR: {e}")

    if not urls:
        log("No se obtuvieron streams")
        return

    # Playlist individual por camara (para escenas separadas en OBS)
    for nombre, url in urls:
        safe = nombre.replace(" ", "_").replace("-", "_")
        path = os.path.join(PLAYLIST_DIR, f"{safe}.m3u")
        with open(path, "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n")
            f.write(f"#EXTINF:-1,{nombre}\n")
            f.write(f"{url}\n")
        log(f"Playlist creada: {path}")

    # Playlist combinada con todas las camaras (para rotar)
    combined = os.path.join(PLAYLIST_DIR, "todas.m3u")
    with open(combined, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for nombre, url in urls:
            f.write(f"#EXTINF:-1,{nombre}\n")
            f.write(f"{url}\n")
    log(f"Playlist combinada: {combined}")

    # Guardar URLs como JSON para referencia
    data = {
        "actualizado": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "camaras": [{"nombre": n, "url": u} for n, u in urls]
    }
    with open(os.path.join(SCRIPT_DIR, "camaras.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    log(f"JSON actualizado")

if __name__ == "__main__":
    intervalo = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    if intervalo > 0:
        log(f"=== Modo automatico: cada {intervalo} minutos ===")
        while True:
            generate_playlists()
            log(f"Proxima actualizacion en {intervalo} min\n")
            time.sleep(intervalo * 60)
    else:
        generate_playlists()
