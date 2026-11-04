# AGENTS.md — Aves de la Patagonia (Realidad Aumentada)

## Project Overview
Web-based augmented reality app to recognize printed bird cards using image tracking and overlay 2.5D bird models with audio. Runs entirely in-browser (A-Frame + MindAR, vendored) and is designed for GitHub Pages (HTTPS required). Contains 22 Patagonian bird species from Río Negro.

## Stack
- **Frontend**: Vanilla HTML/CSS/JS (no build step, no bundler)
- **AR**: [A-Frame](https://aframe.io/) + [MindAR](https://hiukim.github.io/mind-ar-js-doc/) (vendored in `lib/`)
- **Assets**: PNG bird cutouts (`assets/ave-25d/`), MP3 calls (`sonidos/`), compiled image targets (`mind/aves.mind`), printed card images (`tarjetas/`)
- **Scripts**: Node.js tooling in `herramientas/` for regenerating cards/targets/cuts

## Key Entry Points
- `index.html` — Landing/field guide with all 22 species (cards, videos, info)
- `ar.html` — AR viewer (camera + card detection + 2.5D bird + audio). Primary experience.
- `tarjetas.html` — Printable card sheet
- `js/datos.js` — **Source of truth** for all 22 species (order defines target indices in `mind/aves.mind`)
- `js/ar.js` — AR logic: camera start, target detection, bird placement/tracking, audio, demo mode
- `js/aves25d.js` — 2.5D bird rendering (billboard, animation, shadows, effects)
- `js/cantos.js` / `js/sonidos.js` — Audio playback with autoplay unlock
- `lib/` — Vendored A-Frame and patched MindAR (`mindar-image-aframe.prod.js` has custom match logic)

## Critical Constraints
- **Target order is fixed**: The order of species in `js/datos.js` must match exactly with `mind/aves.mind`. If you add/reorder species, you **must** recompile markers with `node compilar-mind.mjs`. Otherwise wrong bird shows on cards.
- **MindAR patch is critical**: `lib/mindar-image-aframe.prod.js` is patched (see `herramientas/parchear-mindar.mjs`). Original MindAR picks first target above threshold; with similar card designs it misidentifies. The patch evaluates all targets and picks the one with most matches. **Re-patch after updating the bundle**.
- **HTTPS required**: Camera only works over HTTPS (GitHub Pages provides this). `http://` on some mobile browsers blocks camera.
- **Assets are vendored**: No CDN dependencies at runtime.

## Development Commands
All commands run from repo root or `herramientas/` as noted:

```bash
# Local testing (Windows)
iniciar.bat                    # starts http.server on port 8780

# Or manually
python -m http.server 8780     # from repo root

# Regenerate cards (after changing design/data)
cd herramientas
npm install                    # first time only
node generar-tarjetas.mjs      # needs Microsoft Edge on Windows

# Recompile AR markers (must run if datos.js order changes)
node compilar-mind.mjs

# Re-patch MindAR if bundle updated
node parchear-mindar.mjs

# Optional asset regeneration
node generar-cortes.mjs        # SVG-based cuts (alternative to photos)
node generar-videos.mjs        # loop videos for field guide
node descargar-cantos.mjs      # download from xeno-canto.org (uses puppeteer + browser)
node descargar-fotos.mjs       # find Wikimedia Commons candidates
python preparar_fotos.py       # remove background from chosen photo (rembg)
```

**Testing tools** (in `herramientas/`):
- `test-navegador.mjs` — Puppeteer-based browser tests (loads page, checks assets, tests AR demo/camera with fake stream)
- `verificar-pages.mjs` — Checks deployed Pages config
- `verificar-todas.mjs` — Tests all 22 species detection/sound (creates fake camera per card)

## Common Gotchas
- **MindAR anchor scale lives in `matrix`, NOT `object3D.scale`**: MindAR writes the pose directly into `object3D.matrix` (which carries a ~1000× scale from `postMatrix`) with `matrixAutoUpdate = false`, and never touches `object3D.scale` — so `ancla.object3D.scale` is always `(1,1,1)`. Never compose a local transform from it. A `suavizar-ancla` component did exactly that and silently shrank every bird to 1/1000 size (sub-pixel = invisible) while detection and audio kept working. Symptom: `targetFound` fires + canto suena, pero el ave no se ve. Verify with `node herramientas/diag-ave.mjs`, which prints the bird's world scale (must be ~1000). Any custom pose/anchor code must `decompose()` the matrix to get the real scale.
- **Tests must assert 3D state, not just the DOM**: `test-navegador.mjs` used to check only that the bird entity existed and that the ficha/sound fired — it passed while the bird was invisible. It now asserts the bird's world scale in section [4].
- **Card recognition**: Lighting matters. Best at 30-60cm with good light. Matte paper works better than glossy.
- **Tracking stability**: There is NO smoothing component anymore — `crearAnclas()` appends the bird root directly to the `mindar-image-target` anchor, so the bird follows MindAR's pose 1:1 (tightest possible zoom tracking). Do not reintroduce a pose-remapping smoother without `decompose()`ing the matrix for scale (see the anchor-scale gotcha above). Hand micro-jitter comes from MindAR's own Kalman filter (`filterMinCF`/`filterBeta`), not from app code.
- **Audio autoplay**: Mobile browsers block autoplay; `js/cantos.js` handles unlock on user gesture (button click). Must click "Iniciar cámara" first on some devices.
- **GitHub Pages**: Must have `.nojekyll` in root (present). Deploy from `main` branch root.
- **File paths**: All paths are relative (no absolute URLs). Assets must be committed.
- **Species count**: Always 22 species total. Any changes affecting count/order require full marker recompilation.

## Architecture Notes
- **AR scene**: `ar.html` loads A-Frame, MindAR, then `js/datos.js`, `js/aves-svg.js`, `js/aves25d.js`, `js/sonidos.js`, `js/cantos.js`, `js/ar.js`. Targets created dynamically from `AVES` array.
- **Bird placement**: `aves25d.js` creates billboarded plane with real photo cutout, anchored at feet to card plane. Shadows, animations, effects applied per instance.
- **Image targets**: Compiled with MindAR compiler into `mind/aves.mind`. Order critical.
- **Audio**: Manifest in `js/sonidos.js`, files in `sonidos/`, controlled by `js/cantos.js`.
