"""
renderer.py  —  All pygame drawing for Turing's Dungeon
"""
import math
import random as _rng
import pygame
from game import (State, RoomType, SHOP_ITEMS, item_price, DIFFICULTIES,
                  DIFFICULTY_ORDER, boss_q_count, boss_needed_count,
                  RELICS, RELIC_ORDER, DID_YOU_KNOW)
from questions import TOPICS, TOPIC_ORDER

# ──────────────────────────── Palette ────────────────────────────
BG          = (10,  10,  22)
PANEL       = (22,  20,  38)
BORDER      = (70,  60, 100)
GOLD        = (255, 195,  50)
WHITE       = (240, 235, 255)
GRAY        = (130, 120, 150)
DARK_GRAY   = (45,  40,  60)
GREEN       = (50,  210,  90)
GREEN_DIM   = (30,  130,  55)
RED         = (220,  50,  50)
RED_DIM     = (140,  30,  30)
BOSS_BG     = (25,   8,   8)
BOSS_BORDER = (180,  30,  30)
BLUE_ACC    = (60,  130, 255)
PURPLE      = (130,  60, 200)
ORANGE      = (255, 140,  30)
TEAL        = (30,  200, 180)
SHOP_BG     = (8,   18,  30)
GOLD_COIN   = (220, 175,  30)
WARM_AMBER  = (255, 160,  60)   # campfire glow
TREASURE_YL = (255, 210,  40)   # treasure room glow
STONE       = (80,  72,  90)

DIFF_COLORS = {
    "easy":   (50,  210,  90),
    "medium": (255, 195,  50),
    "hard":   (220,  50,  50),
}

TOPIC_COLORS = {
    "DFA":   (60,  130, 255),
    "NFA":   (130,  60, 200),
    "ENFA":  (30,  200, 180),
    "REGEX": (255, 140,  30),
    "PUMP":  (50,  210,  90),
    "CFG":   (160, 100,  40),
    "PDA":   (100, 100, 140),
    "TM":    (170, 170, 180),
    "UTM":   (255, 195,  50),
    "PNP":   (220,  50,  50),
}

TIER_TINTS = {
    "easy":   (40,  100, 200),
    "medium": (200, 120,  20),
    "hard":   (160,  20,  20),
}

SHOP_ICON_COLORS = {
    "hp_up":        (220,  60,  60),
    "time_up":      (60,  180, 255),
    "point_boost":  (255, 195,  50),
    "streak_heal":  (255, 140,  30),
    "hint":         (130,  60, 200),
    "skip":         (50,  210,  90),
    "iron_will":    (180, 180, 220),
    "scholar_mark":  (200, 160,  60),
    "scholar_tome":  (180, 100, 255),
    "dungeon_sense": ( 80, 220, 255),
}

ROOM_TYPE_COLORS = {
    RoomType.REGULAR:       BORDER,
    RoomType.CAMPFIRE:      WARM_AMBER,
    RoomType.CHALLENGE:     RED,
    RoomType.VAULT:         GOLD_COIN,
    RoomType.TREASURE:      TREASURE_YL,
    RoomType.MINI_BOSS:     ORANGE,
    RoomType.BOSS:          BOSS_BORDER,
    RoomType.CURSED:        PURPLE,
    RoomType.TEACH_IT_BACK: TEAL,
}

ROOM_TYPE_LABELS = {
    RoomType.REGULAR:       "ROOM",
    RoomType.CAMPFIRE:      "FIRE",
    RoomType.CHALLENGE:     "!",
    RoomType.VAULT:         "$",
    RoomType.TREASURE:      "CHEST",
    RoomType.MINI_BOSS:     "ELITE",
    RoomType.BOSS:          "BOSS",
    RoomType.CURSED:        "CURSED",
    RoomType.TEACH_IT_BACK: "TEACH",
}

# Flavor text for boss intros per topic
BOSS_FLAVOR = {
    "DFA":   "The Finite Guardian bars your path!",
    "NFA":   "A spectral Nondeterminate haunts this hall!",
    "ENFA":  "Epsilon wraiths flicker between the shadows!",
    "REGEX": "The Pattern Weaver manifests from the void!",
    "PUMP":  "The Pigeonhole Demon blocks the descent!",
    "CFG":   "The Grammar Golem rises from the parse tree!",
    "PDA":   "The Stack Sentinel emerges from the deep!",
    "TM":    "The Infinite Tape Tyrant awakens!",
    "UTM":   "The Universal Overlord accepts this challenge!",
    "PNP":   "The Complexity Colossus towers before you!",
}


