# Alchemy & Potion Guide — Every Brew in the Game

*A complete reference for every alchemical product you can make: how the cauldron
works, exactly which ingredients to throw in, where those ingredients come from,
and what each potion does mechanically. Values are pulled straight from the code
(`code/modules/roguetown/roguecrafting/alchemy/`).*

---

## How alchemy actually works

There are two stations, used in sequence:

### 1. Mortar & Pestle — make your dusts/powders
Put a raw item in the mortar, click with the pestle. This **grinds** raw materials
(ores, gems, herbs, butchered parts, plants) into the **dusts and powders** that
the cauldron actually wants. Middle-click prioritizes juicing. XP per grind scales
with your INT (`STAINT`). Many grinds have a **bonus-output roll** for a second
item. (`mortarpestle.dm`, `alch_grind_recipes.dm`)

### 2. Cauldron — brew the potion
1. Boil **at least 90 drams of water** in a cauldron.
2. Drop in **up to 4 ingredients**.
3. The cauldron scores every possible recipe: each ingredient is worth **3 points
   (major attunement), 2 points (medium), or 1 point (minor)** toward the recipes
   it's tied to.
4. **If no recipe reaches 5 points, you get nothing** ("Yuck"). Otherwise it brews
   the **highest-scoring** recipe. Output is normally **90 drams** of reagent (30
   for stat potions). (`cauldron.dm`, `alch_cauldron_recipe_base.dm`)

**Practical rule:** two "major" ingredients for the same potion (3+3 = 6 ≥ 5) is
enough to guarantee it. Four of one major ingredient (12 points) makes it
impossible to accidentally brew something else. **Mixing different ingredients
risks brewing the wrong recipe** — keep your pot pure unless you know the math.

**Skill gates:** every recipe needs a minimum **Alchemy** level or it simply won't
mix. As Head Physician you start at **Master (5)**, so the only thing you *can't*
make round-start is anything gated at Legendary (none of the below are) — you can
brew literally every recipe in this guide from minute one.

**Smelling:** examine an ingredient and (with enough Alchemy/PER+INT) it tells you
what it "smells of" — that smell **is** the recipe it's attuned to. With
`TRAIT_LEGENDARY_ALCHEMIST` (Legendary alchemy) it names the potion outright.

---

## The master ingredient → potion table

Each ingredient points at up to three recipes. **MAJOR = 3 pts, med = 2, minor =
1.** To brew a potion, use ingredients for which it is the **MAJOR** entry.

