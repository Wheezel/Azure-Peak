# Head Physician — Min-Max Guide

*A practical optimization guide for the Head Physician role in Azure Peak. All
numbers below are pulled directly from the codebase — file references are given
so you can verify anything yourself.*

---

## 1. What you actually are

The Head Physician (`code/modules/jobs/job_types/roguetown/burghers/physician.dm`)
is the single most skill-loaded medical role in the game. You spawn whitelisted,
with `min_pq = 3`, one slot per round, and you start *already maxed* in the two
disciplines that take everyone else the whole round to grind.

**Starting traits (free, can't be bought elsewhere this cheaply):**

| Trait | What it does |
|---|---|
| `TRAIT_MEDICINE_EXPERT` | Uncaps Medicine from Expert → **Legendary**. Lets you cauterize *through armor* out of combat. |
| `TRAIT_ALCHEMY_EXPERT` | Uncaps Alchemy → Legendary. |
| `TRAIT_EMPATH` | Read stress / muteness / emotional state on examine. |
| `TRAIT_NOSTINK` | No body-odor stench (QoL, and relevant for plague RP). |

**Starting skills:**

| Skill | Level |
|---|---|
| Medicine | **Legendary (6)** |
| Alchemy | Master (5) |
| Reading | Master (5) |
| Athletics, Swords, Sewing, Knives | Journeyman (3) |
| Crafting, Wrestling | Apprentice (2) |

**Starting stat mods:** INT **+4**, WIL +1, LCK +1, SPD +1, STR **−1**, CON **−1**.

The class is built around a brain, not a body. Your whole optimization problem is:
**maximize INT/WIL, protect your fragile CON, and never put yourself in a fight
you didn't choose.**

---

## 2. Character creation: stats

Your subclass already hands you INT +4. Stack on top of it.

- **Prioritize INT.** Intelligence drives skill XP gain (including sleep-learning),
  diagnosis fidelity, and stat-vs-stat checks. With +4 baked in, pushing a
  statpack that adds more INT compounds everything you do.
- **Don't dump WIL.** Willpower is your pain ceiling — every point is **+10 pain
  threshold** (`mob/living` pain code). Surgery patients who aren't sedated, and
  *you* when something goes wrong, both care about this. WIL also resists stress,
  which matters because you'll be near a lot of dying people.
- **Accept the STR/CON penalty, don't fight it.** You are −1 STR / −1 CON by
  design. Trying to rebuild into a fighter wastes the class. Keep STR at **≥6** so
  you can still wield your cane blade (rapier `minstr = 6`), and leave CON where it
  lands — you survive by not getting hit, not by tanking.
- **LCK +1 is quietly good.** Luck rolls are `(STALUC−10)·multi` percent on
  `goodluck()` checks; a couple extra points shave failure chance off everything
  the engine rolls luck on.

**Rule of thumb:** INT → WIL → LCK/SPD → (floor STR at 6) → CON last.

---

## 3. Virtues & flaws

**Best virtue — Skilled Apprentice (Physician variant), `code/modules/virtues/crafter.dm`.**
Even though you already start Expert in both, the virtue path is the cleanest way
to reinforce the kit and, on relevant builds, hand you the **secular diagnose
spell** plus a backup medicine pouch / improvised surgery kit. If you ever roll a
build that *doesn't* auto-grant secular diagnose, this guarantees it.

**Flaws:** You're a high-RP whitelist role; treat flaws as roleplay flavor, not a
points farm.
- **Avoid** anything that drops INT/WIL/CON (e.g. Leper's −1 to all stats) — you're
  already CON-light and your value is entirely mental.
- **Avoid** combat-magnet flaws (Hunted, Indebted bounty) — you cannot win the
  fights they start.
- If you take a flaw, take one that's purely social/aesthetic so it costs you
  nothing mechanically.

---

## 4. The surgery loop (your bread and butter)

Surgery success and speed are driven by **three multipliers**: tool quality,
patient position, and your Medicine skill. You already max the third — so the
entire skill expression is *managing the first two*.

### Position is the biggest free win
From the surgery code, the location modifier is enormous:

| Patient position | Success | Speed |
|---|---|---|
| Standing | ×0.6 | ×1.4 (slower) |
| Lying on a table | ×0.8 | ×0.8 |
| **Lying on a bed/cot** | **×1.0** | **×0.9 (fastest)** |

**Always operate on a bed.** Standing surgery throws away ~40% of your success
chance for no reason. A sedated patient on a bed is the gold standard.

### Sedate first
A struggling, conscious patient screams and disrupts. Knock them out (Ozium,
poppymilk, sleep poison you brewed yourself) before anything involving a cautery —
cauterize deals 25 burn and makes them scream otherwise.

### Use the right tool for every step
Implement success rates are baked per-step. Your full surgery bag
(`code/game/objects/items/surgery_bag.dm`) carries the 100%/80% tools — use them,
not the improvised substitutes:

| Step | Best tool (success) | Bad substitute |
|---|---|---|
| Incise | Scalpel (80%) | any Sharp (60%) |
| Clamp | Hemostat (75%) | Wirecutter (60%) |
| Retract | Retractor (75%) | Screwdriver (50%) |
| Heal (repeating) | Suture (80%) | Hemostat (60%) |
| Cauterize | Cautery (**100%**) | Welder (70%) |
| Set bone | Bonesetter (80%) | Hand (40%) |
| Relocate joint | Bonesetter (90%) | Hand (50%) |

### What Legendary Medicine buys you over Expert
This is *the* reason the role exists. Legendary (only reachable with your trait):

- **Surgery time −40%** (Master is −20%, everyone else 0%).
- **Healing surgery multiplier ×2.0** on tend-damage steps (Expert is ×1.4).
- **Sewing: 7× progress per stitch and −4.0 bleed per stitch** (Expert sews 4×
  progress and doesn't drop bleed at all). This is the single biggest survivability
  lever in trauma — you stop bleeds nobody else can.
- **Leech/cheele application: 5 seconds** instead of 35 at novice
  (`time = (70 − medicine·10) / 2`).
- **Cauterize through armor** (the `TRAIT_MEDICINE_EXPERT` perk) — you can seal a
  bleed on an armored patient mid-crisis without stripping them first.

### Procedure cheat-sheet
- **Brute/burn damage** → Healing surgery (Incise → Clamp → Retract → repeat Heal →
  Cauterize). Heal step does 10–30 brute or 10 burn per success, scaled by your ×2.0.
- **Poison / toxin** → Bloodletting (cut vein, force blood out): **−25 toxin per
  success**, costs 50 blood. Pair with a transfusion or cheele afterward.
- **Fracture** → Set Bone step (needs the broken flag). **Dislocation** → Relocate
  Bone step. Both bracketed by incise/cauterize.
- **Amputation** → Saw Bone → Amputate, when a limb is beyond saving.

---

## 5. Diagnosis — your information edge

You start with **Secular Diagnosis** (`associated_skill = medicine`, range 4, 0
faith cost, ~3s cooldown — `code/modules/spells/roguetown/acolyte/pestra.dm`). At
Legendary Medicine you're in the **high-tier** bracket, which reveals *exact*
numbers where everyone else gets vague hints:

- Exact toxicity %, exact blood volume (units **and** %), exact bleed rate.
- Severe/natural/minor infection called out plainly.
- Black Rot stage named (Creeping → Festering → Boiling → Necrosis) with cure hint.

**Pro move — blood analysis:** embed your **cheele** (or use a hemostat to draw
blood) on a patient, then diagnose. At high tier this identifies *every substance*
in their blood with amounts — letting you detect poisons, identify what an antag
dosed someone with, or confirm a clean bloodstream before surgery. This is a
genuine investigative tool, not just a healing one.

**EMPATH bonus:** on examine you read stress tiers ("a little / very / extremely
stressed"), muteness, and emotional detachment — invaluable for triage and for
sniffing out something wrong with a patient who won't talk.

---

## 6. Alchemy — turn a workshop into an economy

You start Master alchemy with an income-machine kit. XP per craft scales with
`STAINT` (cauldron grants `INT·2` per brew, even on **failures**), so your high INT
also makes you the fastest alchemist in the round to reach Legendary.

### Priority brews (cauldron, 90 drams water, ≤4 ingredients, recipe ≥5 points)
- **Elixir of Health / Strong Health** — your trauma reserve and your best-seller.
- **Elixir of Restoration** (Expert) — heals *and* restores energy, the premium product.
- **Elixir of Mana / Stamina** — easy volume sellers for adventurers and guards.
- **Antidote / Strong Antidote** — cheap insurance against the poisons going around.
- **Stat potions** (Expert+): Keen Mind (+INT), Stone Flesh (+CON), etc. — sell to
  fighters, or quietly drink the +CON one yourself to patch your weak stat.
- **Sleep poison** (Master) — *your* sedation supply for surgery, no begging the
  apothecary.

### Sell it
Set up the **Potionseller** machine (`potionseller.dm`): load vials/bottles, set a
per-dram price, and it runs as passive income while you operate. You also spawn at
the **`ECONOMIC_RICH`** treasury tier (the highest) plus a coin pouch, so you have
capital from minute one to buy reagents, hire a merc to guard the clinic, or pay
adventurers to fetch rare ingredients.

---

## 7. Heartsblood — your trump card

Beneath the University courtyard, the **Keepers of Pestra** tend the heartbeast.
Your role text gives you standing access. Heartsblood is the *only* practical cure
for **Black Rot**, which normal medicine cannot touch.

- **Heartblood Vial** — fast (~0.4s) application, cures ~34 rot, restores 25 energy.
- **Heartblood Canister** — ~0.8s, cures ~67 rot (≈2× a vial), restores 25 energy.
- The **Calyx** can be used **once per person**: ~5 HP up front plus a long
  regeneration buff (~225 HP over 10 min via Pestra Care), drops **1–2 vials**
  (2 if your Medicine/Holy ≥ 4 — you always qualify), plus coins and echo points.

Coordinate with a Keeper to keep a stock of vials on hand. When someone walks in
with creeping black veins, you're the only person in town who can save them — make
that your signature.

---

## 8. Combat & survival (you are not a fighter)

Your sidearm is the **cane blade** (`courtphysician` rapier variant): a concealed
gold-handled blade with full rapier thrust/cut intents, `wdefense = 7`,
`minstr = 6`. It loses the two-handed grip and the lunge special of a normal
rapier, so treat it as a **self-defense duelling sidearm**, not an offensive
weapon. With Journeyman swords you can parry and survive a mugging — you cannot win
a brawl against a soldier, and you shouldn't try.

Survival priorities:
1. **Stay in the clinic / University.** Your value is the bed, the cauldron, and the
   heartbeast — all stationary.
2. **Carry your own outs:** the two starting health potions, a cheele for emergency
   toxin/blood control, and your diagnose spell to know when to run.
3. **Buy muscle.** You're rich and you have a coin pouch — hire a mercenary or an
   adventurer to guard the clinic rather than fighting yourself.
4. **Don't operate on strong intent.** The job literally warns you not to kill the
   Duke with a careless surgery. A botched high-intent operation on a noble is the
   fastest way to lose the whitelist.

---

## 9. Take Apprentice — force-multiply

You spawn with the **Take Apprentice** spell. It binds one willing student and lets
you seed them with `TRAIT_MEDICINE_EXPERT` / `TRAIT_ALCHEMY_EXPERT` (Novice in the
matching skill). Recruit an apothecary or aspiring medic early: they grow into a
second pair of hands for surgery and a second cauldron for production, and you
oversee the whole clinic instead of being a one-person bottleneck. This is the
intended "Head" part of Head Physician — run a department, don't solo it.

---

## TL;DR optimization checklist

1. **Stats:** stack INT, keep WIL up, floor STR at 6, don't bother rescuing CON.
2. **Virtue:** Skilled Apprentice (Physician) to lock in the kit + secular diagnose.
3. **Always operate on a bed, on a sedated patient, with the correct tool per step.**
4. **Lean on Legendary-only perks:** ×2 healing, −40% time, −4 bleed/stitch sewing,
   cauterize-through-armor, 5-second leech application.
5. **Diagnose + cheele/hemostat** for exact vitals and full blood analysis.
6. **Run the cauldron + Potionseller** for passive gold; brew your own sleep poison
   for sedation and a +CON potion to patch your weak stat.
7. **Stock heartsblood** with the Keepers — own the Black Rot cure.
8. **Never pick a fight.** Hire guards, carry potions, stay home.
9. **Take an apprentice** and run a clinic, not a solo act.

---

### Source files
- Job & gear: `code/modules/jobs/job_types/roguetown/burghers/physician.dm`
- Surgery: `code/modules/surgery/` (healing, bloodletting, fracture, dislocation, amputation, organic_steps)
- Medicine skill: `code/datums/skills/misc.dm`
- Alchemy skill & crafting: `code/datums/skills/craft.dm`, `code/modules/roguetown/roguecrafting/alchemy/`
- Diagnose & Pestra: `code/modules/spells/roguetown/acolyte/pestra.dm`, `code/datums/gods/patrons/divine/pestra.dm`
- Heartsblood: `code/modules/roguetown/roguemachine/heartbeast/`
- Cane blade: `code/game/objects/items/rogueweapons/melee/swords.dm`
- Virtues: `code/modules/virtues/crafter.dm`
- Economy: `code/modules/roguetown/roguemachine/potionseller.dm`, `code/controllers/subsystem/rogue/treasury.dm`
