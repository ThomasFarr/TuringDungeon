# Turing's Dungeon
### CS305: Advanced Computing — Final Project | Spring 2026
### **Author:** Thomas Farrell - s1340394

A dungeon-crawler quiz game that teaches **Theory of Computation** through gameplay. Fight through procedurally generated floors, answer CS theory questions to clear rooms, and defeat boss encounters to advance deeper into the dungeon.

---

## Topic

This project covers the full breadth of CS305 topics:

| Topic | Concepts Covered |
|---|---|
| DFA | State transitions, acceptance, minimization, Myhill-Nerode |
| NFA | Nondeterminism, powerset construction, equivalence to DFA |
| ε-NFA | Epsilon closures, epsilon transitions, conversion |
| Regular Expressions | Kleene star, union, concatenation, equivalence to FA |
| Pumping Lemma | Proving languages are non-regular, applying the lemma |
| Context-Free Grammars | Derivations, parse trees, ambiguity, CNF |
| Pushdown Automata | Stack operations, CFL recognition, equivalence to CFG |
| Turing Machines | Configurations, decidability, recognizability |
| Universal TM & Undecidability | Halting problem, reductions, Rice's theorem |
| P vs NP | NP-completeness, Cook-Levin, polynomial reductions |

Each topic has **24 questions** across three difficulty tiers (easy, medium, hard), totaling **240 unique questions**.

---

## How to Run

### Requirements
- Python 3.8 or higher
- pygame

### Install and Play
```bash
git clone https://github.com/ThomasFarr/TuringsDungeon.git
cd TuringsDungeon
pip install -r requirements.txt
python main.py
```

### Play in the Browser (no install)
The game can be built for the web using pygbag:
```bash
pip install pygbag
pygbag .
```
Then open `http://localhost:8000` in your browser.

---

## How to Play

1. **Select a difficulty** — Easy, Medium, or Hard (affects timer, HP, and penalties)
2. **Choose your topics** — Pick any combination of the 10 CS305 topics
3. **Pick a relic** — Choose a passive ability that buffs your run
4. **Explore the dungeon** — Navigate a branching floor map, entering rooms to answer questions
5. **Find the key** — One room per floor holds the key that unlocks the boss door
6. **Defeat the boss** — Answer a series of boss questions to advance to the next floor
7. **Visit the shop** — Spend gold earned from correct answers on upgrades between floors
8. **Go deeper** — Each floor gets harder; reach the final floor and defeat the last boss to win

### Controls

| Input | Action |
|---|---|
| Mouse | Click buttons, answer choices, room nodes |
| 1 / A, 2 / B, 3 / C, 4 / D | Select answer |
| H | Use a hint (eliminates 2 wrong choices) |
| S | Skip current question (no penalty, no points) |
| D | Toggle deep-dive explanation on feedback screen |
| ESC | Pause game |
| ENTER / SPACE | Confirm / continue |

---

## Features

### Core Gameplay
- **Branching floor maps** with 6 blueprint layouts per floor type
- **Room types**: Regular, Challenge (double stakes), Vault (gamble for gold), Campfire (heal), Treasure, Cursed, Teach It Back, Mini-Boss, Boss
- **Scaling difficulty** — timer decreases and penalties increase every 5 rooms
- **Gold economy** — earn gold from correct answers, spend in the inter-floor shop
- **Full clear bonus** — clear every room on a floor for a gold + points bonus

### Learning Features
- **Spaced repetition** — questions you answer wrong get flagged and re-inserted into later boss fights
- **Adaptive choices** — repeatedly missed questions show fewer wrong choices (3 then 2) to scaffold learning
- **No-repeat floors** — the same question never appears twice on the same floor
- **Teach It Back rooms** — given the answer, pick the matching question (reverses the recall direction)
- **Mastery surge** — answer 3+ questions from the same topic in a row for a point multiplier bonus
- **Knowledge milestones** — hit 25/50/100 correct answers per topic for timer/hint/points rewards
- **Mistake Grimoire** — pause-menu log of every wrong answer this run with explanations
- **End-of-run flashcard review** — study every missed question interactively after a run
- **Floor briefings** — pre-floor topic preview with mastery bars showing your progress
- **Deep-dive explanations** — toggle between a basic answer explanation and a full breakdown of all choices

### Gamification
- **5 passive relics** to choose from at run start (Recall Amulet, Theorist's Wand, Iron Ledger, Surge Stone, Memory Crystal)
- **Floor curses** — voluntarily accept a debuff for bonus gold (Hard Only, No Hints, Double Penalty, Dark Covenant)
- **Boss attack patterns** — bosses occasionally launch debuffs between questions (Timer Curse, Confusion Wave, Gold Drain)
- **Combo meter** — visible streak multiplier during questions
- **Did You Know cards** — CS theory fun facts displayed in the shop
- **Daily Challenge mode** — seeded run (same seed for everyone on the same date) on Hard with all topics
- **Per-topic mastery bars** in the pause menu and run stats
- **Wrong-answer pattern callout** — run stats flag if you keep picking the same wrong choice

---

## Project Structure

```
TuringsDungeon/
├── main.py          # Entry point; asyncio game loop (pygbag compatible)
├── game.py          # State machine, all game logic, DungeonRun, Player
├── renderer.py      # All pygame rendering (screens, HUD, animations)
├── questions.py     # 240-question bank across 10 topics and 3 difficulty tiers
└── requirements.txt # Dependencies (pygame)
```

---

## Dependencies

- [pygame](https://www.pygame.org/) — rendering, input, window management
- [pygbag](https://pygame-web.github.io/) — optional, for building the WebAssembly browser version

---

*CS305: Advanced Computing — Spring 2026*
