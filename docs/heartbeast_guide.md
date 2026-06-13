# Heartbeast (Chimeric Heart Beast) — Complete Q&A Guide

*The heartbeast asks philosophical questions drawn from "aspects" (flesh concepts).
Answer with the right keywords to feed it knowledge — earning blood, tech points,
happiness, and language-tier progress. This guide lists how scoring works, every
aspect + its keywords, and the full question bank. From
`code/modules/roguetown/roguemachine/heartbeast/`.*

---

## How the Q&A works

1. The beast periodically **says a question** (every ~25s when idle). It only draws
   from **aspects its hidden traits "like"**, so a given beast only asks about a
   subset each round.
2. **Attack-hand (click) it** to become its **listener** — tendrils reach toward you
   (you have a **1-minute** window). Click again any time to re-hear the question.
3. **Speak your answer out loud** within **7 tiles**. It scores your spoken message.
4. It asks at its current **Language Tier (1→4)**. Tier only changes the *wording* of
   the question (baby-talk at T1, philosophical at T4) — **the keywords are the same
   at every tier.**

### The scoring (you need ≥ 20 to pass)
| Component | Points |
|---|---|
| **Keywords** — each of the aspect's keywords found in your message, up to 2 | **+25 each (max +50)** |
| **Word count** in range (default **1–50** words; some traits narrow it) | +30 |
| **Punctuation** — end with the preferred mark (**default `?`**; traits may want `.` or `!`) | +20 |
| Quirk bonuses/penalties | varies |

- **Pass = score ≥ 20.** A single keyword (25) already passes. A perfect answer = **100**.
- **Rewards scale with score** (`score/100`): blood, happiness, **tech points = 8 × 2^(tier−1) × rack multiplier** (8/16/32/64 per tier), and **language progress** (≈2 perfect answers, or 4 mediocre, to advance a tier; max tier 4).
- **Failure (< 20):** the beast loses 5% happiness and keeps the question.

### 🎯 The optimal answer (always scores ~100)
> **Recognize the aspect from the question → write a short sentence (a handful of
> words) containing TWO of that aspect's keywords → end it with `?`.**

Example — it asks *"What is pain?"* → answer: **"Is it hurt and suffering?"**
(2 keywords = +50, in word range = +30, ends in `?` = +20 → **100**).

**Tips:**
- The question *names the aspect* (T2+ literally: "What is X?"), so the aspect is
  obvious. At T1 it's baby-talk ("Hurt? Oww?") — match it to the aspect below.
- Stuff in **2 keywords**, not more (only the first 2 count).
- Default punctuation is `?` (mirror the question). If `?` answers keep scoring low,
  the beast's trait may prefer `.` or `!` — try switching.
- Keep it **1–50 words** (basically any normal sentence). Don't ramble past 50.
- Feed it **fresh meat** to raise happiness (boosts blood output); happiness decays
  over time and on failed answers.

---

## 📜 ASPECT CHART — every aspect & its answer keywords

*Include any 2 of these words in your answer. (The aspect name is what the beast is
asking about; the keywords are what you say back.)*

