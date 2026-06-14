# The Holy Psydonic Inquisition — An In-Depth Guide

> *"For the eradication of heresy, so long as Psydon endures."*
> — Inscription upon the HERMES Marquette

This guide covers the Otavan Inquisition faction as it exists in Azure-Peak: who
they are, the roles that make them up (with a deep dive on the **Absolver**),
the **manor** they spawn in, and **every tool** the sect has access to — both the
ones physically placed in the Inquisition Manor and the ones the sect can summon
through their unique Marque economy.

Everything below is drawn directly from the game code. Where a number is given
(devotion cost, cooldown, Marque price, etc.) it reflects the actual values in
the source, but balance numbers can change between versions — treat them as
"how it works," not gospel.

---

## 1. Who Are the Inquisition?

The Inquisition is a small, self-contained **church/station faction** sworn to
**Psydon**, the "Old God" (the `/datum/patron/old_god`). They are envoys of
**Otava**, the largest surviving Psydonic kingdom, sent to Azuria as a
"silver-tipped olive branch" to ward off the dark. Lore-wise Psydon is dead or
sleeping, so the Inquisition is a sect of fanatics keeping a dead-or-dormant
god's flame alive in a land that has largely moved on to the living pantheon
gods.

Mechanically every member shares some hard requirements:

- **Patron must be Psydon** (`/datum/patron/old_god`). The roles are built from
  the ground up around Psydonism and cannot be taken by other faiths.
- They carry **`TRAIT_INQUISITION`** (and most carry **`TRAIT_STEELHEARTED`**),
  which is the key that unlocks their special equipment, the HERMES Marquette,
  the Soul Churner, and more.
- They are a **soft-antagonist / pressure faction**: their job is to root out
  heretics, nitebeastes (werewolves/vampires), and apostates — and they have a
  unique, risky path to seize the throne.

### The Usurpation Path — Rite of Psydonian Tribunal

The Inquisition has its own throne-claim, the **Rite of Psydonian Tribunal**
(`/datum/usurpation_rite/psydonian_tribunal`). Highlights:

- **Only the Inquisitor, Absolver, or Orthodoxist may invoke it** (must be a
  living, non-undead Psydonite).
- It has the **lowest assent requirement** of any rite — only **4** Psydonite
  voices are needed near the throne. *Any* non-undead Psydonite can assent, even
  Psydon heretics — so a full sect can essentially start it themselves.
- Once 4 assents land, the realm is alerted and a **contestation period** begins.
  Survive it and stay conscious near the throne and the realm is yours.
- Success makes you a **Grand Inquisitor** ruling an **Ordinate**, and the
  epilogue frames an incoming war with Grenzelhoft for breaking the balance of
  power.

It's deliberately a high-risk gambit — easy to *start*, hard to *hold* — meant
to drive in-round conflict.

---

## 2. The Roster

The Inquisition fills out as **three roles**, two of which branch into
subclasses. All of them are Psydonites who gain the `change_origin(... /otava)`
"Holy order" background.

| Role | Slots | Min PQ | Whitelist | Identity |
|------|-------|--------|-----------|----------|
| **Inquisitor** | 1 | 10 | **Yes** | Sect leader, jack-of-all-trades |
| **Absolver** | 1 | 3 | No | Pacifist healer & manor-keeper |
| **Orthodoxist** | 3 | 5 | No | The rank-and-file retinue |

### 2.1 The Inquisitor (the leader)

The whitelisted commander of the sect. Picks one of two archetypes at spawn:

- **Inquisitor (Inspector)** — the investigator/diplomat. Master Lockpicking,
  Tracking, and Sneaking; Expert knives, whips, and crossbows. Traits include
  `TRAIT_BLACKBAGGER`, `TRAIT_SLEUTH`, `TRAIT_PERFECT_TRACKER`,
  `TRAIT_PURITAN`, `TRAIT_SILVER_BLESSED`. Capped to **Tier-1 miracles**. Comes
  with a black knifebelt, a psywhip, spectacles, a garrote, inquiry cord,
  grappling hook, a black bag, and a choice of relic or Psydonic weapon.
- **Inquisitor (Ordinator)** — the "Hollywood knight." Very strong, very slow
  (`STATKEY_SPD = -3`), `TRAIT_HEAVYARMOR`, capped to **Tier-2 miracles**. Wears
  ornate fluted plate and picks from greatswords, flail+greatshield, etc.

