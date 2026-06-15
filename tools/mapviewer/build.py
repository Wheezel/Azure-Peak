#!/usr/bin/env python3
"""
Build the interactive map-viewer site from dmm-tools minimap renders.

Pipeline (run in CI and locally):
  1. dmm-tools renders one PNG per z-level  ->  <renders>/dun_world-<z>.png
  2. this script slices each render into a WebP Deep-Zoom tile pyramid,
     extracts point-of-interest pins straight from the .dmm, writes meta.json,
     and drops in the viewer index.html + .nojekyll.

The viewer reads meta.json, so map-size / z-count changes are picked up
automatically -- nothing here is hard-coded to the current map dimensions.

Usage:
  build.py --renders DIR --map path/to.dmm --out SITE_DIR [--tile 1024]
           [--quality 82] [--max-width N]  [--classic DIR]
"""
import argparse, glob, json, math, os, re, shutil, sys, datetime
from collections import Counter, defaultdict
from PIL import Image
Image.MAX_IMAGE_PIXELS = None

TILE_PX = 32  # dmm-tools renders every map tile as 32x32 px

# Walk cost per turf for routing: 0 = blocked, higher = less preferred.
# Roads cheapest, then paving, then open ground; indoors discouraged; walls/water/void blocked.
def turf_cost(t):
    if not t or "transparent/openspace" in t: return 0
    if "water" in t or "open/lava" in t: return 0
    if "closed" in t: return 0
    if "/road" in t: return 1
    if "naturalstone" in t or "cobble" in t: return 2
    if "grass" in t or "dirt" in t or "sand" in t: return 3
    if "floor" in t: return 5
    return 0

# ---------------------------------------------------------------- map parsing
def parse_map(path):
    txt = open(path, errors="replace").read()
    gridstart = re.search(r'^\(\d+,\d+,\d+\) = \{"', txt, re.M).start()
    dtxt = txt[:gridstart]
    entry = re.compile(r'^"([a-zA-Z]+)" = \((.*?)\)\s*$', re.S | re.M)
    key_area, key_flags, key_locks, key_cost, key_portal = {}, {}, {}, {}, {}
    for m in entry.finditer(dtxt):
        k, body = m.group(1), m.group(2)
        ar = re.findall(r'/area/[A-Za-z0-9_/]+', body)
        key_area[k] = ar[-1] if ar else None
        locks = re.findall(r'lockid = "([^"]+)"', body)
        if locks: key_locks[k] = locks
        tu = re.findall(r'/turf/[A-Za-z0-9_/]+', body)
        key_cost[k] = turf_cost(tu[-1] if tu else "")
        key_portal[k] = ("/obj/structure/stairs" in body) or ("/obj/structure/ladder" in body)
        key_flags[k] = {
            "mother": "/obj/structure/roguemachine/mossmother/travel" not in body
                       and "/obj/structure/roguemachine/mossmother" in body,
            "tree":   "/obj/structure/roguemachine/mossmother/travel" in body,
            "sacred": "/obj/structure/flora/roguetree/wise/druids" in body,
        }
    block = re.compile(r'^\((\d+),(\d+),(\d+)\) = \{"\n(.*?)\n"\}', re.S | re.M)
    flagged = defaultdict(list)          # flag -> [(x,y,z)]
    area_pts = defaultdict(lambda: defaultdict(list))  # area -> z -> [(x,y)]
    lock_pts = defaultdict(list)         # lockid -> [(x,y,z)]
    tile_area = defaultdict(dict)        # z -> {(row,col): area_id}  (row 0 = north/top)
    tile_cost = defaultdict(dict)        # z -> {(row,col): walk_cost}
    portal_pts = defaultdict(list)       # z -> [(row,col)]  stairs/ladders (floor links)
    area_ids = {}
    maxx = maxy = 0
    for b in block.finditer(txt):
        x, _, z = int(b.group(1)), int(b.group(2)), int(b.group(3))
        lines = b.group(4).split("\n"); n = len(lines)
        maxy = max(maxy, n); maxx = max(maxx, x); col = x - 1
        for i, key in enumerate(lines):
            key = key.strip(); y = n - i
            fa = key_area.get(key)
            if fa:
                area_pts[fa][z].append((x, y))
                aid = area_ids.get(fa)
                if aid is None: aid = area_ids[fa] = len(area_ids)
                tile_area[z][(i, col)] = aid
            cost = key_cost.get(key, 0)
            if cost: tile_cost[z][(i, col)] = cost
            if key_portal.get(key): portal_pts[z].append((i, col))
            for lid in key_locks.get(key, ()):
                lock_pts[lid].append((x, y, z))
            fl = key_flags.get(key)
            if fl:
                for name, on in fl.items():
                    if on: flagged[name].append((x, y, z))
    return flagged, area_pts, lock_pts, tile_area, tile_cost, portal_pts, maxx, maxy