| Aspect | Answer keywords (use 2) |
|---|---|
| **pain** | hurt, pain, suffering, agony, ache, torment, anguish |
| **blood** | blood, bleed, veins, life, red, flow, sacrifice |
| **fear** | fear, scared, afraid, terror, dread, panic, anxiety |
| **hunger** | hunger, food, eat, crave, starve, appetite, desire |
| **love** | love, care, affection, devotion, passion, connection, bond |
| **death** | death, die, dead, end, afterlife, mortality, rebirth |
| **time** | time, past, future, now, moment, memory, eternity |
| **dreams** | dream, sleep, vision, nightmare, unconscious, fantasy, prophecy |
| **memory** | memory, remember, forget, past, recall, nostalgia, echo |
| **truth** | truth, real, true, fact, honest, reality, authentic |
| **lies** | lie, false, deceive, illusion, trick, untrue, fiction |
| **power** | power, strong, control, authority, dominance, influence, might |
| **weakness** | weak, vulnerable, fragile, helpless, limited, frail, dependent |
| **creation** | create, make, build, form, art, invent, generate |
| **destruction** | destroy, break, ruin, end, demolish, shatter, obliterate |
| **order** | order, pattern, system, structure, arrange, organize, method |
| **chaos** | chaos, random, disorder, confusion, unpredictable, entropy, anarchy |
| **beauty** | beauty, beautiful, pretty, lovely, aesthetic, harmony, grace |
| **ugliness** | ugly, unpleasant, grotesque, hideous, repulsive, disfigured, monstrous |
| **sacrifice** | sacrifice, offer, give, lose, surrender, offerings, devotion |
| **greed** | greed, want, desire, possess, accumulate, hoard, covet |
| **justice** | justice, fair, right, law, balance, equity, retribution |
| **mercy** | mercy, forgive, compassion, kindness, pity, clemency, grace |
| **loneliness** | lonely, alone, isolated, solitude, abandoned, empty, separation |
| **companionship** | companion, friend, together, bond, connection, relationship, unity |
| **hope** | hope, optimism, expect, faith, belief, anticipation, possibility |
| **despair** | despair, hopeless, desperate, defeat, sorrow, anguish, misery |
| **courage** | courage, brave, fearless, bold, valor, heroism, fortitude |
| **cowardice** | coward, fearful, timid, afraid, hesitant, retreat, caution |
| **wisdom** | wisdom, wise, knowledge, understanding, insight, enlightenment, sagacity |
| **ignorance** | ignorance, ignore, unknowing, unaware, naive, innocent, uninformed |
| **freedom** | freedom, free, liberty, autonomy, independence, unbound, release |
| **bondage** | bondage, bound, trapped, restricted, prison, captive, constrained |
| **growth** | growth, grow, develop, evolve, mature, progress, transform |
| **decay** | decay, rot, decompose, deteriorate, wither, fade, corrupt, **pestra** |
| **transformation** | transform, change, become, metamorphosis, evolve, shift, alter |
| **identity** | identity, self, who, person, individual, essence, soul |
| **unity** | unity, one, together, whole, united, connected, harmony |

> **Note on "decay":** its T2–T4 questions are phrased about **Pestra** ("What is
> Pestra?", "What is Pestra's greatest gift?"). Answer with decay/rot keywords (or
> the word **"pestra"** itself).

---

## 📖 FULL QUESTION BANK (every question, by aspect & tier)

*Format: the beast may say any of these. Identify the aspect, answer with 2 keywords
from the chart above, ending in `?`.*

### pain
- **T1:** "Hurt? Oww?" · "Bad feel?" · "Ouch?"
- **T2:** "What is pain?" · "Why we hurt?" · "Pain good?"
- **T3:** "Does suffering have purpose?" · "Is pain a teacher?" · "How does pain change us?"
- **T4:** "What truths does agony reveal?" · "Is suffering necessary for growth?" · "How does pain shape consciousness?"

### blood
- **T1:** "Red wet?" · "Life juice?" · "Bleed?"
- **T2:** "What is blood?" · "Why blood red?" · "Blood life?"
- **T3:** "Does blood carry memory?" · "Is blood sacred?" · "What flows in veins?"
- **T4:** "What ancestral knowledge flows in blood?" · "Is blood the river of lineage?" · "Does blood remember what the mind forgets?"

### fear
- **T1:** "Scary?" · "Run hide?" · "Bad thing?"
- **T2:** "What is fear?" · "Fear good?" · "Why afraid?"
- **T3:** "Does fear protect or imprison?" · "What lies beneath terror?" · "Is fear a warning?"
- **T4:** "What truths does dread unveil?" · "Is fear the shadow of survival?" · "Does terror reveal hidden realities?"

