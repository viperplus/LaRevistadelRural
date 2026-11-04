import re
import sys
import urllib.request

URL = "https://www.skylinewebcams.com/es/webcam/argentina/tierra-del-fuego/ushuaia/ushuaia.html"

def get_stream_url():
    req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as resp:
        html = resp.read().decode("utf-8", errors="ignore")
    match = re.search(r"source\s*:\s*'([^']+\.m3u8[^']*)'", html)
    if not match:
        print("ERROR: no se encontro el stream", file=sys.stderr)
        sys.exit(1)
    source = match.group(1)
    if source.startswith("http"):
        return source
    return "https://www.skylinewebcams.com/" + source

if __name__ == "__main__":
    print(get_stream_url())
