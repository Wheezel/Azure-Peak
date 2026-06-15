# Map viewer (v2) — full-res sprites, auto-built from the repo

An interactive pan/zoom viewer of `dun_world` rendered at **full native sprite
resolution** (32 px/tile), rebuilt and redeployed **automatically by GitHub
Actions whenever the map changes** — so the published map always matches the
repo. The heavy tiles are produced in CI and published straight to GitHub Pages,
so they never get committed to git history.

> The older, lightweight (half-res, committed-to-`/docs`) viewer still lives in
> `docs/map-viewer/`. This workflow also republishes it at **`/classic/`** for
> convenience.

## One-time setup

1. **Point Pages at Actions:** repo **Settings → Pages → Build and deployment →
   Source → GitHub Actions**. (This replaces the old "Deploy from a branch"
   setting that served the half-res viewer.)
2. **Make sure the workflow can deploy:** Pages deploys most cleanly from the
   **default branch**. Either:
   - merge **PR #1** so the workflow runs on `main`, **or**
   - allow this branch in the `github-pages` environment
     (Settings → Environments → `github-pages` → deployment branches), **or**
   - just hit **Run workflow** on the Actions tab (manual `workflow_dispatch`).

Once Pages is on "GitHub Actions," the site goes live at:

```
https://wheezel.github.io/Azure-Peak/            <- full-res viewer
https://wheezel.github.io/Azure-Peak/classic/    <- the half-res /docs viewer
```

## How the auto-update works

`.github/workflows/map-viewer.yml` triggers on push when any of these change
(plus a manual **Run workflow** button):

- `_maps/map_files/dun_world/dun_world.dmm` — the map itself
- `icons/**` — sprite changes
- `tools/mapviewer/**` — the viewer/build tooling

Each run:
1. builds **SpacemanDMM `dmm-tools`** (cached after the first run),
2. renders one PNG per z-level (`dmm-tools … minimap`),
3. runs `build.py` → WebP Deep-Zoom tiles + `pois.json` + `areas.json` +
   `keys.json` + `borders.json` + `walk.json` + `meta.json`,
4. uploads the `_site` folder and deploys it to Pages.

**Viewer controls:** z-level buttons; a **pins** toggle (points of interest); an
**areas** toggle (labels every area with its `.dmm` path); a **keys** toggle —
labels every locked door with the **key that opens it** (🔑 bishop's key, etc.,
by matching each door's `lockid` to the `roguekey` definitions in `keys.dm`),
plus a searchable key table; a **borders** toggle — white outlines around every
area/building (drawn from area boundaries, crisp at any zoom); and a **route**
mode — click a start then a destination and it draws a **Google-Maps-style path**
that prefers roads/paths over open ground and avoids walls/water (A* over a
per-tile walk-cost grid derived from turf types). Routing is per-floor; the view
is preserved when you switch z-levels so stairs line up.

Nothing is hard-coded to the current map size: `build.py` reads the render
dimensions and the viewer reads `meta.json`, so a bigger map / different z-count
just works. POI pins (church, Inquisition manor, Sacred Tree of Dendor, every
Heartroot + the Mossmother) are re-extracted from the `.dmm` on every build.

## Build it locally

```sh
# 1. render (needs dmm-tools on PATH — cargo install --git \
#    https://github.com/SpaceManiac/SpacemanDMM.git dmm-tools-cli)
dmm-tools -e roguetown.dme minimap -o build/renders _maps/map_files/dun_world/dun_world.dmm

# 2. tile + assemble the site
pip install pillow
python tools/mapviewer/build.py --renders build/renders \
    --map _maps/map_files/dun_world/dun_world.dmm --out _site

# 3. serve it (must be over http, not file://)
python -m http.server 8000 --directory _site
# open http://localhost:8000/
```

`build.py` options: `--max-width N` (downscale for a lighter build),
`--quality` (WebP quality, default 82), `--tile` (tile size, default 1024),
`--classic DIR` (also publish another viewer dir under `/classic`).

## Files

```
tools/mapviewer/build.py     renders -> tiles + pois.json + meta.json + index.html
tools/mapviewer/index.html   the viewer (meta-driven; custom WebP tile source)
.github/workflows/map-viewer.yml   render + tile + deploy pipeline
```