### hunger
- **T1:** "Want food?" · "Empty tummy?" · "Eat now?"
- **T2:** "What is hunger?" · "Why we need food?" · "Hunger pain?"
- **T3:** "Is hunger more than physical?" · "What do we truly crave?" · "Does hunger drive creation?"
- **T4:** "What existential void does hunger represent?" · "Is craving flesh the engine of being?" · "What hungers drive us?"

### love
- **T1:** "Good feel?" · "Warm inside?" · "Like person?"
- **T2:** "What is love?" · "Why love hurt?" · "Love good?"
- **T3:** "Is love a binding force?" · "Does love transform?" · "What sacrifices does love demand?"
- **T4:** "Do we truly require love, or is it inner deceit?" · "Is love the fabric binding souls?" · "What divine madness is love?"

### death
- **T1:** "No more?" · "Gone away?" · "Sleep forever?"
- **T2:** "What is death?" · "After death?" · "Why die?"
- **T3:** "Is death an ending or transformation?" · "What awaits beyond the veil?" · "Does death give life meaning?"
- **T4:** "What mysteries lie in the great silence?" · "Is death the final teacher?" · "What rebirth follows dissolution?"

### time
- **T1:** "Now when?" · "Before after?" · "Day night?"
- **T2:** "What is time?" · "Time flow?" · "Can stop time?"
- **T3:** "Does time heal or erode?" · "Is the past alive in us?" · "What is the weight of moments?"
- **T4:** "What eternal now contains all of time?" · "Is memory time's anchor?" · "What dances in the spaces between moments?"

### dreams
- **T1:** "Sleep pictures?" · "Night stories?" · "Not real?"
- **T2:** "What are dreams?" · "Dreams real?" · "Why dream?"
- **T3:** "Do dreams show hidden truths?" · "What world exists behind closed eyes?" · "Are we different in dreams?"
- **T4:** "What realms do sleeping minds wander?" · "Do dreams connect collective unconscious?" · "What prophecies sleep in dreamscapes?"

### memory
- **T1:** "Remember thing?" · "Before now?" · "Old picture?"
- **T2:** "What is memory?" · "Why forget?" · "Memory true?"
- **T3:** "Do memories shape reality?" · "What is forgotten but still felt?" · "Are we our memories?"
- **T4:** "What echoes linger in ancestral memory?" · "Do memories exist outside time?" · "What truths do forgotten things hold?"

### truth
- **T1:** "Real thing?" · "Not lie?" · "True true?"
- **T2:** "What is truth?" · "Truth hurt?" · "Always truth?"
- **T3:** "Are there multiple truths?" · "What lies hide behind facts?" · "Does truth change?"
- **T4:** "What absolute reality underlies apparent truth?" · "Is truth subjective experience?" · "What remains when all lies are stripped away?"

### lies
- **T1:** "Not true?" · "Make believe?" · "False story?"
- **T2:** "What are lies?" · "Why lie?" · "Lies bad?"
- **T3:** "Do lies protect or harm?" · "What truth hides in deception?" · "Are some lies necessary?"
- **T4:** "What fundamental deceptions shape reality?" · "Do lies create new truths?" · "What hides behind the veil of falsehood?"

### power
- **T1:** "Strong?" · "Make do?" · "Boss?"
- **T2:** "What is power?" · "Get power how?" · "Power good?"
- **T3:** "Does power corrupt or reveal?" · "What is true strength?" · "Can power be shared?"
- **T4:** "What cosmic forces manifest as power?" · "Is power responsibility or freedom?" · "What ultimate authority governs existence?"

### weakness
- **T1:** "Not strong?" · "Can't do?" · "Small?"
- **T2:** "What is weakness?" · "Weakness bad?" · "Help weak?"
- **T3:** "Is vulnerability strength?" · "What grows from limitation?" · "Does weakness teach compassion?"
- **T4:** "What profound truths emerge from fragility?" · "Is surrender sometimes victory?" · "What power resides in acceptance?"