| Ingredient | MAJOR (3) | med (2) | minor (1) |
|---|---|---|---|
| **viscera** (butcher) | Strong Health | Health | Antidote |
| **sinew** (butcher) | Stamina Poison | Endurance | Health |
| **tail bone** (butcher) | Strong Antidote | Health | Constitution |
| **troll horn** (butcher trolls) | Strength | Constitution | Endurance |
| **bonemeal** (grind bone) | Mana | Perception | Antidote |
| **coal dust** (grind coal) | Antidote | Endurance | Strength |
| **iron dust** (grind iron) | Endurance | Constitution | Strength |
| **silver dust** (grind silver) | Strong Antidote | Restoration | Strong Health |
| **gold dust** (grind gold) | Strong Mana | Restoration | Perception |
| **earth essentia** | Constitution | Endurance | Strength |
| **fire essentia** | Strength | Constitution | Fire Warding |
| **water essentia** | Keen Mind (INT) | Strong Mana | Perception |
| **air essentia** | Fleet Foot (SPD) | Stamina | Keen Mind |
| **raw essentia** (runedust) | Keen Mind | Strong Mana | Perception |
| **pure essentia** (magicdust) | Strong Mana | Endurance | Constitution |
| **solar dust** (grind sunflower) | Fire Warding | Keen Mind | Perception |
| **feau dust** (craft) | Fleet Foot | Strong Mana | Strong Antidote |
| **infernal dust** (grind fang) | Fire Warding | Strong Stam Poison | Keen Mind |
| **mineral dust** (grind gems) | Poison (Doom) | Strong Mana | Strong Stam Poison |
| **purified salts** (grind salt) | Antidote | Strong Antidote | Strong Mana |
| **seed dust** (grind seeds) | Strong Stamina | Stamina | Strong Antidote |
| **westleach dust** (grind pipeweed) | Perception | Stamina | Fleet Foot |
| **swampweed dust** (grind swampweed) | Poison (Berry) | Strong Stam Poison | Endurance |
| **berry powder** (grind berries) | Poison (Berry) | Mana | Strong Mana |
| **manabloom powder** (grind manabloom) | Mana | Keen Mind | Strong Mana |
| **sleeping powder** (grind zizo-bane) | Sleep Poison | Seven Clovers (LCK) | Mana |
| **essence of briar** (grind rosa petals) | Sleep Poison | Antidote | Seven Clovers |
| **alchemical ozium** (grind poppy→ozium) | Strong Stamina | Seven Clovers | Keen Mind |
| **atropa** (herb) | Poison (Doom) | Poison (Berry) | Stamina Poison |
| **matricaria** (herb) | Poison (Berry) | Perception | Poison (Doom) |
| **symphitum** (herb) | Health | Stamina Poison | Antidote |
| **taraxacum** (herb) | Stamina Poison | Health | Antidote |
| **euphrasia** (herb) | Fleet Foot | Stamina Poison | Keen Mind |
| **paris** (herb) | Strong Stam Poison | Poison (Berry) | Stamina Poison |
| **calendula** (herb) | Strong Health | Endurance | Health |
| **mentha** (herb) | Perception | Keen Mind | Stamina |
| **urtica** (herb) | Health | Fleet Foot | Stamina |
| **salvia** (herb) | Constitution | Strength | Endurance |
| **hypericum** (herb) | Stamina | Strong Mana | Antidote |
| **benedictus** (herb) | Strong Stamina | Stamina | Keen Mind |
| **valeriana** (herb) | Health | Fleet Foot | Stamina Poison |
| **artemisia** (herb) | Seven Clovers | Fleet Foot | Health |
| **rosa** (herb) | Seven Clovers | Antidote | Restoration |

---

## Where ingredients come from

- **Herbs** (atropa, matricaria, symphitum, taraxacum, euphrasia, paris, calendula,
  mentha, urtica, salvia, hypericum, benedictus, valeriana, artemisia, rosa):
  forage them from herb bushes scattered on the map (they regrow), or **plant
  herbseeds** in soil (~7.5 min to mature). Grinding a herb gives its **herbseed**;
  seeds are also sold by the **merchant**. Higher Alchemy/Farming = bonus yield.
- **Butchered parts** (viscera, sinew, tail bone, troll horn): **middle-click an
  animal corpse with a knife** (no spell/intent selected). Higher Butchering skill =
  more carved. Horns come specifically from **trolls**.
- **Ores** (gold/silver/iron/coal) and **gems** (Toper/Gemerald/Saffira/Blortz/
  Dorpel): mined, or bought. Grind ore→dust, grind gem→mineral dust **plus** bonus
  gold/element dust (gems are an expensive shortcut to arcane dusts).
- **Special plants:** poppy (→ozium, also a sedative), swampweed (→swampdust),
  fyritius (→firedust), manabloom (spawns in the bog, →manabloom powder), pipeweed/
  westleach (→tobacco dust), sunflower (→solar dust), berries (→berry powder),
  rosa petals (→briar essence), zizo-bane (found in rot/blight areas →sleep powder).
- **Fish → water dust. Crow → air dust.** (grind them)
- **Arcane essentia** (water/fire/air/earth/rune/magic/solar/feau/infernal dust):
  from grinding the matching source (fish, fyritius, crow, gems, sunflower, infernal
  fangs) or crafting. **Pure essentia** = craft 1 each of water+fire+air+earth dust
  on a table. **Feau dust** = craft 2 iron dust + 1 gold dust.
- **Buy it:** the **Alchemist cargo pack** sells pre-made stat potions, antidotes,
  strong poison and prosthetics; the **merchant** sells all the herb/plant seeds and
  some dusts (ozium, etc.). As Head Physician you start `ECONOMIC_RICH` — buying
  seed stock and a cauldron setup turn-one is viable.

---

# THE POTIONS

*Doses below describe per-tick effect while the reagent metabolizes. "90 drams"
is the standard cauldron yield (≈30 sips). All healing potions self-purge above
60u in the body to stop over-healing.*

## Healing

