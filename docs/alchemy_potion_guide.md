# Alchemy & Potion Guide — Cheapest Recipe for Every Brew

*A complete reference for every alchemical product, optimized for **lowest cost**:
foraged herbs, free butchering scraps, and cheap dusts wherever possible. Values
are from `code/modules/roguetown/roguecrafting/alchemy/`.*

---

## How the cauldron scores

The cauldron scores every recipe from the ingredients you add. Each ingredient is
worth **3 pts (major attunement), 2 (medium), or 1 (minor)** toward the recipes
it's tied to. A recipe needs **≥5 points** and must be the **strict highest**
scorer to brew. (`cauldron.dm`)

> ### ⚠️ Hard rule: **NO DUPLICATES — up to 4 *different* ingredients only.**
> The cauldron **rejects a second ingredient of the same type** ("There is already
> one in the cauldron! That would ruin the mixture!" — `cauldron.dm:145`). So you
> can't "stack 2× urtica." You reach the 5-point floor by combining **different**
> ingredients that share your target: two different **majors** = 6, a **major + a
> medium** = 5, or **three mediums** = 6, etc.

So to make a potion cheaply: **combine the cheapest *distinct* ingredients that each
list your target (as major/medium/minor) until you clear 5 — and make sure no rival
recipe ties it.** Ties (two recipes at the same top score) brew unreliably, so a few
recipes need a 3rd ingredient to break a tie (flagged below).

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

**How to read it:** every recipe is **distinct ingredients only** (no duplicates).
The **🪙 Cheapest** column gives a verified combo that clears 5 pts and wins outright,
favoring the apothecary's herbs and free scraps. MAJOR = 3 pts · MEDIUM = 2 · MINOR = 1.
The last three columns list **every** ingredient attuned to that potion so you can
build your own distinct combo.

| Potion (effect) | Gate | 🪙 Cheapest brew (distinct) | MAJOR (3) | MEDIUM (2) | MINOR (1) |
|---|---|---|---|---|---|
| **Elixir of Health** *(heal brute/fire)* | Appr | **symphitum + urtica** | symphitum, urtica, valeriana | viscera, taraxacum, tail bone | sinew, calendula, artemisia |
| **Health (Strong)** | Jour | **viscera + calendula** | viscera, calendula | — | silver dust |
| **Elixir of Mana** *(+energy)* | Appr | **bonemeal + berry powder** | bonemeal, manabloom powder | berry powder | sleeping powder |
| **Mana (Strong)** | Jour | **hypericum + water essentia + purified salts** *(no metal; or swap salts → berry powder)* | magic dust, gold dust | water essentia, raw essentia, feau dust, mineral dust, hypericum | purified salts, berry powder, manabloom powder |
| **Elixir of Stamina** | Appr | **hypericum + benedictus** | hypericum | seed dust, air essentia, westleach dust, benedictus | mentha, urtica |
| **Stamina (Strong)** | Jour | **seed dust + benedictus** | seed dust, ozium, benedictus | — | — |
| **Antidote** *(cure poison)* | Appr | **briar essence + rosa + viscera** | coal dust, purified salts | briar essence, rosa | viscera, bonemeal, symphitum, taraxacum, hypericum |
| **Antidote (Strong)** | Jour | **tail bone + purified salts** | silver dust, tail bone | purified salts | seed dust, feau dust |
| **Elixir of Restoration** *(heal+energy)* | Exp | **silver dust + gold dust + rosa** | — *(none)* | silver dust, gold dust | rosa |
| **Keen Mind** *(INT +3)* | Exp | **water essentia + mentha** | water essentia, raw essentia | mentha, solar dust, manabloom powder | air essentia, ozium, euphrasia, benedictus, infernal dust |
| **Keen Eye** *(PER +3)* | Exp | **mentha + matricaria** | westleach dust, mentha | bonemeal, matricaria | water essentia, raw essentia, gold dust, solar dust |
| **Enduring Fortitude** *(WIL +3)* | Exp | **iron dust + calendula** *(no-metal: calendula + sinew + coal dust)* | iron dust | coal dust, magic dust, sinew, earth essentia, calendula | swampweed dust, troll horn, salvia |
| **Stone Flesh** *(CON +3)* | Exp | **salvia + earth essentia** *(or salvia + iron dust)* | earth essentia, salvia | fire essentia, iron dust, troll horn | magic dust, tail bone |
| **Fleet Foot** *(SPD +3)* | Exp | **euphrasia + urtica** | air essentia, feau dust, euphrasia | urtica, artemisia, valeriana | westleach dust |
| **Seven Clovers** *(LCK +3)* | Exp | **artemisia + rosa** | artemisia, rosa | sleeping powder, ozium | briar essence |
| **Mountain Muscles** *(STR +3)* | Exp | **troll horn + salvia + coal dust** *(or fire essentia + troll horn)* | fire essentia, troll horn | salvia | coal dust, iron dust, earth essentia |
| **Fire Warding** *(15-min fire immunity)* | Mast | **solar dust + infernal dust** | infernal dust, solar dust | — | fire essentia |
| **Poison (Berry)** *(incap)* | Jour | **matricaria + atropa** *(or matricaria + berry powder)* | swampweed dust, berry powder, matricaria | atropa, paris | — |
| **Poison (Doom)** *(lethal)* | Exp | **atropa + mineral dust** | mineral dust, atropa | — | matricaria |
| **Stamina Poison** *(drain)* | Jour | **taraxacum + euphrasia** | sinew, taraxacum | symphitum, euphrasia | atropa, paris, valeriana |
| **Stamina Poison (Strong)** | Exp | **paris + infernal dust** *(or paris + swampweed dust + mineral dust)* | paris | swampweed dust, infernal dust | mineral dust |
| **Sleep Poison** *(sedate)* | Mast | **sleeping powder + briar essence** | sleeping powder, briar essence | — | — |

**Tie traps (these LOOK valid but brew unreliably — a rival ties the score):**
- **STR:** ~~troll horn + salvia~~ ties CON 5-5 → add **coal dust** (STR 6 vs CON 5).
- **Stamina Poison:** ~~taraxacum + symphitum~~ ties Health 5-5 → use **taraxacum + euphrasia**.
- **Strong Stam Poison:** ~~paris + swampweed dust~~ ties Berry Poison 5-5 → use **paris + infernal dust** (or add mineral dust).

**Recipes that have no herb-only / cheap route:**
- **Restoration** — only silver (med), gold (med), rosa (minor) exist; **must** use both metals. *silver + gold + rosa = 5.*
- **Doom Poison** — needs **atropa + mineral dust** (a gem); you can't double atropa.
- **Fire Warding** — needs **both** solar **and** infernal dust (one minor can't reach 5).

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

> **⚠️ Recipes below: use the MASTER RECIPE TABLE above.** The per-entry "🪙 Cheapest"
> notes in this section predate the no-duplicate fix and may say "2× X" — that does
> **not** work (the cauldron rejects duplicate ingredients). Trust the master table's
> distinct-ingredient combos.

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
