"""
game.py  —  Turing's Dungeon game state machine and logic
"""
import pygame
import random
from collections import namedtuple
from enum import Enum, auto
from questions import QUESTION_BANK, TOPICS, TOPIC_ORDER


class State(Enum):
    TITLE             = auto()
    DIFFICULTY_SELECT = auto()
    TOPIC_SELECT      = auto()
    DUNGEON_MAP       = auto()
    IN_ROOM           = auto()
    FEEDBACK          = auto()
    BOSS_INTRO        = auto()
    BOSS_RESULT       = auto()
    SHOP              = auto()
    SPECIAL_ROOM      = auto()   # campfire or treasure room (no question)
    CAMPFIRE_CHOICE   = auto()   # player picks heal vs time bonus
    VAULT_GAMBLE      = auto()   # player picks safe gold vs double-or-nothing
    PAUSED            = auto()   # pause overlay (not available in IN_ROOM)
    RUN_STATS         = auto()   # detailed end-of-run stats
    BOSS_GATE         = auto()   # lock/gate cinematic before boss intro
    FLOOR_BRIEFING    = auto()   # topic preview shown before each floor
    GRIMOIRE          = auto()   # pause-menu log of wrong answers this run
    FLASHCARD_REVIEW  = auto()   # interactive wrong-Q study after run stats
    RELIC_SELECT      = auto()   # Feature 8: pick passive relic at run start
    BOSS_ATTACK       = auto()   # Feature 11: boss attack cinematic between boss Qs
    GAME_OVER         = auto()
    VICTORY           = auto()


class RoomType(Enum):
    REGULAR   = "regular"
    CAMPFIRE  = "campfire"   # heal room (renamed from REST), no question
    CHALLENGE = "challenge"  # double stakes
    VAULT     = "vault"      # gold bonus on correct
    TREASURE  = "treasure"   # instant gold, no question
    MINI_BOSS = "mini_boss"  # hard question, replaces boss on milestone floors
    BOSS      = "boss"       # final stage of every normal floor
    CURSED       = "cursed"        # looks regular until entered; double penalty, 3x pts
    TEACH_IT_BACK = "teach_it_back"  # show answer, pick the matching question


# ─────────────────── Constants ───────────────────
MAX_FLOORS = 15   # default; actual = len(selected_topics) * 5


# ─────────────────── Floor blueprints (graph-based) ──────────────────────────
# Each blueprint defines a graph of rooms:
#   nodes = list of (col, row, is_branch)
#     col: 0=entrance, max=boss; row: 0=center, ±1/±2=above/below
#     is_branch: True for off-main-path rooms (more likely special rooms)
#   edges = list of (i, j) bidirectional connections
#   boss: index of the boss/mini-boss room (always rightmost col)
#   entrance: index of the starting room (always 0)
#
# Room types are assigned dynamically; main-path rooms are mostly REGULAR,
# branch rooms are weighted toward CAMPFIRE/TREASURE/CHALLENGE.
# The key is hidden in one room (weighted toward branches).

_BPT = namedtuple('_BPT', ['nodes', 'edges', 'boss', 'entrance'])
_F   = False   # main-path node
_X   = True    # branch node

_BLUEPRINTS_NORMAL = [
    # A: boss at main-path end; two short branches at different heights
    _BPT(
        nodes=[(0,0,_F),(1,0,_F),(2,0,_F),(3,0,_F),(4,0,_F),(5,0,_F),
               (1,1,_X),(3,-1,_X)],
        edges=[(0,1),(1,2),(2,3),(3,4),(4,5),(1,6),(3,7)],
        boss=5, entrance=0),
    # B: boss at end of lower branch; main path terminates without boss
    _BPT(
        nodes=[(0,0,_F),(1,0,_F),(2,0,_F),(3,0,_F),(4,0,_F),
               (2,1,_X),(3,1,_X),(4,1,_X)],
        edges=[(0,1),(1,2),(2,3),(3,4),(2,5),(5,6),(6,7)],
        boss=7, entrance=0),
    # C: boss at end of upper branch; small lower branch for variety
    _BPT(
        nodes=[(0,0,_F),(1,0,_F),(2,0,_F),(3,0,_F),(4,0,_F),
               (3,-1,_X),(4,-1,_X),(1,1,_X)],
        edges=[(0,1),(1,2),(2,3),(3,4),(3,5),(5,6),(1,7)],
        boss=6, entrance=0),
    # D: boss at main-path end; two-room branch off early
    _BPT(
        nodes=[(0,0,_F),(1,0,_F),(2,0,_F),(3,0,_F),(4,0,_F),(5,0,_F),
               (1,1,_X),(2,1,_X)],
        edges=[(0,1),(1,2),(2,3),(3,4),(4,5),(1,6),(6,7)],
        boss=5, entrance=0),
    # E: boss at end of lower branch; upper single-room branch
    _BPT(
        nodes=[(0,0,_F),(1,0,_F),(2,0,_F),(3,0,_F),(4,0,_F),
               (3,1,_X),(4,1,_X),(1,-1,_X)],
        edges=[(0,1),(1,2),(2,3),(3,4),(3,5),(5,6),(1,7)],
        boss=6, entrance=0),
    # F: boss at main-path end; branches above and below at different columns
    _BPT(
        nodes=[(0,0,_F),(1,0,_F),(2,0,_F),(3,0,_F),(4,0,_F),(5,0,_F),
               (2,1,_X),(4,-1,_X)],
        edges=[(0,1),(1,2),(2,3),(3,4),(4,5),(2,6),(4,7)],
        boss=5, entrance=0),
]

_BLUEPRINTS_MILESTONE = [
    # Boss at main-path end; single short branch
    _BPT(
        nodes=[(0,0,_F),(1,0,_F),(2,0,_F),(3,0,_F),(1,1,_X)],
        edges=[(0,1),(1,2),(2,3),(1,4)],
        boss=3, entrance=0),
    # Boss at main-path end; branch above
    _BPT(
        nodes=[(0,0,_F),(1,0,_F),(2,0,_F),(3,0,_F),(2,-1,_X)],
        edges=[(0,1),(1,2),(2,3),(2,4)],
        boss=3, entrance=0),
    # Boss at end of lower branch; main path is shorter dead end
    _BPT(
        nodes=[(0,0,_F),(1,0,_F),(2,0,_F),(1,1,_X),(2,1,_X)],
        edges=[(0,1),(1,2),(1,3),(3,4)],
        boss=4, entrance=0),
    # Boss at end of lower branch; main path plus upper branch
    _BPT(
        nodes=[(0,0,_F),(1,0,_F),(2,0,_F),(3,0,_F),(2,1,_X),(3,1,_X)],
        edges=[(0,1),(1,2),(2,3),(2,4),(4,5)],
        boss=5, entrance=0),
]

_BLUEPRINTS_FINAL = [
    # Boss at main-path end; three branches at different positions
    _BPT(
        nodes=[(0,0,_F),(1,0,_F),(2,0,_F),(3,0,_F),(4,0,_F),(5,0,_F),(6,0,_F),
               (1,1,_X),(3,1,_X),(5,-1,_X)],
        edges=[(0,1),(1,2),(2,3),(3,4),(4,5),(5,6),(1,7),(3,8),(5,9)],
        boss=6, entrance=0),
    # Boss at end of a long lower branch; main path shorter
    _BPT(
        nodes=[(0,0,_F),(1,0,_F),(2,0,_F),(3,0,_F),(4,0,_F),(5,0,_F),
               (2,1,_X),(3,1,_X),(4,1,_X),(5,1,_X),(3,-1,_X)],
        edges=[(0,1),(1,2),(2,3),(3,4),(4,5),(2,6),(6,7),(7,8),(8,9),(3,10)],
        boss=9, entrance=0),
    # Boss at end of deep upper branch; main path plus lower branch
    _BPT(
        nodes=[(0,0,_F),(1,0,_F),(2,0,_F),(3,0,_F),(4,0,_F),(5,0,_F),
               (3,-1,_X),(4,-1,_X),(5,-1,_X),(6,-1,_X),(2,1,_X)],
        edges=[(0,1),(1,2),(2,3),(3,4),(4,5),(3,6),(6,7),(7,8),(8,9),(2,10)],
        boss=9, entrance=0),
]


# ─────────────────── Boss scaling helpers ─────────────────────────────────────
def boss_q_count(floor: int, max_floors: int = MAX_FLOORS) -> int:
    """Number of boss questions on the given floor (scales with depth)."""
    if floor >= max_floors: return 5   # final boss always 5 questions
    if floor >= 13: return 5
    if floor >= 8:  return 4
    return 3


def boss_needed_count(floor: int, difficulty: str, max_floors: int = MAX_FLOORS) -> int:
    """How many boss questions must be answered correctly to win."""
    total = boss_q_count(floor, max_floors)
    if floor >= max_floors:            # final boss: 3-of-5 regardless of difficulty
        return 3
    if difficulty == "easy":   return max(1, round(total / 3))
    if difficulty == "medium": return max(1, round(total * 2 / 3))
    return total                       # hard: all required


# ─────────────────── Difficulty catalogue ─────────────────────────────────────
DIFFICULTIES = {
    "easy": {
        "label":          "EASY",
        "timer":          45.0,
        "start_hp":       120,
        "wrong_penalty":  10,
        "hints":          5,
        "skips":          2,
        "boss_needed":    1,
        "timer_decay":    0.5,
        "penalty_growth": 1,
        "timer_min":      15.0,
        "penalty_max":    25,
        "bullets": [
            "45 sec / question",
            "120 starting HP",
            "-10 HP on wrong answer",
            "5 hints  +  2 skips",
            "Boss: 1-of-3 correct to win",
            "Foundational questions first",
            "Harder Qs unlock as you progress",
            "Scaling: -0.5s / +1 HP / 5 rooms",
        ],
    },
    "medium": {
        "label":          "MEDIUM",
        "timer":          30.0,
        "start_hp":       100,
        "wrong_penalty":  20,
        "hints":          3,
        "skips":          0,
        "boss_needed":    2,
        "timer_decay":    1.0,
        "penalty_growth": 2,
        "timer_min":      12.0,
        "penalty_max":    40,
        "bullets": [
            "30 sec / question",
            "100 starting HP",
            "-20 HP on wrong answer",
            "3 hints to start",
            "Boss: 2-of-3 correct to win",
            "Easy + medium Qs from floor 1",
            "Hard Qs unlock at 1/3 progress",
            "Scaling: -1s / +2 HP / 5 rooms",
        ],
    },
    "hard": {
        "label":          "HARD",
        "timer":          20.0,
        "start_hp":       80,
        "wrong_penalty":  30,
        "hints":          1,
        "skips":          0,
        "boss_needed":    3,
        "timer_decay":    1.5,
        "penalty_growth": 3,
        "timer_min":      8.0,
        "penalty_max":    55,
        "bullets": [
            "20 sec / question",
            "80 starting HP",
            "-30 HP on wrong answer",
            "1 hint to start",
            "Boss: ALL questions correct",
            "All question tiers from floor 1",
            "Maximum depth immediately",
            "Scaling: -1.5s / +3 HP / 5 rooms",
        ],
    },
}

DIFFICULTY_ORDER = ["easy", "medium", "hard"]