The Inquisitor also carries `TRAIT_PURITAN`, which is special: **Puritans can
operate the Marquette even though they aren't `TRAIT_INQUISITION`**, can toggle
the **Puritan's Lock** on the HERMES network, and can process writs. They are
the financial controller of the sect.

The Inquisitor (and several others) gains two interrogation verbs — **Test
Faith** and **Reveal Allegiance** — see §6.

### 2.2 The Orthodoxist (the retinue)

The rank-and-file. The base job is a shell (`outfit = null`) that immediately
rolls into one of **five** subclasses:

- **Adjudicator** (`psydoniantemplar`) — a heavy-armor templar with Tier-2
  miracles, fluted chain, and a huge weapon-loadout menu. Sub-discipline
  **Justicar** trades CON/WIL for INT/PER and a cuirass.
- **Disciple** — Psydonite martial-artist monk. Inverse-scaled unarmed builds:
  **Abboteer** (master pugilist, weaponless oath), **Pugilist**, plus
  quarterstaff/katar/knuckleduster options, and a wrestling technique
  (Dropkick/Chokeslam/Stunner/Headbutt). Wears regenerating "skin" armor.
- **Sojourner** — Naledian **Automagic** monk (the Inquisition's Pontifex
  analogue). Arcyne spell-fists: Fist/Grasp/Storm/Blade of Psydon, Shadowstep,
  Empower Weapon. Speaks Celestial, gets a spellbook.
- **Confessor** — the subterfuge specialist. Master Sneaking, Stealing, and
  Lockpicking; `TRAIT_BLACKBAGGER`, `TRAIT_SLEUTH`, `TRAIT_PERFECT_TRACKER`.
  Sub-discipline **Arbalist** trades Dodge Expert for master crossbows and brute
  stats. Spawns with the garrote, black bag, grapple, and a crossbow choice
  (slurbow / crossbow / siegebow) with bolt menus.
- **Psyaltrist** — the Inquisition's bard. Master Music, Expert Holy, a chosen
  instrument, Vicious Mockery, and Tier-2 miracles. The "weaponize the choir"
  class.

Every Orthodoxist spawns with a **manor key**, an **arrival slip**, and a silver
psydagger.

### 2.3 The Absolver — see the dedicated deep dive in §3.

---

## 3. The Absolver — Deep Dive

> *"Once, you were alone in this monastery; a chapel of stone, protecting a
> shard of Psydon's divinity. Now, you've a whole sect to shepherd."*

The Absolver is **THE ONE** — a single-slot role (`total_positions = 1`,
commented `// THE ONE.`). It is the most mechanically unusual role in the
faction: a **forced-pacifist healer** who heals others by **taking their wounds
into their own body**. They are also the **manor-keeper** — the sect's
quartermaster, cook, and infirmarist — carrying `TRAIT_MANORKEEPER`.

### 3.1 Identity & Stat Spread

- **Patron:** Psydon only. **Forbidden races:** ooze. **Min PQ:** 3 (very
  accessible — no whitelist).
- **Defining traits:** `TRAIT_PACIFISM` (cannot initiate violence),
  `TRAIT_NOPAINSTUN`, `TRAIT_EMPATH`, `TRAIT_CRITICAL_RESISTANCE`,
  `TRAIT_SILVER_BLESSED`, `TRAIT_STEELHEARTED`, `TRAIT_INQUISITION`,
  `TRAIT_MANORKEEPER`.
- **Stats:** `+5 CON, +5 WIL, +2 INT, −2 SPD` — tanky and willful but slow. The
  code explicitly notes this is offset by their pacifism-and-heal-through-damage
  gimmick.
- **Skills:** **Expert** Holy magic, Medicine, and Reading; **Journeyman**
  Alchemy, Athletics, Swimming, Climbing, Cooking, Fishing, Crafting; plus
  apprentice Sewing/Farming/Butchering/Tanning/Carpentry/Masonry. This wide
  "homemaker" skillset is the manor-keeper kit.
- **Devotion:** Granted **Cleric Tier 4** miracles, maxed out at spawn, with the
  special `CLERIC_REGEN_ABSOLVER` passive regen — a genuine miracle-worker,
  described in-code as a "PSYDONIAN MIRACLE-WORKER. LUX-MERGING FREEK."

### 3.2 The Lux-Magicka Kit (their signature)