### Elixir of Health — `healthpot`
- **Gate:** Apprentice (any alchemist). **Smell:** sweet berries.
- **Effect:** −1.75 brute & −1.75 fire, −1.25 oxyloss per tick; heals 3 wound HP;
  −5 brain, −1.75 cloneloss, −1 eye per tick. Metabolizes ~1u/tick (fast, strong).
- **Brew with (MAJOR):** symphitum, urtica, valeriana. *(med: viscera, taraxacum,
  tail bone; minor: sinew, artemisia, calendula)*
- Your everyday trauma drink and best-seller.

### Elixir of Health (Strong) — `stronghealth`
- **Gate:** Journeyman. **Smell:** berry pie.
- **Effect:** −5 brute, −5 fire, −5 oxyloss per tick; heals 4 wound HP; −5 brain,
  −5 cloneloss, −2.5 eye. Metabolizes ~2u/tick — a fast, hard burst heal.
- **Brew with (MAJOR):** viscera, calendula. *(minor: silver dust)*

### Elixir of Restoration — `restoration`
- **Gate:** Expert. **Smell:** fizzling berries.
- **Effect:** −3 brute/fire/oxy per tick **and +60 energy/tick**; heals 3 wound HP;
  −5 brain, −3 cloneloss, −1.75 eye. The premium "heal + stamina in one" product.
- **Brew with:** silver dust (med), gold dust (med), rosa (minor) — best made by
  combining silver + gold dust pots in the pot, or lean on rosa stock.

## Mana & Stamina

### Elixir of Mana — `manapot`
- **Gate:** Apprentice. **Smell:** power.
- **Effect:** **+30 energy/tick** (restores stamina/mana pool). ~1u/tick.
- **Brew with (MAJOR):** bonemeal, manabloom powder. *(med: berry powder; minor:
  sleeping powder)*

### Elixir of Mana (Strong) — `strongmana`
- **Gate:** Journeyman. **Smell:** fear.
- **Effect:** **+120 energy/tick**, ~3u/tick — a near-instant mana refill.
- **Brew with (MAJOR):** pure essentia (magicdust), gold dust. *(med: water dust,
  raw essentia, feau dust, mineral dust, hypericum; minor: manabloom/berry powder,
  purified salts)*

### Elixir of Stamina — `stampot`
- **Gate:** Apprentice. **Smell:** fresh air.
- **Effect:** restores ~20 stamina/tick. ~1u/tick.
- **Brew with (MAJOR):** hypericum. *(med: seed dust, westleach dust, air essentia,
  benedictus; minor: mentha, urtica)*

### Elixir of Stamina (Strong) — `strongstam`
- **Gate:** Journeyman. **Smell:** clean winds.
- **Effect:** restores ~50 stamina/tick.
- **Brew with (MAJOR):** seed dust, alchemical ozium, benedictus.

## Antidotes (poison cures)

### Antidote — `antidote`
- **Gate:** Apprentice. **Smell:** wet moss.
- **Effect:** −4 toxin/tick **and strips 1u of every harmful reagent/tick.**
  Metabolizes very slowly (0.1u/tick → lasts ~15 min on a full dose), so you can
  pre-drink it prophylactically before a risky meal/meeting.
- **Brew with (MAJOR):** coal dust, purified salts. *(med: briar essence, rosa;
  minor: viscera, bonemeal, symphitum, taraxacum, hypericum)*

### Antidote (Strong) — `strong_antidote`
- **Gate:** Journeyman. **Smell:** purity.
- **Effect:** −12 toxin/tick **and strips 3u of every harmful reagent/tick.** Same
  long duration. The hard counter to serious poisonings.
- **Brew with (MAJOR):** silver dust, tail bone. *(med: purified salts; minor: seed
  dust, feau dust)*

## Stat Potions (Expert gate, 30 drams)

All seven grant **+3 to one stat while in your system** (status reapplies each tick;
the reagent metabolizes slowly so it lasts a good while). **Overdose at 33u** →
jitters + 3 toxin/tick. **They don't stack** — a second buff potion purges the
first. All smell-gated at **Expert** alchemy.

