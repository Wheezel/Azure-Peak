# Pestran Bishop — Min-Max Guide

*Optimizing a Bishop who takes Pestra (goddess of decay, disease & medicine) as
patron. A Pestran Bishop is an **armed fighter-priest + master healer + church
authority** rolled into one. Values from `priest.dm`, `pestra.dm`, `general.dm`,
and the cleric/devotion system.*

---

## What you are

A Bishop is the head of the Holy See, and **you spawn with devotion maxed (1000)
and `start_maxed=TRUE`** (`priest.dm:107`) — meaning you have **every Pestra miracle
unlocked immediately, up to and including T4 Resurrect.** No devotion grind. You
also get the best passive devotion regen in the game (`CLERIC_REGEN_MAJOR`, 0.8/tick).

Your kit blends three roles nobody else combines:
- **Combat cleric** — Staves & Polearms at **Master**, plus Divine Blast and a
  pestilence melee combo.
- **Top-tier healer/resurrector** — Pestra's full medicine ladder.
- **Church ruler** — excommunicate, curse, convert followers, crown the Duke.

**Stat spread:** INT +4 · WIL +2 · STR −1 · CON −1 · SPD −1 (brain/willpower caster,
fragile body).

---

## 1. Character creation — stats

- **Stack INT.** It already starts +4; INT drives skill XP, miracle/diagnosis
  fidelity, and stat checks.
- **Keep WIL high (+2 base).** Each point is +10 pain threshold and stress resist —
  vital because you're a frontline cleric with low CON.
- **Floor STR at the polearm requirement** so you can actually swing your Master-tier
  spear/quarterstaff; don't over-invest past it.
- **CON −1 is your weakness** — you survive by **healing through damage** (see the
  Fortify combo), not by tanking. Don't dump it further.

---

## 2. Skills — what to grind

You start: Reading Legendary · **Staves Master · Polearms Master · Holy Master** ·
Medicine Expert · Wrestling/Unarmed/Crafting Journeyman · Alchemy Journeyman ·
Cooking/Sewing/Farming Apprentice.

Grind priority:
1. **Holy → Legendary.** This is the single biggest lever. Holy scales as
   `1 + (level/Legendary)`, so at Legendary your **devotion/progression regen and
   prayer effectiveness double**, your healing miracles scale up, and **Intervention's
   cast drops from 4.5s to 1.5s** (`general.dm`). You start Master — push the last tier.
2. **Medicine → Legendary** (uncapped by `TRAIT_MEDICINE_EXPERT`). Unlocks surgery,
   Black Rot extirpation, and the ×2 healing tier to back up your miracles.
3. **Alchemy → Legendary** (uncapped by `TRAIT_ALCHEMY_EXPERT`). Potion production as
   a second supply line.
4. Polearms/Staves are **already Master** — no work needed; you're combat-ready turn one.

---

## 3. Devotion & where to pray

You start maxed, but you'll spend devotion casting. Refill by **praying** (≈2+
devotion per 30-tick action, ×Holy multiplier). Pestra hears you at a **psycross,
the church, the physician's building, the Pestra sanctum, or near any well**
(`pestra.dm:33-54`) — so top-ups are easy almost anywhere. With Legendary Holy +
`CLERIC_REGEN_MAJOR` you refill fast enough to miracle aggressively.

---

## 4. The miracle kit & the combos that matter

### Healing core
| Miracle | Tier | Effect | Cost / CD |
|---|---|---|---|
| **Heal** | T1 | 2.5 HP/sec aura; **Pestra bonus: +40% when target is downed**, plus blood + toxin healing | minor · 15s |
| **Pestra Heal** | T2 | 5 HP/tick **+ a 225-HP heal-over-10-min** (`pestra_care`). Costs **1 infestation charge** | 45 · 10s |
| **Fortify** | T3 | Buff that **amplifies ALL incoming healing** for 1 min (and burns undead 25) | miracle · 30s |
| **Intervention** | T3+ | **Heals all damage + wounds** on a limb; 1.5s cast at Legendary Holy | legendary · 2min |
| **Blood Miracle** | T1 | Transfuse your blood into a target (scales with Holy) | major · 1min |
| **Pestra Leech** | T0 | −30 toxin, +30 blood, spawns leeches | 30 · 60s |
| **Cure Rot** | T3 | cure rot / turning zombie | — |
| **Resurrect (Putrid Revival)** | T4 | Raise the dead — costs **1 filled heartblood canister + 2 vials** (or 2 vials, reduced) | 250 · 10min |