# ──────────────────────────── Renderer ────────────────────────────
class Renderer:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.W, self.H = screen.get_size()

        self._surf = pygame.Surface((self.W, self.H))

        pygame.font.init()
        self.f_huge  = pygame.font.SysFont("Consolas,Courier,monospace", 72, bold=True)
        self.f_title = pygame.font.SysFont("Consolas,Courier,monospace", 48, bold=True)
        self.f_large = pygame.font.SysFont("Consolas,Courier,monospace", 32, bold=True)
        self.f_med   = pygame.font.SysFont("Consolas,Courier,monospace", 22)
        self.f_med_b = pygame.font.SysFont("Consolas,Courier,monospace", 22, bold=True)
        self.f_small = pygame.font.SysFont("Consolas,Courier,monospace", 17)
        self.f_tiny  = pygame.font.SysFont("Consolas,Courier,monospace", 14)

        self._buttons:      dict = {}
        self._choice_rects: dict = {}

    def btn(self, name: str):
        return self._buttons.get(name)

    # ── dispatch ──────────────────────────────────────────────────────────────
    def render(self, game):
        self._buttons = {}
        old = self.screen
        self.screen = self._surf

        s = game.state
        if   s == State.TITLE:             self._title(game)
        elif s == State.DIFFICULTY_SELECT: self._difficulty_select(game)
        elif s == State.TOPIC_SELECT:      self._topic_select(game)
        elif s == State.DUNGEON_MAP:       self._dungeon_map(game)
        elif s == State.IN_ROOM:           self._in_room(game)
        elif s == State.FEEDBACK:          self._feedback(game)
        elif s == State.BOSS_INTRO:        self._boss_intro(game)
        elif s == State.BOSS_GATE:         self._boss_gate(game)
        elif s == State.BOSS_RESULT:       self._boss_result(game)
        elif s == State.SHOP:              self._shop(game)
        elif s == State.SPECIAL_ROOM:      self._special_room(game)
        elif s == State.CAMPFIRE_CHOICE:   self._campfire_choice(game)
        elif s == State.VAULT_GAMBLE:      self._vault_gamble(game)
        elif s == State.PAUSED:            self._paused(game)
        elif s == State.RUN_STATS:         self._run_stats(game)
        elif s == State.FLOOR_BRIEFING:    self._floor_briefing(game)
        elif s == State.GRIMOIRE:          self._grimoire(game)
        elif s == State.FLASHCARD_REVIEW:  self._flashcard_review(game)
        elif s == State.RELIC_SELECT:      self._relic_select(game)
        elif s == State.BOSS_ATTACK:       self._boss_attack(game)
        elif s == State.GAME_OVER:         self._game_over(game)
        elif s == State.VICTORY:           self._victory(game)

        # ── overlays (drawn on top of any state) ──────────────────────────
        if game.streak_flash_timer > 0:
            self._draw_streak_flash(game)

        # Mastery surge flash
        if getattr(game, 'surge_flash_timer', 0) > 0:
            self._draw_surge_flash(game)

        # Cursed entry: pulsing purple crossbones
        if getattr(game, 'cursed_entry_timer', 0) > 0:
            self._draw_cursed_entry(game)

        # Key-found splash
        if getattr(game, 'key_splash_timer', 0) > 0:
            self._draw_key_splash(game)

        # Scholar's Tome torn-page animation
        if getattr(game, 'tome_anim_timer', 0) > 0:
            self._draw_tome_anim(game)

        # Floating score popups
        for pop in getattr(game, 'score_popups', []):
            self._draw_score_popup(pop)

        # Low-HP edge pulse (below 30 HP, not on title/select screens)
        if (game.player and game.state not in
                (State.TITLE, State.DIFFICULTY_SELECT, State.TOPIC_SELECT)):
            if game.player.hp < 30:
                self._draw_low_hp_pulse(game)

        self.screen = old

        if game.shake_timer > 0:
            import random as _r
            intensity = max(1, game.shake_timer // 2)
            ox = _r.randint(-intensity, intensity)
            oy = _r.randint(-intensity // 2, intensity // 2)
            self.screen.fill((0, 0, 0))
            self.screen.blit(self._surf, (ox, oy))
            ov = pygame.Surface((self.W, self.H), pygame.SRCALPHA)
            alpha = int(90 * (game.shake_timer / 22))
            ov.fill((180, 0, 0, alpha))
            self.screen.blit(ov, (0, 0))
        else:
            self.screen.blit(self._surf, (0, 0))

    # ══════════════════════════════ SCREENS ══════════════════════════════════

    # ── TITLE ─────────────────────────────────────────────────────────────────
    def _title(self, game):
        self.screen.fill((8, 6, 14))

        # Stone-tile dungeon floor
        tile = 58
        for gx in range(0, self.W + tile, tile):
            for gy in range(0, self.H + tile, tile):
                shade = 14 + ((gx // tile + gy // tile) % 2) * 6
                pygame.draw.rect(self.screen, (shade, shade - 2, shade + 4),
                                 pygame.Rect(gx, gy, tile - 3, tile - 3))

        # Stone wall / arch atmosphere
        arch_cx = self.W // 2
        arch_cy = self.H // 2 - 60

        # Draw a gothic archway behind the title
        for i in range(5):
            r_size = 220 - i * 12
            alpha_s = pygame.Surface((r_size * 2, r_size * 2), pygame.SRCALPHA)
            col_a = max(0, 30 - i * 6)
            pygame.draw.ellipse(alpha_s, (col_a, col_a, col_a + 5, 180),
                                pygame.Rect(0, 0, r_size * 2, r_size * 2))
            self.screen.blit(alpha_s, (arch_cx - r_size, arch_cy - r_size))

        # Arch frame pillars
        pillar_h = 340
        for px in [arch_cx - 230, arch_cx + 170]:
            pygame.draw.rect(self.screen, (35, 30, 45), pygame.Rect(px, self.H // 2 - 120, 58, pillar_h))
            pygame.draw.rect(self.screen, STONE, pygame.Rect(px, self.H // 2 - 120, 58, pillar_h), 2)
            for bry in range(self.H // 2 - 120, self.H // 2 - 120 + pillar_h, 28):
                pygame.draw.line(self.screen, STONE, (px, bry), (px + 58, bry), 1)

        # Torches (animated)
        for tx, ty in [(arch_cx - 190, self.H // 2 - 90), (arch_cx + 192, self.H // 2 - 90)]:
            self._draw_torch(tx, ty, game.tick)

        # Dungeon chains hanging from top
        for cx2 in [arch_cx - 300, arch_cx + 300]:
            for cy2 in range(0, 120, 18):
                pygame.draw.circle(self.screen, STONE, (cx2, cy2), 5)
                pygame.draw.circle(self.screen, (55, 50, 65), (cx2, cy2), 5, 2)

        # Skull decorations on sides
        for sx in [arch_cx - 340, arch_cx + 300]:
            self._draw_skull(sx, self.H // 2 - 30, game.tick)

        # Floating dust particles
        for i in range(20):
            px2 = (i * 137 + game.tick * 2) % self.W
            py2 = (i * 73 + game.tick) % (self.H - 50)
            alpha_d = int(40 + 30 * math.sin(game.tick * 0.02 + i))
            dust = pygame.Surface((4, 4), pygame.SRCALPHA)
            dust.fill((200, 180, 160, alpha_d))
            self.screen.blit(dust, (px2, py2))

        # Title text
        pulse     = int(200 + 55 * math.sin(game.tick * 0.04))
        title_col = (pulse, int(pulse * 0.77), 50)
        self._tc("TURING'S DUNGEON", self.H // 2 - 130, self.f_huge, title_col)

        # Decorative rune line
        rune_y = self.H // 2 - 42
        rune_chars = "~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~"
        rune_s = self.f_tiny.render(rune_chars, True, (80, 60, 40))
        self.screen.blit(rune_s, rune_s.get_rect(centerx=self.W // 2, y=rune_y))

        self._tc("CS 305  \u00b7  Theory of Computation", self.H // 2 - 18, self.f_large, GRAY)
        self._tc("A Dungeon Crawler Study Game", self.H // 2 + 28, self.f_med, (100, 90, 120))

        br = pygame.Rect(self.W // 2 - 190, self.H // 2 + 88, 380, 58)
        # Button with stone border effect
        pygame.draw.rect(self.screen, (20, 15, 30), br.inflate(6, 6), border_radius=14)
        pygame.draw.rect(self.screen, STONE, br.inflate(6, 6), 2, border_radius=14)
        self._button("ENTER  THE  DUNGEON", br, (18, 14, 28), (30, 22, 45),
                     GOLD, self.f_med_b, "start_btn")

        # Feature 13: Daily Challenge button
        from datetime import date as _dt
        today = _dt.today().strftime("%b %d, %Y")
        dr = pygame.Rect(self.W // 2 - 190, self.H // 2 + 162, 380, 46)
        self._button(f"DAILY  CHALLENGE  —  {today}", dr,
                     (5, 35, 50), (10, 55, 80), TEAL, self.f_small, "daily_btn")

        if int(game.tick * 0.05) % 2 == 0:
            self._tc("Press  ENTER  or  click  to  begin", self.H // 2 + 222, self.f_small, GRAY)

        # Ground/floor line
        pygame.draw.line(self.screen, STONE, (0, self.H - 50), (self.W, self.H - 50), 2)
        self._tc("1/2/3/4  or  A/B/C/D = answer   H = hint   S = skip",
                 self.H - 36, self.f_small, (60, 55, 75))

    def _draw_torch(self, x: int, y: int, tick: int):
        """Draw an animated wall torch at (x, y)."""
        # Bracket
        pygame.draw.rect(self.screen, (60, 55, 70), pygame.Rect(x - 6, y, 12, 28), border_radius=3)
        # Torch handle
        pygame.draw.rect(self.screen, (100, 80, 50), pygame.Rect(x - 3, y - 10, 6, 18), border_radius=2)

        # Animated flame
        for fi in range(6):
            fh = 14 + int(8 * math.sin(tick * 0.15 + fi * 1.1))
            fw = 7 - fi
            fy = y - 10 - fi * 4
            fx = x - fw // 2 + int(3 * math.sin(tick * 0.12 + fi * 0.7))
            col = (WARM_AMBER[0], max(0, 140 - fi * 22), 0) if fi < 3 else (255, 255, 80)
            if fw > 0 and fh > 0:
                pygame.draw.ellipse(self.screen, col, pygame.Rect(fx, fy, fw, fh))

        # Glow halo
        glow = pygame.Surface((80, 80), pygame.SRCALPHA)
        glow_a = int(40 + 20 * math.sin(tick * 0.1))
        pygame.draw.circle(glow, (255, 160, 60, glow_a), (40, 40), 38)
        self.screen.blit(glow, (x - 40, y - 50))

    def _draw_skull(self, x: int, y: int, tick: int):
        """Draw a simple skull decoration."""
        bob = int(3 * math.sin(tick * 0.03))
        y += bob
        # Skull dome
        pygame.draw.circle(self.screen, (50, 46, 58), (x, y), 22)
        pygame.draw.circle(self.screen, STONE, (x, y), 22, 2)
        # Eyes
        for ex in [x - 8, x + 8]:
            pygame.draw.circle(self.screen, BG, (ex, y - 2), 6)
            pygame.draw.circle(self.screen, (30, 25, 40), (ex, y - 2), 6, 1)
        # Jaw
        pygame.draw.rect(self.screen, (45, 42, 54), pygame.Rect(x - 14, y + 10, 28, 12), border_radius=3)
        pygame.draw.rect(self.screen, STONE, pygame.Rect(x - 14, y + 10, 28, 12), 1, border_radius=3)

    # ── DIFFICULTY SELECT ──────────────────────────────────────────────────────
    def _difficulty_select(self, game):
        self.screen.fill(BG)
        self._draw_dungeon_bg(game.tick)

        self._tc("SELECT  DIFFICULTY", 22, self.f_title, GOLD)
        self._tc("Timer \u00b7 HP \u00b7 Penalties \u00b7 Question depth all scale with your choice",
                 76, self.f_tiny, GRAY)
        self._tc("Press  1 / 2 / 3  or  click  a  card", 96, self.f_tiny, DARK_GRAY)

        card_w  = 340
        gap     = (self.W - 3 * card_w) // 4
        card_h  = 520
        card_y  = 118
        hov_pos = pygame.mouse.get_pos()

        for i, dk in enumerate(DIFFICULTY_ORDER):
            dc   = DIFFICULTIES[dk]
            col  = DIFF_COLORS[dk]
            cx   = gap + i * (card_w + gap)
            card = pygame.Rect(cx, card_y, card_w, card_h)
            hov  = card.collidepoint(hov_pos)

            tint = (col[0] // 8, col[1] // 8, col[2] // 8)
            pygame.draw.rect(self.screen, tint, card, border_radius=14)
            bw = 4 if hov else 2
            pygame.draw.rect(self.screen, col, card, bw, border_radius=14)

            lbl = self.f_title.render(dc["label"], True, col)
            self.screen.blit(lbl, lbl.get_rect(centerx=card.centerx, y=card_y + 14))

            pygame.draw.line(self.screen, col,
                             (cx + 20, card_y + 70), (cx + card_w - 20, card_y + 70), 2)

            by = card_y + 84
            for bullet in dc["bullets"]:
                dot = self.f_small.render("\u00bb", True, col)
                self.screen.blit(dot, (cx + 12, by))
                # Render with small font to avoid overflow
                txt_surf = self.f_small.render(bullet, True, WHITE if hov else GRAY)
                # Clip if wider than card
                avail = card_w - 40
                if txt_surf.get_width() > avail:
                    clip = pygame.Surface((avail, txt_surf.get_height()))
                    clip.blit(txt_surf, (0, 0))
                    self.screen.blit(clip, (cx + 28, by))
                else:
                    self.screen.blit(txt_surf, (cx + 28, by))
                by += 26

            num_s = self.f_small.render(f"Press  {i + 1}", True, col)
            self.screen.blit(num_s, num_s.get_rect(centerx=card.centerx, y=card_y + card_h - 58))

            sel_r = pygame.Rect(cx + 28, card_y + card_h - 42, card_w - 56, 36)
            self._button("SELECT", sel_r,
                         (col[0] // 5, col[1] // 5, col[2] // 5),
                         (col[0] // 3, col[1] // 3, col[2] // 3),
                         col, self.f_med_b, f"diff_{dk}")

    # ── TOPIC SELECT ───────────────────────────────────────────────────────────
    def _topic_select(self, game):
        self.screen.fill(BG)
        self._draw_dungeon_bg(game.tick)

        dc  = DIFFICULTIES[game.difficulty]
        col = DIFF_COLORS[game.difficulty]
        self._draw_diff_badge(col, dc["label"], (self.W - 120, 14))

        self._tc("CHOOSE YOUR TOPICS", 30, self.f_title, GOLD)
        self._tc("Questions mix all chosen topics  \u00b7  each topic adds 5 floors",
                 84, self.f_small, GRAY)

        col_x   = [self.W // 2 - 420, self.W // 2 + 18]
        start_y = 126
        row_h   = 58
        row_w   = 394

        for i, key in enumerate(TOPIC_ORDER):
            col2 = i // 5
            row  = i % 5
            x    = col_x[col2]
            y    = start_y + row * row_h
            sel  = key in game.selected_topics
            tc   = TOPIC_COLORS[key]

            row_rect = pygame.Rect(x, y, row_w, 48)
            if sel:
                pygame.draw.rect(self.screen, (tc[0]//6, tc[1]//6, tc[2]//6),
                                 row_rect, border_radius=8)
            pygame.draw.rect(self.screen, tc if sel else DARK_GRAY, row_rect, 2, border_radius=8)
            self._buttons[f"cb_{key}"] = row_rect

            cb = pygame.Rect(x + 8, y + 10, 26, 26)
            pygame.draw.rect(self.screen, DARK_GRAY, cb, border_radius=4)
            pygame.draw.rect(self.screen, tc if sel else BORDER, cb, 2, border_radius=4)
            if sel:
                pygame.draw.rect(self.screen, tc, cb.inflate(-8, -8), border_radius=2)

            # Abbreviate topic name if it would overflow
            full_name  = TOPICS[key]
            name_surf  = (self.f_med_b if sel else self.f_med).render(full_name, True,
                                                                       WHITE if sel else GRAY)
            max_name_w = row_w - 110
            if name_surf.get_width() > max_name_w:
                # Try shorter version
                short = full_name[:18] + ("…" if len(full_name) > 18 else "")
                name_surf = (self.f_med_b if sel else self.f_med).render(
                    short, True, WHITE if sel else GRAY)
            self.screen.blit(name_surf, (x + 42, y + 12))

            badge = pygame.Rect(x + row_w - 54, y + 11, 46, 24)
            pygame.draw.rect(self.screen, tc if sel else DARK_GRAY, badge, border_radius=4)
            self._t(key[:5], (badge.x + 4, badge.y + 4), self.f_tiny, WHITE)

        bw = 160
        by = self.H - 96
        r_back  = pygame.Rect(self.W // 2 - 380, by, 120, 44)
        r_sel   = pygame.Rect(self.W // 2 - 242, by, bw, 44)
        r_clr   = pygame.Rect(self.W // 2 - 70,  by, bw, 44)
        r_begin = pygame.Rect(self.W // 2 + 106,  by, bw + 60, 44)

        self._button("\u2190 BACK",    r_back,  DARK_GRAY, PANEL, GRAY,  self.f_small, "back_diff")
        self._button("SELECT ALL", r_sel,   DARK_GRAY, PANEL, GRAY,  self.f_small, "sel_all")
        self._button("CLEAR ALL",  r_clr,   DARK_GRAY, PANEL, GRAY,  self.f_small, "clr_all")

        n = len(game.selected_topics)
        total_floors = max(5, n * 5)
        if n:
            self._button("BEGIN ADVENTURE  \u25ba", r_begin, (20, 60, 20), (30, 90, 30),
                         GREEN, self.f_med_b, "begin")
        else:
            pygame.draw.rect(self.screen, DARK_GRAY, r_begin, border_radius=8)
            pygame.draw.rect(self.screen, BORDER,    r_begin, 2, border_radius=8)
            txt = self.f_small.render("Select a topic first", True, GRAY)
            self.screen.blit(txt, txt.get_rect(center=r_begin.center))

        lbl = (f"{n} topic{'s' if n != 1 else ''} selected  \u00b7  {total_floors} floors to clear"
               if n else "Select at least one topic to begin")
        self._tc(lbl, by - 26, self.f_small, GOLD if n else GRAY)

    # ── DUNGEON MAP ────────────────────────────────────────────────────────────
    def _dungeon_map(self, game):
        d      = game.dungeon
        p      = game.player
        dc_col = DIFF_COLORS[game.difficulty]

        tiers     = d.unlocked_tiers()
        tier_tint = TIER_TINTS[tiers[-1]]
        if d.floor >= d.max_floors:
            tier_tint = (200, 15, 15)

        self.screen.fill(BG)
        self._draw_dungeon_bg(game.tick, tint=tier_tint, strength=10)

        fl_col = (220, 30, 30) if d.floor >= d.max_floors else dc_col
        hdr    = (f"FINAL DESCENT  \u2014  FLOOR  {d.floor}  /  {d.max_floors}"
                  if d.floor >= d.max_floors
                  else f"FLOOR  {d.floor}  /  {d.max_floors}")
        self._tc(hdr, 18, self.f_title, fl_col)

        tier_str = "  +  ".join(t.upper() for t in tiers) + "  QUESTIONS"
        self._tc(tier_str, 72, self.f_small, GRAY)

        self._draw_hud(p, game.difficulty)

        # Room progress bar
        done  = d.non_boss_cleared
        total = d.non_boss_total
        pr    = pygame.Rect(60, 96, self.W - 120, 12)
        self._progress_bar(done, total, pr, dc_col)
        overall_pct = int(100 * (d.floor - 1) / max(1, d.max_floors))
        self._t(f"Rooms {done}/{total}   ·   Floor {d.floor}/{d.max_floors}   ·   Overall: {overall_pct}%",
                (pr.x, pr.bottom + 4), self.f_small, GRAY)
        key_lbl = "KEY: FOUND" if d.has_key else "KEY: ???"
        key_col = GOLD if d.has_key else (80, 70, 50)
        key_s   = self.f_small.render(key_lbl, True, key_col)
        self.screen.blit(key_s, key_s.get_rect(topright=(self.W - 62, pr.bottom + 4)))

        # Notification banner
        if game.notif_timer > 0:
            pulse  = int(game.tick * 0.06) % 2 == 0
            is_key = "KEY FOUND" in game.notif_text
            n_col  = (GOLD if is_key else dc_col) if pulse else ORANGE
            nr     = pygame.Rect(60, 120, self.W - 120, 32)
            pygame.draw.rect(self.screen, (30, 20, 5), nr, border_radius=8)
            pygame.draw.rect(self.screen, n_col, nr, 2, border_radius=8)
            self._tc(game.notif_text, nr.y + 7, self.f_small, n_col)

        # Floor map — graph-based room nodes
        self._draw_floor_map(game, dc_col)

        # "Descend Deeper" persistent button when boss is beaten
        if game.boss_beaten:
            db = pygame.Rect(self.W // 2 - 160, self.H - 70, 320, 50)
            self._button("DESCEND  DEEPER  ►", db,
                         (10, 50, 10), (20, 80, 20), GREEN, self.f_large, "descend_now")
            self._tc("Press  ENTER  to  continue  to  the  shop",
                     self.H - 12, self.f_tiny, DARK_GRAY)
        else:
            # Bottom hint
            if d.has_key:
                self._tc("Key found!  Enter the boss room  (?)  to fight.",
                         self.H - 28, self.f_small, ORANGE)
            else:
                self._tc("Explore rooms to find the key  —  boss door stays locked without it.",
                         self.H - 28, self.f_small, GRAY)

        # Feature 9: Floor curse offer panel
        curse_offered = getattr(game, 'floor_curse_offered', False)
        curse_accepted = getattr(game, 'floor_curse_accepted', False)
        if curse_offered and not curse_accepted:
            ov = pygame.Surface((self.W, self.H), pygame.SRCALPHA)
            ov.fill((0, 0, 0, 150))
            self.screen.blit(ov, (0, 0))
            bx = self.W // 2 - 310
            by = self.H // 2 - 160
            box = pygame.Rect(bx, by, 620, 330)
            pygame.draw.rect(self.screen, (18, 6, 28), box, border_radius=14)
            pygame.draw.rect(self.screen, PURPLE, box, 3, border_radius=14)
            self._tc("FLOOR  CURSE  OFFER", by + 14, self.f_large, PURPLE)
            self._tc("Accept a curse for bonus gold. Effects last this floor only.",
                     by + 52, self.f_small, GRAY)
            curses = [
                ("hard_only",       "Hard Only",       "+200g",  "Only hard-tier questions",       "curse_hard"),
                ("no_hints",        "No Hints",        "+150g",  "Hints sealed this floor",        "curse_nohint"),
                ("double_penalty",  "Double Penalty",  "+150g",  "Wrong answer HP cost x2",        "curse_double"),
                ("dark_covenant",   "Dark Covenant",   "+500g",  "Hard Only + No Hints + x2 HP",   "curse_dark"),
            ]
            for ci, (key, name, reward, desc, btn_k) in enumerate(curses):
                col_i  = ci % 2
                row_i  = ci // 2
                cbx    = bx + 20 + col_i * 295
                cby    = by + 84 + row_i * 100
                cr2    = pygame.Rect(cbx, cby, 280, 88)
                glow   = GOLD if key == "dark_covenant" else PURPLE
                pygame.draw.rect(self.screen, (28, 12, 40), cr2, border_radius=8)
                pygame.draw.rect(self.screen, glow, cr2, 2, border_radius=8)
                ns = self.f_med_b.render(name, True, glow)
                self.screen.blit(ns, (cbx + 10, cby + 8))
                rs = self.f_med_b.render(reward, True, GOLD)
                self.screen.blit(rs, (cbx + cr2.w - rs.get_width() - 10, cby + 8))
                ds = self.f_tiny.render(desc, True, GRAY)
                self.screen.blit(ds, (cbx + 10, cby + 34))
                bb = pygame.Rect(cbx + 10, cby + 54, 260, 28)
                self._button("ACCEPT", bb, (50, 10, 70), (80, 20, 110), glow, self.f_small, btn_k)
            dec_r = pygame.Rect(self.W // 2 - 130, box.bottom - 44, 260, 36)
            self._button("DECLINE  (no gold)", dec_r, DARK_GRAY, BORDER, GRAY, self.f_small, "curse_decline")

        # Boss confirm overlay
        if game.boss_confirm_idx >= 0:
            ov = pygame.Surface((self.W, self.H), pygame.SRCALPHA)
            ov.fill((0, 0, 0, 160))
            self.screen.blit(ov, (0, 0))
            bx = self.W // 2 - 260
            by = self.H // 2 - 100
            box = pygame.Rect(bx, by, 520, 200)
            pygame.draw.rect(self.screen, (30, 8, 8),  box, border_radius=14)
            pygame.draw.rect(self.screen, BOSS_BORDER, box, 3, border_radius=14)
            self._tc("ENTER  THE  BOSS  ROOM?", by + 22, self.f_large, RED)
            self._tc("The guardian awaits.  You cannot leave once inside.",
                     by + 68, self.f_small, GRAY)
            bw = 200
            yes_r = pygame.Rect(self.W // 2 - bw - 10, by + 108, bw, 52)
            no_r  = pygame.Rect(self.W // 2 + 10,       by + 108, bw, 52)
            self._button("ENTER  ►", yes_r, (60, 10, 10), (90, 18, 18),
                         RED, self.f_large, "boss_confirm_yes")
            self._button("CANCEL", no_r,  (20, 20, 35), (35, 35, 55),
                         GRAY, self.f_large, "boss_confirm_no")
            self._tc("ENTER  to  confirm     ESC  to  cancel",
                     by + 172, self.f_tiny, DARK_GRAY)

    def _draw_stone_room(self, rect, interior, frame, brd_col, brd_w=2):
        """Draw a stone-walled dungeon room node."""
        pygame.draw.rect(self.screen, frame, rect, border_radius=5)
        inner = rect.inflate(-8, -8)
        pygame.draw.rect(self.screen, interior, inner, border_radius=3)
        # Mortar texture lines
        lc = tuple(min(255, c + 20) for c in interior)
        h3 = max(1, inner.height // 3)
        for by in [inner.y + h3, inner.y + h3 * 2]:
            pygame.draw.line(self.screen, lc, (inner.x + 3, by), (inner.right - 3, by), 1)
        pygame.draw.rect(self.screen, brd_col, rect, brd_w, border_radius=5)

    def _draw_floor_map(self, game, dc_col):
        """Graph-based floor map with dungeon-stone aesthetic."""
        d     = game.dungeon
        graph = d.graph
        if not graph:
            return

        accessible = set(d.accessible_rooms)
        mouse      = pygame.mouse.get_pos()
        node_w, node_h = 88, 54

        cols = [r['col'] for r in graph]
        rows = [r['row'] for r in graph]
        min_col, max_col = min(cols), max(cols)
        min_row, max_row = min(rows), max(rows)
        col_span = max(1, max_col - min_col)
        row_span = max(1, max_row - min_row)

        # Compact centered map width
        map_total_w = min(self.W - 100, col_span * 120 + node_w + 40)
        map_x0  = (self.W - map_total_w) // 2
        map_y0  = 158
        map_y1  = self.H - (110 if game.boss_beaten else 80)
        map_h   = map_y1 - map_y0

        def screen_pos(col, row):
            sx  = map_x0 + int((col - min_col) / col_span * (map_total_w - node_w)) + node_w // 2
            mid = map_y0 + map_h // 2
            if row_span == 0:
                sy = mid
            else:
                sy = mid + int((row - (min_row + max_row) / 2) / row_span * map_h * 0.68)
            return sx, sy

        centers = [screen_pos(r['col'], r['row']) for r in graph]

        # ── Stone corridors (drawn behind nodes) ──────────────────────────────
        drawn = set()
        for i, room in enumerate(graph):
            for j in room['adj']:
                edge = (min(i, j), max(i, j))
                if edge in drawn:
                    continue
                drawn.add(edge)
                sx1, sy1 = centers[i]
                sx2, sy2 = centers[j]
                dx, dy   = sx2 - sx1, sy2 - sy1
                dist     = max(1, (dx*dx + dy*dy) ** 0.5)
                ox = int(dx / dist * (node_w // 2 + 2))
                oy = int(dy / dist * (node_h // 2 + 2))
                p1 = (sx1 + ox, sy1 + oy)
                p2 = (sx2 - ox, sy2 - oy)
                cleared_edge = graph[i]['cleared'] or graph[j]['cleared']
                # Outer stone shadow, inner corridor, centre highlight
                pygame.draw.line(self.screen, (22, 18, 32), p1, p2, 11)
                pygame.draw.line(self.screen, (48, 40, 62), p1, p2,  7)
                cline = GREEN_DIM if cleared_edge else (36, 30, 50)
                pygame.draw.line(self.screen, cline,        p1, p2,  2)

        key_revealed = getattr(d, 'key_revealed', False)

        # ── Room nodes ────────────────────────────────────────────────────────
        for i, room in enumerate(graph):
            ncx, ncy = centers[i]
            nr      = pygame.Rect(ncx - node_w // 2, ncy - node_h // 2, node_w, node_h)
            cleared = room['cleared']
            rt      = room['rt']
            is_boss     = (i == d.boss_idx)
            is_key_room = (i == d.key_room_idx)

            if cleared:
                if is_boss:
                    self._draw_stone_room(nr, (10, 28, 12), (34, 78, 40), GREEN_DIM, 2)
                    ls  = self.f_small.render("BOSS",    True, GREEN)
                    sub = self.f_tiny.render("cleared", True, GREEN_DIM)
                    self.screen.blit(ls,  ls.get_rect(center=(nr.centerx, nr.centery - 9)))
                    self.screen.blit(sub, sub.get_rect(center=(nr.centerx, nr.centery + 10)))
                elif is_key_room:
                    self._draw_stone_room(nr, (26, 20, 6), (72, 58, 18), GOLD, 2)
                    kx, ky = nr.centerx - 8, nr.centery - 3
                    pygame.draw.circle(self.screen, GOLD, (kx, ky), 5, 2)
                    pygame.draw.line(self.screen, GOLD, (kx+5, ky), (kx+16, ky), 2)
                    pygame.draw.line(self.screen, GOLD, (kx+12, ky), (kx+12, ky+4), 2)
                    pygame.draw.line(self.screen, GOLD, (kx+16, ky), (kx+16, ky+4), 2)
                    sub = self.f_tiny.render("KEY ROOM", True, GOLD)
                    self.screen.blit(sub, sub.get_rect(center=(nr.centerx, nr.bottom - 8)))
                else:
                    rt_lbl = ROOM_TYPE_LABELS.get(rt, "?")
                    rt_col = ROOM_TYPE_COLORS.get(rt, GREEN_DIM)
                    self._draw_stone_room(nr, (10, 28, 16), (28, 72, 42), GREEN_DIM, 2)
                    ls  = self.f_small.render(rt_lbl, True, rt_col)
                    self._draw_room_icon(nr.centerx, nr.centery - 4, rt)
                    sub = self.f_tiny.render("done", True, (28, 72, 42))
                    self.screen.blit(ls,  ls.get_rect(center=(nr.centerx, nr.centery - 13)))
                    self.screen.blit(sub, sub.get_rect(center=(nr.centerx, nr.bottom - 6)))

            elif i in accessible:
                # Dungeon Sense: reveal key room before clearing
                if key_revealed and is_key_room:
                    pulse = (game.tick // 8) % 2 == 0
                    fc    = (50, 40, 5) if pulse else (30, 24, 4)
                    self._draw_stone_room(nr, fc, (90, 72, 14), GOLD, 3 if pulse else 2)
                    ql  = self.f_large.render("?", True, GOLD)
                    lbl = self.f_tiny.render("KEY HERE", True, GOLD)
                    self.screen.blit(ql,  ql.get_rect(center=(nr.centerx, nr.centery - 8)))
                    self.screen.blit(lbl, lbl.get_rect(center=(nr.centerx, nr.centery + 12)))
                    self._buttons[f"room_{i}"] = nr
                else:
                    hov  = nr.collidepoint(mouse)
                    nr_d = nr.inflate(6, 6) if hov else nr
                    if hov:
                        self._draw_stone_room(nr_d, (30, 22, 42), (88, 78, 108), WHITE, 3)
                        ql  = self.f_large.render("?", True, WHITE)
                        clk = self.f_tiny.render("enter", True, GOLD)
                    else:
                        self._draw_stone_room(nr_d, (24, 16, 18), STONE, WARM_AMBER, 2)
                        ql  = self.f_large.render("?", True, (218, 196, 172))
                        clk = self.f_tiny.render("click", True, WARM_AMBER)
                    self.screen.blit(ql,  ql.get_rect(center=(nr_d.centerx, nr_d.centery - 8)))
                    self.screen.blit(clk, clk.get_rect(center=(nr_d.centerx, nr_d.centery + 12)))
                    self._buttons[f"room_{i}"] = nr_d
                    if hov:
                        tip  = self.f_tiny.render("Unknown room  —  enter to discover", True, GOLD)
                        ty_t = nr_d.y - tip.get_height() - 6
                        tx_t = max(0, min(self.W - tip.get_width() - 4,
                                         nr_d.centerx - tip.get_width() // 2))
                        self.screen.blit(tip, (tx_t, ty_t))

            else:
                # Inaccessible — cold dark stone, barely visible
                self._draw_stone_room(nr, (8, 6, 14), (40, 34, 52), (36, 30, 46), 1)
                ql = self.f_large.render("?", True, (44, 38, 56))
                self.screen.blit(ql, ql.get_rect(center=nr.center))
    # ── IN ROOM ────────────────────────────────────────────────────────────────
    def _in_room(self, game):
        boss  = game.in_boss_mode
        mb    = game.mini_boss_mode
        chal  = game.challenge_mode
        vault = game.vault_mode
        tib   = getattr(game, 'teach_it_back_mode', False)

        if boss:
            bg_tint = BOSS_BORDER
        else:
            topic   = game.dungeon.current_topic
            bg_tint = TOPIC_COLORS.get(topic, BLUE_ACC)

        self.screen.fill(BOSS_BG if boss else BG)
        self._draw_dungeon_bg(game.tick, rough=True, tint=bg_tint, strength=8)

        d  = game.dungeon
        p  = game.player
        q  = game.q_data
        tc = BOSS_BORDER if boss else bg_tint

        self._draw_hud(p, game.difficulty, dungeon=d)

        # Feature 8: active relic badge
        ar = getattr(game, 'active_relic', '')
        if ar and ar in RELICS:
            rc   = RELICS[ar]["color"]
            rn   = RELICS[ar]["name"]
            rs2  = self.f_tiny.render(f"[{RELICS[ar]['icon']}] {rn}", True, rc)
            self.screen.blit(rs2, (self.W - rs2.get_width() - 14, 100))

        # Feature 13: daily challenge badge
        if getattr(game, 'daily_challenge_mode', False):
            ds = self.f_tiny.render("★ DAILY CHALLENGE", True, TEAL)
            self.screen.blit(ds, (self.W - ds.get_width() - 14, 116))

        if boss:
            total  = game.boss_q_total
            needed = game.boss_needed_now
            fl_lbl = (f"FINAL BOSS  \u2014  FLOOR {d.floor}"
                      if d.floor >= d.max_floors else f"FLOOR {d.floor}")
            self._tc(f"{fl_lbl}  \u00b7  BOSS FIGHT  \u00b7  "
                     f"Q {d.boss_q_idx + 1}/{total}  \u00b7  Need {needed}/{total} to win",
                     60, self.f_med_b, BOSS_BORDER)
        elif mb:
            self._tc(f"Floor {d.floor}  \u00b7  ELITE GUARDIAN  \u00b7  "
                     f"{TOPICS.get(d.current_topic, d.current_topic)}"
                     f"  \u00b7  [No HP penalty]",
                     60, self.f_med_b, ORANGE)
        elif chal:
            # Full-width pulsing challenge banner
            pulse    = (game.tick // 7) % 2 == 0
            ban_fill = (185, 12, 0) if pulse else (130, 6, 0)
            ban_brd  = (255, 75, 20) if pulse else (190, 42, 10)
            ban_r    = pygame.Rect(0, 44, self.W, 40)
            pygame.draw.rect(self.screen, ban_fill, ban_r)
            pygame.draw.rect(self.screen, ban_brd,  ban_r, 3)
            warn_col = (255, 225, 40) if pulse else (255, 180, 30)
            self._tc("!! CHALLENGE ROOM !!  DOUBLE HP PENALTY  |  +1 HINT  !!",
                     ban_r.y + 10, self.f_med_b, warn_col)
            # Pulsing red screen-edge glow when challenge is active
            if pulse:
                glow = pygame.Surface((self.W, self.H), pygame.SRCALPHA)
                pygame.draw.rect(glow, (210, 20, 0, 70),
                                 pygame.Rect(0, 0, self.W, self.H), 10)
                self.screen.blit(glow, (0, 0))
        elif vault:
            self._tc(f"Floor {d.floor}  \u00b7  VAULT ROOM  \u00b7  +500 Gold on correct!",
                     60, self.f_med, GOLD_COIN)
        elif tib:
            ban_r = pygame.Rect(0, 44, self.W, 40)
            pygame.draw.rect(self.screen, (8, 48, 48), ban_r)
            pygame.draw.rect(self.screen, TEAL, ban_r, 3)
            self._tc("TEACH IT BACK  \u2014  The answer is shown. Pick the matching QUESTION!",
                     ban_r.y + 10, self.f_med_b, TEAL)
        else:
            weak_marker = "\u26a0 WEAK POOL  " if getattr(game.q_data, '_weak', False) else ""
            self._tc(f"{weak_marker}Floor {d.floor}  \u00b7  Room  \u00b7  "
                     f"{TOPICS.get(d.current_topic, d.current_topic)}", 60, self.f_med, tc)

        tr = pygame.Rect(60, 84, self.W - 220, 20)
        self._timer_bar(game.time_left, p.question_time, tr)
        ts  = self.f_small.render(f"{max(0, int(game.time_left))}s", True, WHITE)
        self.screen.blit(ts, (tr.right + 8, tr.y))
        pen_s = self.f_tiny.render(f"Wrong: \u2212{p.wrong_penalty} HP", True, RED_DIM)
        self.screen.blit(pen_s, (self.W - pen_s.get_width() - 14, tr.y))

        # Feature 14: Combo meter \u2014 show streak multiplier visually when streak >= 2
        streak = p.streak
        if streak >= 2:
            combo_flash = getattr(game, 'combo_flash_timer', 0)
            alpha_scale = min(1.0, combo_flash / 20.0) if combo_flash > 0 else 0.55
            combo_col   = GOLD if streak >= 5 else (ORANGE if streak >= 3 else WHITE)
            combo_txt   = f"x{streak}  COMBO  \u00d7{1 + p.streak_bonus:.1f}"
            if combo_flash > 0:
                pulse_size = int(32 + 8 * (combo_flash / 40.0))
                f_combo = pygame.font.SysFont("Consolas,Courier,monospace", pulse_size, bold=True)
            else:
                f_combo = self.f_med_b
            cs = f_combo.render(combo_txt, True, combo_col)
            cs.set_alpha(int(alpha_scale * 230))
            self.screen.blit(cs, cs.get_rect(centerx=self.W // 2, y=44))

        qr = pygame.Rect(50, 112, self.W - 100, 200)
        pygame.draw.rect(self.screen, PANEL, qr, border_radius=10)
        pygame.draw.rect(self.screen, tc, qr, 2, border_radius=10)
        if boss:
            flavor = "The guardian rises \u2014 defend your knowledge!"
        elif mb:
            flavor = "An elite champion blocks the path. Defeat it!"
        elif tib:
            flavor = "This is the ANSWER \u2014 which question does it belong to?"
        else:
            consec = (game.dungeon._q_consec_wrong.get(game.dungeon._q_hash(q), 0)
                      if (not boss and game.dungeon) else 0)
            if consec >= 2:
                flavor = f"\u26a0 This question has challenged you before ({consec} streak)"
            else:
                flavor = "A phantom scholar challenges you..."
        self._t(flavor, (qr.x + 18, qr.y + 10), self.f_small, TEAL if tib else GRAY)
        q_text = getattr(game, '_teach_it_back_prompt', "") if tib else q["q"]
        self._draw_wrapped(q_text, pygame.Rect(qr.x + 18, qr.y + 34, qr.w - 36, 162),
                           self.f_med_b, TEAL if tib else WHITE)

        choices   = getattr(game, 'q_data_choices', q["c"])
        ans_idx   = getattr(game, 'q_data_answer',  q["a"])
        n_choices = len(choices)

        # Layout: 1 row if 2 choices, else 2\u00d72 grid
        if n_choices <= 2:
            bw = (self.W - 140)
            bh = 68
            bx = [60]
            by = [self.H - 210, self.H - 130]
        else:
            bw = (self.W - 120) // 2 - 10
            bh = 68
            bx = [60, 60 + bw + 20]
            by = [self.H - 210, self.H - 130]

        self._choice_rects = {}
        for idx in range(n_choices):
            if n_choices <= 2:
                rect = pygame.Rect(70, by[idx], self.W - 140, bh)
            else:
                rect = pygame.Rect(bx[idx % 2], by[idx // 2], bw, bh)
            self._choice_rects[idx] = rect
            elim = idx in game.eliminated
            answ = game.chosen != -1

            if elim:
                fill, brd, tc2 = DARK_GRAY, DARK_GRAY, GRAY
            elif answ:
                if idx == ans_idx:       fill, brd, tc2 = (15, 75, 25), GREEN, GREEN
                elif idx == game.chosen: fill, brd, tc2 = (75, 15, 15), RED, RED
                else:                   fill, brd, tc2 = DARK_GRAY, BORDER, GRAY
            else:
                hov  = rect.collidepoint(pygame.mouse.get_pos())
                fill = (8, 50, 50) if (hov and tib) else ((35, 50, 80) if hov else PANEL)
                brd  = TEAL if (hov and tib) else (BLUE_ACC if hov else BORDER)
                tc2  = WHITE

            pygame.draw.rect(self.screen, fill, rect, border_radius=10)
            pygame.draw.rect(self.screen, brd, rect, 2, border_radius=10)

            badge = pygame.Rect(rect.x + 10, rect.y + (bh - 34) // 2, 34, 34)
            pygame.draw.rect(self.screen, brd if not elim else DARK_GRAY, badge, border_radius=6)
            bl = self.f_med_b.render("ABCD"[idx], True, WHITE if not elim else GRAY)
            self.screen.blit(bl, bl.get_rect(center=badge.center))

            self._draw_wrapped(choices[idx],
                               pygame.Rect(rect.x + 54, rect.y + 8, rect.w - 64, rect.h - 16),
                               self.f_small, GRAY if elim else tc2)
            if not elim:
                self._buttons[f"choice_{idx}"] = rect

        if game.answer_anim_timer > 0 and game.chosen >= 0:
            chosen_rect = self._choice_rects.get(game.chosen)
            if chosen_rect:
                t_frac   = game.answer_anim_timer / 20
                radius   = int((1 - t_frac) * 120 + 20)
                alpha    = int(t_frac * 200)
                ring_col = GREEN if game.answer_anim_correct else RED
                anim_surf = pygame.Surface((self.W, self.H), pygame.SRCALPHA)
                pygame.draw.circle(anim_surf, (*ring_col, alpha),
                                   chosen_rect.center, radius, 4)
                self.screen.blit(anim_surf, (0, 0))

        hr = pygame.Rect(60, self.H - 262, 130, 38)
        h_ok = p.hints > 0 and game.chosen == -1
        self._button(f"HINT ({p.hints})", hr,
                     (35, 25, 55) if h_ok else DARK_GRAY,
                     (55, 40, 80) if h_ok else DARK_GRAY,
                     PURPLE if h_ok else GRAY, self.f_small, "hint_btn")
        self._t("H key", (hr.x, hr.bottom + 3), self.f_tiny, GRAY)

        sr = pygame.Rect(204, self.H - 262, 130, 38)
        s_ok = p.skips > 0 and game.chosen == -1
        self._button(f"SKIP ({p.skips})", sr,
                     (20, 55, 30) if s_ok else DARK_GRAY,
                     (30, 80, 45) if s_ok else DARK_GRAY,
                     GREEN if s_ok else GRAY, self.f_small, "skip_btn")
        self._t("S key", (sr.x, sr.bottom + 3), self.f_tiny, GRAY)

        # Minimap — right side, below question panel (question box bottom = 312)
        self._draw_minimap(game, mm_y_override=320)

    # ── FEEDBACK ──────────────────────────────────────────────────────────────
    def _feedback(self, game):
        self.screen.fill(BG)
        self._draw_dungeon_bg(game.tick)

        correct = game.fb_correct
        col     = GREEN if correct else RED

        ban = pygame.Rect(60, 55, self.W - 120, 88)
        pygame.draw.rect(self.screen, (10, 40, 10) if correct else (40, 10, 10), ban, border_radius=12)
        pygame.draw.rect(self.screen, col, ban, 3, border_radius=12)
        self._tc(game.fb_message, 92, self.f_large, col)

        q         = game.q_data
        fb_choices = getattr(game, 'q_data_choices', q["c"])
        fb_ans     = game.fb_correct_idx  # already set to q_data_answer by _answer()
        ans_text   = fb_choices[fb_ans] if fb_ans < len(fb_choices) else q['c'][q['a']]
        weak_flag  = "  [WEAK POOL]" if q.get("_weak") else ""
        ca = f"Correct answer:  {chr(65 + fb_ans)}.  {ans_text}{weak_flag}"
        self._tc(ca, 162, self.f_med_b, GREEN if not q.get("_weak") else ORANGE)

        if not game.in_boss_mode:
            p       = game.player
            skipped = (game.chosen == -2)
            if correct and not skipped:
                if p.streak > 1:
                    self._tc(f"STREAK  {p.streak}   \u00d7{1 + p.streak_bonus:.1f} multiplier active!",
                             194, self.f_med_b, ORANGE if p.streak < 5 else GOLD)
                else:
                    self._tc("Keep answering correctly to build your streak!",
                             194, self.f_small, GRAY)
            elif not correct:
                before = game.fb_streak_before
                self._tc(f"Streak broken!  (was {before})" if before else "No streak to lose.",
                         194, self.f_med_b if before else self.f_small,
                         RED if before else GRAY)
                if game.player.iron_will_cooldown > 0 and game.player.hp == 1:
                    self._tc("IRON WILL ACTIVATED  \u2014  you survive with 1 HP!",
                             222, self.f_small, (180, 180, 255))

        er = pygame.Rect(60, 224, self.W - 120, 188)
        pygame.draw.rect(self.screen, PANEL, er, border_radius=10)
        pygame.draw.rect(self.screen, BORDER, er, 2, border_radius=10)

        # Feature 2: deep-dive toggle button
        deep = getattr(game, 'fb_deep_mode', False)
        tgl_r = pygame.Rect(er.right - 138, er.y + 8, 126, 26)
        tgl_lbl = "DEEP DIVE  ▼" if not deep else "BASIC  ▲"
        tgl_fill = (20, 50, 80) if not deep else (50, 20, 80)
        tgl_col  = TEAL if not deep else PURPLE
        self._button(tgl_lbl, tgl_r, tgl_fill, tgl_fill, tgl_col, self.f_tiny, "fb_deep_toggle")

        self._t("Explanation", (er.x + 16, er.y + 10), self.f_med_b, GOLD)
        if deep:
            # Deep dive: show full explanation + the other choices labelled
            self._draw_wrapped(game.fb_explanation,
                               pygame.Rect(er.x + 16, er.y + 42, er.w - 32, er.h // 2 - 20),
                               self.f_small, WHITE)
            fb_choices = getattr(game, 'q_data_choices', game.q_data.get("c", []))
            fb_ans = getattr(game, 'fb_correct_idx', 0)
            y_off = er.y + er.h // 2 + 10
            for ci, ct in enumerate(fb_choices[:4]):
                clr = GREEN if ci == fb_ans else RED_DIM
                lbl = f"{'✓' if ci == fb_ans else '✗'}  {chr(65+ci)}.  {ct[:60]}"
                ls = self.f_tiny.render(lbl, True, clr)
                self.screen.blit(ls, (er.x + 16, y_off + ci * 18))
        else:
            # Basic: just show the explanation
            self._draw_wrapped(game.fb_explanation,
                               pygame.Rect(er.x + 16, er.y + 42, er.w - 32, er.h - 52),
                               self.f_small, WHITE)

        if game.in_boss_mode:
            bq     = game.dungeon.boss_q_idx
            bsc    = game.dungeon.boss_correct
            needed = game.boss_needed_now
            total  = game.boss_q_total
            self._tc(f"Boss: {bq}/{total} answered   Correct: {bsc}   Need {needed}/{total} to win",
                     430, self.f_med, GOLD)
        else:
            self._draw_hud(game.player, game.difficulty)

        is_retry = not correct and not game.in_boss_mode
        cr = pygame.Rect(self.W // 2 - 200, self.H - 90, 400, 56)
        if is_retry:
            self._button("TRY AGAIN  (new question)  \u25ba", cr,
                         (50, 20, 20), (75, 30, 30), RED, self.f_large, "continue_btn")
            self._tc("Same room \u2014 different question", self.H - 22, self.f_small, GRAY)
        else:
            lbl = "NEXT STAGE  \u25ba" if (correct and not game.in_boss_mode) else "CONTINUE  \u25ba"
            self._button(lbl, cr, (20, 50, 20), (30, 80, 30), GREEN, self.f_large, "continue_btn")
            self._tc("Press  SPACE  or  ENTER", self.H - 22, self.f_small, DARK_GRAY)

    # ── BOSS GATE (lock/key cinematic) ─────────────────────────────────────────
    def _boss_gate(self, game):
        """Animated lock-and-gate cinematic before boss fight (210 ticks)."""
        import math as _mg
        t  = game.boss_gate_elapsed
        cx = self.W // 2
        cy = self.H // 2

        self.screen.fill((6, 2, 14))
        self._draw_dungeon_bg(game.tick, rough=True, tint=(180, 20, 20), strength=4)

        def clamp01(v): return max(0.0, min(1.0, v))
        def phase(s, e): return clamp01((t - s) / max(1, e - s))

        # Shared lock geometry (used by multiple phases)
        lw, lh = 130, 110
        lx     = cx - lw // 2
        ly     = cy - lh // 2 + 20   # top of lock body

        # Shackle geometry: arc connection points sit exactly at the top of the body (ly)
        #   Arc bounding rect = 70 wide × 90 tall, so half-height = 45
        #   Connection points: (cx-35, ly) and (cx+35, ly)
        shk_w    = 70
        sx       = cx - shk_w // 2   # cx - 35
        sy_arc   = ly - 45            # arc rect top; center-y = ly

        # Phase fractions
        lock_frac    = phase(25,  75)
        shackle_open = phase(108, 148)   # left leg rises → upside-down J
        unlock_frac  = phase(140, 168)   # body halves fly apart
        gate_frac    = phase(162, 190)
        reveal_frac  = phase(185, 210)

        # ── PADLOCK BODY + KEYHOLE (t 25..75) ────────────────────────────────
        if lock_frac > 0:
            lc = (int(180 * lock_frac), int(140 * lock_frac), int(40 * lock_frac))
            lb = (int(255 * lock_frac), int(200 * lock_frac), int(60 * lock_frac))
            body_r = pygame.Rect(lx, ly, lw, lh)
            pygame.draw.rect(self.screen, lc, body_r, border_radius=18)
            pygame.draw.rect(self.screen, lb, body_r, 3, border_radius=18)
            # Keyhole
            pygame.draw.circle(self.screen, (10, 4, 30), (cx, ly + 48), 15)
            pygame.draw.rect(self.screen,   (10, 4, 30),
                             pygame.Rect(cx - 7, ly + 48, 14, 24))
            pygame.draw.circle(self.screen, lb, (cx, ly + 48), 15, 2)

        # ── SHACKLE: ∩ until shackle_open > 0, then rises into upside-down J ─
        if lock_frac > 0:
            lb2 = (int(255 * lock_frac), int(200 * lock_frac), int(60 * lock_frac))

            # Right leg — always stays in the lock body throughout the animation
            pygame.draw.line(self.screen, lb2,
                             (cx + 35, ly), (cx + 35, ly + 35), 6)

            # Arc — always present; it's the curved top of the ∩ / J
            pygame.draw.arc(self.screen, lb2,
                            pygame.Rect(sx, sy_arc, shk_w, 90),
                            0, _mg.pi, 6)

            # Left leg — rises upward during shackle_open, vanishes when fully withdrawn
            #   bottom starts at ly+35 (inside lock), rises to ly-30 (clear above body)
            left_leg_y = int(ly + 35 - shackle_open * 65)
            if left_leg_y > ly:
                # Still partially inside the lock body
                pygame.draw.line(self.screen, lb2,
                                 (cx - 35, ly), (cx - 35, left_leg_y), 6)
            # When left_leg_y <= ly: left leg is fully withdrawn → shape is now ⌐ (J)

        # ── KEY slides into keyhole (t 75..112) ──────────────────────────────
        key_frac = phase(75, 112)
        if key_frac > 0 and t < 120:
            hole_y = ly + 48
            key_y  = int((cy + 200) + (hole_y - (cy + 200)) * key_frac)
            kc     = (255, int(200 * key_frac), int(40 * key_frac))
            pygame.draw.circle(self.screen, kc, (cx, key_y - 22), 12)
            pygame.draw.circle(self.screen, (40, 30, 0), (cx, key_y - 22), 7)
            pygame.draw.line(self.screen, kc, (cx, key_y - 10), (cx, key_y + 18), 5)
            pygame.draw.line(self.screen, kc,
                             (cx + 2, key_y),      (cx + 10, key_y),      4)
            pygame.draw.line(self.screen, kc,
                             (cx + 2, key_y + 10), (cx + 10, key_y + 10), 4)

        # ── LOCK BODY halves fly apart (t 140..168) ───────────────────────────
        if unlock_frac > 0:
            off = int(unlock_frac * 80)
            shk = int(4 * (1 - unlock_frac) * (1 if (t // 4) % 2 == 0 else -1))
            if t >= 155:
                shk = 0
            lhalf = pygame.Rect(lx - off + shk, ly, lw // 2, lh)
            rhalf = pygame.Rect(cx + off + shk, ly, lw // 2, lh)
            for hr in (lhalf, rhalf):
                pygame.draw.rect(self.screen, (180, 140, 40), hr, border_radius=12)
                pygame.draw.rect(self.screen, (255, 200, 60), hr, 3, border_radius=12)
            if 140 <= t <= 158:
                fa = max(0, int(255 * (1 - (t - 140) / 18)))
                fs = self.f_large.render("CLICK!", True, (255, 240, 100))
                fs.set_alpha(fa)
                self.screen.blit(fs, fs.get_rect(center=(cx, cy - 60)))

        # ── GATES slide open (t 162..190) ────────────────────────────────────
        if gate_frac > 0:
            travel = int(gate_frac * (self.W // 2 + 40))
            bc = (60, 55, 50)
            bb = (110, 100, 85)
            lgr = pygame.Rect(-travel, 0, self.W // 2 + 20, self.H)
            rgr = pygame.Rect(self.W // 2 - 20 + travel, 0, self.W // 2 + 20, self.H)
            for gr in (lgr, rgr):
                pygame.draw.rect(self.screen, bc, gr)
                pygame.draw.rect(self.screen, bb, gr, 4)
                for by in range(0, self.H, 60):
                    pygame.draw.line(self.screen, bb,
                                     (gr.x + 6, by), (gr.right - 6, by), 3)

        # ── BOSS REVEAL (t 185..210) ─────────────────────────────────────────
        if reveal_frac > 0:
            d        = game.dungeon
            is_final = d.floor >= d.max_floors
            rv_a     = int(255 * reveal_frac)
            bs = self.f_huge.render("FINAL BOSS" if is_final else "BOSS",
                                    True, (220, 40, 40))
            bs.set_alpha(rv_a)
            self.screen.blit(bs, bs.get_rect(center=(cx, cy - 30)))
            pr = 80 + int(15 * abs(_mg.sin(game.tick * 0.12)))
            gv = pygame.Surface((pr * 2, pr * 2), pygame.SRCALPHA)
            pygame.draw.circle(gv, (180, 20, 20, int(60 * reveal_frac)), (pr, pr), pr)
            self.screen.blit(gv, (cx - pr, cy - pr - 30))
            tn = TOPICS.get(d.current_topic, d.current_topic)
            ts = self.f_med.render(tn, True, GOLD_COIN)
            ts.set_alpha(rv_a)
            self.screen.blit(ts, ts.get_rect(center=(cx, cy + 30)))
            sk = self.f_tiny.render("Press  ENTER  to  skip", True, DARK_GRAY)
            sk.set_alpha(rv_a)
            self.screen.blit(sk, sk.get_rect(center=(cx, self.H - 18)))
        else:
            sk = self.f_tiny.render("Press  ENTER  to  skip", True, (38, 34, 28))
            self.screen.blit(sk, sk.get_rect(center=(cx, self.H - 18)))

    # ── BOSS INTRO ─────────────────────────────────────────────────────────────
    def _boss_intro(self, game):
        self.screen.fill(BOSS_BG)
        is_final = game.dungeon.floor >= game.dungeon.max_floors

        topic   = game.dungeon.current_topic
        flavor  = BOSS_FLAVOR.get(topic, "A powerful guardian blocks your path!")
        tint    = (220, 60, 60) if is_final else BOSS_BORDER
        self._draw_dungeon_bg(game.tick, rough=True, tint=tint, strength=6)

        p  = game.player
        d  = game.dungeon
        cx = self.W // 2

        elapsed  = min(game.boss_intro_elapsed, 60)
        scale_f  = elapsed / 60.0
        pulse    = int(10 * abs(math.sin(game.tick * 0.05)))
        base_r   = int(120 * scale_f)
        cy_boss  = self.H // 2 - 55

        for i in range(3):
            r_size = base_r + i * 18 + pulse
            if r_size > 0:
                pygame.draw.circle(self.screen, RED_DIM, (cx, cy_boss), r_size, 3)

        boss_alpha = min(255, int(255 * scale_f))
        skull_txt  = "FINAL BOSS" if is_final else "BOSS"
        boss_col   = (220, 50, 50) if is_final else RED
        skull      = self.f_huge.render(skull_txt, True, boss_col)
        skull.set_alpha(boss_alpha)
        self.screen.blit(skull, skull.get_rect(center=(cx, cy_boss)))

        if elapsed > 30:
            self._tc("BOSS  ENCOUNTER", self.H // 2 + 52,  self.f_title, tint)
            self._tc(flavor,             self.H // 2 + 108, self.f_med_b, GOLD)
            self._tc(f"FLOOR  {d.floor}  /  {d.max_floors}", self.H // 2 + 148, self.f_med, GRAY)

            total  = game.boss_q_total
            needed = game.boss_needed_now
            req_str = (f"Answer ALL {total} correctly to defeat the final boss!"
                       if is_final
                       else f"Answer {needed} of {total} correctly to defeat the boss.")
            self._tc(req_str, self.H // 2 + 180, self.f_small, GRAY)
            self._tc(f"HP: {p.hp}  \u00b7  Gold: {p.gold}  \u00b7  Streak: {p.streak}",
                     self.H // 2 + 206, self.f_small, GRAY)

            br = pygame.Rect(cx - 190, self.H - 90, 380, 56)
            btn_lbl = "FACE  THE  FINAL  BOSS" if is_final else "FACE  THE  BOSS"
            self._button(btn_lbl, br, (50, 5, 5), (80, 10, 10) if not is_final else (120, 10, 10),
                         tint, self.f_large, "face_boss")
            self._tc("Press  ENTER  to  begin", self.H - 22, self.f_small, DARK_GRAY)

    # ── BOSS RESULT ────────────────────────────────────────────────────────────
    def _boss_result(self, game):
        won = game.boss_victory
        self.screen.fill((5, 18, 5) if won else BOSS_BG)
        self._draw_dungeon_bg(game.tick, tint=GREEN if won else BOSS_BORDER)

        d     = game.dungeon
        bc    = GREEN if won else RED
        is_mb = game.mini_boss_completed

        title_txt = ("ELITE  GUARDIAN  SLAIN!" if is_mb
                     else ("BOSS  DEFEATED!" if won else "DEFEATED  BY  BOSS"))
        self._tc(title_txt, self.H // 2 - 145, self.f_huge, bc)

        total  = game.boss_q_total
        needed = game.boss_needed_now
        self._tc(f"{d.boss_correct} / {total}  questions correct",
                 self.H // 2 - 50, self.f_large, WHITE)

        if won:
            perfect    = (d.boss_correct >= total)
            pts_bonus  = int((1500 if perfect else 750) * game.player.point_mult)
            gold_bonus = 500 if perfect else 250
            self._tc(f"+{pts_bonus} pts  \u00b7  +{gold_bonus} gold  \u00b7  +25 HP bonus!",
                     self.H // 2 + 10, self.f_med_b, GOLD)
            if perfect:
                self._tc("PERFECT!  Full bonus + 20% shop discount next visit!",
                         self.H // 2 + 48, self.f_med_b, GOLD)
            next_fl = d.floor + 1
            if next_fl > d.max_floors:
                self._tc("That was the final floor!  Head to the shop...",
                          self.H // 2 + 90, self.f_small, GOLD)
            else:
                self._tc(f"A merchant awaits before floor {next_fl}...",
                          self.H // 2 + 90, self.f_small, TEAL)
        else:
            self._tc("\u221230 HP penalty", self.H // 2 + 10, self.f_med_b, RED)

        if won:
            self._draw_hud(game.player, game.difficulty)
            btn_w  = 280
            gap    = 20
            left_x = self.W // 2 - (btn_w * 2 + gap) // 2
            rb = pygame.Rect(left_x, self.H - 100, btn_w, 56)
            self._button("RETURN  TO  FLOOR", rb,
                         (30, 20, 5), (60, 40, 10), ORANGE, self.f_med_b, "return_to_floor")
            db = pygame.Rect(left_x + btn_w + gap, self.H - 100, btn_w, 56)
            self._button("DESCEND  DEEPER  \u25ba", db,
                         (10, 50, 10), (20, 80, 20), GREEN, self.f_med_b, "descend_now")
            self._tc("Return to clear more rooms, or descend now",
                     self.H - 30, self.f_small, DARK_GRAY)
        else:
            self._draw_hud(game.player, game.difficulty)
            rb = pygame.Rect(self.W // 2 - 180, self.H - 90, 360, 56)
            self._button("RETREAT  TO  FLOOR  MAP", rb,
                         (60, 10, 10), (90, 15, 15), RED, self.f_large, "retreat_btn")
            self._tc("Press  ENTER  to  return  to  map", self.H - 22, self.f_small, DARK_GRAY)

    # ── SPECIAL ROOM (Campfire / Treasure) ────────────────────────────────────
    def _special_room(self, game):
        stype = game.special_room_type

        if stype == "campfire":
            self._draw_campfire_room(game)
        else:
            self._draw_treasure_room(game)

    def _draw_campfire_room(self, game):
        """Campfire room — procedural dungeon art, warm and cozy."""
        self.screen.fill((12, 8, 6))

        # Stone wall background
        for gx in range(0, self.W, 60):
            for gy in range(0, self.H, 40):
                shade = 20 + ((gx // 60 + gy // 40) % 2) * 8
                pygame.draw.rect(self.screen, (shade, shade - 2, shade - 5),
                                 pygame.Rect(gx + 1, gy + 1, 57, 37))
        # Mortar lines
        for gx in range(0, self.W, 60):
            pygame.draw.line(self.screen, (10, 8, 12), (gx, 0), (gx, self.H), 2)
        for gy in range(0, self.H, 40):
            pygame.draw.line(self.screen, (10, 8, 12), (0, gy), (self.W, gy), 2)

        cx = self.W // 2
        cy = self.H // 2 + 40

        # Warm glow radiating from fire
        for r in range(220, 0, -20):
            alpha = max(0, 18 - r // 14)
            glow  = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
            pygame.draw.ellipse(glow, (255, 120, 30, alpha), glow.get_rect())
            self.screen.blit(glow, (cx - r, cy - r + 20))

        # Logs
        for lx, ly, lw, lh, ang in [
            (cx - 50, cy + 28, 100, 16, 0),
            (cx - 30, cy + 20, 80,  14, 20),
        ]:
            log_surf = pygame.Surface((lw, lh))
            log_surf.fill((70, 40, 15))
            pygame.draw.rect(log_surf, (50, 28, 8), log_surf.get_rect(), 2)
            self.screen.blit(log_surf, (lx, ly))

        # Rocks around fire base
        for rx, ry, rr in [(cx - 46, cy + 36, 10), (cx + 42, cy + 36, 10),
                           (cx - 58, cy + 30, 8),  (cx + 54, cy + 30, 8),
                           (cx, cy + 42, 9)]:
            pygame.draw.circle(self.screen, (55, 50, 60), (rx, ry), rr)
            pygame.draw.circle(self.screen, STONE, (rx, ry), rr, 1)

        # Animated flame layers
        tick = game.tick
        flame_layers = [
            (0,  0,  18, 50, (255, 220, 80)),
            (0,  6,  14, 40, (255, 150, 40)),
            (-4, 12, 10, 30, (220, 80,  20)),
            (4,  14, 10, 28, (220, 80,  20)),
            (0,  18, 8,  20, (180, 50,  10)),
        ]
        for (ox, oy_off, fw, fh, col) in flame_layers:
            sway = int(5 * math.sin(tick * 0.13 + oy_off * 0.1))
            pygame.draw.ellipse(
                self.screen, col,
                pygame.Rect(cx - fw + ox + sway, cy - fh + oy_off, fw * 2, fh))

        # Spark particles
        for i in range(12):
            angle = (tick * 3 + i * 30) % 360
            dist  = 20 + (i % 4) * 12
            sx    = cx + int(dist * 0.4 * math.cos(math.radians(angle)) +
                             6 * math.sin(tick * 0.1 + i))
            sy    = cy - 30 - int(dist * math.sin(math.radians(angle * 0.5)) +
                                  tick % 60)
            if sy < cy - 80:
                continue
            col_s = (255, 200, 50) if i % 3 == 0 else (255, 120, 30)
            pygame.draw.circle(self.screen, col_s, (sx, sy), 2)

        # Stone floor
        for i in range(-6, 7):
            for j in range(2):
                tx2 = cx + i * 44 + (j % 2) * 22
                ty2 = cy + 48 + j * 36
                pygame.draw.rect(self.screen, (30, 26, 38),
                                 pygame.Rect(tx2 - 20, ty2 - 15, 40, 30), border_radius=3)
                pygame.draw.rect(self.screen, (45, 40, 55),
                                 pygame.Rect(tx2 - 20, ty2 - 15, 40, 30), 1, border_radius=3)

        # Torches on walls
        self._draw_torch(cx - 340, cy - 80, tick)
        self._draw_torch(cx + 330, cy - 80, tick)

        # Info text
        self._tc("CAMPFIRE", 60, self.f_title, WARM_AMBER)
        self._tc("You rest beside the fire and tend your wounds.",
                 118, self.f_med_b, WHITE)
        self._tc(f"Restored  +{game.special_room_heal}  HP", 152, self.f_large, GREEN)

        p = game.player
        self._tc(f"HP: {p.hp} / {p.max_hp}", 192, self.f_med, GRAY)

        br = pygame.Rect(cx - 180, self.H - 90, 360, 56)
        self._button("CONTINUE  \u25ba", br, (40, 20, 5), (70, 40, 10),
                     WARM_AMBER, self.f_large, "special_continue")
        self._tc("Press  ENTER  to  continue", self.H - 22, self.f_small, DARK_GRAY)

    def _draw_treasure_room(self, game):
        """Treasure room — procedural dungeon art, glittering and golden."""
        self.screen.fill((6, 5, 12))

        # Dark stone walls
        for gx in range(0, self.W, 64):
            for gy in range(0, self.H, 44):
                shade = 16 + ((gx // 64 + gy // 44) % 2) * 6
                pygame.draw.rect(self.screen, (shade - 2, shade - 4, shade + 2),
                                 pygame.Rect(gx + 1, gy + 1, 61, 41))
        for gx in range(0, self.W, 64):
            pygame.draw.line(self.screen, (8, 6, 10), (gx, 0), (gx, self.H), 2)
        for gy in range(0, self.H, 44):
            pygame.draw.line(self.screen, (8, 6, 10), (0, gy), (self.W, gy), 2)

        cx   = self.W // 2
        cy   = self.H // 2 + 30
        tick = game.tick

        # Golden glow from chest
        for r in range(200, 0, -20):
            alpha = max(0, 22 - r // 10)
            glow  = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
            pygame.draw.ellipse(glow, (255, 195, 30, alpha), glow.get_rect())
            self.screen.blit(glow, (cx - r, cy - r + 10))

        # Treasure chest
        chest_w, chest_h = 130, 80
        chest_x = cx - chest_w // 2
        chest_y = cy - chest_h // 2

        # Chest body (lower half)
        body_r = pygame.Rect(chest_x, chest_y + 38, chest_w, chest_h - 38)
        pygame.draw.rect(self.screen, (80, 48, 14), body_r, border_radius=4)
        pygame.draw.rect(self.screen, (120, 80, 28), body_r, 2, border_radius=4)

        # Chest lid (upper half) — slightly open
        lid_open = min(20, tick // 3)
        lid_pts = [
            (chest_x, chest_y + 38),
            (chest_x + chest_w, chest_y + 38),
            (chest_x + chest_w, chest_y + 8 - lid_open),
            (chest_x, chest_y + 8 - lid_open),
        ]
        pygame.draw.polygon(self.screen, (100, 60, 18), lid_pts)
        pygame.draw.polygon(self.screen, (150, 100, 36), lid_pts, 2)

        # Metal bands
        for bx2 in range(chest_x + 16, chest_x + chest_w - 16, chest_w - 32):
            pygame.draw.rect(self.screen, (140, 120, 40),
                             pygame.Rect(bx2 - 4, chest_y + 8 - lid_open, 8, chest_h - 8 + lid_open))

        # Lock
        lk = pygame.Rect(cx - 10, chest_y + 30 - lid_open, 20, 18)
        pygame.draw.rect(self.screen, (180, 150, 50), lk, border_radius=4)

        # Coins spilling out
        coin_positions = [
            (cx - 44, cy + 28), (cx - 22, cy + 34), (cx, cy + 38),
            (cx + 22, cy + 34), (cx + 44, cy + 30), (cx - 60, cy + 24),
            (cx + 58, cy + 26), (cx - 16, cy + 44), (cx + 16, cy + 42),
        ]
        for i, (px3, py3) in enumerate(coin_positions):
            bounce = int(4 * math.sin(tick * 0.15 + i * 0.8))
            col_c  = GOLD if i % 2 == 0 else GOLD_COIN
            pygame.draw.ellipse(self.screen, col_c,
                                pygame.Rect(px3 - 9, py3 - 6 + bounce, 18, 12))
            pygame.draw.ellipse(self.screen, (180, 140, 20),
                                pygame.Rect(px3 - 9, py3 - 6 + bounce, 18, 12), 1)

        # Sparkle particles
        for i in range(16):
            angle = (tick * 2 + i * 22.5) % 360
            dist  = 80 + (i % 3) * 30
            spx   = cx + int(dist * math.cos(math.radians(angle)))
            spy   = cy + int(dist * 0.5 * math.sin(math.radians(angle)))
            alpha_sp = int(150 + 100 * math.sin(tick * 0.1 + i))
            sz = 2 if i % 2 else 3
            spark = pygame.Surface((sz * 2, sz * 2), pygame.SRCALPHA)
            pygame.draw.circle(spark, (255, 220, 80, alpha_sp), (sz, sz), sz)
            self.screen.blit(spark, (spx - sz, spy - sz))

        # Stone floor
        for i in range(-6, 7):
            for j in range(2):
                tx2 = cx + i * 44 + (j % 2) * 22
                ty2 = cy + 58 + j * 36
                pygame.draw.rect(self.screen, (28, 24, 36),
                                 pygame.Rect(tx2 - 20, ty2 - 15, 40, 30), border_radius=3)
                pygame.draw.rect(self.screen, (42, 38, 52),
                                 pygame.Rect(tx2 - 20, ty2 - 15, 40, 30), 1, border_radius=3)

        # Chains on walls
        for chain_x in [cx - 360, cx + 340]:
            for chain_y in range(0, 130, 18):
                pygame.draw.circle(self.screen, STONE, (chain_x, chain_y), 5)
                pygame.draw.circle(self.screen, (55, 50, 65), (chain_x, chain_y), 5, 1)

        # Info text
        self._tc("TREASURE  ROOM", 52, self.f_title, GOLD)
        self._tc("Ancient riches lie within the chest.  Claim them!",
                 110, self.f_med_b, WHITE)
        self._tc(f"+{game.special_room_gold:,} Gold", 148, self.f_large, GOLD_COIN)

        p = game.player
        self._tc(f"Total gold: {p.gold:,}", 190, self.f_med, GRAY)

        br = pygame.Rect(cx - 180, self.H - 90, 360, 56)
        self._button("CLAIM  &  CONTINUE  \u25ba", br, (40, 32, 5), (70, 55, 10),
                     GOLD, self.f_large, "special_continue")
        self._tc("Press  ENTER  to  continue", self.H - 22, self.f_small, DARK_GRAY)

    # ── SHOP ──────────────────────────────────────────────────────────────────
    def _shop(self, game):
        self.screen.fill(SHOP_BG)
        self._draw_dungeon_bg(game.tick, tint=TEAL)

        d = game.dungeon
        p = game.player
        self._tc("MERCHANT'S  HALL", 22, self.f_title, TEAL)

        floors_left = d.max_floors - d.floor + 1
        if d.floor > d.max_floors:
            sub = "Final shop \u2014 then the dungeon is cleared!"
        else:
            sub = (f"Floor {d.floor}  \u00b7  {floors_left} floor{'s' if floors_left != 1 else ''} left"
                   + ("  \u00b7  [PERFECT: 20% off!]"
                      if game.perfect_boss_discount else ""))
        self._tc(sub, 74, self.f_small, TEAL if not game.perfect_boss_discount else GOLD)

        gd_surf = self.f_large.render(f"\u25c6 {p.gold:,} gold", True, GOLD_COIN)
        self.screen.blit(gd_surf, (self.W - gd_surf.get_width() - 50, 22))
        sc_surf = self.f_small.render(f"Score: {p.score:,} pts", True, GOLD)
        self.screen.blit(sc_surf, (self.W - sc_surf.get_width() - 50, 60))

        stock  = game.shop_stock
        card_w = (self.W - 80) // 2 - 10
        card_h = 165
        col_x  = [30, 30 + card_w + 20]
        row_y  = [130, 315]

        for idx, item in enumerate(stock):
            if idx >= 4:
                break
            col  = idx % 2
            row  = idx // 2
            cx   = col_x[col]
            cy   = row_y[row]
            key  = item["key"]
            ic   = SHOP_ICON_COLORS.get(key, GRAY)
            lvl  = p.shop_buys.get(key, 0)
            disc = (key == game.perfect_boss_discount)
            price = item_price(key, p.shop_buys, discount=disc)
            can_buy = p.gold >= price

            card = pygame.Rect(cx, cy, card_w, card_h)
            if disc:
                pygame.draw.rect(self.screen, (60, 50, 5), card, border_radius=10)
                pygame.draw.rect(self.screen, GOLD, card, 3, border_radius=10)
            else:
                pygame.draw.rect(self.screen, PANEL, card, border_radius=10)
                pygame.draw.rect(self.screen, ic if can_buy else BORDER, card, 2, border_radius=10)

            icon_r = pygame.Rect(cx + 10, cy + 10, 70, 70)
            pygame.draw.rect(self.screen, (ic[0]//4, ic[1]//4, ic[2]//4), icon_r, border_radius=8)
            pygame.draw.rect(self.screen, ic, icon_r, 2, border_radius=8)
            icon_s = self.f_small.render(item["icon"], True, ic)
            self.screen.blit(icon_s, icon_s.get_rect(center=icon_r.center))

            lvl_s = self.f_tiny.render(f"Lv {lvl}", True, GOLD if lvl else GRAY)
            self.screen.blit(lvl_s, (icon_r.x + (70 - lvl_s.get_width()) // 2, icon_r.bottom + 4))

            self._t(item["name"], (cx + 90, cy + 12), self.f_med_b, WHITE if can_buy else GRAY)
            self._draw_wrapped(item["desc"],
                               pygame.Rect(cx + 90, cy + 38, card_w - 170, 70),
                               self.f_tiny, GRAY)

            stat = self._shop_stat_line(key, p)
            if stat:
                self._t(stat, (cx + 90, cy + 112), self.f_tiny, ic)

            if disc:
                orig_price = item_price(key, p.shop_buys, discount=False)
                orig_s = self.f_tiny.render(f"{orig_price:,}g", True, GRAY)
                self.screen.blit(orig_s, (cx + card_w - orig_s.get_width() - 90, cy + 10))
                pygame.draw.line(self.screen, RED,
                                 (cx + card_w - orig_s.get_width() - 90, cy + 17),
                                 (cx + card_w - 90, cy + 17), 2)
                sale_s = self.f_tiny.render("SALE", True, GOLD)
                self.screen.blit(sale_s, (cx + card_w - sale_s.get_width() - 90, cy + 24))

            pc  = GOLD_COIN if can_buy else RED
            ps  = self.f_med_b.render(f"{price:,}g", True, pc)
            self.screen.blit(ps, (cx + card_w - ps.get_width() - 90, cy + 40 if disc else cy + 12))

            buy_r = pygame.Rect(cx + card_w - 80, cy + card_h // 2 - 20, 72, 40)
            if can_buy:
                self._button("BUY", buy_r,
                             (ic[0]//5, ic[1]//5, ic[2]//5),
                             (ic[0]//3, ic[1]//3, ic[2]//3),
                             ic, self.f_med_b, f"buy_{key}")
            else:
                pygame.draw.rect(self.screen, DARK_GRAY, buy_r, border_radius=8)
                pygame.draw.rect(self.screen, BORDER,    buy_r, 2, border_radius=8)
                ns = self.f_small.render("BUY", True, GRAY)
                self.screen.blit(ns, ns.get_rect(center=buy_r.center))


        # ── Two locked slots: Gold-to-HP (left) and Shop Re-roll (right) ──
        slot_w  = (self.W - 100) // 2
        slot_h  = 66
        slot_y  = self.H - 162
        left_x  = 40
        right_x = left_x + slot_w + 20

        # LEFT: Gold-to-HP
        ghp_r   = pygame.Rect(left_x, slot_y, slot_w, slot_h)
        ghp_can = p.gold >= 50 and p.hp < p.max_hp
        ghp_col = (200, 60, 60)
        pygame.draw.rect(self.screen, (30, 10, 10),  ghp_r, border_radius=10)
        pygame.draw.rect(self.screen, ghp_col if ghp_can else BORDER, ghp_r, 2, border_radius=10)
        ghp_ic = pygame.Rect(ghp_r.x + 8, ghp_r.y + 8, 50, 50)
        pygame.draw.rect(self.screen, (60, 10, 10), ghp_ic, border_radius=6)
        pygame.draw.rect(self.screen, ghp_col,      ghp_ic, 2, border_radius=6)
        _s = self.f_small.render("+HP", True, ghp_col)
        self.screen.blit(_s, _s.get_rect(center=ghp_ic.center))
        _s = self.f_med_b.render("Gold-to-HP  (50g = +10 HP)", True, WHITE if ghp_can else GRAY)
        self.screen.blit(_s, (ghp_r.x + 66, ghp_r.y + 8))
        _s = self.f_tiny.render(f"HP: {p.hp}/{p.max_hp}", True, ghp_col)
        self.screen.blit(_s, (ghp_r.x + 66, ghp_r.y + 34))
        buy_ghp_r = pygame.Rect(ghp_r.right - 78, ghp_r.y + 13, 70, 38)
        if ghp_can:
            self._button("50g", buy_ghp_r, (50, 10, 10), (80, 20, 20),
                         ghp_col, self.f_med_b, "buy_gold_hp")
        else:
            pygame.draw.rect(self.screen, DARK_GRAY, buy_ghp_r, border_radius=8)
            pygame.draw.rect(self.screen, BORDER,    buy_ghp_r, 2, border_radius=8)
            _s = self.f_small.render("50g", True, GRAY)
            self.screen.blit(_s, _s.get_rect(center=buy_ghp_r.center))

        # RIGHT: Shop Re-roll
        rr_count = getattr(game, "shop_reroll_count", 0)
        rr_cost  = 80 + rr_count * 65
        rr_r     = pygame.Rect(right_x, slot_y, slot_w, slot_h)
        rr_can   = p.gold >= rr_cost
        rr_col   = (40, 170, 200)
        pygame.draw.rect(self.screen, (8, 30, 40),  rr_r, border_radius=10)
        pygame.draw.rect(self.screen, rr_col if rr_can else BORDER, rr_r, 2, border_radius=10)
        rr_ic = pygame.Rect(rr_r.x + 8, rr_r.y + 8, 50, 50)
        pygame.draw.rect(self.screen, (8, 50, 60), rr_ic, border_radius=6)
        pygame.draw.rect(self.screen, rr_col,      rr_ic, 2, border_radius=6)
        _s = self.f_small.render("RR", True, rr_col)
        self.screen.blit(_s, _s.get_rect(center=rr_ic.center))
        _s = self.f_med_b.render("Shop Re-roll", True, WHITE if rr_can else GRAY)
        self.screen.blit(_s, (rr_r.x + 66, rr_r.y + 8))
        _next = rr_cost + 65
        rr_sub = (f"Roll #{rr_count + 1}  —  next will cost {_next}g"
                  if rr_count > 0 else "Randomise all 4 shop items")
        _s = self.f_tiny.render(rr_sub, True, rr_col if rr_can else GRAY)
        self.screen.blit(_s, (rr_r.x + 66, rr_r.y + 34))
        buy_rr_r = pygame.Rect(rr_r.right - 78, rr_r.y + 13, 70, 38)
        rr_lbl   = f"{rr_cost}g"
        if rr_can:
            self._button(rr_lbl, buy_rr_r, (8, 50, 70), (12, 80, 110),
                         rr_col, self.f_med_b, "buy_reroll")
        else:
            pygame.draw.rect(self.screen, DARK_GRAY, buy_rr_r, border_radius=8)
            pygame.draw.rect(self.screen, BORDER,    buy_rr_r, 2, border_radius=8)
            _s = self.f_small.render(rr_lbl, True, GRAY)
            self.screen.blit(_s, _s.get_rect(center=buy_rr_r.center))

        # Feature 7: Did You Know fact card
        fact = getattr(game, 'shop_fun_fact', '')
        if fact:
            fr = pygame.Rect(40, self.H - 162, self.W - 80, 44)
            pygame.draw.rect(self.screen, (8, 24, 8), fr, border_radius=8)
            pygame.draw.rect(self.screen, (30, 100, 30), fr, 2, border_radius=8)
            lbl_f = self.f_tiny.render("DID YOU KNOW?", True, (80, 200, 80))
            self.screen.blit(lbl_f, (fr.x + 10, fr.y + 6))
            self._draw_wrapped(fact, pygame.Rect(fr.x + 10, fr.y + 22, fr.w - 20, 20),
                               self.f_tiny, (160, 220, 160))

        lbl_leave = ("COMPLETE  THE  DUNGEON  ►"
                     if d.floor > d.max_floors else "NEXT  FLOOR  ►")
        lr = pygame.Rect(self.W // 2 - 200, self.H - 72, 400, 52)
        self._button(lbl_leave, lr, (20, 55, 55), (30, 80, 80), TEAL, self.f_large, "leave_shop")
        self._tc("Press  ENTER / SPACE  to  continue", self.H - 14, self.f_tiny, GRAY)

    @staticmethod
    def _shop_stat_line(key: str, p) -> str:
        if key == "hp_up":        return f"Max HP: {p.max_hp}  (+20 per purchase)"
        if key == "time_up":      return f"Timer: {int(p.question_time)}s  (+10s per buy)"
        if key == "point_boost":  return f"Mult: \u00d7{p.point_mult:.2f}  (+0.25 per buy)"
        if key == "streak_heal":  return f"Heal: +{p.streak_heal * 3} HP/correct @3+ streak"
        if key == "hint":         return f"Hints: {p.hints}"
        if key == "skip":         return f"Skips: {p.skips}"
        if key == "iron_will":    return (f"Charges: {p.iron_will_charges}"
                                          + (f"  [cd:{p.iron_will_cooldown}F]"
                                             if p.iron_will_cooldown > 0 else ""))
        if key == "scholar_mark":  return f"Stacks:{p.scholar_mark_stacks}  Used:{p.scholar_mark_reductions}/3"
        if key == "scholar_tome":  return f"Charges: {p.scholar_tome_charges}"
        if key == "dungeon_sense": return f"Charges: {p.dungeon_sense_charges}"
        return ""

    # ── GAME OVER ──────────────────────────────────────────────────────────────
    def _game_over(self, game):
        self.screen.fill((8, 0, 0))
        self._draw_dungeon_bg(game.tick, tint=RED)

        self._tc("GAME  OVER", self.H // 2 - 180, self.f_huge, RED)
        self._tc("Your HP reached zero. The dungeon claims another soul.",
                 self.H // 2 - 80, self.f_med, GRAY)
        self._tc(f"FINAL SCORE:  {game.final_score:,}", self.H // 2 - 30, self.f_title, GOLD)

        if game.player and game.dungeon:
            mf = game.dungeon.max_floors
            diff_lbl = DIFFICULTIES[game.difficulty]["label"]
            self._tc(f"Difficulty: {diff_lbl}   Floors cleared: {game.floors_done}/{mf}"
                     f"   Best streak: {game.player.best_streak}",
                     self.H // 2 + 40, self.f_med, GRAY)
            self._draw_run_stats(game, self.H // 2 + 90)

        br = pygame.Rect(self.W // 2 - 160, self.H - 90, 320, 56)
        self._button("TRY  AGAIN", br, (50, 10, 10), (80, 20, 20), RED, self.f_large, "try_again")
        self._tc("Press  ENTER  to  return  to  title", self.H - 22, self.f_small, DARK_GRAY)

    # ── VICTORY ────────────────────────────────────────────────────────────────
    def _victory(self, game):
        self.screen.fill((5, 18, 5))
        self._draw_dungeon_bg(game.tick, tint=GOLD)

        for i in range(16):
            angle = game.tick * 0.03 + i * (math.pi * 2 / 16)
            sx    = int(self.W // 2 + 300 * math.cos(angle))
            sy    = int(self.H // 2 - 80 + 100 * math.sin(angle * 2))
            pygame.draw.circle(self.screen, GOLD, (sx, sy), 5)

        mf = game.dungeon.max_floors if game.dungeon else 15
        self._tc("DUNGEON  CLEARED!", self.H // 2 - 210, self.f_huge, GOLD)
        self._tc(f"All {mf} floors conquered!  Theory of Computation mastered!",
                 self.H // 2 - 120, self.f_med, WHITE)
        self._tc(f"FINAL SCORE:  {game.final_score:,}", self.H // 2 - 72, self.f_title, GOLD)

        p = game.player
        if p:
            diff_lbl = DIFFICULTIES[game.difficulty]["label"]
            self._tc(f"Difficulty: {diff_lbl}   HP remaining: {game.final_hp}"
                     f"   Best streak: {p.best_streak}",
                     self.H // 2 - 18, self.f_med, GRAY)

        self._draw_run_stats(game, self.H // 2 + 30)

        br = pygame.Rect(self.W // 2 - 160, self.H - 90, 320, 56)
        self._button("PLAY  AGAIN", br, (20, 60, 20), (30, 90, 30), GREEN, self.f_large, "play_again")
        self._tc("Press  ENTER  to  return  to  title", self.H - 22, self.f_small, DARK_GRAY)

    def _draw_run_stats(self, game, top_y: int):
        total_ans = game.run_total_correct + game.run_total_wrong
        accuracy  = (100 * game.run_total_correct // max(1, total_ans))
        stats = [
            f"Correct: {game.run_total_correct}   Wrong: {game.run_total_wrong}"
            f"   Accuracy: {accuracy}%",
            f"Fast answers: {game.run_total_fast}   Perfect boss fights: {game.run_boss_perfects}",
            (f"Gold earned: {game.player.gold if game.player else 0}"
             f"   Score mult: \u00d7{game.player.point_mult:.2f}" if game.player else ""),
        ]
        for i, line in enumerate(stats):
            if line:
                self._tc(line, top_y + i * 26, self.f_small, GRAY)

    # ══════════════════════════════ SHARED UTILITIES ══════════════════════════

    def _draw_dungeon_bg(self, tick, rough=False, tint=None, strength=14):
        tile = 60
        for gx in range(0, self.W + tile, tile):
            for gy in range(0, self.H + tile, tile):
                base = 12 + ((gx // tile + gy // tile) % 2) * 5
                r = min(255, base + (tint[0] // strength if tint else 0))
                g = min(255, base + (tint[1] // strength if tint else 0))
                b = min(255, base + (tint[2] // strength if tint else 0))
                pygame.draw.rect(self.screen, (r, g, b),
                                 pygame.Rect(gx, gy, tile - 2, tile - 2))

    def _draw_hud(self, player, difficulty="medium", dungeon=None):
        dc_col = DIFF_COLORS.get(difficulty, GOLD)

        hb = pygame.Rect(60, 10, 240, 24)
        pygame.draw.rect(self.screen, DARK_GRAY, hb, border_radius=6)
        pct = max(0, player.hp / player.max_hp)
        if pct > 0:
            hp_col = GREEN if pct > 0.5 else (ORANGE if pct > 0.25 else RED)
            fill_r = pygame.Rect(60, 10, max(4, int(240 * pct)), 24)
            pygame.draw.rect(self.screen, hp_col, fill_r, border_radius=6)
        pygame.draw.rect(self.screen, BORDER, hb, 2, border_radius=6)
        hp_s = self.f_small.render(f"HP  {player.hp} / {player.max_hp}", True, WHITE)
        self.screen.blit(hp_s, hp_s.get_rect(center=hb.center))

        sc_s = self.f_med_b.render(f"{player.score:,} pts", True, GOLD)
        gd_s = self.f_small.render(f"\u25c6 {player.gold:,} g", True, GOLD_COIN)
        self.screen.blit(sc_s, (self.W - sc_s.get_width() - 14, 8))
        self.screen.blit(gd_s, (self.W - gd_s.get_width() - 14, 32))

        eff_mult = player.effective_mult
        mult_col = GOLD if eff_mult > 1.5 else (ORANGE if eff_mult > 1.0 else GRAY)
        mult_s   = self.f_tiny.render(f"\u00d7{eff_mult:.2f} mult", True, mult_col)
        self.screen.blit(mult_s, (self.W - mult_s.get_width() - 14, 52))

        hs = self.f_tiny.render(f"Hints:{player.hints}  Skips:{player.skips}", True, GRAY)
        self.screen.blit(hs, (self.W - hs.get_width() - 14, 68))

        if dungeon is not None:
            has_k  = getattr(dungeon, "has_key", False)
            ks_r   = pygame.Rect(308, 10, 86, 24)
            ks_bg  = (80, 60, 10) if has_k else (30, 28, 20)
            ks_brd = GOLD         if has_k else (80, 72, 40)
            pygame.draw.rect(self.screen, ks_bg,  ks_r, border_radius=6)
            pygame.draw.rect(self.screen, ks_brd, ks_r, 2, border_radius=6)
            ks_txt = "KEY FOUND" if has_k else "KEY: ???"
            ks_col = (255, 230, 60) if has_k else (90, 82, 50)
            ks_s   = self.f_tiny.render(ks_txt, True, ks_col)
            self.screen.blit(ks_s, ks_s.get_rect(center=ks_r.center))

        if player.iron_will_charges > 0:
            iw_col = (180, 180, 255) if player.iron_will_cooldown == 0 else GRAY
            iw_s   = self.f_tiny.render(
                f"IRON WILL x{player.iron_will_charges}"
                + (f" [cd:{player.iron_will_cooldown}]" if player.iron_will_cooldown > 0 else " [READY]"),
                True, iw_col)
            self.screen.blit(iw_s, (self.W - iw_s.get_width() - 14, 84))

        streak = player.streak
        if streak >= 5:   sc2, sf = GOLD,   self.f_med_b
        elif streak >= 3: sc2, sf = ORANGE, self.f_med
        else:             sc2, sf = GRAY,   self.f_small
        label = (f"STREAK  {streak}  \u00d7{1 + player.streak_bonus:.1f}"
                 if streak > 0 else "STREAK  0")
        ss = sf.render(label, True, sc2)
        cx = self.W // 2
        self.screen.blit(ss, ss.get_rect(centerx=cx, y=8))

        seg_total = 10
        seg_w, seg_gap = 16, 3
        bar_w = seg_total * (seg_w + seg_gap) - seg_gap
        bar_x = cx - bar_w // 2
        bar_y = 32
        for s in range(seg_total):
            filled = s < min(streak, seg_total)
            col    = (GOLD if s >= 9 else (ORANGE if s >= 4 else GREEN)) if filled else DARK_GRAY
            pygame.draw.rect(self.screen, col,
                             pygame.Rect(bar_x + s * (seg_w + seg_gap), bar_y, seg_w, 8),
                             border_radius=3)

        self._draw_diff_badge(dc_col, DIFFICULTIES[difficulty]["label"], (self.W - 14, 100))

    def _draw_diff_badge(self, col, label: str, top_right: tuple):
        surf = self.f_tiny.render(label, True, col)
        bx   = top_right[0] - surf.get_width() - 10
        by   = top_right[1]
        br   = pygame.Rect(bx - 4, by, surf.get_width() + 8, surf.get_height() + 4)
        pygame.draw.rect(self.screen, (col[0]//6, col[1]//6, col[2]//6), br, border_radius=4)
        pygame.draw.rect(self.screen, col, br, 1, border_radius=4)
        self.screen.blit(surf, (bx, by + 2))

    def _timer_bar(self, time_left: float, max_time: float, rect: pygame.Rect):
        pct = max(0.0, time_left / max(1, max_time))
        pygame.draw.rect(self.screen, DARK_GRAY, rect, border_radius=5)
        if pct > 0:
            fill = rect.copy(); fill.width = max(4, int(rect.width * pct))
            col  = GREEN if pct > 0.55 else (ORANGE if pct > 0.25 else RED)
            pygame.draw.rect(self.screen, col, fill, border_radius=5)
        pygame.draw.rect(self.screen, BORDER, rect, 1, border_radius=5)

    def _progress_bar(self, done: int, total: int, rect: pygame.Rect, col):
        pct = done / max(1, total)
        pygame.draw.rect(self.screen, DARK_GRAY, rect, border_radius=4)
        if pct > 0:
            fill = rect.copy(); fill.width = max(4, int(rect.width * pct))
            pygame.draw.rect(self.screen, col, fill, border_radius=4)
        pygame.draw.rect(self.screen, BORDER, rect, 1, border_radius=4)

    def _draw_streak_flash(self, game):
        alpha  = min(255, int(255 * (game.streak_flash_timer / 150)))
        ov     = pygame.Surface((self.W, 54), pygame.SRCALPHA)
        bg_a   = min(180, alpha)
        ov.fill((255, 165, 0, bg_a))
        self.screen.blit(ov, (0, self.H // 2 - 27))
        flash_s = self.f_large.render(game.streak_flash_text, True, WHITE)
        flash_s.set_alpha(alpha)
        self.screen.blit(flash_s, flash_s.get_rect(center=(self.W // 2, self.H // 2)))

    def _button(self, text: str, rect: pygame.Rect,
                col_n, col_h, text_col, font, name: str):
        hov  = rect.collidepoint(pygame.mouse.get_pos())
        fill = col_h if hov else col_n
        pygame.draw.rect(self.screen, fill, rect, border_radius=10)
        pygame.draw.rect(self.screen, text_col if hov else BORDER, rect, 2, border_radius=10)
        s = font.render(text, True, text_col)
        self.screen.blit(s, s.get_rect(center=rect.center))
        self._buttons[name] = rect

    def _t(self, text: str, pos: tuple, font, color):
        self.screen.blit(font.render(text, True, color), pos)

    def _tc(self, text: str, y: int, font, color):
        s = font.render(text, True, color)
        self.screen.blit(s, s.get_rect(centerx=self.W // 2, y=y))

    def _tc_surf(self, surf, center):
        self.screen.blit(surf, surf.get_rect(center=center))

    def _draw_wrapped(self, text: str, rect: pygame.Rect, font, color, spacing: int = 4):
        words = text.split()
        lines = []; line = []
        for word in words:
            test = " ".join(line + [word])
            if font.size(test)[0] <= rect.width:
                line.append(word)
            else:
                if line: lines.append(" ".join(line))
                line = [word]
        if line: lines.append(" ".join(line))

        y  = rect.y
        lh = font.get_height() + spacing
        for ln in lines:
            if y + lh > rect.bottom: break
            self.screen.blit(font.render(ln, True, color), (rect.x, y))
            y += lh

    # ══════════════════ NEW SCREENS ══════════════════════════════════════════

    def _campfire_choice(self, game):
        self._draw_campfire_room(game)
        ov = pygame.Surface((self.W, 240), pygame.SRCALPHA)
        ov.fill((4, 2, 0, 200))
        self.screen.blit(ov, (0, self.H - 240))
        self._tc("CHOOSE  YOUR  REST", self.H - 230, self.f_large, WARM_AMBER)
        p  = game.player
        cx = self.W // 2
        bw, bh = 310, 70
        hr = pygame.Rect(cx - bw - 12, self.H - 180, bw, bh)
        self._button(f"[1] HEAL  +{game.special_room_heal} HP", hr,
                     (45, 22, 5), (75, 40, 10), WARM_AMBER, self.f_large, "campfire_heal")
        hp_s = self.f_tiny.render(
            f"HP: {p.hp}  to  {min(p.max_hp, p.hp + game.special_room_heal)}", True, GRAY)
        self.screen.blit(hp_s, hp_s.get_rect(center=(hr.centerx, hr.bottom + 10)))
        tr = pygame.Rect(cx + 12, self.H - 180, bw, bh)
        self._button("[2] FOCUS  +15s  next room", tr,
                     (5, 20, 45), (10, 40, 80), BLUE_ACC, self.f_large, "campfire_time")
        tb_s = self.f_tiny.render("Extra time on the very next question only", True, GRAY)
        self.screen.blit(tb_s, tb_s.get_rect(center=(tr.centerx, tr.bottom + 10)))

    def _vault_gamble(self, game):
        self._draw_treasure_room(game)
        ov = pygame.Surface((self.W, 250), pygame.SRCALPHA)
        ov.fill((4, 4, 0, 210))
        self.screen.blit(ov, (0, self.H - 250))
        self._tc("VAULT  --  CHOOSE  YOUR  REWARD", self.H - 242, self.f_large, GOLD)
        cx = self.W // 2
        bw, bh = 300, 70
        sr = pygame.Rect(cx - bw - 12, self.H - 188, bw, bh)
        self._button(f"[1] TAKE  {game.vault_gamble_base}  GOLD", sr,
                     (40, 30, 5), (70, 52, 10), GOLD_COIN, self.f_large, "vault_take")
        ss = self.f_tiny.render("Guaranteed  -- no risk", True, GRAY)
        self.screen.blit(ss, ss.get_rect(center=(sr.centerx, sr.bottom + 10)))
        gr = pygame.Rect(cx + 12, self.H - 188, bw, bh)
        self._button(f"[2] GAMBLE  FOR  {game.vault_gamble_double}  GOLD", gr,
                     (45, 10, 10), (80, 18, 18), RED, self.f_large, "vault_gamble")
        gs = self.f_tiny.render("Answer a question -- wrong = 0 gold, no HP loss", True, GRAY)
        self.screen.blit(gs, gs.get_rect(center=(gr.centerx, gr.bottom + 10)))
        self._tc("Press  1  or  2  to  choose", self.H - 30, self.f_small, DARK_GRAY)

    def _paused(self, game):
        self.screen.fill(BG)
        self._draw_dungeon_bg(game.tick, strength=4)
        ov = pygame.Surface((self.W, self.H), pygame.SRCALPHA)
        ov.fill((0, 0, 0, 150))
        self.screen.blit(ov, (0, 0))
        box = pygame.Rect(self.W // 2 - 300, self.H // 2 - 230, 600, 460)
        pygame.draw.rect(self.screen, PANEL,  box, border_radius=16)
        pygame.draw.rect(self.screen, BORDER, box, 3, border_radius=16)
        self._tc("PAUSED", box.y + 20, self.f_title, WHITE)
        p = game.player
        d = game.dungeon
        stats = [
            f"Floor  {d.floor} / {d.max_floors}",
            f"HP     {p.hp} / {p.max_hp}",
            f"Gold   {p.gold:,}",
            f"Score  {p.score:,}",
            f"Streak {p.streak}",
        ]
        for idx, line in enumerate(stats):
            self._tc(line, box.y + 74 + idx * 26, self.f_med, GRAY)

        # Per-topic mastery bars
        bar_y = box.y + 74 + len(stats) * 26 + 10
        self._t("TOPIC MASTERY:", (box.x + 20, bar_y), self.f_small, GOLD)
        bar_y += 22
        all_t = sorted(set(list(game.per_topic_correct.keys()) + list(game.per_topic_wrong.keys())))
        bar_w = box.w - 40
        for ti, topic in enumerate(all_t[:5]):  # show up to 5 topics to fit
            c  = game.per_topic_correct.get(topic, 0)
            wt = game.per_topic_wrong.get(topic, 0)
            tot = c + wt
            acc = int(100 * c / max(1, tot))
            tc2 = GREEN if acc >= 70 else (GOLD if acc >= 40 else RED)
            lbl = self.f_tiny.render(f"{topic}  {c}/{tot}", True, TOPIC_COLORS.get(topic, GRAY))
            self.screen.blit(lbl, (box.x + 20, bar_y))
            br = pygame.Rect(box.x + 20, bar_y + 14, bar_w, 6)
            pygame.draw.rect(self.screen, DARK_GRAY, br, border_radius=3)
            fw = int(br.width * c / max(1, tot))
            if fw > 0:
                pygame.draw.rect(self.screen, tc2, pygame.Rect(br.x, br.y, fw, 6), border_radius=3)
            bar_y += 26

        rr = pygame.Rect(self.W // 2 - 200, box.bottom - 150, 180, 46)
        self._button("RESUME", rr, (20, 50, 20), (30, 80, 30), GREEN, self.f_large, "resume_btn")
        gr = pygame.Rect(self.W // 2 + 20, box.bottom - 150, 180, 46)
        self._button("GRIMOIRE [G]", gr, (20, 30, 60), (30, 45, 90), TEAL, self.f_small, "grimoire_btn")
        qr = pygame.Rect(self.W // 2 - 200, box.bottom - 92, 400, 46)
        self._button("QUIT  RUN", qr, (55, 12, 12), (85, 18, 18), RED, self.f_large, "quit_run_btn")
        self._tc("ESC  /  ENTER  to  resume", box.bottom + 8, self.f_tiny, DARK_GRAY)

    def _run_stats(self, game):
        won = game.run_victory
        self.screen.fill((5, 18, 5) if won else BOSS_BG)
        self._draw_dungeon_bg(game.tick, tint=GREEN if won else BOSS_BORDER, strength=5)
        head_col = GREEN if won else RED
        self._tc("VICTORY!" if won else "DEFEATED", 22, self.f_title, head_col)
        cx      = self.W // 2
        total_q = game.run_total_correct + game.run_total_wrong
        acc     = int(100 * game.run_total_correct / max(1, total_q))
        highlights = [
            ("Score",         f"{game.final_score:,} pts"),
            ("Floors",        f"{game.floors_done} / {game.dungeon.max_floors}"),
            ("Accuracy",      f"{acc}%  ({game.run_total_correct}/{total_q})"),
            ("Best Streak",   f"{game.player.best_streak}"),
            ("Fast Answers",  f"{game.run_total_fast}"),
            ("Boss Perfects", f"{game.run_boss_perfects}"),
            ("Gold Left",     f"{game.player.gold:,}"),
        ]
        col_w = (self.W - 120) // 2
        for idx, (lbl, val) in enumerate(highlights):
            row, col = divmod(idx, 2)
            bx = 60 + col * (col_w + 20)
            by = 86 + row * 34
            ls = self.f_med.render(lbl + ":", True, GRAY)
            vs = self.f_med_b.render(val, True, WHITE)
            self.screen.blit(ls, (bx, by))
            self.screen.blit(vs, (bx + 168, by))
        div_y = 86 + ((len(highlights) + 1) // 2) * 34 + 8
        pygame.draw.rect(self.screen, BORDER, pygame.Rect(60, div_y, self.W - 120, 2))
        div_y += 12
        self._t("TOPIC  BREAKDOWN:", (60, div_y), self.f_small, GOLD)
        div_y += 26
        all_topics = sorted(set(list(game.per_topic_correct.keys()) +
                                list(game.per_topic_wrong.keys())))
        col_w2 = (self.W - 120) // 3
        for ti, topic in enumerate(all_topics):
            c  = game.per_topic_correct.get(topic, 0)
            w  = game.per_topic_wrong.get(topic, 0)
            t  = c + w
            a  = int(100 * c / max(1, t))
            ci = ti % 3
            ri = ti // 3
            bx = 60 + ci * (col_w2 + 10)
            by = div_y + ri * 30
            if by + 30 > self.H - 90:
                break
            bar_r = pygame.Rect(bx, by + 16, col_w2 - 12, 8)
            pygame.draw.rect(self.screen, DARK_GRAY, bar_r, border_radius=4)
            fw = int(bar_r.width * c / max(1, t))
            tc = GREEN if a >= 70 else (GOLD if a >= 40 else RED)
            if fw > 0:
                pygame.draw.rect(self.screen, tc,
                                 pygame.Rect(bar_r.x, bar_r.y, fw, bar_r.height),
                                 border_radius=4)
            ls = self.f_tiny.render(
                f"{topic}  {c}/{t}  ({a}%)", True, TOPIC_COLORS.get(topic, GRAY))
            self.screen.blit(ls, (bx, by))
        # Milestone badges in topic breakdown
        for ti, topic in enumerate(all_topics):
            ms = game.milestone_achieved.get(topic, 0)
            if ms > 0:
                ci = ti % 3
                ri = ti // 3
                bx2 = 60 + ci * (col_w2 + 10)
                by2 = div_y + ri * 30
                if by2 + 30 <= self.H - 110:
                    badge_txt = "★" * (1 if ms == 25 else (2 if ms == 50 else 3))
                    bs = self.f_tiny.render(badge_txt, True, GOLD)
                    self.screen.blit(bs, (bx2 + col_w2 - 18, by2))

        # Feature 5: Wrong-answer pattern callout
        tally = getattr(game, 'wrong_choice_tally', {})
        if tally:
            most_text, most_cnt = max(tally.items(), key=lambda kv: kv[1])
            if most_cnt >= 2:
                pattern_y = self.H - 130
                pr = pygame.Rect(60, pattern_y, self.W - 120, 36)
                pygame.draw.rect(self.screen, (40, 10, 10), pr, border_radius=6)
                pygame.draw.rect(self.screen, RED_DIM, pr, 1, border_radius=6)
                pts = self.f_tiny.render(
                    f"PATTERN ALERT: You picked  \"{most_text}\"  wrong  {most_cnt}×  this run.",
                    True, (220, 140, 140))
                self.screen.blit(pts, (pr.x + 10, pr.y + 10))

        has_wrong = bool(getattr(game, 'wrong_log', []))
        dr = pygame.Rect(cx - 220, self.H - 78, 220, 54)
        self._button("CONTINUE  ►", dr,
                     (20, 50, 20) if won else (50, 10, 10),
                     (30, 80, 30) if won else (80, 16, 16),
                     GREEN if won else RED, self.f_large, "stats_done")
        if has_wrong:
            fr = pygame.Rect(cx + 10, self.H - 78, 220, 54)
            self._button("STUDY  CARDS  [F]", fr,
                         (20, 45, 55), (30, 65, 80), TEAL, self.f_small, "flashcard_btn")
        self._tc("Press  ENTER  to  return  to  title",
                 self.H - 14, self.f_tiny, DARK_GRAY)

    # ══════════════════ OVERLAY HELPERS ══════════════════════════════════════

    def _draw_minimap(self, game, mm_y_override=None):
        d     = game.dungeon
        graph = d.graph
        if not graph:
            return
        mm_w, mm_h = 160, 90
        mm_x  = self.W - mm_w - 8
        mm_y  = mm_y_override if mm_y_override is not None else 96
        mm_surf = pygame.Surface((mm_w, mm_h), pygame.SRCALPHA)
        mm_surf.fill((8, 6, 14, 200))
        pygame.draw.rect(mm_surf, BORDER, pygame.Rect(0, 0, mm_w, mm_h), 1, border_radius=5)
        cols = [r["col"] for r in graph]
        rows = [r["row"] for r in graph]
        mc, xc = min(cols), max(cols)
        mr, xr = min(rows), max(rows)
        csp = max(1, xc - mc)
        rsp = max(1, xr - mr)
        pad = 10

        def mpos(col, row):
            sx = pad + int((col - mc) / csp * (mm_w - pad * 2))
            sy = (pad + mm_h // 2
                  + int((row - (mr + xr) / 2) / rsp * (mm_h - pad * 2) * 0.6))
            return sx, sy

        centers_mm = [mpos(r["col"], r["row"]) for r in graph]
        drawn_e = set()
        for i, room in enumerate(graph):
            for j in room["adj"]:
                e = (min(i, j), max(i, j))
                if e in drawn_e:
                    continue
                drawn_e.add(e)
                pygame.draw.line(mm_surf, (50, 44, 62), centers_mm[i], centers_mm[j], 1)
        accessible = set(d.accessible_rooms)
        for i, room in enumerate(graph):
            sx, sy = centers_mm[i]
            rad = 4
            if room["cleared"]:
                pygame.draw.circle(mm_surf, GREEN_DIM, (sx, sy), rad)
            elif i == d.active_room_idx:
                pygame.draw.circle(mm_surf, WHITE, (sx, sy), rad + 1)
            elif i in accessible:
                pygame.draw.circle(mm_surf, WARM_AMBER, (sx, sy), rad)
            else:
                pygame.draw.circle(mm_surf, (40, 36, 54), (sx, sy), rad)
            if i == d.boss_idx:
                pygame.draw.circle(mm_surf, BOSS_BORDER, (sx, sy), rad, 1)
        self.screen.blit(mm_surf, (mm_x, mm_y))

    def _draw_cursed_entry(self, game):
        t     = game.cursed_entry_timer
        alpha = int(200 * (t / 50))
        ov    = pygame.Surface((self.W, self.H), pygame.SRCALPHA)
        ov.fill((80, 0, 120, min(160, alpha)))
        self.screen.blit(ov, (0, 0))
        cx, cy   = self.W // 2, self.H // 2
        pulse    = int(255 * (t / 50))
        col      = (min(255, pulse + 80), 0, min(255, pulse + 160))
        bone_len = 90
        thick    = 8
        pygame.draw.line(self.screen, col,
                         (cx - bone_len, cy - bone_len),
                         (cx + bone_len, cy + bone_len), thick)
        pygame.draw.line(self.screen, col,
                         (cx + bone_len, cy - bone_len),
                         (cx - bone_len, cy + bone_len), thick)
        pygame.draw.circle(self.screen, col, (cx, cy - bone_len - 20), 26, thick - 2)
        warn = self.f_title.render("CURSED  ROOM!", True, (255, 80, 255))
        warn.set_alpha(alpha)
        self.screen.blit(warn, warn.get_rect(center=(cx, cy + bone_len + 38)))

    def _draw_key_splash(self, game):
        """Key-found float: glowing circle rises from answer area to HUD key slot."""
        t    = game.key_splash_timer   # 90 -> 0
        frac = t / 90.0                # 1.0 -> 0.0
        ease = frac * frac * (3 - 2 * frac)   # smoothstep

        # Float path: answer area center -> key slot
        start_x, start_y = self.W // 2, int(self.H * 0.72)
        end_x,   end_y   = 351, 22
        px = int(start_x + (end_x - start_x) * (1 - ease))
        py = int(start_y + (end_y - start_y) * (1 - ease))

        radius = max(6, int(18 * ease + 7 * (1 - ease)))

        # Glow halo
        glow_a = int(160 * frac)
        if glow_a > 0:
            glow = pygame.Surface((radius * 4 + 4, radius * 4 + 4), pygame.SRCALPHA)
            pygame.draw.circle(glow, (255, 210, 0, glow_a),
                               (radius * 2 + 2, radius * 2 + 2), radius * 2)
            self.screen.blit(glow, (px - radius * 2 - 2, py - radius * 2 - 2))

        # Core circle
        core_a = min(255, int(255 * frac))
        if core_a > 0:
            core_s = pygame.Surface((radius * 2 + 2, radius * 2 + 2), pygame.SRCALPHA)
            pygame.draw.circle(core_s, (255, 235, 80, core_a),
                               (radius + 1, radius + 1), radius)
            pygame.draw.circle(core_s, (220, 180, 20, core_a),
                               (radius + 1, radius + 1), radius, 2)
            self.screen.blit(core_s, (px - radius - 1, py - radius - 1))

        # "KEY!" label fades out during first half
        if frac > 0.5:
            lbl_a = int(255 * (frac - 0.5) / 0.5)
            lbl = self.f_med_b.render("KEY!", True, (255, 240, 60))
            lbl.set_alpha(lbl_a)
            self.screen.blit(lbl, lbl.get_rect(center=(px, py - radius - 14)))

        # Arrival pulse on key slot
        if frac < 0.22:
            p_a = int(200 * (1 - frac / 0.22))
            ov  = pygame.Surface((self.W, self.H), pygame.SRCALPHA)
            pygame.draw.rect(ov, (255, 220, 0, p_a),
                             pygame.Rect(306, 8, 90, 28), 3, border_radius=7)
            self.screen.blit(ov, (0, 0))

    def _draw_tome_anim(self, game):
        import random as _torn
        t    = game.tome_anim_timer
        frac = t / 70.0               # 1.0 → 0.0
        ov   = pygame.Surface((self.W, self.H), pygame.SRCALPHA)
        ov.fill((20, 10, 40, int(130 * frac)))
        self.screen.blit(ov, (0, 0))
        cx, cy  = self.W // 2, self.H // 2
        split   = int((1 - frac) * 120)   # 0 → 120 as pages fly apart
        half_w  = 185
        page_h  = 260

        # Left half slides left, right half slides right
        left_r  = pygame.Rect(cx - half_w - split, cy - page_h // 2, half_w, page_h)
        right_r = pygame.Rect(cx           + split, cy - page_h // 2, half_w, page_h)
        for pr in (left_r, right_r):
            pygame.draw.rect(self.screen, (220, 200, 160), pr, border_radius=8)
            pygame.draw.rect(self.screen, (160, 130, 80),  pr, 3, border_radius=8)

        # Vertical jagged tear along the centre seam (only while pages are close)
        if split < 40:
            _rng = _torn.Random(42)   # seeded so the edge is stable between frames
            for vy in range(cy - page_h // 2, cy + page_h // 2, 11):
                jag = _rng.randint(-5, 5)
                pygame.draw.line(self.screen, (140, 100, 50),
                                 (cx - split,     vy), (cx - split + jag, vy + 6), 2)
                pygame.draw.line(self.screen, (140, 100, 50),
                                 (cx + split,     vy), (cx + split - jag, vy + 6), 2)

        alpha = int(255 * frac)
        label = self.f_med_b.render("Scholar's Tome  --  Streak Saved!", True, PURPLE)
        label.set_alpha(alpha)
        self.screen.blit(label, label.get_rect(center=(cx, cy)))

    def _draw_score_popup(self, pop):
        alpha = int(255 * min(1.0, pop["timer"] / 30))
        col   = pop.get("color", (255, 240, 60))
        surf  = self.f_large.render(pop["text"], True, col)
        surf.set_alpha(alpha)
        self.screen.blit(surf, surf.get_rect(center=(int(pop["x"]), int(pop["y"]))))

    def _draw_low_hp_pulse(self, game):
        pulse = (game.tick // 8) % 2 == 0
        alpha = 120 if pulse else 60
        ov    = pygame.Surface((self.W, self.H), pygame.SRCALPHA)
        pygame.draw.rect(ov, (220, 20, 0, alpha),
                         pygame.Rect(0, 0, self.W, self.H), 18)
        self.screen.blit(ov, (0, 0))

    def _draw_room_icon(self, cx, cy, rt):
        if rt == RoomType.CAMPFIRE:
            pygame.draw.ellipse(self.screen, WARM_AMBER,
                                pygame.Rect(cx - 5, cy - 8, 10, 12))
            pygame.draw.ellipse(self.screen, (255, 220, 80),
                                pygame.Rect(cx - 3, cy - 5, 6, 8))
        elif rt == RoomType.TREASURE:
            pygame.draw.circle(self.screen, GOLD_COIN, (cx, cy), 6)
            pygame.draw.circle(self.screen, (180, 140, 20), (cx, cy), 6, 1)
        elif rt == RoomType.CHALLENGE:
            s = self.f_small.render("!", True, RED)
            self.screen.blit(s, s.get_rect(center=(cx, cy)))
        elif rt == RoomType.VAULT:
            s = self.f_small.render("$", True, GOLD_COIN)
            self.screen.blit(s, s.get_rect(center=(cx, cy)))
        elif rt == RoomType.CURSED:
            pygame.draw.line(self.screen, PURPLE, (cx - 5, cy - 5), (cx + 5, cy + 5), 2)
            pygame.draw.line(self.screen, PURPLE, (cx + 5, cy - 5), (cx - 5, cy + 5), 2)
        elif rt == RoomType.TEACH_IT_BACK:
            s = self.f_tiny.render("?→Q", True, TEAL)
            self.screen.blit(s, s.get_rect(center=(cx, cy)))


    # ── FLOOR BRIEFING ────────────────────────────────────────────────────────
    def _floor_briefing(self, game):
        d = game.dungeon
        self.screen.fill(BG)
        self._draw_dungeon_bg(game.tick, strength=6)
        self._tc(f"FLOOR  {d.floor}  --  DESCENDING", 28, self.f_title, GOLD)

        topics_here = sorted(set(
            q.get("_topic", "") for q in d._active_pool if q.get("_topic")
        ))
        box = pygame.Rect(60, 80, self.W - 120, self.H - 200)
        pygame.draw.rect(self.screen, PANEL, box, border_radius=14)
        pygame.draw.rect(self.screen, BORDER, box, 2, border_radius=14)

        self._t("Topics you may encounter this floor:", (box.x + 20, box.y + 16), self.f_med_b, GOLD)
        ty = box.y + 54
        for topic in topics_here:
            tc2 = TOPIC_COLORS.get(topic, GRAY)
            full = TOPICS.get(topic, topic)
            c   = game.per_topic_correct.get(topic, 0)
            w   = game.per_topic_wrong.get(topic, 0)
            tot = c + w
            acc = int(100 * c / max(1, tot))
            ms  = game.milestone_achieved.get(topic, 0)
            stars = " *" * (1 if ms == 25 else (2 if ms == 50 else (3 if ms >= 100 else 0)))
            lbl = self.f_med_b.render(f"  {topic}  --  {full}{stars}", True, tc2)
            self.screen.blit(lbl, (box.x + 20, ty))
            if tot > 0:
                bar_r = pygame.Rect(box.x + 20, ty + 26, box.w - 40, 7)
                pygame.draw.rect(self.screen, DARK_GRAY, bar_r, border_radius=3)
                fw = int(bar_r.width * c / max(1, tot))
                bar_col = GREEN if acc >= 70 else (GOLD if acc >= 40 else RED)
                if fw > 0:
                    pygame.draw.rect(self.screen, bar_col,
                                     pygame.Rect(bar_r.x, bar_r.y, fw, 7), border_radius=3)
                acc_s = self.f_tiny.render(f"{acc}%  ({c}/{tot})", True, bar_col)
                self.screen.blit(acc_s, (bar_r.right - acc_s.get_width() - 4, ty + 26))
            ty += 44
            if ty + 44 > box.bottom - 20:
                break

        if d._weak_pool:
            self._tc(f"[!]  {len(d._weak_pool)} weak question(s) in pool -- boss may test them",
                     box.bottom - 30, self.f_small, ORANGE)

        br = pygame.Rect(self.W // 2 - 200, self.H - 100, 400, 56)
        self._button("ENTER  FLOOR  ->", br, (20, 50, 20), (30, 80, 30), GREEN, self.f_large, "briefing_go")
        self._tc("Press  SPACE  or  ENTER  to  begin", self.H - 26, self.f_tiny, DARK_GRAY)

    # ── GRIMOIRE ──────────────────────────────────────────────────────────────
    def _grimoire(self, game):
        self.screen.fill((6, 2, 14))
        self._draw_dungeon_bg(game.tick, tint=PURPLE, strength=5)
        self._tc("MISTAKE  GRIMOIRE", 18, self.f_title, PURPLE)
        self._tc("All wrong answers this run", 62, self.f_small, GRAY)

        wrong = getattr(game, "wrong_log", [])
        page  = getattr(game, "grimoire_page", 0)
        per_p = 4
        start = page * per_p
        shown = wrong[start: start + per_p]

        if not wrong:
            self._tc("No mistakes yet -- keep it up!", self.H // 2, self.f_large, GREEN)
        else:
            for ri, entry in enumerate(shown):
                q      = entry["q"]
                chosen = entry["chosen"]
                corr   = entry["correct_idx"]
                choices = entry["choices"]
                ey = 96 + ri * 125
                er = pygame.Rect(50, ey, self.W - 100, 118)
                pygame.draw.rect(self.screen, PANEL, er, border_radius=10)
                pygame.draw.rect(self.screen, RED_DIM, er, 2, border_radius=10)
                topic_s = self.f_tiny.render(
                    f"[{q.get('_topic','')}]  #{start + ri + 1} of {len(wrong)}",
                    True, TOPIC_COLORS.get(q.get("_topic", ""), GRAY))
                self.screen.blit(topic_s, (er.x + 10, er.y + 8))
                self._draw_wrapped(q.get("q", ""), pygame.Rect(er.x + 10, er.y + 24, er.w - 20, 40),
                                   self.f_small, WHITE)
                your_text = choices[chosen][:60] if 0 <= chosen < len(choices) else "Time out"
                corr_text = choices[corr][:60]   if 0 <= corr  < len(choices) else ""
                ys = self.f_tiny.render(f"Your answer:  {chr(65+chosen)}.  {your_text}", True, RED)
                cs = self.f_tiny.render(f"Correct:      {chr(65+corr)}.  {corr_text}", True, GREEN)
                self.screen.blit(ys, (er.x + 10, er.y + 70))
                self.screen.blit(cs, (er.x + 10, er.y + 88))

            total_pages = max(1, (len(wrong) + per_p - 1) // per_p)
            self._tc(f"Page {page + 1} / {total_pages}", self.H - 88, self.f_small, GRAY)
            if page > 0:
                pr = pygame.Rect(60, self.H - 72, 130, 44)
                self._button("< PREV", pr, DARK_GRAY, BORDER, GRAY, self.f_small, "grimoire_prev")
            if page < total_pages - 1:
                nr = pygame.Rect(self.W - 200, self.H - 72, 130, 44)
                self._button("NEXT >", nr, DARK_GRAY, BORDER, GRAY, self.f_small, "grimoire_next")

        br = pygame.Rect(self.W // 2 - 130, self.H - 72, 260, 44)
        self._button("BACK  TO  PAUSE", br, (30, 20, 50), (50, 30, 75), PURPLE, self.f_small, "grimoire_back")
        self._tc("ESC  to  return", self.H - 16, self.f_tiny, DARK_GRAY)

    # ── FLASHCARD REVIEW ─────────────────────────────────────────────────────
    def _flashcard_review(self, game):
        wrong    = getattr(game, "wrong_log", [])
        idx      = getattr(game, "flashcard_idx", 0)
        revealed = getattr(game, "flashcard_revealed", False)

        if idx >= len(wrong):
            return

        entry   = wrong[idx]
        q       = entry["q"]
        choices = entry["choices"]
        corr    = entry["correct_idx"]
        chosen  = entry["chosen"]

        self.screen.fill((4, 8, 20))
        self._draw_dungeon_bg(game.tick, tint=TEAL, strength=4)

        total = len(wrong)
        self._tc(f"STUDY  FLASHCARDS  --  {idx + 1} / {total}", 18, self.f_title, TEAL)
        self._tc("Review the questions you missed this run", 58, self.f_small, GRAY)

        cr = pygame.Rect(50, 78, self.W - 100, self.H - 220)
        pygame.draw.rect(self.screen, PANEL, cr, border_radius=16)
        tc2 = TOPIC_COLORS.get(q.get("_topic", ""), TEAL)
        pygame.draw.rect(self.screen, tc2, cr, 3, border_radius=16)

        topic_s = self.f_small.render(
            f"TOPIC:  {TOPICS.get(q.get('_topic', ''), q.get('_topic', ''))}",
            True, tc2)
        self.screen.blit(topic_s, (cr.x + 18, cr.y + 14))

        self._draw_wrapped(q.get("q", ""),
                           pygame.Rect(cr.x + 18, cr.y + 42, cr.w - 36, 110),
                           self.f_med_b, WHITE)

        if revealed:
            sep_y = cr.y + 160
            pygame.draw.rect(self.screen, BORDER, pygame.Rect(cr.x + 18, sep_y, cr.w - 36, 1))

            corr_text = choices[corr][:55] if 0 <= corr  < len(choices) else ""
            your_text = choices[chosen][:55] if 0 <= chosen < len(choices) else "Time out"

            cs = self.f_med_b.render(f"[CORRECT]  {chr(65+corr)}.  {corr_text}", True, GREEN)
            self.screen.blit(cs, (cr.x + 18, sep_y + 12))
            if chosen != corr:
                ys = self.f_small.render(f"[You chose]  {chr(65+chosen)}.  {your_text}", True, RED)
                self.screen.blit(ys, (cr.x + 18, sep_y + 40))

            exp_r = pygame.Rect(cr.x + 18, sep_y + 72, cr.w - 36, cr.bottom - sep_y - 90)
            exp_lbl = self.f_small.render("Explanation:", True, GOLD)
            self.screen.blit(exp_lbl, (exp_r.x, exp_r.y))
            self._draw_wrapped(q.get("e", ""),
                               pygame.Rect(exp_r.x, exp_r.y + 22, exp_r.w, exp_r.h - 22),
                               self.f_small, (200, 195, 210))

            nr = pygame.Rect(self.W // 2 - 160, self.H - 90, 320, 56)
            lbl = "FINISH" if idx + 1 >= total else "NEXT  CARD  ->"
            self._button(lbl, nr, (20, 50, 50), (30, 75, 75), TEAL, self.f_large, "fc_next")
        else:
            hint = self.f_med.render("SPACE  or  click  to  reveal  answer", True, GRAY)
            self.screen.blit(hint, hint.get_rect(center=(self.W // 2, cr.y + 185)))
            rr = pygame.Rect(self.W // 2 - 180, self.H - 90, 360, 56)
            self._button("REVEAL  ANSWER", rr, (20, 40, 50), (30, 60, 75), TEAL, self.f_large, "fc_reveal")

        sr = pygame.Rect(self.W - 175, self.H - 90, 155, 56)
        self._button("SKIP  ALL", sr, DARK_GRAY, BORDER, GRAY, self.f_small, "fc_skip_all")
        self._tc("ESC  to  quit", self.H - 16, self.f_tiny, DARK_GRAY)

    # ── MASTERY SURGE FLASH ──────────────────────────────────────────────────
    def _draw_surge_flash(self, game):
        t     = game.surge_flash_timer
        frac  = t / 180.0
        alpha = int(min(1.0, frac * 3) * 200)
        if alpha <= 0:
            return
        ov = pygame.Surface((self.W, self.H), pygame.SRCALPHA)
        pygame.draw.rect(ov, (0, 200, 180, alpha // 3),
                         pygame.Rect(0, 0, self.W, self.H), 16)
        self.screen.blit(ov, (0, 0))
        text = getattr(game, "surge_flash_text", "MASTERY SURGE!")
        surf = self.f_large.render(text, True, TEAL)
        surf.set_alpha(alpha)
        self.screen.blit(surf, surf.get_rect(center=(self.W // 2, self.H // 2 - 80)))

    # ── RELIC SELECT (Feature 8) ─────────────────────────────────────────────
    def _relic_select(self, game):
        self.screen.fill((10, 6, 22))
        self._draw_dungeon_bg(game.tick, tint=PURPLE, strength=10)

        self._tc("CHOOSE  YOUR  RELIC", 28, self.f_title, PURPLE)
        self._tc("A passive relic accompanies you for the entire run.", 76, self.f_small, GRAY)
        if getattr(game, 'daily_challenge_mode', False):
            self._tc("DAILY  CHALLENGE  MODE  ·  Hard  ·  All Topics",
                     102, self.f_small, TEAL)

        choices = getattr(game, 'relic_choices', [])
        cx      = self.W // 2
        card_w, card_h = 340, 160
        total_w = card_w * len(choices) + 30 * (len(choices) - 1)
        start_x = cx - total_w // 2

        for i, rk in enumerate(choices):
            rdata = RELICS.get(rk, {})
            rc    = rdata.get("color", PURPLE)
            bx    = start_x + i * (card_w + 30)
            by    = self.H // 2 - card_h // 2 - 20
            cr    = pygame.Rect(bx, by, card_w, card_h)
            hov   = cr.collidepoint(pygame.mouse.get_pos())
            fill  = tuple(min(255, c // 4 + (20 if hov else 0)) for c in rc)
            pygame.draw.rect(self.screen, fill, cr, border_radius=14)
            pygame.draw.rect(self.screen, rc if hov else BORDER, cr, 3, border_radius=14)

            # Icon
            icon_r = pygame.Rect(bx + 12, by + 12, 56, 56)
            pygame.draw.rect(self.screen, tuple(c // 3 for c in rc), icon_r, border_radius=8)
            pygame.draw.rect(self.screen, rc, icon_r, 2, border_radius=8)
            ics = self.f_small.render(rdata.get("icon", "?"), True, rc)
            self.screen.blit(ics, ics.get_rect(center=icon_r.center))

            ns = self.f_med_b.render(rdata.get("name", rk), True, WHITE if hov else rc)
            self.screen.blit(ns, (bx + 78, by + 14))
            key_s = self.f_tiny.render(f"[{i+1}]", True, GRAY)
            self.screen.blit(key_s, (bx + card_w - 28, by + 14))
            self._draw_wrapped(rdata.get("desc", ""),
                               pygame.Rect(bx + 12, by + 76, card_w - 24, 72),
                               self.f_tiny, (190, 180, 210))
            btn_r = pygame.Rect(bx + card_w // 2 - 100, by + card_h - 42, 200, 36)
            self._button(f"SELECT  [{i+1}]", btn_r,
                         tuple(c // 5 for c in rc), tuple(c // 3 for c in rc),
                         rc, self.f_small, f"relic_{i}")

        skip_r = pygame.Rect(cx - 120, self.H - 68, 240, 42)
        self._button("SKIP  (no relic)", skip_r, DARK_GRAY, BORDER, GRAY, self.f_small, "relic_skip")
        self._tc("Press  1 / 2 / 3  to  choose  a  relic", self.H - 18, self.f_tiny, DARK_GRAY)

    # ── BOSS ATTACK (Feature 11) ─────────────────────────────────────────────
    def _boss_attack(self, game):
        atk  = getattr(game, 'boss_attack_type', 'drain')
        t    = getattr(game, 'boss_attack_elapsed', 0)
        cx, cy = self.W // 2, self.H // 2

        self.screen.fill(BOSS_BG)
        self._draw_dungeon_bg(game.tick, rough=True, tint=(180, 20, 20), strength=5)

        frac  = min(1.0, t / 40.0)
        alpha = int(255 * frac)

        titles = {
            "timer":     "TIMER  CURSE!",
            "confusion": "CONFUSION  WAVE!",
            "drain":     "GOLD  DRAIN!",
        }
        descs = {
            "timer":     "-5s removed from your question timer for the rest of the fight!",
            "confusion": "The guardian distorts your perception — choices will be shuffled!",
            "drain":     "The boss siphons your gold reserves — you lost 75 gold!",
        }
        colors = {"timer": RED, "confusion": PURPLE, "drain": GOLD_COIN}
        col = colors.get(atk, RED)

        title_s = self.f_huge.render(titles.get(atk, "BOSS ATTACK!"), True, col)
        title_s.set_alpha(alpha)
        self.screen.blit(title_s, title_s.get_rect(center=(cx, cy - 60)))

        desc_s = self.f_med.render(descs.get(atk, ""), True, WHITE)
        desc_s.set_alpha(alpha)
        self.screen.blit(desc_s, desc_s.get_rect(center=(cx, cy + 20)))

        # Animated ring pulse
        ring_r = int(60 + 40 * math.sin(t * 0.15))
        pulse_surf = pygame.Surface((ring_r * 2 + 20, ring_r * 2 + 20), pygame.SRCALPHA)
        pygame.draw.circle(pulse_surf, (*col, int(80 * frac)),
                           (ring_r + 10, ring_r + 10), ring_r, 6)
        self.screen.blit(pulse_surf, (cx - ring_r - 10, cy - ring_r - 90))

        if t > 40:
            cont_r = pygame.Rect(cx - 160, cy + 80, 320, 52)
            self._button("DEFEND  ►", cont_r, (50, 5, 5), (80, 10, 10),
                         col, self.f_large, "boss_atk_continue")
            self._tc("Press  ENTER  to  continue", cy + 148, self.f_small, DARK_GRAY)
