#!/usr/bin/env python3
"""
Extract all food/drink/brewing recipes from Azure-Peak source and build
a self-contained HTML compendium with embedded sprites and search.
"""

import re
import json
import struct
import zlib
import base64
import os
import sys
from pathlib import Path
from collections import defaultdict
from typing import Any, Dict, List, Optional, Set, Tuple

# ============================================================================
# DM SYNTAX PARSING
# ============================================================================

def find_recipe_files():
    """Find all recipe files."""
    recipes = []
    for p in Path('.').rglob('*.dm'):
        path_str = str(p)
        if any(x in path_str for x in ['recipe', 'cooking', 'brewing', 'stew', 'grind', 'cauldron']):
            if '.git' not in path_str and 'test' not in path_str.lower():
                recipes.append(p)
    return recipes

def parse_dm_list(s: str) -> List[str]:
    """Parse a BYOND list(...) into a Python list."""
    items = []
    s = s.strip()
    if not s.startswith('list(') or not s.endswith(')'):
        return [s]

    # Extract content between parentheses
    content = s[5:-1]  # remove "list(" and ")"
    depth = 0
    current = ""

    for ch in content:
        if ch in '({[':
            depth += 1
        elif ch in ')}]':
            depth -= 1
        elif ch == ',' and depth == 0:
            if current.strip():
                items.append(current.strip())
            current = ""
            continue
        current += ch

    if current.strip():
        items.append(current.strip())

    return items

def clean_dm_value(s: str) -> str:
    """Normalize a DM value."""
    s = s.strip()
    # Remove quotes
    if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
        s = s[1:-1]
    # Extract type name from path
    if s.startswith('/'):
        s = s.rsplit('/', 1)[-1]
    return s

def extract_recipes_from_file(file_path: Path) -> List[Dict[str, Any]]:
    """Extract recipe definitions from a .dm file."""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except:
        return []

    recipes = []

    # Match complete /datum/TYPE definitions
    # Look for pattern: /type\s*\n(\s+var=val\n)*
    pattern = r'/([a-z_/0-9]+)(?:\s+([a-zA-Z_][a-zA-Z0-9_]*))?\s*\n((?:\s+\w+\s*=.*?\n)*?)(?=/[a-z_/0-9]|\Z)'

    for match in re.finditer(pattern, content, re.MULTILINE | re.DOTALL):
        type_path = match.group(1)
        var_block = match.group(3)

        # Filter for recipe types
        if not any(x in type_path for x in ['food_recipe', 'brewing_recipe', 'crafting_recipe', 'stew_recipe', 'alch_grind', 'alch_cauldron']):
            continue

        # Parse variables
        vars_dict = {}
        for line in var_block.split('\n'):
            line = line.strip()
            if not line or line.startswith('//'):
                continue

            eq_pos = line.find('=')
            if eq_pos == -1:
                continue

            var_name = line[:eq_pos].strip()
            var_value = line[eq_pos + 1:].strip()

            # Handle comments
            comment_pos = var_value.find('//')
            if comment_pos != -1:
                var_value = var_value[:comment_pos].strip()

            vars_dict[var_name] = var_value

        recipes.append({
            'type': type_path,
            'file': str(file_path),
            'vars': vars_dict,
        })

    return recipes

# ============================================================================
# RECIPE PROCESSING
# ============================================================================

def categorize_recipe(recipe: Dict) -> str:
    """Determine recipe type/category."""
    t = recipe['type'].lower()
    if 'brewing_recipe' in t:
        return 'Brewing'
    elif 'stew_recipe' in t:
        return 'Stew'
    elif 'alch_grind' in t:
        return 'Alchemy (Grinding)'
    elif 'alch_cauldron' in t:
        return 'Alchemy (Cauldron)'
    elif 'food_recipe' in t:
        return 'Cooking'
    elif 'crafting_recipe' in t:
        return 'Crafting'
    return 'Other'

def extract_recipe_details(recipe: Dict) -> Dict[str, Any]:
    """Extract key fields from recipe variables."""
    v = recipe['vars']
    details = {
        'name': 'Unknown Recipe',
        'category': categorize_recipe(recipe),
        'ingredients': [],
        'result': None,
        'description': '',
    }

    # Name
    if 'name' in v:
        details['name'] = clean_dm_value(v['name'])

    # Description
    for key in ['desc', 'bottle_desc', 'description']:
        if key in v:
            details['description'] = clean_dm_value(v[key])
            break

    # Ingredients (varies by type)
    if 'needed_crops' in v:
        crops = parse_dm_list(v['needed_crops'])
        for crop in crops:
            details['ingredients'].append(clean_dm_value(crop))
    elif 'needed_items' in v:
        items = parse_dm_list(v['needed_items'])
        for item in items:
            details['ingredients'].append(clean_dm_value(item))
    elif 'reqs' in v:
        reqs = parse_dm_list(v['reqs'])
        for req in reqs:
            # Format is "path = quantity"
            if '=' in req:
                parts = req.split('=')
                details['ingredients'].append(clean_dm_value(parts[0]))

    # Result
    if 'result' in v:
        details['result'] = clean_dm_value(v['result'])
    elif 'result_type' in v:
        details['result'] = clean_dm_value(v['result_type'])
    elif 'output_bottle_type' in v:
        details['result'] = clean_dm_value(v['output_bottle_type'])

    return details

