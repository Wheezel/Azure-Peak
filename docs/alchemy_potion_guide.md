# Alchemy & Potion Guide — Cheapest Recipe for Every Brew

*A complete reference for every alchemical product, optimized for **lowest cost**:
foraged herbs, free butchering scraps, and cheap dusts wherever possible. Values
are from `code/modules/roguetown/roguecrafting/alchemy/`.*

---

## The one trick that makes this cheap

The cauldron scores every recipe from the ingredients you add. Each ingredient is
worth **3 pts (major attunement), 2 (medium), or 1 (minor)** toward the recipes
it's tied to. A recipe needs **≥5 points** and must be the **highest** scorer to
brew. (`cauldron.dm`)

> ### 🪙 Foolproof rule: **2 of ONE ingredient = its MAJOR potion, guaranteed.**
> Two copies of a single ingredient give **6 points** to its major recipe, vs only
> 4 to its medium and 2 to its minor. 6 beats both and clears the 5-point floor —
> so you **always** get the major. Throw in 3–4 of the same item for extra safety;
> it still brews the same thing. **Keep the pot pure** — mixing different
> ingredients is what makes you brew the wrong potion.

So to make any potion cheaply: **find the cheapest ingredient whose MAJOR is that
potion, and brew 2–4 of it.** The only exception is **Restoration**, which no
single ingredient majors in — it needs a 2+2 mix (covered below).

### The two stations
1. **Mortar & pestle** — grind raw stuff (herbs, ore, butchered parts, plants) into
   the dusts/powders the cauldron wants. XP scales with INT. (`mortarpestle.dm`)
2. **Cauldron** — boil **90+ drams of water**, drop in your **2–4 ingredients**,
   collect **90 drams** of potion (30 for stat potions).

### Where the cheap stuff comes from
- **Herbs** (the backbone of this guide) — **forage them free** from bushes on the
  map; they regrow. Grind one herb to get its **seed**, then plant it for an endless
  supply. Common herbs are worth only ~4, so even buying is trivial.
- **Butchering** — **middle-click any animal corpse with a knife** (no spell/intent)
  for **free** viscera, sinew, and tail bone. Grind a tail bone → **bonemeal**.
  Troll corpses give **horns**.
- **Cheap dusts** — grind **coal** (→coal dust, ~1), **iron** (→iron dust, 3),
  cheap ore for **earth essentia** (~1) and **air essentia** (4). **Fish** grind into
  **water essentia** for free.
- **Skill gate** — every recipe needs a minimum Alchemy level. As Head Physician you
  start **Master (5)**, so you can brew everything here from minute one.

---

# 🪙 MASTER RECIPE TABLE

**How to read it:** brew **2× of any MAJOR ingredient** (pure pot) to guarantee that
potion. The **🪙 Cheapest** column gives the cheapest viable brew, avoiding fire
essentia and precious (gold/silver) dust wherever possible — some use a **medium
combo** (two different mediums whose own majors point elsewhere, so the shared
medium wins at 8 pts vs 6/6). MAJOR = 3 pts · MEDIUM = 2 · MINOR = 1.