### creation
- **T1:** "Make new?" · "Build thing?" · "From nothing?"
- **T2:** "What is creation?" · "Why create?" · "Create how?"
- **T3:** "Does creation require destruction?" · "What spark begins making?" · "Is all art born of pain?"
- **T4:** "What divine impulse drives creation?" · "Does the universe dream through makers?" · "What emerges from the void of potential?"

### destruction
- **T1:** "Break thing?" · "No more?" · "Smash?"
- **T2:** "What is destruction?" · "Why destroy?" · "Destroy good?"
- **T3:** "Does destruction make space for creation?" · "What beauty exists in ruin?" · "Is ending necessary?"
- **T4:** "What cosmic cycle requires dissolution?" · "Does destruction reveal essential forms?" · "Must all be ended for us to begin anew?"

### order
- **T1:** "Things neat?" · "Place for thing?" · "Not messy?"
- **T2:** "What is order?" · "Why order good?" · "Make order?"
- **T3:** "Does order limit or protect?" · "What patterns govern reality?" · "Is chaos the enemy of order?"
- **T4:** "What cosmic structures maintain existence?" · "Does order emerge from chaos?" · "What divine mathematics govern all thing?"

### chaos
- **T1:** "All messy?" · "No pattern?" · "Things random?"
- **T2:** "What is chaos?" · "Chaos bad?" · "Why chaos?"
- **T3:** "Does chaos create freedom?" · "What order emerges from randomness?" · "Is chaos the source of novelty?"
- **T4:** "What infinite possibilities dwell in disorder?" · "Does chaos birth new realities?" · "What dances in the space between laws?"

### beauty
- **T1:** "Pretty thing?" · "Nice see?" · "Good look?"
- **T2:** "What is beauty?" · "Why beautiful?" · "Beauty where?"
- **T3:** "Is beauty subjective or universal?" · "What makes something beautiful?" · "Does beauty require imperfection?"
- **T4:** "What divine harmony manifests as beauty?" · "Does beauty reveal truths?" · "What eternal forms underlie apparent beauty?"

### ugliness
- **T1:** "Not pretty?" · "Bad look?" · "Wrong shape?"
- **T2:** "What is ugly?" · "Why ugly?" · "Ugly bad?"
- **T3:** "Does ugliness have its own beauty?" · "What truths hide in unpleasant forms?" · "Is ugliness necessary?"
- **T4:** "What profound realities manifest as ugliness?" · "Does horror contain its own awe?" · "What sacred truths wear masks of disgust?"

### sacrifice
- **T1:** "Give up?" · "Lose for other?" · "Hurt for good?"
- **T2:** "What is sacrifice?" · "Why sacrifice?" · "Sacrifice worth?"
- **T3:** "Does sacrifice create meaning?" · "What transformations require offering?" · "Is loss necessary for gain?"
- **T4:** "What exchanges demand sacrifice?" · "Does giving away create abundance?" · "What divine economy governs offering?"

### greed
- **T1:** "Want more?" · "Not share?" · "All mine?"
- **T2:** "What is greed?" · "Why greedy?" · "Greed good?"
- **T3:** "Does greed drive progress?" · "What emptiness creates wanting?" · "Is accumulation a form of poverty?"
- **T4:** "What existential lack manifests as greed?" · "Does infinite desire create finite beings?" · "What void do possessions attempt to fill?"

### justice
- **T1:** "Fair thing?" · "Good get good?" · "Bad get bad?"
- **T2:** "What is justice?" · "Justice fair?" · "Make justice?"
- **T3:** "Is justice absolute or relative?" · "Does vengeance serve justice?" · "Can mercy be just?"
- **T4:** "What balance manifests as justice?" · "Does universal law require equilibrium?" · "What scales measure deeds?"

