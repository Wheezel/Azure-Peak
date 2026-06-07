# Surgery Guide — Every Operation in the Game

*A complete reference for every surgery a physician can perform: what each one
does, where it targets, the exact step order, which tools work (and their success
%), skill requirements, and how outcomes are calculated. Values are pulled from
`code/modules/surgery/`.*

---

## How surgery works (read this first)

### Starting a surgery
1. The patient should be **lying down**, ideally on a **bed** (best) or table.
2. **Expose the body zone** — you can't cut through most armor/clothing (some
   surgical garments allow it; `TRAIT_MEDICINE_EXPERT` lets you *cauterize* through
   armor out of combat).
3. **Target the body zone** (set your selected zone) and click the patient with the
   correct tool on **help intent**. You'll be prompted to pick the procedure.
4. Perform each step in order with the right tool. Each step rolls success
   independently. (`surgery_helpers.dm`, `_surgery_step.dm`)

### The success formula
```
success = 100%  ×  tool quality %  ×  position modifier  ×  skill modifier
```

**Position modifier — your biggest free lever:**

| Patient position | Success | Speed |
|---|---|---|
| **On a bed** | **×1.0** | ×0.9 (fastest) |
| On a table | ×0.8 | ×0.95 |
| Lying (no furniture) | ×0.7 | ×1.1 |
| Standing | ×0.6 | ×1.4 (slowest) |

**Skill modifier (Medicine):** each step has a `skill_median` (usually Journeyman/
Expert). Above it you gain bonus success per level; below it you take a penalty.
At **Master** you also get −20% time, at **Legendary** −40% time. As Head Physician
you start **Legendary**, so you're above the median on everything.

**Failure consequences:** a botched step can **cause infection** — worse the lower
the roll (0–15% roll = major infection, 16–50% = infection, 51–70% = minor). This is
why position + correct tools matter even at high skill.

**Sedation:** an awake patient screams and struggles (especially on Cauterize, which
deals 25 burn). Knock them out first — **Ozium**, poppymilk, or your own **Sleep
Poison**. A sedated patient on a bed is the gold standard.

### The shared building-block steps
Most surgeries are bracketed by these. Tool success % in parentheses:

| Step | Tools (success %) | Time | Min skill | What it does |
|---|---|---|---|---|
| **Incise** | Scalpel (80), any Sharp (60) | 1.6s | Novice | Opens an incision |
| **Clamp** | Hemostat (75), Wirecutter (60), improvised (38) | 2.4s | Apprentice | Clamps bleeders |
| **Retract** | Retractor (75), Screwdriver (50), improvised (38) | 2.4s | Apprentice | Holds the wound open |
| **Saw** | Saw (80), Shovel (50), Sharp (25) | 5s | Journeyman | Saws through bone |
| **Drill** | Drill (80), Screwdriver (25) | 3s | Journeyman | Drills a puncture |
| **Cauterize** | Cautery (**100**), Welder (70), Hot item (35) | 2.4s | Novice | Seals all bleeds; **deals 25 burn**, patient screams unless sedated |

Your full **surgery bag** carries the 100%/80% versions of every tool — use them, not
the improvised substitutes.

---

# THE SURGERIES

## Trauma & wound care

### Tend Wounds (Healing Surgery)
- **Does:** heals brute and/or burn damage directly. Your main way to fix serious
  injury that potions can't keep up with.
- **Zone:** Chest. **Steps:** Incise → Clamp → Retract → **Heal (repeating)** →
  Cauterize.
- **The Heal step** comes in flavors the game picks based on damage type:
  - *Tend bruises:* 10 brute/success (+1 per 6 missing HP); advanced 20; expert 30.
  - *Tend burns:* 10 burn/success (scaling divisor improves with tier).
  - *Tend damage (combo):* 6 brute + 6 burn/success.
- **Healing multiplier by Medicine skill:** ×1.2 Journeyman, ×1.4 Expert, ×1.7
  Master, **×2.0 Legendary**. Cut by ~55% if the patient is still clothed — **strip
  the zone.**
- Repeat the Heal step until they're patched, then Cauterize to close.

### Bloodletting (Force Toxins Out)
- **Does:** removes poison. Each success **−25 toxin, −50 blood volume.** Pair with a
  blood transfusion or cheele afterward.
- **Zone:** an arm or leg. **Steps:** Incise → Clamp → **Cut Vein** (Scalpel 75 /
  Sharp 30, 5s, Journeyman) → **Bloodlet** (by hand, 80%, 6.4s, repeating).