| Potion (effect) | Gate | 🪙 Cheapest brew | MAJOR (3) | MEDIUM (2) | MINOR (1) |
|---|---|---|---|---|---|
| **Elixir of Health** *(heal brute/fire)* | Appr | **2× urtica** (free herb) | symphitum, urtica, valeriana | viscera, taraxacum, tail bone | sinew, calendula, artemisia |
| **Health (Strong)** | Jour | **2× calendula** or viscera (free) | viscera, calendula | — | silver dust |
| **Elixir of Mana** *(+energy)* | Appr | **2× bonemeal** (free butcher) | bonemeal, manabloom powder | berry powder | sleeping powder |
| **Mana (Strong)** | Jour | **2 hypericum + 2 water essentia** (free) | magic dust, gold dust | water essentia, raw essentia, feau dust, mineral dust, hypericum | purified salts, berry powder, manabloom powder |
| **Elixir of Stamina** | Appr | **2× hypericum** (free herb) | hypericum | seed dust, air essentia, westleach dust, benedictus | mentha, urtica |
| **Stamina (Strong)** | Jour | **2× seed dust** (~free) | seed dust, ozium, benedictus | — | — |
| **Antidote** *(cure poison)* | Appr | **2× purified salts** (no metal) | coal dust, purified salts | briar essence, rosa | viscera, bonemeal, symphitum, taraxacum, hypericum |
| **Antidote (Strong)** | Jour | **2× tail bone** (free butcher) | silver dust, tail bone | purified salts | seed dust, feau dust |
| **Elixir of Restoration** *(heal+energy)* | Exp | **1 silver + 1 gold + 1 rosa** *(only way)* | — *(none)* | silver dust, gold dust | rosa |
| **Keen Mind** *(INT +3)* | Exp | **2× water essentia** (free fish) | water essentia, raw essentia | mentha, solar dust, manabloom powder | air essentia, ozium, euphrasia, benedictus, infernal dust |
| **Keen Eye** *(PER +3)* | Exp | **2× mentha** (free herb) | westleach dust, mentha | bonemeal, matricaria | water essentia, raw essentia, gold dust, solar dust |
| **Enduring Fortitude** *(WIL +3)* | Exp | **2 calendula + 2 sinew** (free) | iron dust | coal dust, magic dust, sinew, earth essentia, calendula | swampweed dust, troll horn, salvia |
| **Stone Flesh** *(CON +3)* | Exp | **2× salvia** (free herb) | earth essentia, salvia | fire essentia, iron dust, troll horn | magic dust, tail bone |
| **Fleet Foot** *(SPD +3)* | Exp | **2× euphrasia** (free herb) | air essentia, feau dust, euphrasia | urtica, artemisia, valeriana | westleach dust |
| **Seven Clovers** *(LCK +3)* | Exp | **2× artemisia** or rosa (free) | artemisia, rosa | sleeping powder, ozium | briar essence |
| **Mountain Muscles** *(STR +3)* | Exp | **2× troll horn** (free butcher) | fire essentia, troll horn | salvia | coal dust, iron dust, earth essentia |
| **Fire Warding** *(15-min fire immunity)* | Mast | **2× solar dust** (grind sunflower) | infernal dust, solar dust | — | fire essentia |
| **Poison (Berry)** *(incap)* | Jour | **2× matricaria** (free herb) | swampweed dust, berry powder, matricaria | atropa, paris | — |
| **Poison (Doom)** *(lethal)* | Exp | **2× atropa** (rare herb) | mineral dust, atropa | — | matricaria |
| **Stamina Poison** *(drain)* | Jour | **2× taraxacum** or sinew (free) | sinew, taraxacum | symphitum, euphrasia | atropa, paris, valeriana |
| **Stamina Poison (Strong)** | Exp | **2× paris** (uncommon herb) | paris | swampweed dust, infernal dust | mineral dust |
| **Sleep Poison** *(sedate)* | Mast | **2× briar essence** or sleeping powder | sleeping powder, briar essence | — | — |