### mercy
- **T1:** "Not punish?" · "Forgive?" · "Be kind?"
- **T2:** "What is mercy?" · "Why mercy?" · "Mercy weak?"
- **T3:** "Is mercy strength or weakness?" · "What healing comes from forgiveness?" · "Does mercy transform both given and receiver?"
- **T4:** "What grace manifests as mercy?" · "Does compassion transcend justice?" · "What kindness flows through existence?"

### loneliness
- **T1:** "All alone?" · "No friend?" · "Empty inside?"
- **T2:** "What is loneliness?" · "Why lonely?" · "Loneliness hurt?"
- **T3:** "Is solitude different from loneliness?" · "What connections alleviate isolation?" · "Does loneliness reveal our need for others?"
- **T4:** "What existential separation creates loneliness?" · "Does the soul yearn for connection?" · "What divine unity do we remember in isolation?"

### companionship
- **T1:** "With other?" · "Not alone?" · "Friend?"
- **T2:** "What is companionship?" · "Why together?" · "Alone bad?"
- **T3:** "Does connection define identity?" · "What bonds transform individuals?" · "Is companionship necessary for growth?"
- **T4:** "If nothing is alive, can one still achieve companionship?" · "Do souls recognize each other?" · "What communion exists between beings?"

### hope
- **T1:** "Maybe good?" · "Think better?" · "Not give up?"
- **T2:** "What is hope?" · "Why hope?" · "Hope help?"
- **T3:** "Does hope create reality?" · "What sustains hope in darkness?" · "Is hope a choice or feeling?"
- **T4:** "What potential manifests as hope?" · "Does hope glimpse future possibilities?" · "What promise fuels expectation?"

### despair
- **T1:** "No hope?" · "All bad?" · "Give up?"
- **T2:** "What is despair?" · "Why despair?" · "Despair end?"
- **T3:** "Does despair reveal truth?" · "What growth comes from hopelessness?" · "Is despair a necessary depth?"
- **T4:** "What existential truths manifest as despair?" · "Does the abyss gaze back?" · "What revelations come from absolute surrender?"

### courage
- **T1:** "Not scared?" · "Do anyway?" · "Be brave?"
- **T2:** "What is courage?" · "Why brave?" · "Courage good?"
- **T3:** "Does courage require fear?" · "What actions define bravery?" · "Is courage a choice or quality?"
- **T4:** "What strength manifests as courage?" · "Does valor transcend self-preservation?" · "What overcomes terror?"

### cowardice
- **T1:** "Too scared?" · "Run away?" · "Not do?"
- **T2:** "What is cowardice?" · "Why coward?" · "Coward bad?"
- **T3:** "Does cowardice preserve life?" · "What wisdom hides in caution?" · "Is fear sometimes wise?"
- **T4:** "What survival instinct manifests as cowardice?" · "Does prudence disguise as fear?" · "What feeling guides retreat?"

### wisdom
- **T1:** "Know things?" · "Smart?" · "Understand?"
- **T2:** "What is wisdom?" · "Get wisdom?" · "Wise good?"
- **T3:** "Does wisdom come from experience?" · "Can wisdom be taught?" · "Is wisdom different from knowledge?"
- **T4:** "What understanding manifests as wisdom?" · "Does truth resonate through ages?" · "What eternal patterns do sages perceive?"

### ignorance
- **T1:** "Not know?" · "Dumb?" · "No understand?"
- **T2:** "What is ignorance?" · "Why ignorant?" · "Ignorance bad?"
- **T3:** "Does ignorance protect or limit?" · "What freedoms come from not knowing?" · "Is some ignorance bliss?"
- **T4:** "What necessary veils manifest as ignorance?" · "Does unknowing create space for wonder?" · "What mysteries require not knowing?"