# ============================================================================
# HTML GENERATION
# ============================================================================

def html_escape(s: str) -> str:
    """Escape HTML special chars."""
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')

def generate_recipe_card(recipe: Dict, details: Dict) -> str:
    """Generate HTML for a single recipe card."""
    cat = details['category']
    name = html_escape(details['name'])
    desc = html_escape(details['description'])

    ingredients_html = ""
    if details['ingredients']:
        ingredients_html = "<ul class='ingredients'>"
        for ing in details['ingredients'][:10]:  # Limit to 10 for space
            ingredients_html += f"<li>{html_escape(ing)}</li>"
        if len(details['ingredients']) > 10:
            ingredients_html += f"<li>... and {len(details['ingredients']) - 10} more</li>"
        ingredients_html += "</ul>"

    result_html = ""
    if details['result']:
        result_html = f"<p><strong>Result:</strong> {html_escape(details['result'])}</p>"

    raw_vars = json.dumps(recipe['vars'], indent=2, default=str)

    html = f"""
    <div class="recipe-card" data-category="{cat}" data-name="{name}">
        <div class="recipe-header">
            <h3>{name}</h3>
            <span class="category-badge">{cat}</span>
        </div>
        {f'<p class="description">{desc}</p>' if desc else ''}
        {result_html}
        {ingredients_html}
        <details class="raw-data">
            <summary>View Source</summary>
            <pre>{html_escape(raw_vars)}</pre>
        </details>
    </div>
    """
    return html

