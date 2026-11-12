# -*- coding: utf-8 -*-
"""Genera la version PDF de la revista a partir de impresion.html.

Uso (desde la carpeta revista/):
    python herramientas/generar-pdf.py

Requiere: playwright (con chromium instalado) y pymupdf.
"""
import os, sys, time, socket, subprocess, shutil

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EDIT = os.path.join(BASE, "ediciones", "01")
URL_PATH = "ediciones/01/impresion.html"
OUT = os.path.join(EDIT, "revista.pdf")
TMP = os.path.join(EDIT, "revista.tmp.pdf")

def puerto_libre():
    s = socket.socket()
    s.bind(("", 0))
    p = s.getsockname()[1]
    s.close()
    return p

def esperar_servidor(puerto, timeout=30):
    import urllib.request
    t0 = time.time()
    while time.time() - t0 < timeout:
        try:
            urllib.request.urlopen("http://127.0.0.1:%d/" % puerto, timeout=2).read()
            return True
        except Exception:
            time.sleep(0.5)
    return False

def main():
    puerto = puerto_libre()
    srv = subprocess.Popen(
        [sys.executable, "-m", "http.server", str(puerto)],
        cwd=BASE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        if not esperar_servidor(puerto):
            raise SystemExit("El servidor local no arranco.")
        from playwright.sync_api import sync_playwright
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            page = browser.new_page()
            page.goto("http://127.0.0.1:%d/%s" % (puerto, URL_PATH),
                      wait_until="load", timeout=120000)
            time.sleep(8)
            page.wait_for_function(
                "Array.from(document.images).every(i => i.complete)",
                timeout=60000)
            page.pdf(
                path=TMP,
                format="A4",
                print_background=True,
                prefer_css_page_size=True,
                display_header_footer=True,
                header_template="<div></div>",
                footer_template=(
                    '<div style="font-size:8px;width:100%;text-align:center;'
                    'color:#6b6b6b;font-family:system-ui,sans-serif;">'
                    'La Revista del Rural · Edición N.º 05 · '
                    'Página <span class="pageNumber"></span> de '
                    '<span class="totalPages"></span></div>'),
                margin={"top": "18mm", "bottom": "18mm",
                        "left": "16mm", "right": "16mm"},
            )
            browser.close()
        print("PDF generado:", TMP)
    finally:
        srv.terminate()
        srv.wait()

    # Optimizacion con pymupdf: downsampling + garbage collection + compresion.
    try:
        import fitz
        from PIL import Image
        import io
        doc = fitz.open(TMP)
        processed = set()
        for page in doc:
            for img in page.get_images(full=True):
                xref = img[0]
                if xref in processed:
                    continue
                processed.add(xref)
                try:
                    info = doc.extract_image(xref)
                except Exception:
                    continue
                if info.get("ext") not in ("jpeg", "jpg", "png", "webp"):
                    continue
                if info["width"] <= 1200 and info["height"] <= 1200:
                    continue
                try:
                    pil = Image.open(io.BytesIO(info["image"]))
                except Exception:
                    continue
                if pil.mode not in ("RGB", "L"):
                    pil = pil.convert("RGB")
                w, h = pil.size
                s = 1200 / max(w, h)
                if s < 1:
                    pil = pil.resize((max(1, round(w * s)), max(1, round(h * s))),
                                     Image.LANCZOS)
                buf = io.BytesIO()
                pil.save(buf, "JPEG", quality=75, optimize=True, progressive=True)
                new_bytes = buf.getvalue()
                if len(new_bytes) < len(info["image"]):
                    try:
                        page.replace_image(xref, stream=new_bytes)
                    except Exception:
                        pass
        doc.save(OUT, garbage=4, deflate=True, clean=True, pretty=False)
        doc.close()
        os.remove(TMP)
        print("PDF optimizado:", OUT)
        print("Tamaño final: %.1f MB" % (os.path.getsize(OUT) / 1024 / 1024))
    except Exception as e:
        if os.path.isfile(TMP):
            try:
                if os.path.isfile(OUT):
                    os.remove(OUT)
                shutil.move(TMP, OUT)
            except Exception as e2:
                print("No se pudo mover el PDF:", e2)
        print("Optimizacion omitida (%s). PDF sin optimizar: %s" % (e, OUT))

if __name__ == "__main__":
    main()
