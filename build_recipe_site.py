#!/usr/bin/env python3
"""
build_recipe_site.py — Build a clean GitHub Pages recipe site for Azure-Peak.

Pipeline:
  1. Index every /obj and /datum/reagent definition (name/icon/icon_state/desc)
     with BYOND path-based inheritance resolution.
  2. Parse food / brewing / stew / crafting-cooking recipes into structured data.
  3. Resolve every referenced type to a human name + extracted sprite PNG.
  4. Emit docs/ (index.html + assets/sprites/*.png) ready for GitHub Pages.

No raw source is shown to the reader — only names, sprites, ingredients, steps.
"""

import re, os, io, struct, zlib, hashlib, json
from pathlib import Path
from collections import defaultdict

ROOT = Path('.')
DOCS = ROOT / 'docs'
SPRITES = DOCS / 'assets' / 'sprites'

# ---------------------------------------------------------------------------
# 1. TYPE INDEX (name / icon / icon_state / desc) with inheritance
# ---------------------------------------------------------------------------

# path -> {'name','icon','icon_state','desc'} (only directly-set vars)
TYPES = {}

DEF_RE = re.compile(r'^(/(?:obj|datum|turf|mob)/[a-zA-Z0-9_/]+)\s*$')
VAR_RE = re.compile(r'^\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*(.+?)\s*$')

WANTED_VARS = {'name', 'icon', 'icon_state', 'desc',
               'faretype', 'eat_effect', 'extra_eat_effect',
               # item-transform producers (mill / slice / cook)
               'mill_result', 'slice_path', 'slices_num',
               'cooked_type', 'fried_type', 'deep_fried_type', 'boiled_type'}

def strip_comment(v: str) -> str:
    # remove trailing // comment (naively, but values rarely contain //)
    in_str = False
    q = ''
    out = []
    i = 0
    while i < len(v):
        c = v[i]
        if in_str:
            out.append(c)
            if c == q:
                in_str = False
        else:
            if c in '"\'':
                in_str = True; q = c; out.append(c)
            elif c == '/' and i + 1 < len(v) and v[i+1] == '/':
                break
            else:
                out.append(c)
        i += 1
    return ''.join(out).strip()

def unquote(v: str):
    v = v.strip()
    if len(v) >= 2 and v[0] in '"\'' and v[-1] == v[0]:
        return v[1:-1]
    return v

def index_file(path: Path):
    try:
        lines = path.read_text(encoding='utf-8', errors='ignore').split('\n')
    except:
        return
    cur = None
    for line in lines:
        if not line.strip():
            continue
        m = DEF_RE.match(line)
        if m:
            cur = m.group(1)
            # don't clobber an earlier richer def; create if absent
            TYPES.setdefault(cur, {})
            continue
        if cur and (line.startswith('\t') or line.startswith(' ')):
            vm = VAR_RE.match(line)
            if vm:
                var, val = vm.group(1), vm.group(2)
                if var in WANTED_VARS:
                    val = strip_comment(val)
                    # only keep simple scalar values
                    if var in ('name', 'desc', 'icon_state'):
                        TYPES[cur][var] = unquote(val)
                    elif var == 'icon':
                        TYPES[cur]['icon'] = unquote(val)
                    else:  # faretype / eat_effect / extra_eat_effect (raw token)
                        TYPES[cur][var] = val.strip()
            # a non-indented line ends the block; handled by DEF_RE/loop
        else:
            # line at column 0 that's not a def (e.g. proc, comment) -> close block
            if not line.startswith('\t') and not line.startswith(' '):
                cur = None

def build_type_index():
    files = [p for p in ROOT.rglob('*.dm') if '.git' not in p.parts]
    # Process core code/ first, then modular/ — modular overrides win, mirroring
    # BYOND include order so duplicate type defs resolve to the modular version.
    files.sort(key=lambda p: (1 if (p.parts and p.parts[0] == 'modular') else 0, str(p)))
    for p in files:
        index_file(p)

def resolve(path: str, field: str, depth=0):
    """Resolve a var through BYOND path-based inheritance (walk up the path)."""
    if not path or depth > 30:
        return None
    info = TYPES.get(path)
    if info and field in info and info[field]:
        return info[field]
    # walk up one path segment
    parent = path.rsplit('/', 1)[0]
    if parent.count('/') >= 1 and parent != path:
        return resolve(parent, field, depth + 1)
    return None

def nice_name(path: str) -> str:
    n = resolve(path, 'name')
    if n:
        return n
    # fallback: last path segment, prettified
    seg = path.rsplit('/', 1)[-1]
    return seg.replace('_', ' ')

# ---- buff index (eat_effect -> "+1 CON for 30 minutes") --------------------
BUFF_RAW = {}  # buff_path -> {'duration': str, 'stats': {ABBR: int}}
STAT_ABBR = {'STR': 'STR', 'CON': 'CON', 'WIL': 'WIL', 'INT': 'INT',
             'PER': 'PER', 'SPD': 'SPD', 'LCK': 'LCK', 'END': 'END',
             'FOR': 'FOR'}
PROC_SEGS = {'on_creation', 'on_apply', 'on_remove', 'tick', 'New', 'Destroy',
             'proc', 'process', 'be_replaced', 'refresh'}

def _base_buff(path):
    seg = path.rsplit('/', 1)[-1]
    if seg in PROC_SEGS:
        return path.rsplit('/', 1)[0]
    return path