The Absolver's healing is **"lux-magicka"** — explicitly *not* normal miracles
(same conceptual bucket as the Naledians). The core conceit: you don't mend a
wound, you **move it onto yourself**.

**WEEP** — *lesser lux-magicka* (`/obj/effect/proc_holder/spell/invoked/psydonlux_tamper`)
- Range 3, **devotion cost 80**, recharge **30 seconds**.
- Siphons **lesser** injuries (gashes, fractures) off a target and imposes them
  on you instead. If the target has lost blood, they're **fully replenished from
  your own veins**.
- Cannot be used on yourself, the dead, deadites, or someone irreversibly gone.

**ABSOLVE** — *greater lux-magicka* (`/obj/effect/proc_holder/spell/invoked/psydonabsolve`)
- Range 3, **devotion cost 100**, recharge **30 seconds**.
- Siphons **all** injuries — brute, burn, blood loss, even **dismemberment** —
  off the target, completely healing them, and inflicts all of it on you.
- **Casting it on a dead target fully resurrects them — at the cost of your own
  life.** The spell makes you confirm explicit warnings: *"THIS TARGET IS DEAD.
  ABSOLUTION WILL CLAIM YOUR LIFE"* and *"THIS TARGET IS MISSING LIMBS. YOU WILL
  SACRIFICE YOUR OWN LIMBS."*
- The revive path is a full ritual: you collapse and **die**, the target is
  revived with a full heal, cleansed of zombie/rot states, and both of you get
  the `psyvived` buff. (It even tallies a `STATS_LUX_REVIVALS` round statistic.)
- Flavored with battle-cries (*"MY LYFE FOR YOURS! LYVE, AS DOES HE!"*).

**PERSIST** — *T4 self-sustain* (`/datum/action/cooldown/spell/psydon/persist`)
- Replaces the standard `respite` orison. **5-minute** cooldown.
- Channels up to 10 ticks of self-healing while standing still. Heals scale with
  **how hurt you are** (more brute/burn = bigger heals, up to −14 each per tick
  past 400 damage) and **the value of your worn psycross** (a silver cross gives
  −7, the golden `psicross/g` −9, the weeping cross −11 to healing values — i.e.
  more healing).
- **Costs 50 devotion per tick.** Wearing the cursed `inhumen/aalloy` psycross
  causes it to **backfire**, damaging you instead. This is how the Absolver pays
  themselves back after eating someone else's wounds.

**REDEEM** — *conversion* (`/obj/effect/proc_holder/spell/invoked/convert_psydon`)
- **Devotion 100**, **20-minute** cooldown, 10-second cast.
- Offers a non-combat-mode target the chance to **willingly renounce their faith
  and become a Psydonite**. If accepted, it strips their old miracles/devotion
  and converts their patron to Psydon. The intended "merciful" alternative to
  executing a heretic.

**Plus:** a **secular Diagnose** (`/diagnose/secular`) for reading injuries, and
the **REDEEM**-adjacent crafting recipe **Quicksilver Absolution**
(`qsabsolution`, see §7) taught at spawn.

### 3.3 Equipment

The Absolver spawns heavily kitted as a frontline medic-tank:

- **Golgatha** — the **SYON Shard Censer** on their belt (their signature relic;
  full breakdown in §7).
- **Psydon's Thorns** bracers (`psythorns`) and an **Absolver greathelm** with a
  matching blacksteel "thorns" mask.
- A psydon fencer cuirass over a heavy inq gambeson, psydon boots, psygloves, a
  silver psicross, the Absolutionist robe cloak, an Otavan satchel.
- A blessed signet ring, a leather belt and a rich coin pouch.
- **Backpack:** the Psydonic bible, 2 full bandage bundles, **2 health pots**, an
  abso arrival slip (worth **16 Marques**), a needle, a **leech**
  (`worms/leech/cheele`), and an **Inquisitor's keyring**.

### 3.4 How to Play the Absolver

You are the sect's **lifeline and logistics hub**, not a duelist (you literally
cannot start fights). The loop:

1. Stay behind your Orthodoxists. Let them take hits.
2. **WEEP** off their lesser wounds mid-fight; **ABSOLVE** to fully reset a
   dying ally (or, in extremis, trade your life to resurrect a fallen one).
3. **PERSIST** between engagements — ideally wearing the best psycross you can —
   to dump the damage you've absorbed back to zero.
4. Run the manor: cook, manage the infirmary (surgery kit is in the basement),
   craft Quicksilver to de-convert captured nitebeastes, and keep the sect
   supplied.
