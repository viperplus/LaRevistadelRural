import urllib.request, re

req = urllib.request.Request(
    'https://www.skylinewebcams.com/es/webcam/argentina/tierra-del-fuego/ushuaia/ushuaia.html',
    headers={'User-Agent': 'Mozilla/5.0'}
)
resp = urllib.request.urlopen(req, timeout=15)
html = resp.read().decode('utf-8', errors='ignore')
m = re.search(r"source\s*:\s*'([^']+\.m3u8[^']*)'", html)
source = m.group(1)
real_url = 'https://hd-auth.skylinewebcams.com/' + source.replace('livee.', 'live.')
print('REAL URL:', real_url)

req2 = urllib.request.Request(real_url, headers={'User-Agent': 'Mozilla/5.0'})
resp2 = urllib.request.urlopen(req2, timeout=10)
data = resp2.read(500).decode('utf-8', errors='ignore')
print('STATUS:', resp2.status)
print('CONTENT:', data[:300])