def index_buffs():
    for p in ROOT.rglob('*.dm'):
        if '.git' in p.parts:
            continue
        try:
            lines = p.read_text(encoding='utf-8', errors='ignore').split('\n')
        except:
            continue
        cur = None
        for line in lines:
            if not line.strip():
                continue
            if line[0] not in ' \t':
                m = re.match(r'(/datum/status_effect/[A-Za-z0-9_/]+)', line)
                cur = _base_buff(m.group(1)) if m else None
                continue
            if cur is None:
                continue
            s = line.strip()
            dm = re.match(r'duration\s*=\s*(.+)', s)
            if dm:
                BUFF_RAW.setdefault(cur, {}).setdefault('duration', strip_comment(dm.group(1)))
            em = re.match(r'effectedstats\s*=\s*list\((.*)\)', s)
            if em:
                stats = {}
                for k, v in re.findall(r'STATKEY_(\w+)\s*=\s*(-?\d+)', em.group(1)):
                    if k in STAT_ABBR:
                        stats[STAT_ABBR[k]] = int(v)
                if stats:
                    BUFF_RAW.setdefault(cur, {}).setdefault('stats', stats)

def fmt_duration(d):
    d = d.strip()
    m = re.match(r'(\d+)\s*MINUTES', d)
    if m:
        n = int(m.group(1)); return f"{n} minute" + ('s' if n != 1 else '')
    m = re.match(r'(\d+)\s*SECONDS', d)
    if m:
        n = int(m.group(1)); return f"{n} second" + ('s' if n != 1 else '')
    m = re.match(r'(\d+)$', d)
    if m:
        n = int(m.group(1)) // 10; return f"{n} second" + ('s' if n != 1 else '')
    return d

def resolve_buff(path):
    if not path or not path.startswith('/datum/status_effect/buff'):
        return None
    stats = BUFF_RAW.get(path, {}).get('stats')
    dur = BUFF_RAW.get(path, {}).get('duration')
    pp = path
    while (not stats or not dur) and pp.count('/') > 3:
        pp = pp.rsplit('/', 1)[0]
        info = BUFF_RAW.get(pp, {})
        stats = stats or info.get('stats')
        dur = dur or info.get('duration')
    if not stats:
        return None
    parts = [(f"+{v}" if v > 0 else str(v)) + f" {k}" for k, v in stats.items()]
    out = ", ".join(parts)
    if dur:
        out += " for " + fmt_duration(dur)
    return out

def result_effect(path):
    outs = []
    for fld in ('eat_effect', 'extra_eat_effect'):
        ev = resolve(path, fld)
        if ev:
            s = resolve_buff(ev.strip())
            if s and s not in outs:
                outs.append(s)
    return "; ".join(outs) if outs else None

FARE_LABEL = {
    'FARE_IMPOVERISHED': ('impoverished', 'imp'),
    'FARE_POOR': ('poor', 'poor'),
    'FARE_NEUTRAL': ('neutral', 'neutral'),
    'FARE_FINE': ('fine', 'fine'),
    'FARE_LAVISH': ('lavish', 'lavish'),
}

def result_fare(path):
    f = resolve(path, 'faretype')
    if f and f.strip() in FARE_LABEL:
        return FARE_LABEL[f.strip()][1]
    return None

# ---------------------------------------------------------------------------
# 2. DMI SPRITE EXTRACTION (correct grid slicing)
# ---------------------------------------------------------------------------

def read_dmi_meta(path: str):
    try:
        data = Path(path).read_bytes()
    except:
        return None
    if not data.startswith(b'\x89PNG\r\n\x1a\n'):
        return None
    off = 8
    while off < len(data):
        try:
            ln = struct.unpack('>I', data[off:off+4])[0]
            typ = data[off+4:off+8]
            chunk = data[off+8:off+8+ln]
            if typ == b'zTXt':
                kw, rest = chunk.split(b'\x00', 1)
                if kw == b'Description':
                    return zlib.decompress(rest[1:]).decode('latin1', 'ignore')
            elif typ == b'tEXt':
                kw, rest = chunk.split(b'\x00', 1)
                if kw == b'Description':
                    return rest.decode('latin1', 'ignore')
            off += 12 + ln
        except:
            break
    return None

_DMI_CACHE = {}

def dmi_layout(dmi_path: str):
    """Return (width,height, ordered list of (state_name, cell_count))."""
    if dmi_path in _DMI_CACHE:
        return _DMI_CACHE[dmi_path]
    meta = read_dmi_meta(dmi_path)
    if not meta:
        _DMI_CACHE[dmi_path] = None
        return None
    w = h = 32
    states = []
    cur = None
    dirs = frames = 1
    def flush():
        if cur is not None:
            states.append([cur, max(1, dirs) * max(1, frames)])
    for line in meta.split('\n'):
        s = line.strip()
        if s.startswith('width'):
            w = int(s.split('=')[1])
        elif s.startswith('height'):
            h = int(s.split('=')[1])
        elif s.startswith('state'):
            flush()
            mm = re.search(r'"((?:[^"\\]|\\.)*)"', s)
            cur = mm.group(1) if mm else ''
            cur = cur.replace('\\"', '"')
            dirs = frames = 1
        elif s.startswith('dirs'):
            dirs = int(s.split('=')[1])
        elif s.startswith('frames'):
            frames = int(s.split('=')[1])
    flush()
    res = (w, h, states)
    _DMI_CACHE[dmi_path] = res
    return res

_SPRITE_OUT_CACHE = {}