**The four "medium-combo / free" tricks** (avoid fire essentia & gold/silver dust):
- **Mana (Strong)** = 2 hypericum + 2 water essentia → big-mana **8** vs Stamina 6 / Keen Mind 6. *(or just 2× gold/magic dust if you have them)*
- **Enduring Fortitude** = 2 calendula + 2 sinew → Fortitude **8** vs Strong Health 6 / Stamina Poison 6. *(replaces iron dust)*
- **Antidote** = 2 purified salts (grind salt). *Avoid 2 rosa + 2 briar essence — it ties LCK and brews unreliably.* Coal dust (~1) also works.
- **Mountain Muscles** = 2 troll horn (butcher a troll) → STR **6** vs CON 4. *(the only non-fire-essentia route; salvia can't win, its CON major dominates)*

**The one unavoidable cost — Restoration:** only silver dust (med), gold dust (med),
and rosa (minor) touch it, so you **must** use both metals. Cheapest is **1 silver +
1 gold + 1 rosa = exactly 5 pts** (beats Strong Antidote / Strong Mana / Seven Clovers
at 3 each). No herb-only version exists.

## Fixed-recipe specials (table craft, not the cauldron point system)

| Item | Effect | Ingredients (exact) | Gate |
|---|---|---|---|
| **Quicksilver Poultice** | cures lesser werewolves / vampires | 1 bloodied fyritius + 45u blessed water + 1 cloth + 1 silver dust | Master (craftdiff 4) |
| **Absolving Silver** *(lux variant)* | stronger cure poultice | same as above | Transmutation (craftdiff 0) |
| **Rot Cure Potion** | cures zombie/deadite infection (10u ≈ 2 people) | 1 alchemical bottle + 1 fyritius + 2 filled heartblood vials + 2 viscera | Master (craftdiff 5) |
| **Pure essentia** (magic dust) | crafting reagent | 1 each water + fire + air + earth essentia | on a table |
| **Feau dust** | crafting reagent | 2 iron dust + 1 gold dust | on a table |

*Bloodied fyritius:* grow a fyritius, then **hit a bleeding transformed werewolf or
any bleeding vampire with it** (5-sec channel) to soak their cursed blood. Inquisitors
can drench it from a cursed-blood indexer instead.

---

# THE POTIONS — details & effects

*Per-tick effects while the reagent metabolizes. Healing potions self-purge above
60u to stop over-healing.*

## Healing

### Elixir of Health — `healthpot`  ·  Apprentice
- 🪙 **Cheapest:** 2× **urtica** or **valeriana** (free foraged common herbs). *Also
  major in symphitum.*
- **Effect:** −1.75 brute & fire, −1.25 oxy per tick; heals 3 wound HP; −5 brain,
  −1.75 cloneloss, −1 eye. Fast, strong everyday heal & best-seller.

### Elixir of Health (Strong) — `stronghealth`  ·  Journeyman
- 🪙 **Cheapest:** 2× **calendula** (free forage) or 2× **viscera** (free butcher).
- **Effect:** −5 brute, −5 fire, −5 oxy per tick; heals 4 wound HP; −5 brain/clone,
  −2.5 eye. Fast burst heal.

### Elixir of Restoration — `restoration`  ·  Expert
- 🪙 **Cheapest:** **2× silver dust + 2× gold dust** (the only multi-ingredient
  recipe; no cheap route).
- **Effect:** −3 brute/fire/oxy **and +60 energy** per tick; heals 3 wound HP. The
  premium "heal + stamina in one."

## Mana & Stamina

### Elixir of Mana — `manapot`  ·  Apprentice
- 🪙 **Cheapest:** 2× **bonemeal** (free: butcher any animal, grind the tail bone).
- **Effect:** +30 energy/tick.

### Elixir of Mana (Strong) — `strongmana`  ·  Journeyman
- 🪙 **Cheapest:** 2× **gold dust**, or 2× **magic dust** (craft from cheap essentia).
- **Effect:** +120 energy/tick — near-instant mana refill.

### Elixir of Stamina — `stampot`  ·  Apprentice
- 🪙 **Cheapest:** 2× **hypericum** (free forage).
- **Effect:** restores ~20 stamina/tick.

### Elixir of Stamina (Strong) — `strongstam`  ·  Journeyman
- 🪙 **Cheapest:** 2× **seed dust** (grind any seeds — practically free). *Also major
  in benedictus and ozium.*
- **Effect:** restores ~50 stamina/tick.

## Antidotes

### Antidote — `antidote`  ·  Apprentice
- 🪙 **Cheapest:** 2× **coal dust** (grind coal, ~1 each).
- **Effect:** −4 toxin/tick **and strips 1u of every harmful reagent/tick**;
  metabolizes very slowly (~15 min/dose) so you can pre-drink it.

### Antidote (Strong) — `strong_antidote`  ·  Journeyman
- 🪙 **Cheapest:** 2× **tail bone** (free butcher). *Silver dust also majors here but
  costs 20.*
- **Effect:** −12 toxin/tick **and strips 3u of every harmful reagent/tick.** Hard
  counter to poisoning.

## Stat Potions — Expert gate, 30 drams

All grant **+3 to one stat while in your system** (reapplies each tick). **Overdose
at 33u** → jitter + 3 toxin/tick. **Don't stack** — a second buff purges the first.

| Potion | Stat | 🪙 Cheapest |
|---|---|---|
| **Keen Mind** | INT +3 | 2× **water essentia** (grind fish, free) |
| **Keen Eye** | PER +3 | 2× **mentha** (forage, free) |
| **Enduring Fortitude** | WIL +3 | 2× **iron dust** (grind iron, ~3) |
| **Stone Flesh** | CON +3 | 2× **earth essentia** (~1) or **salvia** (forage) |
| **Fleet Foot** | SPD +3 | 2× **air essentia** (~4) or **euphrasia** (forage) |
| **Seven Clovers** | LCK +3 | 2× **artemisia** or **rosa** (forage, free) |
| **Mountain Muscles** | STR +3 | 2× **fire essentia** (bonus from grinding coal/iron) or **troll horn** |

> **Physician tip:** brew **Stone Flesh** (CON) — it's nearly free from earth essentia
> and patches your −1 CON. **Keen Mind** (free from fish) boosts skill gain and
> diagnosis numbers.

## Utility

### Potion of Fire Warding — `fire_resist`  ·  Master, 30 drams
- 🪙 **Cheapest:** 2× **solar dust** (grind sunflowers you grow). *Infernal dust also
  majors but needs slain abyssal fangs.*
- **Effect:** grants `TRAIT_FIRE_RESIST` — **15 minutes of fire immunity** per dose.

## Poisons

### Poison (Berry) — `berrypoison`  ·  Journeyman
- 🪙 **Cheapest:** 2× **matricaria** (free forage). *Berry powder & swampweed dust
  also major.*
- **Effect:** +3 nausea, +2 toxin/tick; incapacitates, non-lethal single dose.

### Poison (Doom) — `strongpoison`  ·  Expert
- 🪙 **Cheapest:** 2× **atropa** (forage; rare herb ~10). *Mineral dust from gems is
  the pricier alternative.*
- **Effect:** +6 nausea, +4.5 toxin/tick — **lethal** in a standard dose.

### Stamina Poison — `stampoison`  ·  Journeyman
- 🪙 **Cheapest:** 2× **taraxacum** (free forage) or 2× **sinew** (free butcher).
- **Effect:** −45 energy/tick; exhausts a target.

### Stamina Poison (Strong) — `strongstampoison`  ·  Expert
- 🪙 **Cheapest:** 2× **paris** (forage; uncommon ~6).
- **Effect:** −180 energy/tick — drops stamina near-instantly.

### Sleep Poison — `sleep_powder`  ·  Master
- 🪙 **Cheapest:** 2× **briar essence** (grind rosa petals — rosa is a free common
  herb), or 2× **sleeping powder** (grind zizo-bane, foraged free in rot/blight areas).
- **Effect:** knocks a target out. **Your in-house surgical sedative** — see the
  surgery guide. *(Dosing people is antagonistic; keep it to legitimate use on a
  `min_pq 3` whitelist role.)*

---

## Your "free clinic" shopping list

Everything below costs **0 coin** — just foraging, fishing, and butchering:

- **Forage common herbs:** urtica/valeriana (Health), hypericum (Stamina), mentha
  (Keen Eye), artemisia/rosa (Seven Clovers + Sleep via petals), salvia (Stone
  Flesh), taraxacum (Stamina Poison), matricaria (Berry Poison), calendula (Strong
  Health).
- **Butcher animals:** tail bone → grind to **bonemeal** (Mana) or use whole (Strong
  Antidote); **viscera** (Strong Health); **sinew** (Stamina Poison).
- **Fish:** grind to **water essentia** (Keen Mind).
- **Grind coal:** **coal dust** (Antidote) + bonus **fire essentia** (→ Mountain
  Muscles). Grind iron for **iron dust** (Enduring Fortitude) + bonus fire essentia.

The only potions that truly cost money are **Restoration** and **Strong Mana**
(precious metals), and the rarer poisons — everything else a physician needs is
free off the land.

### Source files
`alch_cauldron_recipes.dm`, `alch_grind_recipes.dm`, `ingredients.dm`,
`cauldron.dm`, `mortarpestle.dm`, `potionbuffs.dm`, reagent effects in `reagents.dm`;
prices in `code/__DEFINES/economy/pricing_defines.dm`.