5. Use **REDEEM** to convert heretics you'd rather save than burn.

Your CON/WIL pool, critical resistance, no-pain-stun, and silver-blessing make
you an absurd damage sponge — which is the entire point, because that sponge is
where your allies' wounds go.

---

## 4. The Inquisition Manor

The sect spawns in a dedicated building made of four areas
(`/area/rogue/indoors/inq...`):

| Area | In-game name | What it is |
|------|--------------|------------|
| `/inq` | **The Inquisition** | Ground-floor chapel/HQ, kitchen, map room |
| `/inq/office` | **The Inquisitor's Office** | Inquisitor's quarters & admin |
| `/inq/basement` | **The Inquisition's Basement** | Cells, infirmary, sleeping quarters |
| `/inq/import` | **foreign imports** | The drop room where Marquette orders land |

The following are the **fixtures and tools physically placed in the manor on the
map** (as opposed to ordered in). Counts are approximate map placements.

### 4.1 Ground Floor — "The Inquisition" (chapel/HQ)

- **HERMES mailer** (`/obj/structure/roguemachine/mail`) — the sect's economic
  heart and shop terminal (full detail §5).
- **SCOMM stones** (`/roguemachine/scomm`, incl. a `receive_only` unit) — secure
  communications, plus a **treasury withdraw** machine (`/roguemachine/withdraw`).
- **Stone & silver psycrosses** (`/structure/fluff/psycross/psycrucifix`) — not
  decoration: a large psycross **must be nearby** to perform Test Faith / Reveal
  Allegiance interrogations and to apply Quicksilver.
- A full **kitchen**: hearth, oven, **millstone**, fermentation kegs (red wine /
  white wine / water), pans, platters, cutlery, a chef's knife & cleaver, a
  tanning rack — the Absolver's domain.
- A **map table**, knight statues, red Psydon banners, a clock, a well, and a
  graveyard nook (graves/coffins) behind cemetery bars.

### 4.2 The Office

- The **Inquisitor's start point**, double bed, fancy chairs, large desk.
- A **scomstone** (personal secure-comms stone), additional **manor keys**,
  spare **INDEXERs**, **accusation & confession** writs, a **tallowpot** for
  stamping, and spare Confessor/Inquisitor garb.
- Its own HERMES and SCOMM terminals.

### 4.3 The Basement (the working heart of the sect)

This is where most of the **tools** live and where the Orthodoxists and Absolver
spawn:

- **Holding cells** — barred windows, donjon stone doors, and
  **high-security** doors. The dungeon for the accused.
- **Infirmary** — a full **surgery kit**: bonesetter, cautery, surgery hammer,
  bone saw, scalpel, an (empty) surgery bag, needles, and bandage rolls. This is
  the Absolver's operating theatre.
- **Tools of the trade on the shelves**: spare **INDEXERs**, **inquiry
  cordage**, **accusation/confession** writs, **listening devices** and **secret
  whisperers** (the bug + relay pair), **quicksilver** plus the
  **Inquisitorial Missive** that explains how to brew more, **fyritius** flowers
  (a Quicksilver reagent), a manor key, tallow & tallowpots for stamping.
- A **forge**, a **gear painter**, and an **inquisitorial supply crate**.
- More silver psycrosses, a Psydon statue, blue votive candles, and the
  Orthodoxist/Absolver spawn landmarks.

### 4.4 Foreign Imports

A small, locked-off `import` room. **You don't stock this — the HERMES does.**
When anyone buys from the Marquette, the order physically **drops into a random
tile of this room**. It's the loading dock for everything in §5's catalog.

---

## 5. The Marque Economy — HERMES & the Marquette

The Inquisition doesn't use normal money for its gear; it runs on **Marques**, a
favor-currency earned by **doing inquisitorial work and mailing the proof back
to Otava**. The whole system runs through the **HERMES** mail machine.

### 5.1 HERMES basics

`/obj/structure/roguemachine/mail` — named "HERMES #n". For everyone it's a
mail/parcel machine (first letter every 5 minutes is free, then it costs coin;
you can wrap items into packages and mail them). For the Inquisition it's much
more: loading a **Marque coin** (`/obj/item/roguecoin/inqcoin`) opens a **secret
compartment — the Marquette** (`display_marquette`).

