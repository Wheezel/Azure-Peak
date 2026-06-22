# 🗿 Encyclopaedia Azurea: Recipe Compendium

A comprehensive, searchable HTML guide to all food, drink, and crafting recipes in Azure-Peak.

## Overview

- **643 recipes** extracted from source code
- **6 categories**: Cooking, Brewing, Stews, Alchemy (Grinding), Alchemy (Cauldron), Crafting
- **Searchable interface** with category filters
- **Self-contained HTML file** (~526 KB) — no external dependencies or server required
- **Automatically generated** from BYOND DM source code

## Usage

### View the Compendium

1. Open `recipe_compendium.html` in any web browser
2. Search by recipe name, ingredient, or result
3. Filter by category (Cooking, Brewing, Stews, Alchemy, Crafting)
4. Click "View Source" to see the raw recipe definition

### Regenerate (if recipes change)

```bash
python3 extract_recipes.py
```

This re-parses all `.dm` recipe files and regenerates `recipe_compendium.html`.

## What's Included

### By Category

| Category | Count | Source |
|---|---|---|
| **Cooking** | 248 | `/datum/food_recipe` (new system) |
| **Stews** | 111 | `/datum/stew_recipe` |
| **Brewing** | 42 | `/datum/brewing_recipe` (wine, beer, spirits) |
| **Alchemy (Grinding)** | 52 | `/datum/alch_grind_recipe` |
| **Alchemy (Cauldron)** | 23 | `/datum/alch_cauldron_recipe` |
| **Crafting** | 167 | `/datum/crafting_recipe` |
| **TOTAL** | **643** | |

### Recipe Information

Each recipe card displays:

- **Recipe Name** — The in-game display name
- **Category** — Which type of crafting (Cooking, Brewing, etc.)
- **Description** — Flavor text or mechanical notes
- **Result** — What item(s) the recipe produces
- **Ingredients** — Up to 10 listed ingredients (see "View Source" for full details)
- **Source** — Link to the DM file and raw variable definitions

## Technical Details

### Extraction Process

1. **Scan** — Find all `.dm` files in recipe-related directories
2. **Parse** — Use regex + BYOND DM syntax analysis to extract recipe definitions
3. **Extract** — Pull key fields (name, ingredients, results, descriptions)
4. **Render** — Generate searchable HTML with CSS styling and JavaScript interactivity

### Supported Recipe Types

- `food_recipe` — Modern cooking system (most food items)
- `crafting_recipe/roguetown/cooking` — Slapcrafting (special prep recipes)
- `brewing_recipe` — Fermented drinks (wine, beer, spirits, tea)
- `stew_recipe` — Stew-specific recipes
- `alch_grind_recipe` — Alchemical grinding (powders, extracts)
- `alch_cauldron_recipe` — Alchemical brewing (potions)

### Known Limitations

- Some recipes may show "Unknown Recipe" if the `name` variable is defined procedurally
- Ingredient lists are simplified (first 10 displayed; full list in source view)
- Sprites are not yet embedded (future enhancement)
- This is a *snapshot* of recipes at extraction time; live changes require regeneration

## Architecture

```
extract_recipes.py
├─ find_recipe_files()          # Locate all recipe .dm files
├─ extract_recipes_from_file()  # Parse BYOND syntax
├─ extract_recipe_details()     # Pull name, ingredients, results
├─ generate_recipe_card()       # Build HTML for one recipe
└─ main()                        # Generate final HTML with styling & JS
```

### Key Functions

- **`parse_dm_list(s)`** — Parse BYOND `list(...)` syntax into Python list
- **`clean_dm_value(s)`** — Normalize DM type paths and quoted strings
- **`extract_recipes_from_file(path)`** — Regex-based DM parsing
- **`extract_recipe_details(recipe)`** — Map raw vars to card display format

## Future Enhancements

- [ ] Embed PNG sprites from DMI files for visual reference
- [ ] Add clickable links between recipes (ingredient → producer recipe)
- [ ] Include crafting difficulty, time estimates, skill requirements
- [ ] Export as JSON for tool integration
- [ ] Dependency tree visualization (raw → cooked → final dish)
- [ ] Filter by ingredient availability (growable/tradable/found only)

## Contributing

To improve the compendium:

1. Update recipe definitions in the source `.dm` files
2. Run `python3 extract_recipes.py`
3. Commit both the script changes and the updated `recipe_compendium.html`

---

Generated from Azure-Peak source code. Last updated: 2026-06-22.
