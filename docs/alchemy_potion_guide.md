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

# 🪙 CHEAPEST RECIPE — MASTER TABLE

*Brew 2–4 of the listed ingredient (pure pot) unless it says "mix".*

| Potion | Cheapest recipe | Source | Cost | Gate |
|---|---|---|---|---|
| **Elixir of Health** | 2× **urtica** *(or valeriana)* | forage (common herb) | free | Apprentice |
| **Health (Strong)** | 2× **calendula** *(or viscera)* | forage / butcher | free | Journeyman |
| **Elixir of Mana** | 2× **bonemeal** | butcher → grind tail bone | free | Apprentice |
| **Mana (Strong)** | 2× **gold dust** | grind gold *(see note)* | ~precious | Journeyman |
| **Elixir of Stamina** | 2× **hypericum** | forage | free | Apprentice |
| **Stamina (Strong)** | 2× **seed dust** | grind any seeds | ~free | Journeyman |
| **Antidote** | 2× **coal dust** | grind coal | ~1 ea | Apprentice |
| **Antidote (Strong)** | 2× **tail bone** | butcher animal | free | Journeyman |
| **Elixir of Restoration** | **2× silver dust + 2× gold dust** *(mix)* | grind precious | expensive | Expert |
| **Keen Mind** (INT) | 2× **water essentia** | grind fish | free | Expert |
| **Keen Eye** (PER) | 2× **mentha** | forage | free | Expert |
| **Enduring Fortitude** (WIL) | 2× **iron dust** | grind iron | ~3 ea | Expert |
| **Stone Flesh** (CON) | 2× **earth essentia** *(or salvia)* | grind cheap ore / forage | ~1 ea | Expert |
| **Fleet Foot** (SPD) | 2× **air essentia** *(or euphrasia)* | grind / forage | ~4 | Expert |
| **Seven Clovers** (LCK) | 2× **artemisia** *(or rosa)* | forage | free | Expert |
| **Mountain Muscles** (STR) | 2× **fire essentia** *(or troll horn)* | grind fyritius / butcher troll | see note | Expert |
| **Fire Warding** | 2× **solar dust** | grind sunflower | grow | Master |
| **Poison (Berry)** | 2× **matricaria** | forage | free | Journeyman |
| **Poison (Doom)** | 2× **atropa** | forage (rare herb) | ~10 | Expert |
| **Stamina Poison** | 2× **taraxacum** *(or sinew)* | forage / butcher | free | Journeyman |
| **Stamina Poison (Strong)** | 2× **paris** | forage (uncommon herb) | ~6 | Expert |
| **Sleep Poison** | 2× **briar essence** *(or sleeping powder)* | grind rosa petals / forage zizo-bane | free | Master |

**Notes on the few non-free ones:**
- **Strong Mana** has no cheap major — gold dust (≈15) or magic dust (≈8) are the
  options. Magic dust is **crafted** from 1 each of water+fire+air+earth dust on a
  table, so if you're already grinding cheap essentia you can make it for near-free
  in effort, just slowly.
- **Restoration** is the only potion with **no major ingredient at all**. Use **2
  silver dust + 2 gold dust**: that scores Restoration 8 (each is medium) vs Strong
  Antidote 6 and Strong Mana 6, so Restoration wins. It's intentionally the premium
  heal — there is no budget version.
- **Mountain Muscles (STR)** needs **fire essentia** or a **troll horn**. Fire
  essentia drops as a **bonus 25% of the time when you grind coal or iron**, so
  stockpile it passively while making Antidote/Fortitude, then brew STR for free.

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