### freedom
- **T1:** "Do anything?" · "No rules?" · "Free?"
- **T2:** "What is freedom?" · "Why free?" · "Freedom good?"
- **T3:** "Does freedom require responsibility?" · "Can one be free alone?" · "Is absolute freedom possible?"
- **T4:** "What liberation manifests as freedom?" · "Does the soul yearn for unbounded existence?" · "What divine autonomy underlies being?"

### bondage
- **T1:** "Not free?" · "Trapped?" · "Can't move?"
- **T2:** "What is bondage?" · "Why trapped?" · "Bondage bad?"
- **T3:** "Do limitations create meaning?" · "What freedoms exist within constraints?" · "Are all beings bound in some way?"
- **T4:** "What necessary structures manifest as bondage?" · "Does form require limitation?" · "What divine laws bind existence?"

### growth
- **T1:** "Get bigger?" · "Change good?" · "Learn more?"
- **T2:** "What is growth?" · "Why grow?" · "Grow how?"
- **T3:** "Does growth require discomfort?" · "What transformations are necessary?" · "Can growth be forced?"
- **T4:** "What evolution manifests as growth?" · "Does being unfold through becoming?" · "What divine potential seeks expression?"

### decay (Pestra)
- **T1:** "Get old?" · "Break down?" · "Not work?"
- **T2:** "What is Pestra?" · "Why Pestra?" · "Pestra bad?"
- **T3:** "Does Pestra's decay make space for new life?" · "What beauty exists in deterioration?" · "Is ending part of cycles?"
- **T4:** "What is Pestra's greatest gift?" · "Does Pestra's dissolution serve renewal?" · "What ancient patterns does Pestra require return to source?"

### transformation
- **T1:** "Change thing?" · "Become different?" · "Not same?"
- **T2:** "What is transformation?" · "Why change?" · "Transform how?"
- **T3:** "Does transformation require destruction?" · "What remains constant through change?" · "Are we the same after transformation?"
- **T4:** "What metamorphosis manifests as change?" · "Does being dance between forms?" · "What eternal essence wears temporary shapes?"

### identity
- **T1:** "Who me?" · "I am?" · "Self?"
- **T2:** "What is identity?" · "Why self?" · "Identity change?"
- **T3:** "Are we our memories or actions?" · "What defines personhood?" · "Does identity exist independently?"
- **T4:** "What eternal self manifests as identity?" · "Does consciousness wear temporary masks?" · "What divine spark animates being?"

### unity
- **T1:** "All one?" · "Together same?" · "Not separate?"
- **T2:** "What is unity?" · "Why together?" · "Unity good?"
- **T3:** "Does unity require diversity?" · "What connects all things?" · "Can individuality exist in unity?"
- **T4:** "What oneness manifests as unity?" · "Can seperation be kept from bringing destruction?" · "What divine whole contains all parts?"

---

## The beast's feedback (so you know if you passed)

| Tier | Success sounds like | Failure sounds like |
|---|---|---|
| 1 | "Grok..." / "Know... yes..." / "Pattern... good..." | "Bad... pattern..." / "Wrong... shape..." / "Confuse... RrRrrhhh..." |
| 2 | "Understanding flows..." / "Knowledge accepted." | "Incomprehensible..." / "The meaning eludes..." |
| 3 | "The understanding flows gracefully." | "Your meaning remains obscure to me." |
| 4 | "The essence of understanding flows through me with perfect clarity." | "This answer fails to convey meaningful understanding." |

It may also visibly **pulse** — gently (moderate, score 50–74) or strongly (deeply
satisfied, 75–100). A strong pulse = near-perfect answer.

### Source files
`heart_concepts.dm` (aspects/questions/keywords), `heart_component.dm` (scoring &
rewards), `heart_beast.dm` (the structure & feeding), plus `heart_traits.dm`,
`heart_quirks.dm`, `heart_personalities.dm` (the beast's random personality that
decides which aspects it asks about and tweaks word-count/punctuation preferences).
