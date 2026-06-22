# Encyclopaedia Azurea — Recipe Compendium

A self-contained, searchable recipe guide for Azure-Peak's food & drink,
served as a GitHub Pages site. The page itself is **`docs/index.html`**.

Open `docs/index.html` in a browser, or visit the published Pages URL once
Pages is enabled (see below).

## What it shows

For every dish, brew and stew (~420 recipes) the page lists, in a table:

- the **result sprite** and its name, coloured by fare quality
  (fine / neutral / poor / lavish / impoverished);
- a plain-language **instruction** — e.g. *"Add 1 sausage to a bun."* — with
  ingredients highlighted;
- the **buff** it grants when eaten — e.g. *"+1 CON, +1 WIL for 10 minutes"*.

Recipes are grouped into **Cooking**, **Prepared (slapcraft)**, **Stew** and
**Brewing**, with a search box and category filters.

## Regenerating

The whole site is generated from the game's `.dm` source:

```bash
pip install Pillow
python3 build_recipe_site.py
```

This re-reads every recipe, resolves item/reagent names and sprites (honouring
BYOND path inheritance and `modular/` overrides), parses eat-effect buffs into
stat/duration text, extracts the sprites from the `.dmi` files, and rewrites
`docs/index.html`, `docs/recipes.json` and `docs/assets/sprites/`.

## Enabling GitHub Pages

This repo already serves Pages from the `docs/` folder (note `docs/.nojekyll`).
In **Settings → Pages**, set the source branch and the `/docs` folder; the
compendium is the site's `index.html`.
