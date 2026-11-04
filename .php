import io, sys, os
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")
E=r"C:\Users\black\Desktop\opencode archivos\clase n°4\revista\ediciones\01\egresados.html"
h=open(E,encoding="utf-8").read()
# look for any img tags
import re
all=re.findall(r'<img[^>]+>', h)
print("total img tags:", len(all))
for a in all[:15]:
    print(a[:200])
    print()