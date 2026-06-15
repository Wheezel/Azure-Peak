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

# ---------------------------------------------------------------- map parsing
def parse_map(path):
    txt = open(path, errors="replace").read()
    gridstart = re.search(r'^\(\d+,\d+,\d+\) = \{"', txt, re.M).start()
    dtxt = txt[:gridstart]
    entry = re.compile(r'^"([a-zA-Z]+)" = \((.*?)\)\s*$', re.S | re.M)
    key_area, key_flags = {}, {}
    for m in entry.finditer(dtxt):
        k, body = m.group(1), m.group(2)
        ar = re.findall(r'/area/[A-Za-z0-9_/]+', body)
        key_area[k] = ar[-1] if ar else None
        key_flags[k] = {
            "mother": "/obj/structure/roguemachine/mossmother/travel" not in body
                       and "/obj/structure/roguemachine/mossmother" in body,
            "tree":   "/obj/structure/roguemachine/mossmother/travel" in body,
            "sacred": "/obj/structure/flora/roguetree/wise/druids" in body,
        }
    block = re.compile(r'^\((\d+),(\d+),(\d+)\) = \{"\n(.*?)\n"\}', re.S | re.M)
    # gather points for flagged keys + area tiles, and overall map height
    flagged = defaultdict(list)          # flag -> [(x,y,z)]
    area_pts = defaultdict(lambda: defaultdict(list))  # area -> z -> [(x,y)]
    maxy = 0
    for b in block.finditer(txt):
        x, _, z = int(b.group(1)), int(b.group(2)), int(b.group(3))
        lines = b.group(4).split("\n"); n = len(lines); maxy = max(maxy, n)
        for i, key in enumerate(lines):
            key = key.strip(); y = n - i
            fa = key_area.get(key)
            if fa: area_pts[fa][z].append((x, y))
            fl = key_flags.get(key)
            if fl:
                for name, on in fl.items():
                    if on: flagged[name].append((x, y, z))
    return flagged, area_pts, maxy

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
    args = ap.parse_args()

    here = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(args.out, exist_ok=True)
    renders = sorted(glob.glob(os.path.join(args.renders, "*-*.png")))
    if not renders:
        sys.exit(f"no renders found in {args.renders}")

    flagged, area_pts, maxy = parse_map(args.map)

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
        "names": {"1": "underground", "2": "surface / town", "3": "mountains / bog", "4": "high ground"},
        "generated": datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
        "commit": (os.environ.get("GITHUB_SHA", "")[:7]),
    }
    json.dump(meta, open(os.path.join(args.out, "meta.json"), "w"), indent=1)
    json.dump(build_pois(flagged, area_pts, maxy),
              open(os.path.join(args.out, "pois.json"), "w"), indent=1)
    shutil.copy(os.path.join(here, "index.html"), os.path.join(args.out, "index.html"))
    open(os.path.join(args.out, ".nojekyll"), "w").close()
    if args.classic and os.path.isdir(args.classic):
        shutil.copytree(args.classic, os.path.join(args.out, "classic"), dirs_exist_ok=True)
    print("[done]", args.out, "levels", meta["levels"], "dims", dims)

if __name__ == "__main__":
    main()