# ─────────────────── Relic catalogue (Feature 8) ──────────────────────────────
RELICS = {
    "recall_amulet": {
        "name":  "Recall Amulet",
        "desc":  "Weak-pool questions reappear after 2 wrong answers (not 3). Boss always opens with a weak question if one exists.",
        "icon":  "RECALL",
        "color": (200, 140, 255),
    },
    "theorists_wand": {
        "name":  "Theorist's Wand",
        "desc":  "Gain +3 seconds of timer bonus for each correct answer (up to +30s total).",
        "icon":  "WAND",
        "color": (60, 200, 255),
    },
    "iron_ledger": {
        "name":  "Iron Ledger",
        "desc":  "Wrong answers cost 60 gold instead of HP. If you cannot pay, you take damage normally.",
        "icon":  "LEDGER",
        "color": (180, 180, 220),
    },
    "surge_stone": {
        "name":  "Surge Stone",
        "desc":  "Mastery surge triggers at 2 consecutive correct answers per topic (not 3). Surge bonus is +7% points.",
        "icon":  "SURGE",
        "color": (30, 200, 180),
    },
    "memory_crystal": {
        "name":  "Memory Crystal",
        "desc":  "Earn +1 Hint for every 8 correct answers. Bonus shown in HUD.",
        "icon":  "CRYST",
        "color": (255, 195, 50),
    },
}
RELIC_ORDER = ["recall_amulet", "theorists_wand", "iron_ledger", "surge_stone", "memory_crystal"]


# ─────────────────── Did You Know facts (Feature 7) ───────────────────────────
DID_YOU_KNOW = [
    "The pumping lemma can prove a language is NOT regular — but can never prove it IS regular.",
    "Every NFA converts to a DFA via the powerset construction, potentially with exponentially more states.",
    "The Church-Turing thesis is not a theorem — it cannot be proven because 'computation' lacks a formal definition outside TMs.",
    "Rice's Theorem (1953): no nontrivial property of what a Turing machine computes is decidable.",
    "The halting problem is undecidable, but IS recognizable (semi-decidable). Its complement is NOT recognizable.",
    "Every context-free language can be parsed in O(n³) time using the CYK algorithm.",
    "ε-NFA → NFA → DFA is a chain of power-preserving conversions — all three recognize exactly the regular languages.",
    "The Cook-Levin theorem (1971) proved SAT is NP-complete, founding the theory of NP-hardness.",
    "P = NP would imply polynomial-time algorithms exist for all problems currently requiring exponential search.",
    "The Myhill-Nerode theorem gives an exact characterization of regular languages via equivalence classes of strings.",
    "Deterministic and nondeterministic Turing machines recognize the same class of languages — unlike finite automata!",
    "The intersection of two context-free languages is NOT always context-free — CFLs are not closed under intersection.",
    "Savitch's theorem shows NPSPACE = PSPACE — nondeterminism buys nothing beyond polynomial space.",
    "A pushdown automaton with two stacks has the same power as a Turing machine.",
    "Every regular language is context-free; every CFL is decidable; every decidable language is recognizable.",
    "The Busy Beaver function grows faster than any computable function — it is not Turing-computable.",
    "The complement of a recognizable language may not be recognizable — but the complement of a decidable language is always decidable.",
    "Linear-bounded automata recognize exactly the context-sensitive languages, one step above CFLs in the Chomsky hierarchy.",
    "Gödel's incompleteness theorems and the halting problem both exploit the same trick: self-referential statements.",
    "The star height of a regular expression is the maximum nesting depth of Kleene stars — linked to loop complexity.",
    "Regular expressions and DFAs have equal expressive power — a fact called Kleene's theorem.",
    "Ogden's lemma is a stronger CFL pumping lemma requiring at least one 'marked' position in the pumped segment.",
    "PSPACE contains both P and NP; TQBF (quantified Boolean formula) is PSPACE-complete.",
    "The halting problem reduces to almost every other undecidable problem — it is the canonical hard problem.",
    "DFA minimization via Myhill-Nerode produces the unique (up to isomorphism) minimal DFA for any regular language.",
]


# ─────────────────── Shop catalogue ───────────────────────────────────────────
# Gold (player.gold) is the shop currency; score is a vanity metric.
SHOP_ITEMS = [
    {
        "key":  "hp_up",
        "name": "Max HP  +20",
        "desc": "Raises your maximum HP by 20 and immediately heals 20.",
        "icon": "HP+",
        "base": 320,
        "inc":  180,
    },
    {
        "key":  "time_up",
        "name": "+10s Per Question",
        "desc": "Adds 10 seconds to the timer for every question.",
        "icon": "TIME",
        "base": 280,
        "inc":  200,
    },
    {
        "key":  "point_boost",
        "name": "+25% Points",
        "desc": "All correct answers award 25% more points (stacks).",
        "icon": "PTS+",
        "base": 420,
        "inc":  280,
    },
    {
        "key":  "streak_heal",
        "name": "Streak Healing",
        "desc": "Heal +3 HP per correct answer while streak is 3 or higher.",
        "icon": "HEAL",
        "base": 240,
        "inc":  180,
    },
    {
        "key":  "hint",
        "name": "Buy a Hint",
        "desc": "Grants +1 hint charge. Hints eliminate 2 wrong choices.",
        "icon": "HINT",
        "base": 160,
        "inc":  100,
    },
    {
        "key":  "skip",
        "name": "Question Skip",
        "desc": "Grants +1 skip. Skip any question with no penalty.",
        "icon": "SKIP",
        "base": 220,
        "inc":  150,
    },
    {
        "key":  "iron_will",
        "name": "Iron Will",
        "desc": "Once: a killing blow leaves you at 1 HP. 3-floor cooldown.",
        "icon": "IRON",
        "base": 560,
        "inc":  400,
    },
    {
        "key":  "scholar_mark",
        "name": "Scholar's Mark",
        "desc": "Every 5-streak lowers wrong-answer penalty by 1 (up to 3x).",
        "icon": "MARK",
        "base": 500,
        "inc":  450,
    },
    {
        "key":  "scholar_tome",
        "name": "Scholar's Tome",
        "desc": "Once: saves your streak when you answer wrong.  Single use.",
        "icon": "TOME",
        "base": 380,
        "inc":  300,
    },
    {
        "key":  "dungeon_sense",
        "name": "Dungeon Sense",
        "desc": "Reveals which room holds the key on the current floor.",
        "icon": "SENS",
        "base": 200,
        "inc":  160,
    },
]


def item_price(key: str, shop_buys: dict, discount: bool = False) -> int:
    for it in SHOP_ITEMS:
        if it["key"] == key:
            base = it["base"] + it["inc"] * shop_buys.get(key, 0)
            if discount:
                base = int(base * 0.80)   # 20% off
            return base
    return 9999


# ─────────────────── Player ───────────────────────────────────────────────────
class Player:
    def __init__(self, difficulty: str = "medium"):
        dc = DIFFICULTIES[difficulty]

        self.difficulty    = difficulty
        self.max_hp        = dc["start_hp"]
        self.hp            = self.max_hp
        self.score         = 0          # vanity score — never spent
        self.gold          = 0          # shop currency
        self.hints         = dc["hints"]
        self.skips         = dc["skips"]

        self.streak        = 0
        self.best_streak   = 0

        self.question_time = dc["timer"]
        self.wrong_penalty = dc["wrong_penalty"]
        self.boss_needed   = dc["boss_needed"]

        self.point_mult    = 1.0
        self.streak_heal   = 0

        # Iron Will
        self.iron_will_charges  = 0
        self.iron_will_cooldown = 0

        # Scholar's Mark
        self.scholar_mark_stacks     = 0
        self.scholar_mark_reductions = 0

        self.shop_buys = {it["key"]: 0 for it in SHOP_ITEMS}

        # New consumable fields
        self.scholar_tome_charges  = 0    # streak-save charges
        self.room_time_bonus       = 0.0  # extra seconds granted to next room
        self.dungeon_sense_charges = 0    # key-reveal charges (consumed on floor gen)

    def take_damage(self, amount: int):
        self.hp = max(0, self.hp - amount)

    def heal(self, amount: int):
        self.hp = min(self.max_hp, self.hp + amount)

    def break_streak(self):
        self.streak = 0

    def extend_streak(self):
        self.streak     += 1
        self.best_streak = max(self.best_streak, self.streak)

    @property
    def streak_bonus(self) -> float:
        return min(self.streak, 10) * 0.10

    @property
    def is_dead(self) -> bool:
        return self.hp <= 0

    def calc_points(self, base: int, apply_streak: bool = True) -> int:
        mult = self.point_mult
        if apply_streak:
            mult *= (1.0 + self.streak_bonus)
        return max(1, int(base * mult))

    @property
    def effective_mult(self) -> float:
        return self.point_mult * (1.0 + self.streak_bonus)


# ─────────────────── DungeonRun ───────────────────────────────────────────────
_TIER_RANGES = {
    "easy":   (0,  8),
    "medium": (5,  13),
    "hard":   (10, 24),
}