- Use when antidotes aren't available or the toxin load is severe.

### Remove Embedded Object
- **Does:** pulls out arrows/blades/shrapnel stuck in a limb. Removes **all** embedded
  objects in the targeted part at once.
- **Zone:** any (auto-detects). **Steps:** Incise → Clamp → **Remove Object**
  (Hemostat 80 / improvised 65 / hand 50, 3.2s, Novice).
- Low skill floor — a reliable early procedure.

### Mouth-to-Mouth (CPR)
- **Does:** **heals 10 oxyloss per success.** Keeps a suffocating/just-dead patient
  oxygenated. Repeatable.
- **Zone:** Mouth (precise). Patient must be lying; you can't do it on yourself, and
  you **can't** do it if you have `TRAIT_NOBREATH` (undead/skeletal). Any item/hand
  works, 4s, no skill floor.

## Bones & joints

### Bone Setting (Fix Fracture)
- **Does:** sets a fractured bone so it can heal (patient must then rest).
- **Requires:** an active **fracture** on the part. **Zones:** skull, head, chest,
  groin, arms/hands, legs/feet.
- **Steps:** Incise → Clamp → Retract → **Set Bone** (Bonesetter 80 / hand 40, 6.4s,
  Journeyman+).

### Bone Relocation (Fix Dislocation)
- **Does:** relocates a dislocated joint.
- **Requires:** a **dislocation** on the part. **Zones:** same as above.
- **Steps:** Incise → Clamp → Retract → **Relocate Bone** (Bonesetter 90 / hand 50,
  6.4s, Apprentice+) → Cauterize.

## Limbs

### Amputation
- **Does:** severs a limb — it drops to the floor. Works on organic and robotic limbs.
- **Zones:** head, arms, legs. **Steps:** Incise → Clamp → Retract → Saw → **Amputate**
  (Scalpel 80 / Saw 60 / improvised saw 50 / Sharp 40, 6.4s, Apprentice+).
- Used to remove a rotted/ruined limb before attaching a replacement.

### Prosthetic / Limb Replacement
- **Does:** attaches a replacement limb to a **missing** body slot. Three variants:
  - **Augmentation** — attach a **robotic** limb. Steps: Incise → Clamp → Retract →
    Saw → **Replace Limb** (bodypart item, 80%, Journeyman+). The limb must match the
    patient's morphology and the empty zone.
  - **Prosthetic Replacement** — attach an organic/any limb (arms, legs, head). Step:
    **Add Prosthetic** (bodypart, 80%, 3s, Journeyman+). Morphology & zone validated;
    blocked by Necra's Vow and on Dullahan heads.
  - **Prosthetic Removal** — detach a robotic limb (arms/legs). Step: **Remove
    Prosthetic** (Saw 90%, 10s, Journeyman+).
- **Taur implant:** a special "Implant taur" step exists — only if **both legs are
  missing**, morphology-validated.

## Organs

### Organ Manipulation (Extract / Insert)
- **Does:** removes an organ from a patient, or inserts one you're holding.
- **Zones:** hard organs (skull, chest) require the Saw step; soft organs (eyes,
  mouth, stomach, groin, arms) don't.