| Potion | Stat | Brew with (MAJOR) |
|---|---|---|
| **Mountain Muscles** | STR +3 | fire essentia, troll horn *(med: salvia)* |
| **Keen Eye** | PER +3 | westleach dust, mentha *(med: matricaria)* |
| **Enduring Fortitude** | WIL +3 | iron dust *(med: coal/earth/magic dust, sinew, calendula)* |
| **Stone Flesh** | CON +3 | earth essentia, salvia *(med: fire/iron dust, troll horn)* |
| **Keen Mind** | INT +3 | water essentia, raw essentia *(med: mentha, solar dust)* |
| **Fleet Foot** | SPD +3 | air essentia, feau dust, euphrasia *(med: urtica, artemisia, valeriana)* |
| **Seven Clovers** | LCK +3 | artemisia, rosa *(med: sleeping powder, ozium)* |

> **Min-max tip:** brew **Stone Flesh** and drink it yourself — it patches the
> Physician's −1 CON weakness. **Keen Mind** stacks INT for faster skill gains and
> sharper diagnosis numbers.

## Utility

### Potion of Fire Warding — `fire_resist`
- **Gate:** Master. **Smell:** authority. **30 drams.**
- **Effect:** grants `TRAIT_FIRE_RESIST` — **fire immunity for 15 minutes** per dose.
- **Brew with (MAJOR):** infernal dust, solar dust. *(minor: fire essentia)*

## Poisons (offense / sedation)

### Poison (Berry) — `berrypoison`
- **Gate:** Journeyman. **Smell:** death.
- **Effect:** +3 nausea, +2 toxin/tick (slow, 0.1u/tick). Incapacitates, won't kill
  in one dose. Dwarves resist it heavily.
- **Brew with (MAJOR):** swampweed dust, berry powder, matricaria. *(med: atropa,
  paris)*

### Poison (Doom) — `strongpoison`
- **Gate:** Expert. **Smell:** doom.
- **Effect:** +6 nausea, +4.5 toxin/tick — **lethal** in a standard dose. Deliberately
  hard to make.
- **Brew with (MAJOR):** mineral dust, atropa. *(minor: matricaria)*

### Stamina Poison — `stampoison`
- **Gate:** Journeyman. **Smell:** a slow breeze.
- **Effect:** −45 energy/tick (drains stamina), 0.3u/tick. Exhausts a target.
- **Brew with (MAJOR):** sinew, taraxacum. *(med: symphitum, euphrasia; minor:
  atropa, paris, valeriana)*

### Stamina Poison (Strong) — `strongstampoison`
- **Gate:** Expert. **Smell:** stagnant air.
- **Effect:** −180 energy/tick, very fast (0.9u/tick) — drops someone's stamina
  near-instantly.
- **Brew with (MAJOR):** paris. *(med: swampweed dust, infernal dust; minor: mineral
  dust)*

### Sleep Poison — `sleep_powder`
- **Gate:** Master. **Smell:** numbing mint.
- **Effect:** applies a **knockout/sleep** status on metabolizing — puts a target to
  sleep. *Your in-house surgical sedative* so you never have to beg the apothecary.
- **Brew with (MAJOR):** sleeping powder (grind zizo-bane), essence of briar (grind
  rosa petals).

> **Ethics/PQ note:** brewing poisons is fine as a tool (sedation, pest control,
> sanctioned justice), but dosing people is an antagonistic act. As a whitelisted
> `min_pq 3` role, keep poison use to legitimate medical/RP purposes.

---

## Fast cheat-sheet: "I want X, I grind Y"

| Want | Grind / craft this |
|---|---|
| Healing pots | symphitum/urtica/valeriana herbs, or viscera+calendula for Strong |
| Mana pots | bone→bonemeal, or manabloom; magicdust/gold for Strong |
| Stamina pots | hypericum/benedictus; seed dust or ozium for Strong |
| Antidotes | coal→coaldust + salt→puresalt; silver dust/tail bone for Strong |
| Stat potions | the matching essentia dust (fire=STR, earth=CON, water=INT, air=SPD…) |
| Fire Warding | infernal fang→infernal dust, or sunflower→solar dust |
| Sedative (Sleep) | zizo-bane→sleeping powder, or rosa petals→briar essence |
| Lethal poison | gems→mineral dust + atropa herb |

### Source files
`alch_cauldron_recipes.dm`, `alch_grind_recipes.dm`, `ingredients.dm`,
`cauldron.dm`, `mortarpestle.dm`, `potionbuffs.dm`, and reagent effects in
`code/modules/roguetown/roguecrafting/alchemy/reagents.dm`.
