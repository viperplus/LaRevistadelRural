import requests, re

s = requests.Session()
s.headers.update({"User-Agent": "Mozilla/5.0"})
r = s.get("https://www.skylinewebcams.com/es/webcam/argentina/tierra-del-fuego/ushuaia/tren-del-fin-del-mundo.html", timeout=15)
m = re.search(r"source\s*:\s*'([^']+\.m3u8[^']*)'", r.text)
source = m.group(1)
real = "https://hd-auth.skylinewebcams.com/" + source.replace("livee.", "live.")
print("M3U8:", real)

r2 = s.get(real, timeout=10)
print("Status:", r2.status_code)
print(r2.text[:500])

seg = re.search(r"(https://hddn[^\s]+\.ts)", r2.text)
if seg:
    print("\nSegment URL:", seg.group(1))
    r3 = s.get(seg.group(1), timeout=10, stream=True)
    print("Segment status:", r3.status_code)
    print("Content-Type:", r3.headers.get("Content-Type"))
    chunk = next(r3.iter_content(100))
    print("First bytes:", chunk[:20].hex())