class DungeonRun:
    """
    Multi-floor dungeon.
    Floor count = len(selected_topics) * 5  (min 5).
    Each floor uses a preset branching blueprint with 3-5 stages.
    Every 5th floor (except the last) has a MINI_BOSS replacing the boss.
    Questions are drawn from a shuffled combined pool of all selected topics.
    """

    def __init__(self, selected_topics: list, start_difficulty: str):
        self.selected_topics  = selected_topics
        self.start_difficulty = start_difficulty

        # Dynamic floor count: each topic adds 5 floors
        self.max_floors = max(5, len(selected_topics) * 5)

        # Floor tracking
        self.floor = 1

        # Floor graph: list of room dicts
        # Each room: {'col', 'row', 'is_branch', 'rt': RoomType, 'cleared': bool, 'adj': [int]}
        self.graph:        list = []
        self.entrance_idx: int  = 0
        self.boss_idx:     int  = -1
        self.key_room_idx: int  = -1
        self.has_key:      bool = False
        self.active_room_idx: int = -1   # index of room currently being played (-1 = none)

        # Boss fight state
        self.boss_q_idx     = 0
        self.boss_correct   = 0
        self._boss_pool_idx = 0

        # Learning feature: no-repeat per floor
        self._floor_used_q_hashes: set  = set()

        # Learning feature: weak pool (wrong questions for boss injection + flashcards)
        self._weak_pool:       list = []   # list of question dicts answered wrong this run
        self._weak_pool_keys:  set  = set()  # set of hash-keys already in _weak_pool
        self._q_consec_wrong:  dict = {}   # hash_key → consecutive wrong streak
        self._boss_weak_q:     dict = None   # weak-pool question to inject in next boss
        self._boss_weak_injected: bool = False

        # Build per-tier regular question pools
        self._tier_pools: dict = {}
        for tier, (s, e) in _TIER_RANGES.items():
            pool = []
            for t in selected_topics:
                for q in QUESTION_BANK[t]["regular"][s:e]:
                    tagged = dict(q)
                    tagged["_topic"] = t
                    tagged["_tier"]  = tier
                    pool.append(tagged)
            random.shuffle(pool)
            self._tier_pools[tier] = pool

        # Boss pool — one tier above player difficulty
        boss_tier = "medium" if start_difficulty == "easy" else "hard"
        bs, be    = _TIER_RANGES[boss_tier]
        boss_pool = []
        for t in selected_topics:
            for q in QUESTION_BANK[t]["regular"][bs:be]:
                tagged = dict(q); tagged["_topic"] = t; tagged["_tier"] = boss_tier
                boss_pool.append(tagged)
        random.shuffle(boss_pool)
        self._boss_pool = boss_pool

        # Mini-boss pool — always hard tier
        hs, he  = _TIER_RANGES["hard"]
        mb_pool = []
        for t in selected_topics:
            for q in QUESTION_BANK[t]["regular"][hs:he]:
                tagged = dict(q); tagged["_topic"] = t; tagged["_tier"] = "hard"
                mb_pool.append(tagged)
        if not mb_pool:
            mb_pool = list(boss_pool)
        random.shuffle(mb_pool)
        self._mini_boss_pool: list = mb_pool
        self._mini_boss_idx:  int  = 0

        # Active combined regular pool
        self._active_pool: list = []
        self._pool_idx:    int  = 0
        self._rebuild_active_pool()

        # Generate first floor's layout
        self._generate_floor()

    # ── tier management ─────────────────────────────────────────────────────
    def unlocked_tiers(self) -> list:
        floors_done = self.floor - 1
        sd          = self.start_difficulty
        third       = max(1, self.max_floors // 3)
        two_thirds  = max(2, 2 * self.max_floors // 3)
        if sd == "hard":
            return ["easy", "medium", "hard"]
        elif sd == "medium":
            if floors_done < third:
                return ["easy", "medium"]
            return ["easy", "medium", "hard"]
        else:   # easy
            if floors_done < third:
                return ["easy"]
            elif floors_done < two_thirds:
                return ["easy", "medium"]
            return ["easy", "medium", "hard"]

    def _rebuild_active_pool(self):
        tiers = self.unlocked_tiers()
        pool  = []
        for t in tiers:
            pool.extend(self._tier_pools[t])
        random.shuffle(pool)
        self._active_pool = pool
        self._pool_idx    = 0

    # ── floor graph generation ───────────────────────────────────────────────
    def _generate_floor(self):
        """Build a new floor graph from a random blueprint."""
        fl       = self.floor
        is_final = (fl >= self.max_floors)
        is_ms    = (fl % 5 == 0 and not is_final)

        if is_final:
            bp = random.choice(_BLUEPRINTS_FINAL)
        elif is_ms:
            bp = random.choice(_BLUEPRINTS_MILESTONE)
        else:
            bp = random.choice(_BLUEPRINTS_NORMAL)

        # Build nodes
        self.graph = [
            {'col': col, 'row': row, 'is_branch': br,
             'rt': RoomType.REGULAR, 'cleared': False, 'adj': []}
            for (col, row, br) in bp.nodes
        ]
        # Build bidirectional adjacency
        for (i, j) in bp.edges:
            self.graph[i]['adj'].append(j)
            self.graph[j]['adj'].append(i)

        self.entrance_idx    = bp.entrance
        self.boss_idx        = bp.boss
        self.has_key         = False
        self.key_revealed    = False
        self.active_room_idx = -1

        # Assign boss room type
        boss_rt = RoomType.MINI_BOSS if is_ms else RoomType.BOSS
        self.graph[self.boss_idx]['rt'] = boss_rt

        # Assign types to non-boss rooms
        for i, room in enumerate(self.graph):
            if i == self.boss_idx:
                continue
            if room['is_branch']:
                room['rt'] = random.choices(
                    [RoomType.CAMPFIRE, RoomType.TREASURE, RoomType.CHALLENGE,
                     RoomType.VAULT,    RoomType.CURSED,   RoomType.TEACH_IT_BACK,
                     RoomType.REGULAR],
                    weights=[10, 10, 9, 4, 5, 6, 56], k=1)[0]
            else:
                room['rt'] = random.choices(
                    [RoomType.REGULAR, RoomType.VAULT, RoomType.CHALLENGE,
                     RoomType.TEACH_IT_BACK],
                    weights=[72, 8, 14, 6], k=1)[0]

        # Cap vault rooms at 1 per floor
        _vault_rooms = [i for i, _r in enumerate(self.graph)
                        if _r.get('rt') == RoomType.VAULT]
        for _vi in _vault_rooms[1:]:
            self.graph[_vi]['rt'] = RoomType.REGULAR

        # Place key — weighted 65 % toward branch rooms
        non_boss  = [i for i in range(len(self.graph)) if i != self.boss_idx]
        branches  = [i for i in non_boss if self.graph[i]['is_branch']]
        main_path = [i for i in non_boss if not self.graph[i]['is_branch']]
        if branches and random.random() < 0.65:
            self.key_room_idx = random.choice(branches)
        elif main_path:
            self.key_room_idx = random.choice(main_path)
        else:
            self.key_room_idx = random.choice(non_boss)

    # ── room graph properties ────────────────────────────────────────────────
    @property
    def accessible_rooms(self) -> list:
        """Uncleared rooms the player can currently enter (adjacent to a cleared room, or entrance)."""
        result = []
        for i, room in enumerate(self.graph):
            if room['cleared']:
                continue
            if i == self.entrance_idx:
                result.append(i)
            else:
                for adj_i in room['adj']:
                    if self.graph[adj_i]['cleared']:
                        result.append(i)
                        break
        return result

    @property
    def current_room_type(self) -> RoomType:
        if self.active_room_idx < 0 or self.active_room_idx >= len(self.graph):
            return RoomType.REGULAR
        return self.graph[self.active_room_idx]['rt']

    @property
    def is_boss_room(self) -> bool:
        return self.active_room_idx == self.boss_idx

    @property
    def is_full_clear(self) -> bool:
        return all(r['cleared'] for r in self.graph)

    @property
    def non_boss_total(self) -> int:
        return sum(1 for i in range(len(self.graph)) if i != self.boss_idx)

    @property
    def non_boss_cleared(self) -> int:
        return sum(1 for i, r in enumerate(self.graph)
                   if i != self.boss_idx and r['cleared'])

    # ── question access ─────────────────────────────────────────────────────
    @property
    def current_question(self) -> dict:
        if self.is_boss_room:
            return self._boss_pool[self._boss_pool_idx % len(self._boss_pool)]
        return self._active_pool[self._pool_idx % max(1, len(self._active_pool))]

    @property
    def mini_boss_question(self) -> dict:
        return self._mini_boss_pool[self._mini_boss_idx % len(self._mini_boss_pool)]

    @property
    def current_topic(self) -> str:
        if not self._active_pool:
            return self.selected_topics[0] if self.selected_topics else "DFA"
        if self.is_boss_room:
            return self._boss_pool[self._boss_pool_idx % len(self._boss_pool)].get(
                "_topic", self.selected_topics[0])
        return self._active_pool[self._pool_idx % len(self._active_pool)].get(
            "_topic", self.selected_topics[0])

    # ── room entry / clearing ────────────────────────────────────────────────
    def enter_room(self, room_idx: int):
        self.active_room_idx = room_idx

    def clear_current_room(self) -> bool:
        """Mark active room cleared. Returns True if the key was just found."""
        i = self.active_room_idx
        if i < 0 or i >= len(self.graph):
            return False
        self.graph[i]['cleared'] = True
        found = (i == self.key_room_idx and not self.has_key)
        if found:
            self.has_key = True
        self.active_room_idx = -1
        return found

    def retreat_from_room(self):
        """Exit the active room without clearing it (boss defeat)."""
        self.active_room_idx = -1

    # ── learning feature helpers ─────────────────────────────────────────────
    @staticmethod
    def _q_hash(q: dict) -> str:
        return q.get("q", "")[:60]

    def advance_to_unused_question(self):
        """Advance _pool_idx past questions already used this floor (up to one full pass)."""
        pool = self._active_pool
        if not pool:
            return
        start = self._pool_idx
        for _ in range(len(pool)):
            hk = self._q_hash(pool[self._pool_idx % len(pool)])
            if hk not in self._floor_used_q_hashes:
                return
            self._pool_idx += 1
        self._pool_idx = start  # all used — allow repeat (graceful fallback)

    def record_correct(self, q: dict):
        hk = self._q_hash(q)
        self._floor_used_q_hashes.add(hk)
        self._q_consec_wrong[hk] = 0

    def record_wrong(self, q: dict):
        hk = self._q_hash(q)
        self._floor_used_q_hashes.add(hk)
        streak = self._q_consec_wrong.get(hk, 0) + 1
        self._q_consec_wrong[hk] = streak
        if hk not in self._weak_pool_keys:
            self._weak_pool_keys.add(hk)
            tagged = dict(q)
            self._weak_pool.append(tagged)
        if self._boss_weak_q is None and not self._boss_weak_injected:
            self._boss_weak_q = dict(q)

    def get_adaptive_choices(self, q: dict) -> tuple:
        """Return (choices_list, answer_idx) trimmed by consecutive-wrong streak."""
        hk  = self._q_hash(q)
        streak = self._q_consec_wrong.get(hk, 0)
        choices = list(q["c"])
        ans_idx = q["a"]
        n_remove = 0
        if streak >= 3:
            n_remove = 2  # show only 2 choices
        elif streak >= 2:
            n_remove = 1  # show only 3 choices
        if n_remove > 0:
            wrong_idxs = [i for i in range(len(choices)) if i != ans_idx]
            random.shuffle(wrong_idxs)
            remove = wrong_idxs[:n_remove]
            new_choices = [c for i, c in enumerate(choices) if i not in remove]
            new_ans = new_choices.index(choices[ans_idx])
            return new_choices, new_ans
        return choices, ans_idx

    def prepare_boss_questions(self):
        """Inject one weak-pool question into the boss pool at a random position."""
        if self._boss_weak_q is None:
            self._boss_weak_injected = False
            return
        wq = dict(self._boss_weak_q)
        wq.setdefault("_topic", self.selected_topics[0] if self.selected_topics else "DFA")
        wq.setdefault("_tier",  "hard")
        wq["_weak"] = True  # mark so renderer can flag it
        pool = list(self._boss_pool)
        pos  = random.randint(0, min(len(pool), self.boss_q_idx + 1))
        pool.insert(pos, wq)
        self._boss_pool = pool
        self._boss_weak_q = None
        self._boss_weak_injected = True

    # ── question access ─────────────────────────────────────────────────────
    def consume_question(self):
        self._pool_idx += 1

    def consume_mini_boss_question(self):
        self._mini_boss_idx += 1

    def advance_boss_question(self):
        self.boss_q_idx     += 1
        self._boss_pool_idx += 1

    def advance_floor(self) -> bool:
        """Move to next floor. Returns True if a new tier was unlocked."""
        old_tiers = self.unlocked_tiers()
        self.floor        += 1
        self.boss_q_idx    = 0
        self.boss_correct  = 0
        self._floor_used_q_hashes  = set()
        self._boss_weak_injected   = False
        new_tiers = self.unlocked_tiers()
        self._rebuild_active_pool()
        self._generate_floor()
        return new_tiers != old_tiers


# ─────────────────── Game (state machine) ─────────────────────────────────────
class Game:
    def __init__(self, screen: pygame.Surface):
        self.screen  = screen
        self.W, self.H = screen.get_size()

        from renderer import Renderer
        self.renderer = Renderer(screen)

        self.state:      State      = State.TITLE
        self.player:     Player     = None
        self.dungeon:    DungeonRun = None
        self.difficulty: str        = "medium"

        self.selected_topics: list = []

        # Question state
        self.q_data:     dict  = None
        self.chosen:     int   = -1
        self.eliminated: list  = []
        self.time_left:  float = 0.0

        # Room mode flags
        self.in_boss_mode:   bool = False
        self.challenge_mode: bool = False
        self.vault_mode:     bool = False
        self.mini_boss_mode: bool = False
        self.mini_boss_completed: bool = False   # for BOSS_RESULT screen label
        self.boss_beaten:         bool = False   # boss won this floor; can return then descend
        self.full_clear_bonus_given: bool = False

        # Special room (campfire / treasure)
        self.special_room_type: str = ""   # "campfire" or "treasure"
        self.special_room_gold: int = 0
        self.special_room_heal: int = 0

        # Feedback
        self.fb_correct:       bool = False
        self.fb_message:       str  = ""
        self.fb_pts_earned:    int  = 0
        self.fb_gold_earned:   int  = 0
        self.fb_explanation:   str  = ""
        self.fb_correct_idx:   int  = 0
        self.fb_streak_before: int  = 0

        # Boss fight
        self.boss_victory:       bool = False
        self.boss_q_total:       int  = 3
        self.boss_needed_now:    int  = 1
        self.boss_intro_elapsed: int  = 0

        # Scaling / tier-unlock notifications
        self.rooms_cleared: int = 0
        self.notif_text:    str = ""
        self.notif_timer:   int = 0

        # Visual effects
        self.shake_timer:         int   = 0
        self.answer_anim_timer:   int   = 0
        self.answer_anim_correct: bool  = False
        self.streak_flash_text:   str   = ""
        self.streak_flash_timer:  int   = 0

        # Shop
        self.shop_stock:            list = []
        self.perfect_boss_discount: str  = ""
        self.shop_reroll_count:     int  = 0

        # Animation tick
        self.tick: int = 0

        # End-of-run stats
        self.final_score:       int = 0
        self.final_hp:          int = 0
        self.floors_done:       int = 0
        self.run_total_correct: int = 0
        self.run_total_wrong:   int = 0
        self.run_total_fast:    int = 0
        self.run_boss_perfects: int = 0
        self.run_victory:       bool = False
        self.per_topic_correct: dict = {}
        self.per_topic_wrong:   dict = {}

        # New feature state
        self.cursed_mode:           bool  = False
        self.cursed_entry_timer:    int   = 0
        self.key_splash_timer:      int   = 0
        self.tome_anim_timer:       int   = 0
        self.score_popups:          list  = []
        self.pause_prev_state             = None
        self._pause_just_entered          = False
        self.boss_confirm_idx:      int   = -1
        self.boss_gate_elapsed:     int   = 0
        self.vault_gamble_base:     int   = 0
        self.vault_gamble_double:   int   = 0

        # Learning feature state
        self.teach_it_back_mode:    bool  = False
        self._teach_it_back_prompt: str  = ""
        self.surge_topic:           str   = ""   # topic currently on a same-topic streak
        self.surge_count:           int   = 0    # # correct in a row for surge_topic
        self.surge_flash_timer:     int   = 0
        self.surge_flash_text:      str   = ""
        self.per_topic_total:       dict  = {}   # cumulative correct per topic (across floors)
        self.milestone_achieved:    dict  = {}   # topic → highest milestone reached (0/25/50/100)
        self.wrong_log:             list  = []   # list of (q_dict, chosen_idx) this run
        self.q_data_choices:        list  = []   # potentially trimmed choices list for current Q
        self.q_data_answer:         int   = 0    # answer index into q_data_choices
        self.flashcard_idx:         int   = 0    # index into wrong_log during FLASHCARD_REVIEW
        self.flashcard_revealed:    bool  = False
        self.floor_briefing_done:   bool  = True  # True = skip first floor briefing pre-game
        self.grimoire_page:         int   = 0

        # Feature 8: Relic system
        self.active_relic:          str   = ""    # key from RELICS
        self.relic_choices:         list  = []    # 3 relic keys shown on relic select screen
        self.relic_correct_count:   int   = 0     # for memory_crystal: total correct this run

        # Feature 9: Floor curses
        self.floor_curse:           str   = ""    # "hard_only" | "no_hints" | "double_penalty" | ""
        self.floor_curse_offered:   bool  = False # True once offer shown this floor
        self.floor_curse_accepted:  bool  = False

        # Feature 11: Boss attack patterns
        self.boss_attack_type:      str   = ""    # "timer" | "confusion" | "drain"
        self.boss_attack_elapsed:   int   = 0

        # Feature 13: Daily challenge
        self.daily_challenge_mode:  bool  = False
        self.daily_seed:            int   = 0

        # Feature 2: Explanation deep-dive toggle
        self.fb_deep_mode:          bool  = False

        # Feature 5: Wrong-answer pattern tracking
        self.wrong_choice_tally:    dict  = {}    # choice_text → count of times chosen incorrectly

        # Feature 14: Combo meter (uses player.streak, just needs renderer flag)
        self.combo_flash_timer:     int   = 0

        # Shop fun fact
        self.shop_fun_fact:         str   = ""

    # ─────────────── update ──────────────────────────────────────────────────
    def update(self, events: list, dt: int):
        self.tick += 1

        if self.notif_timer > 0:
            self.notif_timer -= 1
        if self.shake_timer > 0:
            self.shake_timer -= 1
        if self.answer_anim_timer > 0:
            self.answer_anim_timer -= 1
        if self.streak_flash_timer > 0:
            self.streak_flash_timer -= 1
        if self.state == State.BOSS_INTRO:
            self.boss_intro_elapsed += 1

        # New feature timers
        if self.cursed_entry_timer > 0: self.cursed_entry_timer -= 1
        if self.key_splash_timer   > 0: self.key_splash_timer   -= 1
        if self.tome_anim_timer    > 0: self.tome_anim_timer    -= 1
        if self.surge_flash_timer  > 0: self.surge_flash_timer  -= 1
        if self.combo_flash_timer  > 0: self.combo_flash_timer  -= 1
        if self.state == State.BOSS_ATTACK:
            self.boss_attack_elapsed += 1
        for _p in self.score_popups:
            _p['y']     -= 1.2
            _p['timer'] -= 1
        self.score_popups = [_p for _p in self.score_popups if _p['timer'] > 0]

        # ESC → pause (not during active question, title, or end screens)
        _pausable = (State.DUNGEON_MAP, State.FEEDBACK, State.BOSS_INTRO,
                     State.BOSS_RESULT, State.SHOP, State.SPECIAL_ROOM,
                     State.CAMPFIRE_CHOICE, State.VAULT_GAMBLE,
                     State.BOSS_GATE, State.FLOOR_BRIEFING)
        if self.state in _pausable:
            for _ev in events:
                if _ev.type == pygame.KEYDOWN and _ev.key == pygame.K_ESCAPE:
                    self.pause_prev_state = self.state
                    self.state = State.PAUSED
                    self._pause_just_entered = True
                    break

        s = self.state
        if   s == State.TITLE:             self._upd_title(events)
        elif s == State.DIFFICULTY_SELECT: self._upd_difficulty_select(events)
        elif s == State.TOPIC_SELECT:      self._upd_topic_select(events)
        elif s == State.DUNGEON_MAP:       self._upd_dungeon_map(events)
        elif s == State.IN_ROOM:           self._upd_in_room(events, dt)
        elif s == State.FEEDBACK:          self._upd_feedback(events)
        elif s == State.BOSS_INTRO:        self._upd_boss_intro(events)
        elif s == State.BOSS_GATE:         self._upd_boss_gate(events)
        elif s == State.BOSS_RESULT:       self._upd_boss_result(events)
        elif s == State.SHOP:              self._upd_shop(events)
        elif s == State.SPECIAL_ROOM:      self._upd_special_room(events)
        elif s == State.CAMPFIRE_CHOICE:   self._upd_campfire_choice(events)
        elif s == State.VAULT_GAMBLE:      self._upd_vault_gamble(events)
        elif s == State.PAUSED:            self._upd_paused(events)
        elif s == State.RUN_STATS:         self._upd_run_stats(events)
        elif s == State.FLOOR_BRIEFING:    self._upd_floor_briefing(events)
        elif s == State.GRIMOIRE:          self._upd_grimoire(events)
        elif s == State.FLASHCARD_REVIEW:  self._upd_flashcard_review(events)
        elif s == State.RELIC_SELECT:      self._upd_relic_select(events)
        elif s == State.BOSS_ATTACK:       self._upd_boss_attack(events)
        elif s == State.GAME_OVER:         self._upd_game_over(events)
        elif s == State.VICTORY:           self._upd_victory(events)

    def render(self):
        self.renderer.render(self)

    # ─────────────── helpers ─────────────────────────────────────────────────
    def _start_run(self):
        self.player        = Player(self.difficulty)
        self.dungeon       = DungeonRun(list(self.selected_topics), self.difficulty)
        self.rooms_cleared = 0
        self.notif_text    = ""
        self.notif_timer   = 0
        self.run_total_correct    = 0
        self.run_total_wrong      = 0
        self.run_total_fast       = 0
        self.run_boss_perfects    = 0
        self.perfect_boss_discount = ""
        self.streak_flash_text    = ""
        self.streak_flash_timer   = 0
        self.mini_boss_completed     = False
        self.boss_beaten             = False
        self.full_clear_bonus_given  = False
        self.per_topic_correct       = {}
        self.per_topic_wrong         = {}
        self.cursed_mode             = False
        self.cursed_entry_timer      = 0
        self.key_splash_timer        = 0
        self.tome_anim_timer         = 0
        self.score_popups            = []
        self.boss_confirm_idx        = -1
        self.boss_gate_elapsed        = 0
        self.vault_gamble_base       = 0
        self.vault_gamble_double     = 0
        self.teach_it_back_mode      = False
        self._teach_it_back_prompt   = ""
        self.surge_topic             = ""
        self.surge_count             = 0
        self.surge_flash_timer       = 0
        self.surge_flash_text        = ""
        self.per_topic_total         = {}
        self.milestone_achieved      = {}
        self.wrong_log               = []
        self.q_data_choices          = []
        self.q_data_answer           = 0
        self.flashcard_idx           = 0
        self.flashcard_revealed      = False
        self.floor_briefing_done     = False
        self.grimoire_page           = 0

        # Feature 8: Relic
        self.active_relic            = ""
        self.relic_correct_count     = 0
        # Offer 3 random relics to choose from
        self.relic_choices           = random.sample(RELIC_ORDER, min(3, len(RELIC_ORDER)))

        # Feature 9: Curses
        self.floor_curse             = ""
        self.floor_curse_offered     = False
        self.floor_curse_accepted    = False

        # Feature 11: Boss attacks
        self.boss_attack_type        = ""
        self.boss_attack_elapsed     = 0

        # Feature 5: Pattern tracking
        self.wrong_choice_tally      = {}

        # Feature 2: Deep mode
        self.fb_deep_mode            = False

        # Feature 14: Combo flash
        self.combo_flash_timer       = 0

        # Daily challenge: set seed if active
        if self.daily_challenge_mode:
            random.seed(self.daily_seed)

        self.state = State.RELIC_SELECT

    def _apply_difficulty_scaling(self):
        dc          = DIFFICULTIES[self.player.difficulty]
        old_timer   = self.player.question_time
        old_penalty = self.player.wrong_penalty

        self.player.question_time = max(dc["timer_min"],
                                        self.player.question_time - dc["timer_decay"])
        self.player.wrong_penalty = min(dc["penalty_max"],
                                        self.player.wrong_penalty + dc["penalty_growth"])

        if (self.player.question_time < old_timer or
                self.player.wrong_penalty > old_penalty):
            self.notif_text  = (
                f"Difficulty rising!  "
                f"Timer \u2192 {self.player.question_time:.0f}s   |   "
                f"Wrong \u2192 \u2212{self.player.wrong_penalty} HP"
            )
            self.notif_timer = 300

    def _check_scaling(self):
        self.rooms_cleared += 1
        if self.rooms_cleared % 5 == 0:
            self._apply_difficulty_scaling()

    def _enter_room(self):
        """Enter the room whose index is in dungeon.active_room_idx."""
        dungeon    = self.dungeon
        stage_type = dungeon.current_room_type

        if stage_type == RoomType.BOSS:
            self.boss_q_total    = boss_q_count(dungeon.floor, dungeon.max_floors)
            self.boss_needed_now = boss_needed_count(
                dungeon.floor, self.difficulty, dungeon.max_floors)
            self.boss_intro_elapsed  = 0
            self.mini_boss_completed = False
            self.state = State.BOSS_INTRO

        elif stage_type == RoomType.CAMPFIRE:
            self.special_room_type = "campfire"
            self.special_room_heal = 35
            self.special_room_gold = 0
            self.state = State.CAMPFIRE_CHOICE

        elif stage_type == RoomType.TREASURE:
            gold = random.randint(300, 600)
            self.player.gold      += gold
            self.special_room_type = "treasure"
            self.special_room_gold = gold
            self.special_room_heal = 0
            self.state = State.SPECIAL_ROOM

        elif stage_type == RoomType.VAULT:
            self.vault_gamble_base   = 300
            self.vault_gamble_double = 600
            self.challenge_mode      = False
            self.vault_mode          = False
            self.cursed_mode         = False
            self.mini_boss_mode      = False
            self.state = State.VAULT_GAMBLE

        elif stage_type == RoomType.CURSED:
            self.cursed_mode        = True
            self.cursed_entry_timer = 50
            self.challenge_mode     = False
            self.vault_mode         = False
            self.mini_boss_mode     = False
            self.teach_it_back_mode = False
            self._load_regular_question()
            self.state = State.IN_ROOM

        elif stage_type == RoomType.MINI_BOSS:
            self.mini_boss_mode     = True
            self.cursed_mode        = False
            self.teach_it_back_mode = False
            self._load_mini_boss_question()
            self.state = State.IN_ROOM

        elif stage_type == RoomType.TEACH_IT_BACK:
            self.challenge_mode     = False
            self.vault_mode         = False
            self.cursed_mode        = False
            self.mini_boss_mode     = False
            self.teach_it_back_mode = True
            self._load_teach_it_back_question()
            self.state = State.IN_ROOM

        else:
            self.challenge_mode     = (stage_type == RoomType.CHALLENGE)
            self.vault_mode         = False
            self.cursed_mode        = False
            self.mini_boss_mode     = False
            self.teach_it_back_mode = False
            self._load_regular_question()
            self.state = State.IN_ROOM

    def _enter_chosen_room(self, room_idx: int):
        """Validate then enter the chosen room."""
        dungeon = self.dungeon

        if room_idx not in dungeon.accessible_rooms:
            return

        if room_idx == dungeon.boss_idx and not dungeon.has_key:
            self.notif_text  = "This path is blocked.  Find the dungeon key first!"
            self.notif_timer = 220
            return

        # Boss confirm overlay — don't enter immediately
        if room_idx == dungeon.boss_idx and dungeon.has_key:
            self.boss_confirm_idx = room_idx
            return

        dungeon.enter_room(room_idx)
        self._enter_room()

    def _confirm_boss_entry(self):
        idx = self.boss_confirm_idx
        self.boss_confirm_idx = -1
        self.dungeon.enter_room(idx)
        d = self.dungeon
        self.boss_q_total        = boss_q_count(d.floor, d.max_floors)
        self.boss_needed_now     = boss_needed_count(d.floor, self.difficulty, d.max_floors)
        self.mini_boss_completed = False
        self.boss_gate_elapsed   = 0
        d.prepare_boss_questions()
        self.state               = State.BOSS_GATE

    def _load_regular_question(self):
        self.dungeon.advance_to_unused_question()
        raw             = self.dungeon.current_question
        self.q_data     = raw
        choices, ans    = self.dungeon.get_adaptive_choices(raw)
        self.q_data_choices = choices
        self.q_data_answer  = ans
        self.chosen     = -1
        self.eliminated = []
        bonus           = self.player.room_time_bonus
        self.time_left  = self.player.question_time + bonus
        self.player.room_time_bonus = 0.0
        self.in_boss_mode = False
        # Feature 9: no_hints curse
        if getattr(self, 'floor_curse', '') in ('no_hints', 'dark_covenant'):
            # Store pre-curse hint count; hints are effectively 0 this floor
            # We just visually block hints — enforce in _use_hint
            pass

    def _load_mini_boss_question(self):
        raw                 = self.dungeon.mini_boss_question
        self.q_data         = raw
        self.q_data_choices = list(raw["c"])
        self.q_data_answer  = raw["a"]
        self.chosen         = -1
        self.eliminated     = []
        self.time_left      = self.player.question_time
        self.in_boss_mode   = False

    def _load_boss_question(self):
        raw                 = self.dungeon.current_question
        self.q_data         = raw
        self.q_data_choices = list(raw["c"])
        self.q_data_answer  = raw["a"]
        self.chosen         = -1
        self.eliminated     = []
        self.time_left      = self.player.question_time
        self.in_boss_mode   = True

    def _load_teach_it_back_question(self):
        """Teach It Back: show the answer text as the 'question', player picks the right Q."""
        self.dungeon.advance_to_unused_question()
        raw             = self.dungeon.current_question
        self.q_data     = raw
        # The "question" shown is the correct answer text; "choices" are the question stems
        correct_ans_text = raw["c"][raw["a"]]
        q_stems = [raw["q"]]   # correct question
        # Add 3 distractors: neighboring questions' stems from the active pool
        pool = self.dungeon._active_pool
        pool_size = len(pool)
        base_idx = self.dungeon._pool_idx % max(1, pool_size)
        used = {raw["q"]}
        for offset in range(1, pool_size):
            cand = pool[(base_idx + offset) % pool_size]
            if cand.get("q") not in used:
                q_stems.append(cand["q"])
                used.add(cand["q"])
            if len(q_stems) == 4:
                break
        while len(q_stems) < 4:
            q_stems.append("(No alternative question available)")
        random.shuffle(q_stems)
        correct_q_idx = q_stems.index(raw["q"])
        # Store in q_data_choices / q_data_answer for the renderer
        self.q_data_choices = q_stems
        self.q_data_answer  = correct_q_idx
        self.chosen         = -1
        self.eliminated     = []
        self.time_left      = self.player.question_time + 10.0   # extra time for harder format
        self.in_boss_mode   = False
        self._teach_it_back_prompt = correct_ans_text  # what gets displayed as the "question"

    def _answer(self, idx: int):
        if self.chosen != -1:
            return
        self.chosen           = idx
        self.fb_deep_mode     = False   # reset deep toggle each new feedback
        # Use adaptive answer index when choices have been trimmed
        correct               = (idx == self.q_data_answer)
        self.fb_correct       = correct
        self.fb_explanation   = self.q_data["e"]
        self.fb_correct_idx   = self.q_data_answer
        self.fb_streak_before = self.player.streak

        if self.in_boss_mode:
            # ── Boss fight answer ──────────────────────────────────────────
            if correct:
                self.dungeon.boss_correct += 1
                pts = self.player.calc_points(400, apply_streak=False)
                self.player.score += pts
                self.player.gold  += 100
                self.fb_pts_earned  = pts
                self.fb_gold_earned = 100
                self.player.extend_streak()
                self.fb_message = f"CORRECT!   +{pts} pts   +100 gold"
            else:
                self.player.break_streak()
                self.fb_pts_earned  = 0
                self.fb_gold_earned = 0
                self.fb_message = f"WRONG!   Answer: {chr(65 + self.q_data['a'])}"
            self.dungeon.advance_boss_question()

        else:
            # ── Regular / special room answer ─────────────────────────────
            if self.mini_boss_mode:
                self.dungeon.consume_mini_boss_question()
            else:
                self.dungeon.consume_question()

            # Determine base points, penalties, gold
            if self.mini_boss_mode:
                base_pts     = 450
                hp_penalty   = 0
                gold_correct = 300
            elif self.cursed_mode:
                base_pts     = 300   # 3x regular
                hp_penalty   = min(self.player.wrong_penalty * 2,
                                   DIFFICULTIES[self.difficulty]["penalty_max"])
                gold_correct = 150
            elif self.challenge_mode:
                base_pts     = 240
                hp_penalty   = min(self.player.wrong_penalty * 2,
                                   DIFFICULTIES[self.difficulty]["penalty_max"])
                gold_correct = 200
            elif self.vault_mode:
                base_pts     = 120
                hp_penalty   = 0    # vault gamble: no HP loss
                gold_correct = self.vault_gamble_double
            else:
                base_pts     = 100
                hp_penalty   = self.player.wrong_penalty
                gold_correct = 100

            if correct:
                pts = self.player.calc_points(base_pts)

                # G4: time bonus — answered in the first 30% of the clock
                time_bonus = 0
                if (self.player.question_time > 0 and
                        self.time_left / self.player.question_time > 0.70):
                    time_bonus = max(1, pts // 10)
                    pts       += time_bonus
                    self.run_total_fast += 1

                self.player.score += pts
                self.player.gold  += gold_correct
                self.fb_pts_earned  = pts
                self.fb_gold_earned = gold_correct

                prev_streak = self.player.streak
                self.player.extend_streak()
                new_streak  = self.player.streak

                if self.challenge_mode:
                    self.player.hints += 1

                # Scholar's Mark: reduce penalty at streak multiples of 5
                if (self.player.scholar_mark_stacks > 0 and
                        new_streak > 0 and new_streak % 5 == 0 and
                        self.player.scholar_mark_reductions < 3):
                    reduction = max(0, min(1, self.player.wrong_penalty - 5))
                    if reduction > 0:
                        self.player.wrong_penalty           -= reduction
                        self.player.scholar_mark_reductions += 1
                        self.streak_flash_text  = (
                            f"Scholar's Mark!  Penalty now -{self.player.wrong_penalty} HP"
                        )
                        self.streak_flash_timer = 180

                # Streak milestone flash
                if new_streak in (3, 5, 10) and not self.streak_flash_timer:
                    msgs = {3: "ON FIRE!  3 STREAK",
                            5: "BLAZING!  5 STREAK",
                            10: "UNSTOPPABLE!  10 STREAK"}
                    self.streak_flash_text  = msgs[new_streak]
                    self.streak_flash_timer = 150

                # Streak heal
                if self.player.streak_heal > 0 and self.player.streak >= 3:
                    self.player.heal(self.player.streak_heal * 3)
                self.player.heal(5)

                self.run_total_correct += 1
                self.relic_correct_count = getattr(self, 'relic_correct_count', 0) + 1

                # Feature 8 relic effects — correct answer
                if self.active_relic == "theorists_wand":
                    bonus = min(3.0, (self.player.question_time + 3.0 + 30.0) - self.player.question_time)
                    self.player.question_time = min(self.player.question_time + 3.0,
                                                    self.player.question_time + 30.0)
                if self.active_relic == "memory_crystal" and self.relic_correct_count % 8 == 0:
                    self.player.hints += 1
                    self.notif_text  = f"Memory Crystal: +1 Hint  ({self.relic_correct_count} correct total)"
                    self.notif_timer = 240

                # Feature 14: combo flash on 3+ streak
                if self.player.streak >= 3:
                    self.combo_flash_timer = 40

                # Per-topic stat + floating popup
                _t = self.dungeon.current_topic
                self.per_topic_correct[_t] = self.per_topic_correct.get(_t, 0) + 1
                # Cumulative across run (for milestones)
                self.per_topic_total[_t] = self.per_topic_total.get(_t, 0) + 1
                self.dungeon.record_correct(self.q_data)
                self.score_popups.append({
                    'text': f'+{pts}', 'x': self.W // 2,
                    'y': float(self.H // 2 + 30), 'timer': 55,
                    'color': (255, 240, 60)
                })

                # ── Mastery surge: 3+ same-topic correct in a row ───────────
                if not self.in_boss_mode:
                    surge_thresh = 2 if self.active_relic == "surge_stone" else 3
                    surge_bonus  = 0.07 if self.active_relic == "surge_stone" else 0.05
                    if _t == self.surge_topic:
                        self.surge_count += 1
                    else:
                        self.surge_topic = _t
                        self.surge_count = 1
                    if self.surge_count == surge_thresh:
                        self.player.point_mult += surge_bonus
                        self.surge_flash_text  = (f"MASTERY SURGE!  {TOPICS.get(_t, _t)} x{surge_thresh}!"
                                                  f"  +{int(surge_bonus*100)}% pts")
                        self.surge_flash_timer = 180
                    elif self.surge_count == surge_thresh + 2:
                        self.player.point_mult += surge_bonus
                        self.surge_flash_text  = (f"MASTERY SURGE!  {TOPICS.get(_t, _t)} x{surge_thresh+2}!"
                                                  f"  +{int(surge_bonus*100)}% pts")
                        self.surge_flash_timer = 180

                # ── Knowledge milestones ─────────────────────────────────────
                if not self.in_boss_mode:
                    _cum = self.per_topic_total.get(_t, 0)
                    _prev_ms = self.milestone_achieved.get(_t, 0)
                    for ms_thresh, ms_reward in ((25, "timer"), (50, "hint"), (100, "pts")):
                        if _cum >= ms_thresh > _prev_ms:
                            self.milestone_achieved[_t] = ms_thresh
                            if ms_reward == "timer":
                                self.player.question_time += 3.0
                                _ms_msg = f"MILESTONE!  {TOPICS.get(_t,_t)}: 25 correct  → +3s per Q"
                            elif ms_reward == "hint":
                                self.player.hints += 1
                                _ms_msg = f"MILESTONE!  {TOPICS.get(_t,_t)}: 50 correct  → +1 Hint"
                            else:
                                self.player.point_mult += 0.10
                                _ms_msg = f"MILESTONE!  {TOPICS.get(_t,_t)}: 100 correct  → +10% pts"
                            self.notif_text  = _ms_msg
                            self.notif_timer = 360
                            break

                streak_lbl = (f"  (streak {new_streak}  \u00d7{1 + self.player.streak_bonus:.1f})"
                              if new_streak > 1 else "")
                tb_lbl     = f"  \u26a1+{time_bonus}" if time_bonus else ""
                gold_lbl   = f"  +{gold_correct}g"
                hint_lbl   = "  [+1 Hint]" if self.challenge_mode else ""
                self.fb_message = (
                    f"CORRECT!   +{pts} pts{gold_lbl}{tb_lbl}{hint_lbl}{streak_lbl}"
                )

            else:
                # Wrong answer
                # Feature 8: Iron Ledger relic — pay gold instead of HP
                if self.active_relic == "iron_ledger" and hp_penalty > 0:
                    gold_cost = 60
                    if self.player.gold >= gold_cost:
                        self.player.gold -= gold_cost
                        hp_penalty = 0
                        self.notif_text  = f"Iron Ledger: paid {gold_cost}g instead of taking damage."
                        self.notif_timer = 180

                if hp_penalty > 0:
                    self.player.take_damage(hp_penalty)

                    # Iron Will save
                    if (self.player.hp <= 0 and
                            self.player.iron_will_charges > 0 and
                            self.player.iron_will_cooldown == 0):
                        self.player.hp                 = 1
                        self.player.iron_will_charges -= 1
                        self.player.iron_will_cooldown = 3
                        self.notif_text  = (
                            "IRON WILL activated \u2014 death prevented!  (3-floor cooldown)"
                        )
                        self.notif_timer = 300

                # Scholar's Tome: intercept streak break once
                _tome_saved = False
                if self.player.scholar_tome_charges > 0:
                    self.player.scholar_tome_charges -= 1
                    self.tome_anim_timer             = 70
                    _tome_saved                      = True
                    self.streak_flash_text  = "Scholar's Tome!  Streak saved!"
                    self.streak_flash_timer = 150

                if not _tome_saved:
                    if self.fb_streak_before >= 3:
                        self.shake_timer = 22
                    self.player.break_streak()

                # Per-topic wrong stat + weak pool
                _t = self.dungeon.current_topic
                self.per_topic_wrong[_t] = self.per_topic_wrong.get(_t, 0) + 1
                if not self.in_boss_mode:
                    self.dungeon.record_wrong(self.q_data)
                    # Log wrong answer for end-of-run flashcard review
                    self.wrong_log.append({'q': dict(self.q_data),
                                           'chosen': idx,
                                           'correct_idx': self.q_data_answer,
                                           'choices': list(self.q_data_choices)})
                    # Feature 5: pattern tally — track which choice text was picked wrong
                    if 0 <= idx < len(self.q_data_choices):
                        ct = self.q_data_choices[idx][:50]
                        self.wrong_choice_tally[ct] = self.wrong_choice_tally.get(ct, 0) + 1
                    # Reset surge
                    self.surge_topic = ""
                    self.surge_count = 0

                self.fb_pts_earned  = 0
                self.fb_gold_earned = 0
                self.run_total_wrong += 1

                if self.vault_mode:
                    pen_lbl = "   [Vault sealed \u2014 no gold!]"
                elif hp_penalty > 0:
                    pen_lbl = f"   \u2212{hp_penalty} HP"
                else:
                    pen_lbl = "   [No HP penalty]"
                self.fb_message = (
                    f"WRONG!{pen_lbl}   Answer: {chr(65 + self.q_data['a'])}"
                )

            # Trigger answer animation
            self.answer_anim_timer   = 20
            self.answer_anim_correct = correct

        self.state = State.FEEDBACK

    def _use_hint(self):
        if self.player.hints <= 0 or self.chosen != -1:
            return
        # Feature 9: no_hints / dark_covenant curse blocks hints
        if getattr(self, 'floor_curse', '') in ('no_hints', 'dark_covenant'):
            self.notif_text  = "CURSED FLOOR: hints are sealed!"
            self.notif_timer = 160
            return
        wrong = [i for i in range(4)
                 if i != self.q_data["a"] and i not in self.eliminated]
        if len(wrong) < 2:
            return
        self.eliminated.extend(random.sample(wrong, 2))
        self.player.hints -= 1

    def _use_skip(self):
        if self.player.skips <= 0 or self.chosen != -1:
            return
        self.player.skips   -= 1
        self.chosen          = -2
        self.fb_correct      = True
        self.fb_message      = "SKIPPED \u2014 room cleared, no points or gold"
        self.fb_pts_earned   = 0
        self.fb_gold_earned  = 0
        self.fb_streak_before = self.player.streak
        self.fb_explanation  = (f"Correct answer was  {chr(65 + self.q_data['a'])}.  "
                                f"{self.q_data['c'][self.q_data['a']]}")
        self.fb_correct_idx  = self.q_data["a"]
        if self.mini_boss_mode:
            self.dungeon.consume_mini_boss_question()
        else:
            self.dungeon.consume_question()
        self.state = State.FEEDBACK

    def _continue_from_feedback(self):
        if self.player.is_dead:
            self._end_run(victory=False)
            return

        if self.in_boss_mode:
            remaining = self.boss_q_total - self.dungeon.boss_q_idx

            if not self.fb_correct:
                # Wrong answer: check if a win is still mathematically possible
                can_still_win = (self.dungeon.boss_correct + remaining) >= self.boss_needed_now
                if not can_still_win:
                    # Fail-fast: end the boss fight immediately as a loss
                    self.boss_victory = False
                    self.player.take_damage(30)
                    self.player.break_streak()
                    self.dungeon.retreat_from_room()
                    self.state = State.BOSS_RESULT
                    return
                # Win still possible and more questions remain: boss retaliates
                if remaining > 0:
                    self._trigger_boss_attack()
                    return
                # Win still possible but no questions left — fall through to resolve

            # Correct answer (or wrong on last Q but already won enough)
            if remaining > 0:
                self._load_boss_question()
                self.state = State.IN_ROOM
            else:
                won     = (self.dungeon.boss_correct >= self.boss_needed_now)
                perfect = (self.dungeon.boss_correct >= self.boss_q_total)
                self.boss_victory = won
                if won:
                    pts_bonus  = int((1500 if perfect else 750) * self.player.point_mult)
                    gold_bonus = 500 if perfect else 250
                    self.player.score += pts_bonus
                    self.player.gold  += gold_bonus
                    self.player.heal(25)
                    if perfect:
                        self.run_boss_perfects += 1
                    self.dungeon.clear_current_room()
                    self.boss_beaten = True
                else:
                    self.player.take_damage(30)
                    self.player.break_streak()
                    self.dungeon.retreat_from_room()
                self.state = State.BOSS_RESULT
        else:
            if self.fb_correct:
                is_mini = self.mini_boss_mode

                found_key = self.dungeon.clear_current_room()
                self._check_scaling()
                self.challenge_mode = False
                self.vault_mode     = False
                self.cursed_mode    = False
                if found_key:
                    self.notif_text       = "KEY FOUND!  Boss door is now unlocked!"
                    self.notif_timer      = 300
                    self.key_splash_timer = 90

                if is_mini:
                    self._complete_mini_boss_floor()
                else:
                    self.mini_boss_mode = False
                    self.state = State.DUNGEON_MAP
            else:
                # Wrong answer
                if self.vault_mode:
                    # Lost vault gamble — clear room (used up the attempt) and return to map
                    self.dungeon.clear_current_room()
                    self._check_scaling()
                    self.vault_mode  = False
                    self.cursed_mode = False
                    self.state = State.DUNGEON_MAP
                elif self.mini_boss_mode:
                    self._load_mini_boss_question()
                    self.state = State.IN_ROOM
                else:
                    # Retry same room (cursed_mode stays True if applicable)
                    self._load_regular_question()
                    self.state = State.IN_ROOM

    def _complete_mini_boss_floor(self):
        """Mini-boss defeated — clear boss room, grant rewards, go to BOSS_RESULT."""
        self.mini_boss_mode      = False
        self.mini_boss_completed = True
        self.boss_victory        = True
        self.dungeon.boss_correct = 1
        self.dungeon.boss_q_idx   = 1
        self.boss_q_total         = 1
        self.boss_needed_now      = 1
        pts_bonus  = int(1200 * self.player.point_mult)
        gold_bonus = 500
        self.player.score += pts_bonus
        self.player.gold  += gold_bonus
        self.player.heal(25)
        self.run_boss_perfects += 1
        self.perfect_boss_discount = random.choice([it["key"] for it in SHOP_ITEMS])
        # Boss room was already cleared by clear_current_room() in _continue_from_feedback
        self.boss_beaten = True
        self.state = State.BOSS_RESULT

    def _proceed_to_shop(self):
        """Advance floor → shop.  Called from BOSS_RESULT 'Descend' or MAP 'Descend' button."""
        if self.player.is_dead:
            self._end_run(victory=False)
            return

        # Full-clear bonus
        if not self.full_clear_bonus_given and self.dungeon.is_full_clear:
            bonus_g = 750
            bonus_p = int(2000 * self.player.point_mult)
            self.player.gold  += bonus_g
            self.player.score += bonus_p
            self.full_clear_bonus_given = True
            self.notif_text  = f"FULL CLEAR BONUS!  +{bonus_g} gold  +{bonus_p} pts"
            self.notif_timer = 360

        self._check_scaling()

        # Perfect boss → 20 % off one random shop item
        if not self.mini_boss_completed:
            if self.dungeon.boss_correct >= self.boss_q_total:
                self.perfect_boss_discount = random.choice([it["key"] for it in SHOP_ITEMS])
            else:
                self.perfect_boss_discount = ""

        if self.player.iron_will_cooldown > 0:
            self.player.iron_will_cooldown -= 1

        tier_unlocked = self.dungeon.advance_floor()
        if tier_unlocked:
            tiers      = self.dungeon.unlocked_tiers()
            tier_names = " + ".join(t.upper() for t in tiers)
            self.notif_text  = f"New questions unlocked!  Now drawing from:  {tier_names}"
            self.notif_timer = 420

        self.mini_boss_completed    = False
        self.boss_beaten            = False
        self.full_clear_bonus_given = False
        self._enter_shop()

    def _enter_shop(self):
        self.shop_reroll_count = 0   # price resets each new shop visit
        self._roll_shop_stock()
        # Feature 7: pick a random "Did You Know" fact for this shop visit
        self.shop_fun_fact = random.choice(DID_YOU_KNOW) if DID_YOU_KNOW else ""
        self.state = State.SHOP

    def _roll_shop_stock(self):
        """Pick 4 random items, honouring the perfect-boss discount slot."""
        stock = random.sample(SHOP_ITEMS, min(4, len(SHOP_ITEMS)))
        if self.perfect_boss_discount:
            keys = [it["key"] for it in stock]
            if self.perfect_boss_discount not in keys:
                disc = next((it for it in SHOP_ITEMS
                             if it["key"] == self.perfect_boss_discount), None)
                if disc:
                    stock[0] = disc
        self.shop_stock = stock

    def _leave_shop(self):
        self.perfect_boss_discount = ""
        if self.dungeon.floor > self.dungeon.max_floors:
            self.floors_done = self.dungeon.max_floors
            self._end_run(victory=True)
        else:
            # Feature 9: reset curse state for new floor
            self.floor_curse          = ""
            self.floor_curse_offered  = True   # will show offer on map
            self.floor_curse_accepted = False
            self.floor_briefing_done  = False
            self.state = State.FLOOR_BRIEFING

    def _buy_item(self, key: str):
        disc  = (key == self.perfect_boss_discount)
        price = item_price(key, self.player.shop_buys, discount=disc)
        if self.player.gold < price:
            return
        self.player.gold           -= price
        self.player.shop_buys[key] += 1

        if   key == "hp_up":         self.player.max_hp              += 20;  self.player.heal(20)
        elif key == "time_up":       self.player.question_time       += 10.0
        elif key == "point_boost":   self.player.point_mult          += 0.25
        elif key == "streak_heal":   self.player.streak_heal         += 1
        elif key == "hint":          self.player.hints               += 1
        elif key == "skip":          self.player.skips               += 1
        elif key == "iron_will":     self.player.iron_will_charges   += 1
        elif key == "scholar_mark":  self.player.scholar_mark_stacks += 1
        elif key == "scholar_tome":  self.player.scholar_tome_charges += 1
        elif key == "dungeon_sense":
            self.dungeon.key_revealed = True
            self.notif_text  = "Dungeon Sense active!  Key room is marked on the map."
            self.notif_timer = 300

    def _end_run(self, victory: bool):
        self.final_hp    = self.player.hp
        self.floors_done = self.dungeon.floor - 1
        if victory:
            self.player.score += self.player.hp * 10
        self.final_score = self.player.score
        self.run_victory = victory
        self.state       = State.RUN_STATS

    def _enter_flashcard_review(self):
        self.flashcard_idx      = 0
        self.flashcard_revealed = False
        self.state              = State.FLASHCARD_REVIEW

    # ─────────────── state update handlers ────────────────────────────────────
    def _upd_title(self, events):
        r = self.renderer
        for ev in events:
            if ev.type == pygame.KEYDOWN and ev.key in (pygame.K_RETURN, pygame.K_SPACE):
                self.daily_challenge_mode = False
                self.state = State.DIFFICULTY_SELECT
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                if r.btn("start_btn") and r.btn("start_btn").collidepoint(ev.pos):
                    self.daily_challenge_mode = False
                    self.state = State.DIFFICULTY_SELECT
                # Feature 13: Daily challenge button
                if r.btn("daily_btn") and r.btn("daily_btn").collidepoint(ev.pos):
                    self._start_daily_challenge()

    def _start_daily_challenge(self):
        """Feature 13: seeded daily run — same seed for everyone on the same date."""
        from datetime import date
        self.daily_challenge_mode = True
        self.daily_seed = int(date.today().strftime("%Y%m%d"))
        # Auto-select hard difficulty and all topics
        self.difficulty      = "hard"
        from questions import TOPIC_ORDER as _TO
        self.selected_topics = list(_TO)
        self._start_run()

    def _upd_difficulty_select(self, events):
        r = self.renderer
        for ev in events:
            if ev.type == pygame.KEYDOWN:
                km = {pygame.K_1: "easy", pygame.K_2: "medium", pygame.K_3: "hard"}
                if ev.key in km:
                    self.difficulty      = km[ev.key]
                    self.selected_topics = []
                    self.state           = State.TOPIC_SELECT
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                for dk in DIFFICULTY_ORDER:
                    b = r.btn(f"diff_{dk}")
                    if b and b.collidepoint(ev.pos):
                        self.difficulty      = dk
                        self.selected_topics = []
                        self.state           = State.TOPIC_SELECT

    def _upd_topic_select(self, events):
        r = self.renderer
        for ev in events:
            if ev.type != pygame.MOUSEBUTTONDOWN or ev.button != 1:
                continue
            for key in TOPIC_ORDER:
                cb = r.btn(f"cb_{key}")
                if cb and cb.collidepoint(ev.pos):
                    if key in self.selected_topics:
                        self.selected_topics.remove(key)
                    else:
                        self.selected_topics.append(key)
            if r.btn("sel_all") and r.btn("sel_all").collidepoint(ev.pos):
                self.selected_topics = list(TOPIC_ORDER)
            if r.btn("clr_all") and r.btn("clr_all").collidepoint(ev.pos):
                self.selected_topics = []
            if r.btn("back_diff") and r.btn("back_diff").collidepoint(ev.pos):
                self.state = State.DIFFICULTY_SELECT
            if self.selected_topics:
                if r.btn("begin") and r.btn("begin").collidepoint(ev.pos):
                    self.selected_topics = [k for k in TOPIC_ORDER
                                            if k in self.selected_topics]
                    self._start_run()

    def _upd_dungeon_map(self, events):
        r       = self.renderer
        dungeon = self.dungeon

        # Boss confirm overlay — handle separately, block other input
        if self.boss_confirm_idx >= 0:
            for ev in events:
                if ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_RETURN:
                        self._confirm_boss_entry()
                    elif ev.key == pygame.K_ESCAPE:
                        self.boss_confirm_idx = -1
                if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                    if r.btn("boss_confirm_yes") and r.btn("boss_confirm_yes").collidepoint(ev.pos):
                        self._confirm_boss_entry()
                    if r.btn("boss_confirm_no") and r.btn("boss_confirm_no").collidepoint(ev.pos):
                        self.boss_confirm_idx = -1
            return

        for ev in events:
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                # Feature 9: floor curse accept / decline
                if self.floor_curse_offered and not self.floor_curse_accepted:
                    if r.btn("curse_hard") and r.btn("curse_hard").collidepoint(ev.pos):
                        self._accept_floor_curse("hard_only", 200)
                    elif r.btn("curse_nohint") and r.btn("curse_nohint").collidepoint(ev.pos):
                        self._accept_floor_curse("no_hints", 150)
                    elif r.btn("curse_double") and r.btn("curse_double").collidepoint(ev.pos):
                        self._accept_floor_curse("double_penalty", 150)
                    elif r.btn("curse_dark") and r.btn("curse_dark").collidepoint(ev.pos):
                        self._accept_floor_curse("dark_covenant", 500)
                    elif r.btn("curse_decline") and r.btn("curse_decline").collidepoint(ev.pos):
                        self.floor_curse_offered = False
                if self.boss_beaten:
                    if r.btn("descend_now") and r.btn("descend_now").collidepoint(ev.pos):
                        self._proceed_to_shop()
                for i in range(len(dungeon.graph)):
                    b = r.btn(f"room_{i}")
                    if b and b.collidepoint(ev.pos):
                        self._enter_chosen_room(i)
            if ev.type == pygame.KEYDOWN and ev.key in (pygame.K_RETURN, pygame.K_SPACE):
                if self.boss_beaten:
                    self._proceed_to_shop()

    def _upd_in_room(self, events, dt: int):
        self.time_left -= dt / 1000.0
        if self.time_left <= 0 and self.chosen == -1:
            self._answer(-1)
            return

        r = self.renderer
        for ev in events:
            if ev.type == pygame.KEYDOWN:
                km = {pygame.K_1: 0, pygame.K_a: 0,
                      pygame.K_2: 1, pygame.K_b: 1,
                      pygame.K_3: 2, pygame.K_c: 2,
                      pygame.K_4: 3, pygame.K_d: 3}
                if ev.key in km and km[ev.key] not in self.eliminated:
                    self._answer(km[ev.key])
                if ev.key == pygame.K_h:
                    self._use_hint()
                if ev.key == pygame.K_s:
                    self._use_skip()
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                for i in range(4):
                    b = r.btn(f"choice_{i}")
                    if b and b.collidepoint(ev.pos) and i not in self.eliminated:
                        self._answer(i)
                if r.btn("hint_btn") and r.btn("hint_btn").collidepoint(ev.pos):
                    self._use_hint()
                if r.btn("skip_btn") and r.btn("skip_btn").collidepoint(ev.pos):
                    self._use_skip()

    def _upd_feedback(self, events):
        r = self.renderer
        for ev in events:
            if ev.type == pygame.KEYDOWN and ev.key in (pygame.K_RETURN, pygame.K_SPACE):
                self._continue_from_feedback()
            if ev.type == pygame.KEYDOWN and ev.key == pygame.K_d:
                self.fb_deep_mode = not getattr(self, 'fb_deep_mode', False)
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                if r.btn("continue_btn") and r.btn("continue_btn").collidepoint(ev.pos):
                    self._continue_from_feedback()
                if r.btn("fb_deep_toggle") and r.btn("fb_deep_toggle").collidepoint(ev.pos):
                    self.fb_deep_mode = not getattr(self, 'fb_deep_mode', False)

    def _upd_boss_gate(self, events):
        self.boss_gate_elapsed += 1
        for ev in events:
            if ev.type == pygame.KEYDOWN and ev.key in (
                    pygame.K_RETURN, pygame.K_SPACE, pygame.K_ESCAPE):
                self._enter_boss_intro()
                return
        if self.boss_gate_elapsed >= 210:
            self._enter_boss_intro()

    def _enter_boss_intro(self):
        self.boss_intro_elapsed = 0
        self.state = State.BOSS_INTRO

    def _upd_boss_intro(self, events):
        r = self.renderer
        for ev in events:
            if ev.type == pygame.KEYDOWN and ev.key in (pygame.K_RETURN, pygame.K_SPACE):
                self._begin_boss()
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                if r.btn("face_boss") and r.btn("face_boss").collidepoint(ev.pos):
                    self._begin_boss()

    def _begin_boss(self):
        self.dungeon.boss_q_idx   = 0
        self.dungeon.boss_correct = 0
        self._load_boss_question()
        self.state = State.IN_ROOM

    def _upd_boss_result(self, events):
        r = self.renderer
        for ev in events:
            if ev.type == pygame.KEYDOWN and ev.key in (pygame.K_RETURN, pygame.K_SPACE):
                if self.boss_victory:
                    self._proceed_to_shop()       # default: descend
                else:
                    self.state = State.DUNGEON_MAP  # defeat: retreat
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                if self.boss_victory:
                    if r.btn("return_to_floor") and r.btn("return_to_floor").collidepoint(ev.pos):
                        self.state = State.DUNGEON_MAP   # boss_beaten stays True
                    if r.btn("descend_now") and r.btn("descend_now").collidepoint(ev.pos):
                        self._proceed_to_shop()
                else:
                    if r.btn("retreat_btn") and r.btn("retreat_btn").collidepoint(ev.pos):
                        self.state = State.DUNGEON_MAP

    def _upd_shop(self, events):
        r = self.renderer
        for ev in events:
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                for it in self.shop_stock:
                    b = r.btn(f"buy_{it['key']}")
                    if b and b.collidepoint(ev.pos):
                        self._buy_item(it["key"])
                if r.btn("buy_gold_hp") and r.btn("buy_gold_hp").collidepoint(ev.pos):
                    self._buy_gold_hp()
                if r.btn("buy_reroll") and r.btn("buy_reroll").collidepoint(ev.pos):
                    self._buy_reroll()
                if r.btn("leave_shop") and r.btn("leave_shop").collidepoint(ev.pos):
                    self._leave_shop()
            if ev.type == pygame.KEYDOWN and ev.key in (pygame.K_RETURN, pygame.K_SPACE):
                self._leave_shop()

    def _buy_gold_hp(self):
        cost = 50
        if self.player.gold < cost or self.player.hp >= self.player.max_hp:
            return
        self.player.gold -= cost
        self.player.heal(10)

    def _buy_reroll(self):
        cost = 80 + self.shop_reroll_count * 65
        if self.player.gold < cost:
            return
        self.player.gold -= cost
        self.shop_reroll_count += 1
        self._roll_shop_stock()

    def _upd_special_room(self, events):
        r = self.renderer
        for ev in events:
            if ev.type == pygame.KEYDOWN and ev.key in (pygame.K_RETURN, pygame.K_SPACE):
                self._continue_from_special_room()
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                if r.btn("special_continue") and r.btn("special_continue").collidepoint(ev.pos):
                    self._continue_from_special_room()

    def _continue_from_special_room(self):
        found_key = self.dungeon.clear_current_room()
        self._check_scaling()
        self.special_room_type = ""
        if found_key:
            self.notif_text       = "KEY FOUND!  Boss door is now unlocked!"
            self.notif_timer      = 300
            self.key_splash_timer = 90
        self.state = State.DUNGEON_MAP

    def _upd_game_over(self, events):
        r = self.renderer
        for ev in events:
            if ev.type == pygame.KEYDOWN and ev.key in (pygame.K_RETURN, pygame.K_SPACE):
                self._go_to_title()
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                if r.btn("try_again") and r.btn("try_again").collidepoint(ev.pos):
                    self._go_to_title()

    def _upd_victory(self, events):
        r = self.renderer
        for ev in events:
            if ev.type == pygame.KEYDOWN and ev.key in (pygame.K_RETURN, pygame.K_SPACE):
                self._go_to_title()
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                if r.btn("play_again") and r.btn("play_again").collidepoint(ev.pos):
                    self._go_to_title()

    # ── New state handlers ────────────────────────────────────────────────────

    def _upd_campfire_choice(self, events):
        r = self.renderer
        for ev in events:
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                if r.btn("campfire_heal") and r.btn("campfire_heal").collidepoint(ev.pos):
                    self.player.heal(self.special_room_heal)
                    self._finish_campfire()
                elif r.btn("campfire_time") and r.btn("campfire_time").collidepoint(ev.pos):
                    self.player.room_time_bonus = 15.0
                    self._finish_campfire()
            if ev.type == pygame.KEYDOWN:
                if ev.key in (pygame.K_1,):
                    self.player.heal(self.special_room_heal)
                    self._finish_campfire()
                elif ev.key in (pygame.K_2,):
                    self.player.room_time_bonus = 15.0
                    self._finish_campfire()

    def _finish_campfire(self):
        found_key = self.dungeon.clear_current_room()
        self._check_scaling()
        self.special_room_type = ""
        if found_key:
            self.notif_text       = "KEY FOUND!  Boss door is now unlocked!"
            self.notif_timer      = 300
            self.key_splash_timer = 90
        self.state = State.DUNGEON_MAP

    def _upd_vault_gamble(self, events):
        r = self.renderer
        for ev in events:
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                if r.btn("vault_take") and r.btn("vault_take").collidepoint(ev.pos):
                    self.player.gold      += self.vault_gamble_base
                    self.special_room_gold = self.vault_gamble_base
                    found_key = self.dungeon.clear_current_room()
                    self._check_scaling()
                    if found_key:
                        self.notif_text       = "KEY FOUND!  Boss door is now unlocked!"
                        self.notif_timer      = 300
                        self.key_splash_timer = 90
                    self.state = State.DUNGEON_MAP
                elif r.btn("vault_gamble") and r.btn("vault_gamble").collidepoint(ev.pos):
                    self.vault_mode = True
                    self._load_regular_question()
                    self.state = State.IN_ROOM
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_1:
                    self.player.gold      += self.vault_gamble_base
                    self.special_room_gold = self.vault_gamble_base
                    found_key = self.dungeon.clear_current_room()
                    self._check_scaling()
                    if found_key:
                        self.notif_text       = "KEY FOUND!"
                        self.notif_timer      = 300
                        self.key_splash_timer = 90
                    self.state = State.DUNGEON_MAP
                elif ev.key == pygame.K_2:
                    self.vault_mode = True
                    self._load_regular_question()
                    self.state = State.IN_ROOM

    def _upd_paused(self, events):
        if getattr(self, '_pause_just_entered', False):
            self._pause_just_entered = False
            return
        r = self.renderer
        for ev in events:
            if ev.type == pygame.KEYDOWN:
                if ev.key in (pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_SPACE):
                    self.state = self.pause_prev_state
                if ev.key == pygame.K_g:
                    self.pause_prev_state = self.pause_prev_state or State.DUNGEON_MAP
                    self.state = State.GRIMOIRE
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                if r.btn("resume_btn") and r.btn("resume_btn").collidepoint(ev.pos):
                    self.state = self.pause_prev_state
                if r.btn("quit_run_btn") and r.btn("quit_run_btn").collidepoint(ev.pos):
                    self._end_run(victory=False)
                if r.btn("grimoire_btn") and r.btn("grimoire_btn").collidepoint(ev.pos):
                    self.state = State.GRIMOIRE

    def _upd_run_stats(self, events):
        r = self.renderer
        for ev in events:
            if ev.type == pygame.KEYDOWN:
                if ev.key in (pygame.K_RETURN, pygame.K_SPACE):
                    self._go_to_title()
                if ev.key == pygame.K_f and self.wrong_log:
                    self._enter_flashcard_review()
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                if r.btn("stats_done") and r.btn("stats_done").collidepoint(ev.pos):
                    self._go_to_title()
                if r.btn("flashcard_btn") and r.btn("flashcard_btn").collidepoint(ev.pos):
                    self._enter_flashcard_review()

    def _upd_floor_briefing(self, events):
        r = self.renderer
        for ev in events:
            if ev.type == pygame.KEYDOWN and ev.key in (pygame.K_RETURN, pygame.K_SPACE,
                                                         pygame.K_ESCAPE):
                self.floor_briefing_done = True
                self.state = State.DUNGEON_MAP
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                if r.btn("briefing_go") and r.btn("briefing_go").collidepoint(ev.pos):
                    self.floor_briefing_done = True
                    self.state = State.DUNGEON_MAP

    def _upd_grimoire(self, events):
        r = self.renderer
        for ev in events:
            if ev.type == pygame.KEYDOWN and ev.key in (pygame.K_ESCAPE, pygame.K_RETURN,
                                                         pygame.K_SPACE):
                self.state = State.PAUSED
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                if r.btn("grimoire_back") and r.btn("grimoire_back").collidepoint(ev.pos):
                    self.state = State.PAUSED
                if r.btn("grimoire_prev") and r.btn("grimoire_prev").collidepoint(ev.pos):
                    self.grimoire_page = max(0, getattr(self, 'grimoire_page', 0) - 1)
                if r.btn("grimoire_next") and r.btn("grimoire_next").collidepoint(ev.pos):
                    max_p = max(0, (len(self.wrong_log) - 1) // 5)
                    self.grimoire_page = min(max_p, getattr(self, 'grimoire_page', 0) + 1)

    def _upd_flashcard_review(self, events):
        r = self.renderer
        if not self.wrong_log:
            self._go_to_title()
            return
        for ev in events:
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_SPACE and not self.flashcard_revealed:
                    self.flashcard_revealed = True
                elif ev.key in (pygame.K_RETURN, pygame.K_SPACE) and self.flashcard_revealed:
                    self.flashcard_idx += 1
                    self.flashcard_revealed = False
                    if self.flashcard_idx >= len(self.wrong_log):
                        self._go_to_title()
                elif ev.key == pygame.K_ESCAPE:
                    self._go_to_title()
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                if not self.flashcard_revealed:
                    if r.btn("fc_reveal") and r.btn("fc_reveal").collidepoint(ev.pos):
                        self.flashcard_revealed = True
                else:
                    if r.btn("fc_next") and r.btn("fc_next").collidepoint(ev.pos):
                        self.flashcard_idx += 1
                        self.flashcard_revealed = False
                        if self.flashcard_idx >= len(self.wrong_log):
                            self._go_to_title()
                if r.btn("fc_skip_all") and r.btn("fc_skip_all").collidepoint(ev.pos):
                    self._go_to_title()

    # ── Feature 8: Relic select ───────────────────────────────────────────────
    def _upd_relic_select(self, events):
        r = self.renderer
        for ev in events:
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                for i, rk in enumerate(self.relic_choices):
                    b = r.btn(f"relic_{i}")
                    if b and b.collidepoint(ev.pos):
                        self.active_relic = rk
                        self.state = State.FLOOR_BRIEFING
                        return
                # Allow skipping relic selection
                if r.btn("relic_skip") and r.btn("relic_skip").collidepoint(ev.pos):
                    self.active_relic = ""
                    self.state = State.FLOOR_BRIEFING
            if ev.type == pygame.KEYDOWN and ev.key in (pygame.K_1, pygame.K_2, pygame.K_3):
                i = {pygame.K_1: 0, pygame.K_2: 1, pygame.K_3: 2}[ev.key]
                if i < len(self.relic_choices):
                    self.active_relic = self.relic_choices[i]
                    self.state = State.FLOOR_BRIEFING

    # ── Feature 11: Boss attack ───────────────────────────────────────────────
    def _trigger_boss_attack(self):
        attacks = ["timer", "confusion", "drain"]
        self.boss_attack_type    = random.choice(attacks)
        self.boss_attack_elapsed = 0
        self.state               = State.BOSS_ATTACK

    def _upd_boss_attack(self, events):
        # Apply attack effect on first tick
        if self.boss_attack_elapsed == 1:
            if self.boss_attack_type == "timer":
                self.player.question_time = max(5.0, self.player.question_time - 5.0)
                self.notif_text  = "BOSS ATTACK!  Timer Curse: -5s per question this floor!"
                self.notif_timer = 300
            elif self.boss_attack_type == "drain":
                drain = min(75, self.player.gold)
                self.player.gold -= drain
                self.notif_text  = f"BOSS ATTACK!  Gold Drain: lost {drain} gold!"
                self.notif_timer = 300
            # "confusion" is handled by the renderer: shuffle choice display once

        for ev in events:
            if (ev.type == pygame.KEYDOWN and
                    ev.key in (pygame.K_RETURN, pygame.K_SPACE)):
                self._resolve_boss_attack()
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                if self.renderer.btn("boss_atk_continue") and \
                        self.renderer.btn("boss_atk_continue").collidepoint(ev.pos):
                    self._resolve_boss_attack()
        if self.boss_attack_elapsed >= 240:
            self._resolve_boss_attack()

    def _resolve_boss_attack(self):
        self._load_boss_question()
        self.state = State.IN_ROOM

    # ── Feature 9: Floor curse accept ────────────────────────────────────────
    def _accept_floor_curse(self, curse: str, gold_reward: int):
        self.floor_curse          = curse
        self.floor_curse_accepted = True
        self.floor_curse_offered  = False
        self.player.gold         += gold_reward
        self.notif_text           = f"CURSE ACCEPTED!  +{gold_reward} gold."
        self.notif_timer          = 240
        # Apply curse effects immediately if needed
        if curse in ("double_penalty", "dark_covenant"):
            self.player.wrong_penalty = min(
                DIFFICULTIES[self.difficulty]["penalty_max"],
                self.player.wrong_penalty * 2)
        if curse in ("hard_only", "dark_covenant"):
            self.dungeon._active_pool = [
                q for q in self.dungeon._active_pool
                if q.get("_tier") == "hard"
            ]
            if not self.dungeon._active_pool:
                # Fallback: use all questions if no hard tier available
                self.dungeon._active_pool = self.dungeon._tier_pools.get("hard", [])

    def _go_to_title(self):
        self.state                 = State.TITLE
        self.player                = None
        self.dungeon               = None
        self.shop_stock            = []
        self.perfect_boss_discount = ""
        self.daily_challenge_mode  = False