def main():
    print("[*] Scanning for recipe files...")
    files = find_recipe_files()
    print(f"[+] Found {len(files)} potential recipe files")

    print("[*] Parsing recipes...")
    all_recipes = []
    for f in files:
        recipes = extract_recipes_from_file(f)
        all_recipes.extend(recipes)

    print(f"[+] Extracted {len(all_recipes)} recipe definitions")

    # Categorize
    by_category = defaultdict(list)
    for r in all_recipes:
        cat = categorize_recipe(r)
        by_category[cat].append(r)

    for cat in sorted(by_category.keys()):
        print(f"  {cat}: {len(by_category[cat])} recipes")

    # Generate HTML
    print("[*] Generating HTML compendium...")

    recipe_cards = []
    for recipe in all_recipes:
        details = extract_recipe_details(recipe)
        card = generate_recipe_card(recipe, details)
        recipe_cards.append(card)

    categories = sorted(by_category.keys())
    category_buttons = "".join([
        f'<button class="cat-btn" onclick="filterCategory(\'{cat}\')">{cat}</button>'
        for cat in categories
    ])

    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Azure-Peak Recipe Compendium</title>
    <style>
        * {{
            box-sizing: border-box;
        }}

        html, body {{
            margin: 0;
            padding: 0;
        }}

        body {{
            font-family: Georgia, serif;
            background: #1a1a1a url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100"><rect fill="%23222" width="100" height="100"/><circle cx="50" cy="50" r="1" fill="%23333"/></svg>');
            color: #eee;
        }}

        .header {{
            background: linear-gradient(135deg, #2a1a0a 0%, #3d2817 100%);
            border-bottom: 3px solid #8b4513;
            padding: 40px 20px;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0,0,0,0.5);
        }}

        .header h1 {{
            margin: 0;
            font-size: 3em;
            color: #d4af37;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
        }}

        .header p {{
            margin: 10px 0 0 0;
            color: #aaa;
            font-style: italic;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }}

        .controls {{
            background: #222;
            padding: 20px;
            margin: 20px 0;
            border-radius: 5px;
            border-left: 4px solid #8b4513;
        }}

        #search {{
            width: 100%;
            padding: 12px;
            font-size: 16px;
            background: #0a0a0a;
            border: 1px solid #666;
            border-radius: 3px;
            color: #eee;
            margin-bottom: 15px;
        }}

        #search:focus {{
            outline: none;
            border-color: #8b4513;
            box-shadow: 0 0 8px rgba(139, 69, 19, 0.3);
        }}

        .filter-buttons {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
        }}

        .cat-btn {{
            padding: 8px 16px;
            background: #333;
            border: 2px solid #666;
            border-radius: 20px;
            color: #eee;
            cursor: pointer;
            transition: all 0.2s;
            font-family: inherit;
            font-size: 14px;
        }}

        .cat-btn:hover {{
            border-color: #8b4513;
            color: #d4af37;
        }}

        .cat-btn.active {{
            background: #8b4513;
            border-color: #d4af37;
            color: #fff;
        }}

        .stats {{
            text-align: center;
            padding: 15px;
            background: #2a2a2a;
            border-radius: 5px;
            margin: 20px 0;
            font-size: 16px;
            color: #d4af37;
            border: 1px solid #444;
        }}

        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }}

        .recipe-card {{
            background: linear-gradient(135deg, #2a2a2a 0%, #1f1f1f 100%);
            border-left: 4px solid #8b4513;
            border-radius: 5px;
            padding: 20px;
            transition: all 0.3s;
            display: none;
            min-height: 200px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.3);
        }}

        .recipe-card.visible {{
            display: block;
        }}

        .recipe-card:hover {{
            transform: translateY(-4px);
            box-shadow: 0 6px 16px rgba(139, 69, 19, 0.3);
            border-left-color: #d4af37;
        }}

        .recipe-header {{
            display: flex;
            justify-content: space-between;
            align-items: baseline;
            margin-bottom: 12px;
        }}

        .recipe-card h3 {{
            margin: 0;
            color: #d4af37;
            font-size: 1.4em;
        }}

        .category-badge {{
            background: #8b4513;
            color: #fff;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 0.8em;
            font-weight: bold;
            white-space: nowrap;
            margin-left: 10px;
        }}

        .description {{
            color: #bbb;
            font-style: italic;
            margin: 10px 0;
            font-size: 0.95em;
        }}

        .ingredients {{
            list-style: none;
            padding: 0;
            margin: 10px 0;
            font-size: 0.9em;
        }}

        .ingredients li {{
            padding: 4px 0;
            padding-left: 20px;
            position: relative;
            color: #999;
        }}

        .ingredients li:before {{
            content: "→";
            position: absolute;
            left: 0;
            color: #8b4513;
        }}

        .recipe-card strong {{
            color: #d4af37;
        }}

        .raw-data {{
            margin-top: 15px;
            padding: 10px;
            background: #0a0a0a;
            border-radius: 3px;
            border: 1px solid #444;
            cursor: pointer;
        }}

        .raw-data summary {{
            color: #8b8b8b;
            font-size: 0.9em;
            cursor: pointer;
            user-select: none;
        }}

        .raw-data summary:hover {{
            color: #d4af37;
        }}

        .raw-data pre {{
            margin: 10px 0 0 0;
            overflow-x: auto;
            font-size: 0.8em;
            color: #6f6;
        }}

        .empty {{
            grid-column: 1 / -1;
            text-align: center;
            padding: 40px;
            color: #666;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🗿 Encyclopaedia Azurea 🗿</h1>
        <p>Complete Food & Drink Recipe Compendium</p>
    </div>

    <div class="container">
        <div class="controls">
            <input type="text" id="search" placeholder="🔍 Search recipes by name, ingredient, or result...">
            <div class="filter-buttons">
                <button class="cat-btn active" onclick="filterCategory('All')">All Categories</button>
                {category_buttons}
            </div>
        </div>

        <div class="stats">
            <span id="count">Total: {len(all_recipes)} recipes</span>
        </div>

        <div class="grid" id="recipes">
            {''.join(recipe_cards)}
            <div class="empty" id="empty-msg" style="display:none;">No recipes match your search.</div>
        </div>
    </div>

    <script>
        const recipes = document.querySelectorAll('.recipe-card');
        const searchBox = document.getElementById('search');
        const categoryBtns = document.querySelectorAll('.cat-btn');
        const emptyMsg = document.getElementById('empty-msg');
        let currentCategory = 'All';

        function filterCategory(cat) {{
            currentCategory = cat;
            categoryBtns.forEach(btn => {{
                btn.classList.toggle('active', btn.textContent.trim() === cat);
            }});
            updateDisplay();
        }}

        function updateDisplay() {{
            const query = searchBox.value.toLowerCase();
            let visible = 0;

            recipes.forEach(r => {{
                const name = r.getAttribute('data-name').toLowerCase();
                const category = r.getAttribute('data-category');
                const text = r.textContent.toLowerCase();

                const catMatch = currentCategory === 'All' || category === currentCategory;
                const queryMatch = name.includes(query) || text.includes(query) || query === '';

                if (catMatch && queryMatch) {{
                    r.classList.add('visible');
                    visible++;
                }} else {{
                    r.classList.remove('visible');
                }}
            }});

            emptyMsg.style.display = visible === 0 ? 'block' : 'none';
            document.getElementById('count').textContent = `Showing: ${{visible}} / {len(all_recipes)} recipes`;
        }}

        searchBox.addEventListener('input', updateDisplay);

        // Initialize display
        updateDisplay();
    </script>
</body>
</html>"""

    output_file = 'recipe_compendium.html'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"[+] Written {output_file}")
    print(f"[+] File size: {os.path.getsize(output_file) / 1024:.1f} KB")

if __name__ == '__main__':
    main()