- **Steps:** Incise → Clamp → Retract → *(Saw for hard zones)* → **Manipulate Organs**
  → Cauterize.
  - **Extract:** Hemostat 80 / improvised 70 / crowbar 65 / hand 60. Removes the
    chosen organ and drops it. (Removing a Dullahan's brain kills it.)
  - **Insert:** the organ item itself acts as the tool (80%). Calls `Insert()`.
  - Skill: Journeyman min / Expert median.
- **Mold Organs ("make organs"):** rebuild a *missing* organ from the patient's DNA
  (Hemostat 80 / crowbar 65 / improvised 40, Journeyman+). Moldable: groin organs
  (penis/vagina/testicles) and chest (breasts).

### Sever External Organs
- **Does:** cuts off a visible external organ (e.g. eyes, tongue). On success removes
  the organ and adds an artery + large slash wound; failure just adds the slash.
- After an Incision: Scalpel 80 / Saw 60 / improvised saw 50 / Sharp 40, 5s, Novice
  min / Journeyman median.

### Plastic Surgery (Reshape Face)
- **Does:** if the patient has a **disfigurement**, removes it; otherwise lets you
  **rename** them (change their face/identity). **Failure disfigures** the head and
  the patient screams.
- **Zone:** head. **Steps:** Incise → Clamp → Retract → **Reshape Face** (Scalpel 70 /
  Wirecutter 50 / Sharp 35, 6.4s, Journeyman+) → Cauterize.

## Hearth / Pestra surgeries (the special stuff)

### Cure Rot
- **Does:** burns out ordinary rot / reverses a turning zombie. Damage dealt by the
  burn shrinks with Medicine skill (**0 damage at Expert+**).
- **Zone:** chest. **Steps:** Incise → **Burn Rot** (Cautery 85 / holy symbol 85 /
  Welder 70 / hot 35, 8s, Apprentice+) → Cauterize.

### Black Rot Extirpation
- **Does:** excises **Black Rot** — the dangerous corruption normal medicine can't
  touch. Requires the `black_rot` status. Deals 50 brute (reduced by Medicine×6, to a
  floor of 0) and applies a cleansing buff; a second success accelerates the cleanse.
- **Zone:** chest. **Steps:** Incise → Clamp → Retract → **Extract Residue** (Scalpel
  **only**, 85%, 12s, **Expert+**) → Cauterize.
- This is the signature Head Physician save — only you reliably qualify.

### Extract Lux (divine essence)
- **Does:** extracts a living person's divine essence into a physical **lux** item
  (used for resurrection and lux purification). Applies a "devitalised" debuff to the
  donor; can't extract from already-devitalised targets or Tieflings.
- **Zone:** chest. **Steps:** Incise → Clamp → Retract → Saw → **Extract Lux** (Scalpel
  80, 8s, Journeyman+) → Cauterize.

### Revival (Raise the Dead)
- **Does:** resurrects a **dead** patient (heart must be present, rot cured first).
  Two methods:
  - **Infuse Lux** — uses a lux item (80%, 10s, **Expert+**). Full revive, restores
    oxy, returns the soul, applies a temporary "revived" stat penalty. Awards the
    surgeon PQ.
  - **Infuse Tick** — uses a **bloated leechtick** (80%, 10s, Apprentice+). Same
    revive, but applies a harsher "leech schizophrenia" debuff. Lower skill floor —
    the budget resurrection.
- **Zone:** chest. **Steps:** Incise → Clamp → Retract → Saw → **Infuse** → Cauterize.

---

## Quick reference — "what tool, what zone"

| Goal | Zone | Key step & best tool |
|---|---|---|
| Heal brute/burn | chest | Heal (suture), strip clothes, on a bed |
| Cure poison | arm/leg | Cut Vein (scalpel) → Bloodlet (hand) |
| Pull out an arrow | any | Remove Object (hemostat) |
| CPR | mouth | Mouth-to-Mouth (hand) |
| Set a fracture | broken part | Set Bone (bonesetter) |
| Fix a dislocation | dislocated part | Relocate Bone (bonesetter) |
| Cut off a limb | head/arm/leg | Saw → Amputate (scalpel/saw) |
| Attach a limb | empty slot | Add Prosthetic / Replace Limb (the limb) |
| Transplant an organ | chest/skull/soft | Manipulate Organs (hemostat) |
| Change a face / fix disfigurement | head | Reshape Face (scalpel) |
| Cure normal rot | chest | Burn Rot (cautery) |
| **Cure Black Rot** | chest | Extract Residue (**scalpel only**, Expert+) |
| Harvest lux | chest | Extract Lux (scalpel) |
| **Resurrect the dead** | chest | Infuse Lux / Infuse Tick |

## Golden rules
1. **Bed + sedated + stripped zone + correct tool** — do this and even risky steps
   succeed.
2. **Cauterize last** to seal bleeders (it costs 25 burn — sedate first).
3. Your **Legendary Medicine** gives ×2.0 heal, −40% time, and lets you cauterize
   through armor — lean on it.
4. A failed step **infects** the patient; low rolls infect worse. Don't operate
   standing or through clothes "to save time."

### Source files
`code/modules/surgery/surgeries/` (healing, bloodletting, fracture, dislocation,
amputation, organ_manipulation, external_organs, plastic_surgery, limb_replacement,
remove_embedded_object, mouth_to_mouth, organic_steps), `surgeries_hearth/`
(cure_rot, cure_black_rot, extract_lux, revival, revival_big_fat_tick), and
`_surgery_step.dm` / `surgery_helpers.dm` for the success math.