- The **Puritan's Lock**: the Inquisitor (anyone with `TRAIT_PURITAN`) can
  insert their key/keyring to toggle `inqonly`, restricting Marque-spending so
  only Puritans can buy. This is the leader's spending control over the sect.
- All HERMES machines on the network share the lock state.

### 5.2 Earning Marques — the writs

You earn Marques by signing inquisitorial **writs in blood** (left-click
yourself while bleeding) and mailing them through HERMES. Stamping a folded writ
with **redtallow** (the tallowpot) adds **+4 Marques**.

- **Arrival Slip** (`inqslip/arrival`) — proof you showed up. Mail it once on
  arrival. Worth **8** Marques for an Orthodoxist, **16** for an Absolver, **16**
  for an Inquisitor (so two Orthodoxists, or one senior member, can afford a
  relic).
- **Accusation** (`inqslip/accusation`, base value 4) — a request for
  haemological faith-testing. Pair a **filled INDEXER** (someone's blood) with a
  signed accusation, fold, and mail. Pays out based on whether the indexed person
  is a **pantheonist, ascendant, or nitebeaste** — and pays **bonus** Marques for
  **cursed blood** (werewolf/vampire) and indexing.
- **Confession** (`inqslip/confession`, base value 6) — an admission of guilt.
  Only the *accused* can sign it (often extracted via interrogation, see §6).
  Optionally pack in an INDEXER of their blood for more Marques.

The mail code rewards "correct" targets — members of the Cabal, Horde, Depraved,
or Freeman traits, or the excommunicated — and tracks global lists of who's been
`accused`, `confessed`, `indexed`, and whose `cursedsamples` are on file. It
quietly hands you a fresh INDEXER back when a target was already processed.

### 5.3 Spending Marques — the Marquette catalog

The Marquette (`code/modules/roguetown/roguemachine/inqports/`) is organized
into five tabs. Buying an item teleports it into the **foreign imports** room.
Selected highlights:

**✤ SUPPLIES ✤**
- The Archbishop's Allowance — 80 silver coins (16 Marques, max 3)
- The Archbishop's Bullion — 6 blessed-silver ingots (16, max 5)
- **The Archbishop's Poultice — Quicksilver** (12, max 1) — cure for cursed blood
- Otavan Bakery Special — psycross-buns + blessed water (8)
- Restoration / Lifeblood / Manna bottles, medical needles & bandages
- Smokebombs, bottlebombs, blastpowder sticks & satchel, flint

**✤ ARTICLES ✤**
- **Relic — The Crankbox, Everwarding** (16, max 1) — the Soul Churner
- **Relic — The Mirrors, Everseeing** (8, max 2) — Black Mirrors (scrying)
- **Relic — The Ballista, Eversundering** (16, max 1) — relic siegebow + silver stakes
- **Relic — The Platemaille, Everwithstanding** (16, max 1) — full Ordinator plate set
- Redtallow & tallowpots (for stamping), blessed signet rings
- **INDEXERs** (3 for 3), **Accusations**, **Confessions**, combo crates

**✤ EQUIPMENT ✤**
- Silver arrows/bolts/heavy-bolts/stakes, sunderbolt & pyrobolt quivers, siegestakes
- **Nocshade-Lenses** (anti-glare spectacles), **climbing gear**
- **Seizing Garrote** (4; hidden unless you have `TRAIT_BLACKBAGGER`)
- **Listening Device** (2) & **Secret Whisperer** (2) — the surveillance pair
- Inquiry cordage, chains, **black bags**, Psydonic bibles

**✤ WARDROBE ✤**
- Psycrosses (incl. silver), Otavan satchels, the **Psydonian Crown of Thorns**,
  chain-orle, the **Greathelms of Psydon** crate, fencer/standard/confessor/
  inspector wardrobe sets, and a lavish "Cost of Nobility" noble dress-up crate.

**✤ RELIQUARY ✤** — Puritan-flagged; the highest-end gear.

---

## 6. Interrogation Mechanics

Several roles (Inquisitor, Confessor, Psyaltrist, and via the Inspector/Ordinator
loadouts) gain two verbs under **RoleUnique.Interrogation**. Both require: a
**restrained victim grabbed in one hand**, a **silver psycross held in the
other**, and a **large psycross structure within 5 tiles**. The cross burns away
on use.

- **Test Faith** — shoves the silver cross in the victim's face (*"TO WHOM DO
  YOU PRAY!?"*) and forces them to **confess their patron** — revealing their
  true god.
- **Reveal Allegiance** ("torture_victim") — (*"CONFESS! TELL ME YOUR
  SECRETS!"*) forces the victim to blurt one of their **antagonist confession
  lines**, exposing cabalists, cultists, etc.

These pair directly with the writ economy: extract a confession, have them sign
a Confession writ in blood, INDEX their blood, and mail the lot for Marques.

The capture toolkit (garrote → black bag → cordage/chains → cell) exists to get
a live suspect into that chair in the first place.

---

## 7. The Complete Toolbox

Every notable Inquisition tool, what it does, and where it comes from.

### Investigation & Processing

- **INDEXER** (`/obj/item/inqarticles/indexer`) — a retractable blood-drawing
  ampoule. Toggle the blade, jab a target on the USE intent, and it draws blood
  over several cycles (draining ~30 blood/cycle, so dangerous on the
  blood-starved) until it clicks shut. A full INDEXER reveals the donor's
  worshipped pantheon when mailed, and screams **"CURSED BLOOD!"** if the donor
  is a werewolf/vampire (worth far more Marques). Right-click to empty it. The
  backbone of the accusation/confession economy.
- **Writs** — Arrival / Accusation / Confession slips (see §5.2).
- **Black Mirror** (`/obj/item/inqarticles/bmirror`) — a **scrying relic**.
  Open it, prick yourself on its spike to feed it blood (costs ~240 blood + 40
  brute — dangerous), then activate and **enter any living player's name** to
  remotely **scry/observe them** for a window of time (unless they have
  `TRAIT_ANTISCRYING`). 3 uses, then it shatters; a broken-but-cleaned mirror can
  be mailed back for a 2-Marque refund. Clean off the blood-fog with cloth
  between uses. From the "Mirrors, Everseeing" Marquette relic.

### Surveillance — the bug & relay pair

- **Listener** (`/obj/item/listeningdevice`) — *"An ever-attentive ear."*
  Middle-click to arm it, then **label it with up to six letters**.
  Right-click to disguise it (alpha drops, it just reads as a "thing"). While
  active it hears nearby speech and **broadcasts it to every Secret Whisperer**
  tagged with its label. Plant it where suspects talk.
- **Secret Whisperer** (`/obj/item/speakerinq`) — the receiver, disguised as a
  *"psydonian signet ring"* when worn on the ring slot. It **speaks aloud
  whatever its paired Listener hears**, in the original speaker's voice color.
  Middle-click to silence it. Wear it and eavesdrop on a bugged room from afar.

### Capture & Restraint

- **Seizing Garrote** (`/obj/item/inqarticles/garrote`) — a **non-lethal**
  apprehension tool (the Confessor's signature; also given to Inspectors). Wield
  it, GRAB intent on the **neck** to lock a chokehold, then CHOKE to drive them
  to unconsciousness via oxygen loss (double speed vs. mindless foes, faster vs.
  black-bagged targets). Victims are muted and can't be tight-grab-messaged.
  Resisting damages the cordage; if it snaps, **rethread it with inquiry
  cordage**. Deliberately gated behind training/`TRAIT_BLACKBAGGER` (slower
  without it).
- **Black Bag** (`/obj/item/clothing/head/inqarticles/blackbag`) — a
  spell-woven sack. Attack the head to **"blackbag"** a target: it **fully
  blinds** them, makes their head **immune to damage** (no cheap-frag
  decapitations), and makes them choke out faster under a garrote. Trained
  (`TRAIT_BLACKBAGGER`) bagging is twice as fast; unconscious targets bag faster
  still. Self-removal is slow; you can't be force-stripped out of it quickly.
- **Inquiry Cordage** (`/obj/item/rope/inqarticles/inquirycord`) — consecrated,
  spell-laced restraint rope. Long break-out time (8s) and very long slip-out
  (90s). Also the consumable used to **repair a snapped garrote**.
- **Chains** — heavier restraints, from the Marquette.

### The Relics (heavy gear)

- **Golgatha — the SYON Shard Censer** (`/obj/item/flashlight/flare/torch/lantern/psycenser`)
  — the Absolver's signature relic and an Inquisitor loadout option. Open it for
  a wide blue light. With the **BLESS** intent it **anoints Psydonic silver
  weapons** (boosting crit/debuffs vs. sunderable foes) and **buffs Psydonite
  allies** (Willpower/Constitution/Fortune). While lit, it **rebukes anyone who
  attacks its silver-blessed bearer** — burning them with "dying light" that
  scours mindless foes especially hard (the `syonchurn` effect) so long as they
  stay in its glow. **Danger:** using the SMASH intent while it's open **detonates
  the SYON shard in a large explosion** and gibs anyone adjacent — a last-resort
  suicide-bomb that devastates nearby Psydonites' morale.
- **Melancholic Crankbox / Soul Churner** (`/obj/item/psydonmusicbox`) — *"The
  Crankbox, Everwarding."* A two-handed music box housing **fifteen bound
  heathen souls**. Cranked, it plays a dirge that **immunizes faithful
  Psydonites/Inquisition to magic** (`churnerprotection`) and **disrupts
  spellcasting and crushes the morale** of everyone else, with patron-specific
  taunting voice-lines from the trapped souls. Non-Inquisition crankers suffer
  horror stress themselves. An inspiring musician can choose to **Harmonize**
  (quell, protect-only) or let them **Scream** (full debuff). Smashing/destroying
  it releases the souls. The faction's anti-mage trump card — keep its true
  nature secret.
- **Reliquary Box** (`/obj/structure/reliquarybox`) + **Reliquary Key** — a
  single-use red chest. Insert the bird-key and **choose one** relic:
  Crankbox (antimagic), Daybreak (silver whip), Stigmata (silver halberd),
  Apocrypha (silver greatsword), or Golgatha (the censer). A one-shot,
  choose-wisely power pickup.
- **Relic weapons** — `Stigmata` (halberd), `Eucharist`/`Creed`/`Consecratia`
  (swords/flail), `Apocrypha` (greatsword), `Providence` (relic siegebow),
  `Covenant` (greatshield), etc., handed out via Inquisitor/Ordinator/Marquette
  loadouts. All Psydonic blessed silver.

### Consumables & Cures

- **Quicksilver Poultice** (`/obj/item/quicksilver`) — *"A panacea of alchemy,
  aberrant blood, and divine silver."* Apply near a psycross to **anoint** a
  Psydonite with `TRAIT_SILVER_BLESSED` (curse protection). Crucially, it can
  **de-convert nitebeastes**: applied to a **lesser werewolf** or a (non-Lord)
  **vampire**, it burns the curse out of them and saves them — though the eldest
  werewolves and Methuselah-tier vampires reject it. The Inquisitor/Absolver get
  an extra dose out of each one. Brewable from silver ore, blessed water, cloth,
  and a fyritius bud dipped in aberrant blood (the **Inquisitorial Missive**
  found in the manor explains the rite). The Absolver also knows the
  **Quicksilver Absolution** lux-infused variant recipe.
- **Psycross-buns, blessed water, restoration/lifeblood/manna** — standard
  Marquette healing/support stock.

### Optics & Mobility

- **Nocshade-Lenses** (`/obj/item/clothing/mask/rogue/spectacles/inq`) — Otavan
  anti-glare eyepieces.
- **Climbing gear**, **grappling hooks**, **lockpick rings** — the Confessor/
  Inspector infiltration kit.

---

## 8. Quick-Start Cheat Sheet

**If you're the Inquisitor:** sign & mail your arrival slip (16 Marques),
establish the Puritan's Lock, and bankroll the sect. Investigate, track, and
direct captures. You're the diplomat *and* the executioner.

**If you're an Orthodoxist:** pick a subclass for your role — Adjudicator/
Disciple for the front line, Confessor for captures, Sojourner for magic,
Psyaltrist for support. Mail your arrival slip (8), then do legwork: bug rooms,
draw blood, escort suspects.

**If you're the Absolver:** you can't fight — you **outlast**. Stand behind the
line, **WEEP** and **ABSOLVE** wounds onto yourself, **PERSIST** to recover, run
the kitchen and infirmary, brew Quicksilver, and **REDEEM** the redeemable. Your
arrival slip is also worth 16.

**The core gameplay loop of the faction:**
> Investigate (Listener/Mirror/tracking) → Capture (garrote → black bag →
> cordage → cell) → Interrogate (Test Faith / Reveal Allegiance at a psycross) →
> Process (INDEX blood, sign writs) → Mail via HERMES for **Marques** → Spend
> Marques on the **Marquette** → repeat, escalating toward either purging the
> heretics or invoking the **Rite of Psydonian Tribunal** for the throne.

*Psydon endures.*
