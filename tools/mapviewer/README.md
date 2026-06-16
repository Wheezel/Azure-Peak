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
per-tile walk-cost grid derived from turf types), with a **clear route** button.
Routing is **cross-floor**: stairs/ladders are extracted as floor links
(`portals.json`), so a path can go up/down levels — it draws the portion on the
current floor and drops **↑/↓ markers** where it changes z; since the view is
preserved across z-switches, you just follow the markers between floors.
Endpoints can be set by **clicking the map** or via the route panel's **From/To
search boxes** — a dropdown of matching **areas**, **keys** (a door it opens),
and **POIs** (click or arrow-key + Enter); picking one flies you there and routes
when both ends are set.

Outside route mode, **clicking a staircase, ladder, or travel-portal jumps to
where it leads** — stairs/ladders to the partner landing on the adjacent floor,
**travel-tiles to the linked map** (e.g. a `wretch` portal teleports to the
Wretch Coast).

**Openspace is rendered see-through, like in game:** where a level has openspace,
the level below shows through it (dimmed for depth, composited recursively in
`build.py`). And **shift-right-clicking openspace drops the view to the level
below** at that spot (`openspace.json` marks the see-through tiles).

**All world z-levels are included.** The world stacks several maps at runtime, so
the viewer renders them in load order with matching z-numbers: **dun_world →
z1–4**, **dungeon → z5–6**, **wretch_coast → z7–9** (config in `build.py`'s
`DEFAULT_MAPS`). Maps have their own dimensions, so grids are per-z. Cross-map
travel isn't coordinate-aligned — it goes through **travel tiles**, which
`build.py` matches by id (a tile's `aportalgoesto` → another's `aportalid`) into
teleport edges (`links.json`). The router uses stairs/ladders within a map **and
these teleport links across maps**, so a route can go e.g. from the town out to
the Wretch Coast.

The viewer is **touch/mobile friendly**: pinch-zoom and drag, finger-sized
controls, a horizontally-scrollable toolbar, and panels that reflow on small
screens.

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