> **💥 #1 combo — Fortify → Heal/Pestra Heal.** Fortify multiplies *all* incoming
> healing, and it's an aura you can self-cast. Pop Fortify, then Heal yourself or a
> patient and the output balloons. This is how a CON −1 cleric out-sustains damage —
> always fight with Fortify up.

### Combat combo (you're an armed cleric, lean in)
| Miracle | Tier | Effect |
|---|---|---|
| **Infestation** | T1 | Vermin swarm: debuffs the target (−CON/−SPD, toxin/tick) **and grants you 10 infestation charges** (range 8) |
| **Pestilent Blade** | T2 | Spends **1 charge** to enchant your weapon — *devastating against infested targets*, weak otherwise |
| **Divine Blast** | — | 20 dmg ranged (range 12, 5s CD), **+20 vs undead/excommunicated**; Pestra adds vomit + toxloss + a leech on hit |

> **💥 #2 combo — Infestation → Pestilent Blade → Master polearm.** Open a fight with
> **Infestation** (it banks **10 charges** and softens the enemy), enchant your spear
> with **Pestilent Blade**, then beat them down with your Master polearm — the blade
> hits hardest precisely because they're now infested. One Infestation fuels ~10
> blade enchants *or* Pestra Heals, so cast it early and you're set for the fight.

### Limb work
**Attach Bodypart** (T2) reattaches held limbs/organs and strips rot off them — pair
with your Medicine surgery skills to be the town's reconstruction surgeon.

---

## 5. Resurrection — own the death niche

You can **Resurrect from round one** (you start at T4). It consumes **heartblood**
(1 filled canister + 2 vials, or 2 vials reduced). As Pestra clergy you have standing
with the **Keepers of Pestra** at the heartbeast — **stockpile heartblood vials early**
and you become the town's irreplaceable resurrector. Heartblood also cures **Black
Rot**, and your Cure Rot miracle handles zombies, so the entire decay/death domain is
yours. This is the Pestran Bishop's signature power spike over a generic Bishop.

---

## 6. Church authority — your unique leverage

No other role has these. Use them to build power, not just heal:
- **Recruit Templar / Recruit Acolyte** — convert willing players into your faction
  (`priest.dm:326`). Build a holy retinue/militia under you.
- **Excommunicate / Apostasy (mark of shame)** — cut a target off from their patron's
  prayers; political and spiritual leverage.
- **Divine Curse / Divine Blessing** — punish or reward the flock.
- **Crown the ruler** — you legitimize the Duke ("By the authority of the gods…").
- **Marriage**, and **Take Apprentice** to seed a successor with your traits.

A min-maxed Pestran Bishop isn't a solo healer — they run a faction: convert Templars
to fight for you, heal/resurrect them, and rule the church.

---

## 7. Survival & PQ

- Whitelisted, **`min_pq 5`** — it's a leadership role; play it with weight.
- **Fight with Fortify up, heal between exchanges**, and use Infestation to debuff
  before committing. Your CON is low — never trade blows raw.
- Carry your starting **Pestra needle + cheele** (blood transfusion/anti-poison) as
  backup to the miracles.
- Pray to keep devotion topped before any fight or rez.

---

## TL;DR min-max checklist
1. **Stats:** stack INT, keep WIL high, floor STR for your polearm, don't dump CON.
2. **Grind Holy → Legendary first** (doubles devotion regen, halves Intervention) →
   then Medicine and Alchemy → Legendary.
3. **You start maxed devotion** — you have Resurrect + the full kit immediately.
4. **Healing combo:** Fortify → Heal/Pestra Heal (amplified output; out-sustains your low CON).
5. **Combat combo:** Infestation (bank 10 charges) → Pestilent Blade → Master polearm; Divine Blast to poke.
6. **Stockpile heartblood** with the Keepers → be the town's resurrector + Black Rot cure.
7. **Use church powers:** recruit Templars/Acolytes into a retinue, excommunicate/curse rivals, crown the Duke.
8. **Second career:** Legendary Medicine (surgery, black rot) + Legendary Alchemy (potions) make you functionally unkillable and self-sufficient.

### Source files
`code/modules/jobs/job_types/roguetown/church/priest.dm`,
`code/datums/gods/patrons/divine/pestra.dm`,
`code/modules/spells/roguetown/acolyte/pestra.dm`,
`code/modules/spells/roguetown/acolyte/general.dm` (Heal/Fortify/Intervention/Blood Miracle),
`code/modules/spells/roguetown/acolyte/resurrect.dm`, and the devotion system in
`code/controllers/subsystem/rogue/miscprocs.dm` / `code/__DEFINES/cleric.dm`.