def centroid(area_pts, area):
    by_z = area_pts.get(area)
    if not by_z: return None
    z = max(by_z, key=lambda zz: len(by_z[zz]))
    pts = by_z[z]
    return (round(sum(p[0] for p in pts)/len(pts)),
            round(sum(p[1] for p in pts)/len(pts)), z)

def build_pois(flagged, area_pts, maxy):
    def px(x, y): return [(x-1)*TILE_PX + TILE_PX//2, (maxy-y)*TILE_PX + TILE_PX//2]
    pois = defaultdict(list)
    def add(z, name, x, y, typ):
        p = px(x, y); pois[z].append({"name": name, "x": x, "y": y, "px": p[0], "py": p[1], "type": typ})
    for x, y, z in flagged.get("mother", []): add(z, "Mossmother (root hub)", x, y, "mother")
    for x, y, z in flagged.get("tree", []):   add(z, "Heartroot tree", x, y, "tree")
    for x, y, z in flagged.get("sacred", []): add(z, "Sacred Tree of Dendor", x, y, "sacred")
    c = centroid(area_pts, "/area/rogue/indoors/town/church")
    if c: add(c[2], "The House of the Ten (church)", c[0], c[1], "church")
    m = centroid(area_pts, "/area/rogue/indoors/inq")
    if m: add(m[2], "The Inquisition (manor)", m[0], m[1], "manor")
    return {str(z): v for z, v in sorted(pois.items())}

def build_areas(area_pts, maxy, min_tiles=10):
    """Per z-level, every area's short name + centroid + bbox (in render px).
    Powers the toggleable 'areas' identification layer in the viewer."""
    out = defaultdict(list)
    for area, by_z in area_pts.items():
        if not area: continue
        short = area.replace("/area/rogue/", "").replace("indoors/", "").replace("outdoors/", "")
        for z, pts in by_z.items():
            if len(pts) < min_tiles: continue
            xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
            cx = sum(xs)/len(xs); cy = sum(ys)/len(ys)
            out[str(z)].append({
                "name": short,
                "px": round((cx-1)*TILE_PX + TILE_PX/2),
                "py": round((maxy-cy)*TILE_PX + TILE_PX/2),
                "w": (max(xs)-min(xs)+1)*TILE_PX,
                "h": (max(ys)-min(ys)+1)*TILE_PX,
                "n": len(pts),
            })
    for z in out: out[z].sort(key=lambda a: -a["n"])
    return dict(out)

def parse_keys(path):
    """lockid -> key name, parsed from the roguekey definitions (keys.dm).
    Lets the keys layer say which key opens each locked door."""
    lockmap = {}
    if not path or not os.path.isfile(path):
        return lockmap
    txt = open(path, errors="replace").read()
    last_name = None
    for tok in re.finditer(r'name = "([^"]+)"|lockid = "([^"]+)"', txt):
        if tok.group(1) is not None:
            last_name = tok.group(1)
        elif tok.group(2) not in lockmap and last_name:
            lockmap[tok.group(2)] = last_name
    return lockmap

def build_keys(lock_pts, lockmap, maxy):
    """Per z-level, every locked door: its lockid + the key that opens it."""
    out = defaultdict(list)
    for lid, pts in lock_pts.items():
        keyname = lockmap.get(lid)
        for (x, y, z) in pts:
            out[str(z)].append({
                "lockid": lid, "key": keyname,
                "px": (x-1)*TILE_PX + TILE_PX//2,
                "py": (maxy-y)*TILE_PX + TILE_PX//2,
            })
    return dict(out)

def build_borders(tile_area, maxx, maxy):
    """White outlines between areas (in render px) — merged into horizontal/
    vertical runs so buildings/rooms are easy to see. Each seg = [x1,y1,x2,y2]."""
    out = {}
    TP = TILE_PX
    for z, grid in tile_area.items():
        segs = []
        for c in range(maxx - 1):              # vertical edges between col c | c+1
            run = None
            for i in range(maxy):
                if grid.get((i, c)) != grid.get((i, c+1)):
                    if run is None: run = i
                elif run is not None:
                    segs.append([(c+1)*TP, run*TP, (c+1)*TP, i*TP]); run = None
            if run is not None: segs.append([(c+1)*TP, run*TP, (c+1)*TP, maxy*TP])
        for i in range(maxy - 1):              # horizontal edges between row i | i+1
            run = None
            for c in range(maxx):
                if grid.get((i, c)) != grid.get((i+1, c)):
                    if run is None: run = c
                elif run is not None:
                    segs.append([run*TP, (i+1)*TP, c*TP, (i+1)*TP]); run = None
            if run is not None: segs.append([run*TP, (i+1)*TP, maxx*TP, (i+1)*TP])
        out[str(z)] = segs
    return out

def build_walk(tile_cost, maxx, maxy):
    """Per z-level walk grid for routing: row strings of cost digits (0 = blocked).
    Row 0 = north/top, matching the rendered image."""
    out = {}
    for z, grid in tile_cost.items():
        out[str(z)] = ["".join(str(grid.get((i, c), 0)) for c in range(maxx)) for i in range(maxy)]
    return out

def build_portals(portal_pts):
    """Per z-level stair/ladder tiles [[row,col],...] — the floor-to-floor links
    used by cross-floor routing."""
    return {str(z): sorted(set(map(tuple, rc))) for z, rc in portal_pts.items()}

# ---------------------------------------------------------------- dzi tiling
def make_dzi(src, base, out, tile, overlap, quality, max_width=None):
    im = Image.open(src).convert("RGB")
    if max_width and im.width > max_width:
        im = im.resize((max_width, round(im.height*max_width/im.width)), Image.LANCZOS)
    W, H = im.size
    maxlevel = math.ceil(math.log2(max(W, H)))
    fd = os.path.join(out, f"{base}_files")
    for L in range(maxlevel+1):
        scale = 0.5**(maxlevel-L)
        lw = max(1, math.ceil(W*scale)); lh = max(1, math.ceil(H*scale))
        lvl = im if (lw == W and lh == H) else im.resize((lw, lh), Image.LANCZOS)
        ld = os.path.join(fd, str(L)); os.makedirs(ld, exist_ok=True)
        for c in range(math.ceil(lw/tile)):
            for r in range(math.ceil(lh/tile)):
                x, y = c*tile, r*tile
                box = (max(x-overlap, 0), max(y-overlap, 0),
                       min(x+tile+overlap, lw), min(y+tile+overlap, lh))
                lvl.crop(box).save(os.path.join(ld, f"{c}_{r}.webp"), quality=quality, method=4)
    return [W, H]

# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--renders", required=True)
    ap.add_argument("--map", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--tile", type=int, default=1024)
    ap.add_argument("--overlap", type=int, default=1)
    ap.add_argument("--quality", type=int, default=82)
    ap.add_argument("--max-width", type=int, default=0, help="downscale renders to this width (0 = native/full res)")
    ap.add_argument("--classic", default="", help="optional dir to copy in under /classic")
    ap.add_argument("--keys", default="code/game/objects/items/rogueitems/keys.dm",
                    help="path to keys.dm for the lockid -> key-name mapping")
    args = ap.parse_args()

    here = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(args.out, exist_ok=True)
    renders = sorted(glob.glob(os.path.join(args.renders, "*-*.png")))
    if not renders:
        sys.exit(f"no renders found in {args.renders}")

    flagged, area_pts, lock_pts, tile_area, tile_cost, portal_pts, maxx, maxy = parse_map(args.map)
    lockmap = parse_keys(args.keys)

    dims = {}
    for png in renders:
        m = re.search(r'-(\d+)\.png$', os.path.basename(png))
        if not m: continue
        z = int(m.group(1))
        print(f"[tiles] z{z} <- {png}")
        dims[str(z)] = make_dzi(png, f"dun_world-z{z}", args.out, args.tile,
                                args.overlap, args.quality, args.max_width or None)

    meta = {
        "levels": sorted(int(z) for z in dims),
        "dims": dims,
        "tile": args.tile, "overlap": args.overlap,
        "grid": {"cols": maxx, "rows": maxy},
        "names": {"1": "underground", "2": "surface / town", "3": "mountains / bog", "4": "high ground"},
        "generated": datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
        "commit": (os.environ.get("GITHUB_SHA", "")[:7]),
    }
    json.dump(meta, open(os.path.join(args.out, "meta.json"), "w"), indent=1)
    json.dump(build_pois(flagged, area_pts, maxy),
              open(os.path.join(args.out, "pois.json"), "w"), indent=1)
    json.dump(build_areas(area_pts, maxy),
              open(os.path.join(args.out, "areas.json"), "w"), indent=1)
    json.dump(build_keys(lock_pts, lockmap, maxy),
              open(os.path.join(args.out, "keys.json"), "w"), indent=1)
    json.dump(build_borders(tile_area, maxx, maxy),
              open(os.path.join(args.out, "borders.json"), "w"), separators=(",", ":"))
    json.dump(build_walk(tile_cost, maxx, maxy),
              open(os.path.join(args.out, "walk.json"), "w"), separators=(",", ":"))
    json.dump(build_portals(portal_pts),
              open(os.path.join(args.out, "portals.json"), "w"), separators=(",", ":"))
    shutil.copy(os.path.join(here, "index.html"), os.path.join(args.out, "index.html"))
    open(os.path.join(args.out, ".nojekyll"), "w").close()
    if args.classic and os.path.isdir(args.classic):
        shutil.copytree(args.classic, os.path.join(args.out, "classic"), dirs_exist_ok=True)
    print("[done]", args.out, "levels", meta["levels"], "dims", dims)

if __name__ == "__main__":
    main()