def extract_sprite(icon_file: str, icon_state: str):
    """Extract sprite -> save PNG under docs/assets/sprites, return relative path or None."""
    if not icon_file:
        return None
    key = f"{icon_file}::{icon_state}"
    if key in _SPRITE_OUT_CACHE:
        return _SPRITE_OUT_CACHE[key]
    dmi_path = ROOT / icon_file
    if not dmi_path.exists():
        _SPRITE_OUT_CACHE[key] = None
        return None
    layout = dmi_layout(str(dmi_path))
    if not layout:
        _SPRITE_OUT_CACHE[key] = None
        return None
    w, h, states = layout
    # find cumulative cell index of the requested state's first cell
    idx = 0
    found = None
    for name, cells in states:
        if name == icon_state:
            found = idx
            break
        idx += cells
    if found is None:
        # try empty-state fallback (first state) if icon_state == ""
        if icon_state == "" and states:
            found = 0
        else:
            _SPRITE_OUT_CACHE[key] = None
            return None
    try:
        from PIL import Image
        if str(dmi_path) not in _IMG_CACHE:
            _IMG_CACHE[str(dmi_path)] = Image.open(dmi_path).convert('RGBA')
        sheet = _IMG_CACHE[str(dmi_path)]
        cols = max(1, sheet.width // w)
        col = found % cols
        row = found // cols
        box = (col*w, row*h, col*w + w, row*h + h)
        sprite = sheet.crop(box)
        # name file by hash
        hsh = hashlib.md5(key.encode()).hexdigest()[:16]
        out = SPRITES / f"{hsh}.png"
        if not out.exists():
            sprite.save(out, format='PNG')
        rel = f"assets/sprites/{hsh}.png"
        _SPRITE_OUT_CACHE[key] = rel
        return rel
    except Exception:
        _SPRITE_OUT_CACHE[key] = None
        return None

_IMG_CACHE = {}

def sprite_for_type(path: str):
    icon = resolve(path, 'icon')
    state = resolve(path, 'icon_state') or ""
    return extract_sprite(icon, state)

# ---------------------------------------------------------------------------
# 3. RECIPE PARSING
# ---------------------------------------------------------------------------

def grab_block(content, start):
    """Return (vars_text) from a recipe def at index `start` to next col-0 def."""
    nxt = re.search(r'\n/(?:datum|obj)/', content[start:])
    end = start + nxt.start() if nxt else len(content)
    return content[start:end]

def parse_assignments(block):
    """Parse top-level `var = value` (value may span multiple lines if in parens)."""
    out = {}
    i = 0
    lines = block.split('\n')
    # join continuation lines where parens are unbalanced
    merged = []
    buf = ''
    depth = 0
    for ln in lines:
        if buf:
            buf += ' ' + ln.strip()
        else:
            buf = ln
        # count only THIS line's delta (not the whole accumulating buffer)
        depth += ln.count('(') - ln.count(')')
        if depth <= 0:
            merged.append(buf)
            buf = ''
            depth = 0
    if buf:
        merged.append(buf)
    for ln in merged:
        m = re.match(r'\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*(.+)$', ln)
        if m:
            out[m.group(1)] = strip_comment(m.group(2))
    return out

def parse_list_pairs(val):
    """Parse list(a = b, c, list(d,e) = f) -> list of (key, qty_or_None)."""
    val = val.strip()
    if not val.startswith('list('):
        # single path
        return [(val.strip(), None)] if val and val != 'list()' else []
    inner = val[5:]
    # strip trailing ) matching
    # find matching close
    depth = 1; i = 0
    while i < len(inner) and depth:
        if inner[i] == '(':
            depth += 1
        elif inner[i] == ')':
            depth -= 1
        i += 1
    inner = inner[:i-1]
    # split top-level commas
    parts = []
    depth = 0; cur = ''
    for c in inner:
        if c in '([': depth += 1
        elif c in ')]': depth -= 1
        if c == ',' and depth == 0:
            parts.append(cur); cur = ''
        else:
            cur += c
    if cur.strip():
        parts.append(cur)
    pairs = []
    for p in parts:
        p = p.strip()
        if not p:
            continue
        # split on top-level '='
        depth = 0; eq = -1
        for j, c in enumerate(p):
            if c in '([': depth += 1
            elif c in ')]': depth -= 1
            elif c == '=' and depth == 0:
                eq = j; break
        if eq >= 0:
            key = p[:eq].strip()
            qty = p[eq+1:].strip()
        else:
            key = p; qty = None
        pairs.append((key, qty))
    return pairs

# resolved global recipe collection
RECIPES = []
SEEN = set()  # avoid dupes

COOKSTEP_TOOL = 'COOKSTEP_TOOL'

def ref(path):
    """Build a {name, sprite} ref for a type path (or reagent)."""
    name = nice_name(path)
    spr = sprite_for_type(path)
    return {'name': name, 'sprite': spr, 'path': path}

def fmt_qty(qty):
    if qty is None:
        return None
    q = qty.strip()
    if q in ('COOKSTEP_TOOL',):
        return 'tool'
    # reagent unit quantities are plain ints; item counts too
    if re.fullmatch(r'\d+', q):
        return q
    return None

def add_food_recipe(typ, v):
    name = unquote(v.get('name', '')) or nice_name(typ)
    # Hidden recipes are intermediate prep steps (e.g. butterdough). Keep them
    # so their output is listed, traceable and linkable — just mark them.
    intermediate = v.get('hidden', '').strip() == 'TRUE'
    base = v.get('base_item')
    bases = []
    if base:
        if base.strip().startswith('list('):
            for k, _ in parse_list_pairs(base):
                bases.append(ref(k))
        else:
            bases.append(ref(base.strip()))
    steps = []
    ing = v.get('ingredients')
    if ing:
        for k, qty in parse_list_pairs(ing):
            if k == 'COOKSTEP_SHARP':
                steps.append({'kind': 'sharp', 'label': 'Score it with any sharp tool'})
                continue
            if k.startswith('list('):
                opts = [ref(o) for o, _ in parse_list_pairs(k)]
                steps.append({'kind': 'anyof', 'options': opts})
                continue
            r = ref(k)
            if qty and qty.strip() == 'COOKSTEP_TOOL':
                r['verb'] = 'Use'
                r['note'] = 'tool (not consumed)'
            elif '/datum/reagent' in k and qty and re.fullmatch(r'\d+', qty.strip()):
                r['verb'] = 'Add'
                r['note'] = f"{qty.strip()} units"
            else:
                r['verb'] = 'Add'
            steps.append({'kind': 'item', 'ref': r})
    cook = None
    cm = v.get('cook_method', '')
    cmap = {'COOK_BAKE': 'Bake it in an oven',
            'COOK_FRY': 'Fry it in a pan over a hearth',
            'COOK_DEEPFRY': 'Deep-fry it in a pot of hot oil',
            'COOK_BOIL': 'Boil it in a pot of water'}
    if cm.strip() in cmap:
        cook = cmap[cm.strip()]
    elif v.get('needs_cooking', '').strip() == 'TRUE':
        cook = 'Cook it over a hearth or in an oven'
    result = v.get('result_type')
    res = ref(result.strip()) if result else None
    amt = v.get('result_amount', '1').strip()
    RECIPES.append({
        'name': name, 'category': 'Cooking', 'bases': bases,
        'steps': steps, 'cook': cook, 'result': res, 'amount': amt,
        'desc': '', 'intermediate': intermediate,
    })

def add_brewing_recipe(typ, v):
    name = unquote(v.get('name', '')) or nice_name(typ)
    desc = unquote(v.get('bottle_desc', ''))
    ings = []
    for field in ('needed_crops', 'needed_items'):
        if field in v:
            for k, qty in parse_list_pairs(v[field]):
                r = ref(k)
                r['note'] = (qty.strip() + '×') if qty and re.fullmatch(r'\d+', qty.strip() or '') else None
                ings.append(r)
    reags = []
    if 'needed_reagents' in v:
        for k, qty in parse_list_pairs(v['needed_reagents']):
            r = ref(k)
            r['note'] = (qty.strip() + 'u') if qty and re.fullmatch(r'\d+', (qty or '').strip()) else None
            reags.append(r)
    result = v.get('output_bottle_type') or v.get('reagent_to_brew')
    res = ref(result.strip()) if result else None
    if res and v.get('bottle_name'):
        res['name'] = unquote(v['bottle_name'])
    btime = v.get('brew_time', '').replace('MINUTES', 'min').replace('SECONDS', 'sec').strip()
    RECIPES.append({
        'name': name, 'category': 'Brewing', 'bases': [],
        'ingredients_flat': ings + reags,
        'result': res, 'desc': desc, 'brew_time': btime,
        'steps': [], 'cook': None, 'amount': v.get('brewed_amount', '').strip(),
    })

def add_crafting_cooking(typ, v):
    # /datum/crafting_recipe/roguetown/cooking/*
    name = unquote(v.get('name', '')) or nice_name(typ)
    if v.get('hides_from_books', '').strip() == 'TRUE':
        return
    ings = []
    if 'reqs' in v:
        for k, qty in parse_list_pairs(v['reqs']):
            r = ref(k)
            r['note'] = (qty.strip() + '×') if qty and re.fullmatch(r'\d+', (qty or '').strip()) else None
            ings.append(r)
    result = v.get('result')
    res = ref(result.strip()) if result else None
    if res and ispath_clothing(result):
        return  # skip non-food cosmetic outputs
    RECIPES.append({
        'name': name, 'category': 'Prepared (slapcraft)', 'bases': [],
        'ingredients_flat': ings, 'result': res, 'desc': '',
        'steps': [], 'cook': None, 'amount': '1',
    })

def ispath_clothing(p):
    return p and '/obj/item/clothing' in p

def add_stew_recipe(typ, v):
    # Stews: boil a pot of water, then add any ONE of the listed inputs to
    # produce the `output` reagent. inputs = list(path, path, ...)
    output = v.get('output')
    res = ref(output.strip()) if output else None
    name = unquote(v.get('name', ''))
    if not name:
        name = (res['name'].title() if res else nice_name(typ).title())
    ings = []
    if 'inputs' in v:
        for k, _ in parse_list_pairs(v['inputs']):
            if k.startswith('list('):
                for o, _ in parse_list_pairs(k):
                    ings.append(ref(o))
            else:
                ings.append(ref(k))
    if not ings and not res:
        return
    RECIPES.append({
        'name': name, 'category': 'Stew', 'bases': [],
        'ingredients_flat': ings, 'result': res, 'desc': '',
        'any_of': True,
        'steps': [], 'cook': 'Boil a pot of water, then add any one ingredient below',
        'amount': '1',
    })

# Inheritable food_recipe vars (a child recipe inherits these from its
# abstract parent if it does not set them itself).
FOOD_INHERIT = ('base_item', 'cook_method', 'needs_cooking', 'result_amount')

def resolve_recipe_var(typ, field, food_vars):
    p = typ
    while p.count('/') > 2:
        p = p.rsplit('/', 1)[0]
        if p in food_vars and field in food_vars[p]:
            return food_vars[p][field]
        if p == '/datum/food_recipe':
            break
    return None

def parse_recipes():
    targets = []
    for p in ROOT.rglob('*.dm'):
        if '.git' in p.parts:
            continue
        s = str(p)
        if any(x in s for x in ['recipe', 'cooking', 'brewing', 'stew']):
            targets.append(p)
    food_vars = {}  # every /datum/food_recipe/* (incl. abstract parents)
    for p in targets:
        try:
            content = p.read_text(encoding='utf-8', errors='ignore')
        except:
            continue
        for m in re.finditer(r'^(/datum/[a-zA-Z0-9_/]+)\s*$', content, re.MULTILINE):
            typ = m.group(1)
            block = grab_block(content, m.start())
            v = parse_assignments(block)
            key = typ
            if typ.startswith('/datum/food_recipe/'):
                # remember vars for inheritance; emit in a later pass
                if typ not in food_vars:
                    food_vars[typ] = v
                continue
            if key in SEEN:
                continue
            if typ.startswith('/datum/brewing_recipe/') and ('output_bottle_type' in v or 'reagent_to_brew' in v):
                SEEN.add(key); add_brewing_recipe(typ, v)
            elif typ.startswith('/datum/crafting_recipe/roguetown/cooking/') and 'result' in v:
                SEEN.add(key); add_crafting_cooking(typ, v)
            elif typ.startswith('/datum/stew_recipe/') and ('inputs' in v or 'output' in v):
                SEEN.add(key); add_stew_recipe(typ, v)

    # Second pass: emit concrete food recipes, resolving inherited vars.
    for typ, v in food_vars.items():
        if 'abstract_type' in v:           # abstract parent, not a real recipe
            continue
        if 'result_type' not in v:         # a listable dish always yields something
            continue
        merged = dict(v)
        for fld in FOOD_INHERIT:
            if fld not in merged:
                val = resolve_recipe_var(typ, fld, food_vars)
                if val is not None:
                    merged[fld] = val
        if typ in SEEN:
            continue
        SEEN.add(typ); add_food_recipe(typ, merged)

# ---- "Preparation" recipes: mill / slice / roast item transforms ----------
# Many base ingredients (flour, butter slices, roasted beans, toast) are not
# made by a recipe datum but by transforming a raw item. We surface one for
# every makeable ingredient that's referenced anywhere, recursing until the
# chain bottoms out at a growable/importable item with no producer.
TRANSFORMS = [
    ('mill_result', 'Mill'),
    ('slice_path', 'Cut'),
    ('boiled_type', 'Boil'),
    ('deep_fried_type', 'Deep-fry'),
    ('fried_type', 'Fry'),
    ('cooked_type', 'Bake'),
]
REVERSE = {}  # result_path -> (verb, source_path, slices_num|None)

def build_reverse_index():
    for path, info in TYPES.items():
        if not path.startswith('/obj/item/reagent_containers'):
            continue
        for var, verb in TRANSFORMS:
            tgt = info.get(var)
            if not tgt or not tgt.startswith('/'):
                continue
            tgt = tgt.strip()
            if tgt == path or tgt in REVERSE:
                continue
            sl = info.get('slices_num') if var == 'slice_path' else None
            REVERSE[tgt] = (verb, path, sl)

def _collect_referenced():
    refs = set()
    def add(r):
        if r and r.get('path'):
            refs.add(r['path'])
    for rec in RECIPES:
        for b in rec.get('bases', []):
            add(b)
        for s in rec.get('steps', []):
            if s.get('ref'):
                add(s['ref'])
            for o in s.get('options', []):
                add(o)
        for i in rec.get('ingredients_flat', []):
            add(i)
    return refs

def add_preparation_recipes():
    from collections import deque
    build_reverse_index()
    produced = {rec['result']['path'] for rec in RECIPES
                if rec.get('result') and rec['result'].get('path')}
    queue = deque(p for p in _collect_referenced() if p not in produced)
    done = set()
    while queue:
        p = queue.popleft()
        if p in done or p in produced or p.startswith('/datum/reagent'):
            continue
        done.add(p)
        rev = REVERSE.get(p)
        if not rev:
            continue  # raw growable / importable item — chain ends here
        verb, src, sl = rev
        slc = sl.strip() if (sl and re.fullmatch(r'\d+', str(sl).strip())) else None
        res = ref(p)
        RECIPES.append({
            'name': res['name'], 'category': 'Preparation',
            'bases': [ref(src)], 'steps': [], 'cook': None,
            'result': res, 'amount': '1', 'desc': '',
            'prep_verb': verb, 'slices': slc, 'intermediate': False,
        })
        produced.add(p)
        queue.append(src)  # recurse so the source is itself traceable

# ---------------------------------------------------------------------------
# 4. SITE GENERATION
# ---------------------------------------------------------------------------

def _esc(s):
    return (s or '').replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

# item_path -> recipe id of the recipe that produces it (set in build_producers)
PRODUCERS = {}

def _ing(ref, self_id=None):
    """Render an ingredient. If it is itself produced by a recipe, make it a
    clickable link carrying that recipe's id (for the hover tooltip)."""
    if isinstance(ref, str):
        return f'<span class="ing">{_esc(ref)}</span>'
    name = _esc(ref.get('name', ''))
    pid = PRODUCERS.get(ref.get('path'))
    if pid is not None and pid != self_id:
        return f'<span class="ing link" data-make="{pid}">{name}</span>'
    return f'<span class="ing">{name}</span>'

def build_instruction(r):
    """Natural-language instruction HTML, screenshot-style."""
    cat = r['category']
    sid = r.get('id')
    if cat == 'Preparation':
        base = r['bases'][0] if r.get('bases') else None
        bl = _ing(base, sid) if base else 'a raw item'
        verb = r.get('prep_verb', 'Prepare')
        if verb == 'Cut' and r.get('slices'):
            return f"Cut {bl} (yields {r['slices']} per item)."
        return f"{verb} {bl}."
    if cat == 'Cooking':
        items, tools, anyofs, sharp = [], [], [], False
        for s in r.get('steps', []):
            if s['kind'] == 'sharp':
                sharp = True
            elif s['kind'] == 'anyof':
                anyofs.append(" or ".join(_ing(o, sid) for o in s['options']))
            else:
                x = s['ref']
                if x.get('note') == 'tool (not consumed)':
                    tools.append(_ing(x, sid))
                elif x.get('note') and 'units' in x['note']:
                    items.append(f"{x['note'].replace(' units','')}dr of {_ing(x, sid)}")
                else:
                    items.append("1 " + _ing(x, sid))
        base_txt = ""
        if r.get('bases'):
            bnames = [_ing(b, sid) for b in r['bases']]
            base_txt = (" to " if items else " ") + (" or ".join(bnames) if len(bnames) > 1 else bnames[0])
        sent = ""
        addbits = items + anyofs
        if addbits:
            sent = "Add " + ", ".join(addbits) + base_txt
        elif r.get('bases'):
            sent = "Start with " + (" or ".join(_ing(b, sid) for b in r['bases']))
        if tools:
            sent += " using " + ", ".join(tools)
        if sharp:
            sent += (", scoring it with a sharp tool" if sent else "Score it with a sharp tool")
        sent = (sent or "Prepare") + "."
        if r.get('cook'):
            sent += " " + r['cook'] + "."
        return sent
    if cat == 'Brewing':
        ings = []
        for i in r.get('ingredients_flat', []):
            if i['name'].lower() == 'water':
                continue
            note = i.get('note')
            label = (note + " " if note else "") + _ing(i, sid)
            ings.append(label.strip())
        sent = "Ferment " + ", ".join(ings) + " with water in a barrel." if ings else "Ferment in a barrel."
        extra = []
        if r.get('amount'):
            extra.append(f"yields {r['amount']} bottles")
        if r.get('brew_time'):
            extra.append(f"after {r['brew_time']}")
        if extra:
            sent += " (" + ", ".join(extra) + ")"
        return sent
    if cat == 'Stew':
        opts = [_ing(i, sid) for i in r.get('ingredients_flat', [])]
        if len(opts) > 6:
            shown = ", ".join(opts[:6]) + f", or {len(opts)-6} more"
        else:
            shown = " or ".join(opts) if len(opts) <= 2 else ", ".join(opts[:-1]) + ", or " + opts[-1]
        return "Boil a pot of water, then add any one of: " + shown + "."
    # slapcraft / prepared
    ings = []
    for i in r.get('ingredients_flat', []):
        note = i.get('note')
        ings.append((note + " " if note else "") + _ing(i, sid))
    return "Combine " + ", ".join(ings) + "." if ings else "Prepare at a table."

def build_producers():
    for r in RECIPES:
        res = r.get('result')
        if res and res.get('path'):
            PRODUCERS.setdefault(res['path'], r['id'])

def enrich():
    # assign stable ids, map item -> producing recipe, then build text
    for i, r in enumerate(RECIPES):
        r['id'] = i
    build_producers()
    for r in RECIPES:
        res = r.get('result')
        if res and res.get('path'):
            r['fare'] = result_fare(res['path'])
            r['effect'] = result_effect(res['path'])
        else:
            r['fare'] = None
            r['effect'] = None
        r['instr'] = build_instruction(r)

def main():
    print('[*] Building type index (3596 dm files)...')
    build_type_index()
    print(f'    indexed {len(TYPES)} type definitions')
    print('[*] Indexing eat-effect buffs...')
    index_buffs()
    print(f'    indexed {len(BUFF_RAW)} buff definitions')
    SPRITES.mkdir(parents=True, exist_ok=True)
    print('[*] Parsing recipes...')
    parse_recipes()
    n_direct = len(RECIPES)
    print(f'    parsed {n_direct} direct recipes')
    print('[*] Tracing makeable base ingredients (mill/slice/roast)...')
    add_preparation_recipes()
    print(f'    added {len(RECIPES) - n_direct} preparation recipes')
    enrich()
    print(f'    total {len(RECIPES)} recipes')
    by = defaultdict(int)
    for r in RECIPES:
        by[r['category']] += 1
    for k in sorted(by):
        print(f'      {k}: {by[k]}')
    spr_count = len(list(SPRITES.glob('*.png')))
    print(f'[*] Extracted {spr_count} sprites')
    # dump JSON for the page
    (DOCS / 'recipes.json').write_text(json.dumps(RECIPES, ensure_ascii=False))
    print('[+] wrote docs/recipes.json')
    write_site()
    print('[+] wrote docs/index.html')


CAT_ORDER = ['Cooking', 'Preparation', 'Prepared (slapcraft)', 'Stew', 'Brewing']

def write_site():
    order = {c: i for i, c in enumerate(CAT_ORDER)}
    recipes_sorted = sorted(RECIPES, key=lambda r: (order.get(r['category'], 99), r['name'].lower()))
    cats = sorted({r['category'] for r in RECIPES}, key=lambda c: order.get(c, 99))
    data_json = json.dumps(recipes_sorted, ensure_ascii=False)
    cat_counts = {c: sum(1 for r in RECIPES if r['category'] == c) for c in cats}
    (DOCS / 'index.html').write_text(PAGE_TEMPLATE
        .replace('/*DATA*/', data_json)
        .replace('/*TOTAL*/', str(len(RECIPES)))
        .replace('/*CATS*/', json.dumps([{'name': c, 'count': cat_counts[c]} for c in cats])),
        encoding='utf-8')


PAGE_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Encyclopaedia Azurea — Recipe Compendium</title>
<style>
  :root{ --bg:#1b2230; --bg2:#1f2736; --line:#2c3647; --gold:#d9b35c; --gold2:#f0d896;
         --text:#dfe5ee; --muted:#8693a6; --ing:#6fb4e6; --fine:#7ec46b; --poor:#e07a6b;
         --neutral:#e2c15a; --lavish:#6bd0e0; --imp:#9aa3b0; --stat:#5aa9e6; }
  *{box-sizing:border-box}
  body{margin:0;font-family:'Iowan Old Style','Palatino Linotype',Georgia,serif;
       background:var(--bg);color:var(--text);font-size:16px}
  img{image-rendering:pixelated}
  header{padding:30px 16px 20px;text-align:center;background:linear-gradient(180deg,#222c3d,#1b2230);
         border-bottom:2px solid var(--line)}
  header h1{margin:0;font-size:2.2em;color:var(--gold2);letter-spacing:1px;text-shadow:0 2px 6px #000}
  header p{margin:7px 0 0;color:var(--muted);font-style:italic}
  .wrap{max-width:1240px;margin:0 auto;padding:16px}
  .controls{position:sticky;top:0;z-index:5;background:var(--bg);padding:12px 0;border-bottom:1px solid var(--line)}
  #q{width:100%;padding:11px 14px;font-size:16px;background:#141a25;border:1px solid var(--line);
     border-radius:8px;color:var(--text);font-family:inherit}
  #q:focus{outline:none;border-color:var(--gold)}
  .cats{display:flex;flex-wrap:wrap;gap:8px;margin-top:10px}
  .cat{padding:6px 13px;background:#222c3d;border:1px solid var(--line);border-radius:18px;color:var(--text);
       cursor:pointer;font-family:inherit;font-size:13px}
  .cat:hover{border-color:var(--gold);color:var(--gold2)}
  .cat.on{background:var(--gold);border-color:var(--gold);color:#1b2230;font-weight:bold}
  .count{color:var(--muted);font-size:13px;margin:10px 2px}
  h2.section{font-variant:small-caps;letter-spacing:2px;color:var(--gold2);font-size:1.7em;
     margin:34px 0 6px;padding-bottom:6px;border-bottom:2px solid var(--line);font-weight:600}
  .sub{color:var(--muted);font-style:italic;margin:0 0 6px;font-size:.92em}
  table{width:100%;border-collapse:collapse}
  tr.r{border-bottom:1px solid var(--line)}
  tr.r:hover{background:#222c3d66}
  td{padding:14px 12px;vertical-align:middle}
  td.name{width:230px}
  td.eff{width:230px;color:var(--text);font-size:.95em;text-align:right}
  .nm{display:flex;align-items:center;gap:11px}
  .nm img{width:40px;height:40px;flex:0 0 40px;background:#0e131c;border-radius:6px;padding:3px}
  .nm .ph{width:40px;height:40px;display:inline-flex;align-items:center;justify-content:center;
          background:#0e131c;border-radius:6px;color:#3a4658;flex:0 0 40px}
  .title{font-style:italic;font-size:1.05em;line-height:1.2}
  .title.fine{color:var(--fine)} .title.poor{color:var(--poor)} .title.neutral{color:var(--neutral)}
  .title.lavish{color:var(--lavish)} .title.imp{color:var(--imp)} .title.none{color:var(--text)}
  .interm{display:inline-block;margin-left:7px;font-size:.66em;color:var(--muted);border:1px solid var(--line);
    border-radius:8px;padding:1px 7px;text-transform:uppercase;letter-spacing:.5px;vertical-align:middle;font-style:normal}
  .instr{line-height:1.5}
  .ing{color:var(--ing)}
  .ing.link{cursor:pointer;border-bottom:1px dotted currentColor}
  .ing.link:hover{color:#9fd0ff}
  #tip{position:fixed;z-index:50;max-width:360px;background:#0e131c;border:1px solid var(--gold);
       border-radius:8px;padding:10px 12px;box-shadow:0 8px 26px rgba(0,0,0,.6);font-size:.92em;
       pointer-events:none;display:none}
  #tip .tt-h{color:var(--gold2);font-style:italic;font-weight:bold;margin-bottom:4px}
  #tip .tt-l{color:var(--muted);font-size:.8em;text-transform:uppercase;letter-spacing:.5px;margin-bottom:2px}
  #tip .tt-b{color:var(--text);line-height:1.45}
  #tip .tt-e{margin-top:6px;color:var(--text)}
  tr.flash{animation:fl 1.7s ease}
  @keyframes fl{0%,100%{background:transparent}18%{background:#d9b35c40}}
  .meta{color:var(--muted);font-size:.85em;margin-top:3px}
  .eff .s{color:var(--stat);font-weight:bold}
  .eff .dash{color:var(--muted)}
  .empty{text-align:center;color:var(--muted);padding:50px}
  footer{text-align:center;color:#55606f;padding:30px;font-size:.85em}
  @media(max-width:760px){td.eff,td.name{width:auto}.controls{position:static}}
</style>
</head>
<body>
<header>
  <h1>&#9884; Encyclopaedia Azurea &#9884;</h1>
  <p>Food &amp; Drink Recipe Compendium &mdash; every dish, brew &amp; stew of Azure-Peak</p>
</header>
<div class="wrap">
  <div class="controls">
    <input id="q" type="text" placeholder="&#128269;  Search by dish, ingredient or effect&hellip;" autocomplete="off">
    <div class="cats" id="cats"></div>
  </div>
  <div class="count" id="count"></div>
  <div id="out"></div>
</div>
<footer>Generated from Azure-Peak source &bull; <span id="t"></span> recipes &bull; sprites &amp; effects extracted from in-game data</footer>
<script>
const RECIPES = /*DATA*/;
const CATS = /*CATS*/;
const TOTAL = /*TOTAL*/;
const SUBTITLES = {
  "Cooking":"Combine a base item with ingredients at a table, then cook where noted.",
  "Preparation":"Mill, slice or roast a raw item into a base ingredient used by other recipes.",
  "Prepared (slapcraft)":"Combine items by hand or at a table — no cooking station required.",
  "Stew":"Boil a pot of water, then drop in any one listed ingredient.",
  "Brewing":"Ferment crops with water in a barrel; many improve with age."
};
document.getElementById('t').textContent = TOTAL;
let curCat='All', curQ='';

function esc(s){return (s||'').replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));}
function effHTML(e){
  if(!e) return '<span class="dash">&mdash;</span>';
  // color +N STAT tokens
  return esc(e).replace(/([+\-]\d+)\s+([A-Z]{2,3})/g,'<b>$1 <span class="s">$2</span></b>');
}
function rowHTML(r){
  const rs=r.result;
  const img = rs && rs.sprite ? `<img src="${rs.sprite}" onerror="this.outerHTML='&lt;span class=&quot;ph&quot;&gt;&#9634;&lt;/span&gt;'" alt="">` : '<span class="ph">&#9634;</span>';
  const fare = r.fare||'none';
  let meta='';
  if(r.brew_time) meta = `<div class="meta">Brew time ${esc(r.brew_time)}${r.amount?` &middot; yields ${esc(r.amount)}`:''}</div>`;
  return `<tr class="r" data-cat="${r.category}" data-id="${r.id}">
    <td class="name"><div class="nm">${img}<span class="title ${fare}">${esc(r.name)}</span>${r.intermediate?'<span class="interm">prep step</span>':''}</div></td>
    <td><div class="instr">${r.instr||''}</div>${meta}</td>
    <td class="eff">${effHTML(r.effect)}</td>
  </tr>`;
}
function render(){
  const out=document.getElementById('out');
  let html='', n=0;
  for(const cat of (curCat==='All'?CATS.map(c=>c.name):[curCat])){
    const rows=RECIPES.filter(r=>r.category===cat && (!curQ || r._s.includes(curQ)));
    if(!rows.length) continue;
    n+=rows.length;
    html+=`<h2 class="section">${esc(cat)} Recipes</h2>`;
    if(SUBTITLES[cat]) html+=`<p class="sub">${SUBTITLES[cat]}</p>`;
    html+='<table><tbody>'+rows.map(rowHTML).join('')+'</tbody></table>';
  }
  out.innerHTML = n? html : '<div class="empty">No recipes match your search.</div>';
  document.getElementById('count').textContent = `Showing ${n} of ${TOTAL} recipes`;
}
function buildSearch(r){
  let t=r.name+' '+r.category+' '+(r.instr||'').replace(/<[^>]+>/g,'')+' '+(r.effect||'');
  if(r.result)t+=' '+r.result.name;
  return t.toLowerCase();
}
RECIPES.forEach(r=>r._s=buildSearch(r));
function buildCats(){
  const c=document.getElementById('cats');
  const mk=(name,count)=>{const b=document.createElement('button');b.className='cat'+(name==='All'?' on':'');
    b.textContent=count!=null?`${name} (${count})`:name;b.dataset.cat=name;
    b.onclick=()=>{curCat=name;[...c.children].forEach(x=>x.classList.toggle('on',x.dataset.cat===name));render();};return b;};
  c.appendChild(mk('All',TOTAL));
  for(const ct of CATS) c.appendChild(mk(ct.name,ct.count));
}
document.getElementById('q').addEventListener('input',e=>{curQ=e.target.value.toLowerCase().trim();render();});

// ---- clickable predecessor ingredients + hover tooltip --------------------
const BYID={}; RECIPES.forEach(r=>BYID[r.id]=r);
const out=document.getElementById('out');
const tip=document.createElement('div'); tip.id='tip'; document.body.appendChild(tip);
function showTip(el){
  const r=BYID[+el.dataset.make]; if(!r) return;
  tip.innerHTML=`<div class="tt-l">How to make</div><div class="tt-h">${esc(r.name)}</div>`+
                `<div class="tt-b">${r.instr||''}</div>`+
                (r.effect?`<div class="tt-e">${effHTML(r.effect)}</div>`:'');
  tip.style.display='block';
}
function moveTip(e){const pad=14;let x=e.clientX+pad,y=e.clientY+pad;
  const w=tip.offsetWidth,h=tip.offsetHeight;
  if(x+w>innerWidth)x=e.clientX-w-pad; if(y+h>innerHeight)y=e.clientY-h-pad;
  tip.style.left=Math.max(4,x)+'px'; tip.style.top=Math.max(4,y)+'px';}
out.addEventListener('mouseover',e=>{const el=e.target.closest('.ing.link'); if(el){showTip(el);moveTip(e);}});
out.addEventListener('mousemove',e=>{if(tip.style.display==='block')moveTip(e);});
out.addEventListener('mouseout',e=>{if(e.target.closest('.ing.link'))tip.style.display='none';});
out.addEventListener('click',e=>{
  const el=e.target.closest('.ing.link'); if(!el)return;
  const id=+el.dataset.make; if(!BYID[id])return;
  tip.style.display='none'; curCat='All'; curQ='';
  document.getElementById('q').value='';
  [...document.getElementById('cats').children].forEach(x=>x.classList.toggle('on',x.dataset.cat==='All'));
  render();
  const row=document.querySelector(`tr[data-id="${id}"]`);
  if(row){row.scrollIntoView({behavior:'smooth',block:'center'});
          row.classList.add('flash'); setTimeout(()=>row.classList.remove('flash'),1700);}
});

buildCats();render();
</script>
</body>
</html>"""


if __name__ == "__main__":
    main()
