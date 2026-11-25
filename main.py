#!/usr/bin/env python3
"""THE WORLD'S NEWS IN ONE PICTURE - Tuesday 24 November 2026.
Rebuilt after the Rank 1 reference for Tue 17 Nov 2026: one huge date
title, 3 huge hero cards, 10 medium cards, a large map bottom-left and
a 2-column digest bottom-right. 35 stories in total (v1 content).
Pure Python standard library only: os, struct, zlib, math.
No third-party imaging library, no network, no external files.
Deterministic output. Run: python3 -P -s main.py
Output: $MAKEFUN_OUTPUT_DIR/entry.png, or /output/entry.png if it
exists, otherwise ./output/entry.png. Never writes to /bot.
"""
import os
import struct
import zlib
from math import sqrt, cos, sin, radians

W, H = 1024, 1024
IVORY = (250, 247, 240)
NAVY = (16, 30, 51)
NAVY2 = (28, 48, 78)
GOLD = (198, 158, 54)
SEA = (220, 232, 240)
LAND = (216, 205, 178)
LAND_LINE = (120, 110, 85)
INK = (24, 28, 38)
GREY = (90, 92, 98)
WHITE = (255, 255, 255)
RED = (176, 58, 44)       # Americas
BLUE = (31, 78, 121)      # Europe
ORANGE = (200, 110, 30)   # Middle East
PURPLE = (110, 70, 140)   # Asia
GREEN = (40, 130, 70)     # Africa
TEAL = (0, 120, 110)      # Oceania
DARKGREY = (90, 92, 98)   # World
LBLUE = (90, 110, 180)
AMBER = (180, 120, 30)

REGION_COLORS = {
    "WORLD": DARKGREY, "EUROPE": BLUE, "AMERICAS": RED,
    "MIDDLE EAST": ORANGE, "ASIA-PACIFIC": PURPLE,
    "AFRICA": GREEN, "OCEANIA": TEAL,
}

def _g(*rows):
    return rows

FONT = {
" ": _g("00000","00000","00000","00000","00000","00000","00000"),
"A": _g("01110","10001","10001","11111","10001","10001","10001"),
"B": _g("11110","10001","10001","11110","10001","10001","11110"),
"C": _g("01110","10001","10000","10000","10000","10001","01110"),
"D": _g("11110","10001","10001","10001","10001","10001","11110"),
"E": _g("11111","10000","10000","11110","10000","10000","11111"),
"F": _g("11111","10000","10000","11110","10000","10000","10000"),
"G": _g("01110","10001","10000","10111","10001","10001","01111"),
"H": _g("10001","10001","10001","11111","10001","10001","10001"),
"I": _g("01110","00100","00100","00100","00100","00100","01110"),
"J": _g("00111","00010","00010","00010","00010","10010","01100"),
"K": _g("10001","10010","10100","11000","10100","10010","10001"),
"L": _g("10000","10000","10000","10000","10000","10000","11111"),
"M": _g("10001","11011","10101","10101","10001","10001","10001"),
"N": _g("10001","11001","10101","10011","10001","10001","10001"),
"O": _g("01110","10001","10001","10001","10001","10001","01110"),
"P": _g("11110","10001","10001","11110","10000","10000","10000"),
"Q": _g("01110","10001","10001","10001","10101","10010","01101"),
"R": _g("11110","10001","10001","11110","10100","10010","10001"),
"S": _g("01111","10000","10000","01110","00001","00001","11110"),
"T": _g("11111","00100","00100","00100","00100","00100","00100"),
"U": _g("10001","10001","10001","10001","10001","10001","01110"),
"V": _g("10001","10001","10001","10001","10001","01010","00100"),
"W": _g("10001","10001","10001","10101","10101","11011","10001"),
"X": _g("10001","10001","01010","00100","01010","10001","10001"),
"Y": _g("10001","10001","01010","00100","00100","00100","00100"),
"Z": _g("11111","00001","00010","00100","01000","10000","11111"),
"0": _g("01110","10001","10011","10101","11001","10001","01110"),
"1": _g("00100","01100","00100","00100","00100","00100","01110"),
"2": _g("01110","10001","00001","00110","01000","10000","11111"),
"3": _g("11111","00010","00100","00010","00001","10001","01110"),
"4": _g("00010","00110","01010","10010","11111","00010","00010"),
"5": _g("11111","10000","11110","00001","00001","10001","01110"),
"6": _g("00110","01000","10000","11110","10001","10001","01110"),
"7": _g("11111","00001","00010","00100","01000","01000","01000"),
"8": _g("01110","10001","10001","01110","10001","10001","01110"),
"9": _g("01110","10001","10001","01111","00001","00010","01100"),
"a": _g("00000","00000","01110","00001","01111","10001","01111"),
"b": _g("10000","10000","11110","10001","10001","10001","11110"),
"c": _g("00000","00000","01110","10000","10000","10001","01110"),
"d": _g("00001","00001","01111","10001","10001","10001","01111"),
"e": _g("00000","00000","01110","10001","11111","10000","01110"),
"f": _g("00110","01001","01000","11110","01000","01000","01000"),
"g": _g("00000","01111","10001","10001","01111","00001","01110"),
"h": _g("10000","10000","11110","10001","10001","10001","10001"),
"i": _g("00100","00000","01100","00100","00100","00100","01110"),
"j": _g("00010","00000","00110","00010","00010","00010","10010"),
"k": _g("10000","10000","10010","10100","11000","10100","10010"),
"l": _g("01100","00100","00100","00100","00100","00100","01110"),
"m": _g("00000","00000","11010","10101","10101","10101","10101"),
"n": _g("00000","00000","11110","10001","10001","10001","10001"),
"o": _g("00000","00000","01110","10001","10001","10001","01110"),
"p": _g("00000","00000","11110","10001","10001","11110","10000"),
"q": _g("00000","00000","01111","10001","10001","01111","00001"),
"r": _g("00000","00000","10110","11001","10000","10000","10000"),
"s": _g("00000","00000","01111","10000","01110","00001","11110"),
"t": _g("01000","01000","11100","01000","01000","01000","00110"),
"u": _g("00000","00000","10001","10001","10001","10011","01101"),
"v": _g("00000","00000","10001","10001","10001","01010","00100"),
"w": _g("00000","00000","10001","10001","10101","10101","01010"),
"x": _g("00000","00000","10001","01010","00100","01010","10001"),
"y": _g("00000","00000","10001","10001","01111","00001","01110"),
"z": _g("00000","00000","11111","00010","00100","01000","11111"),
".": _g("00000","00000","00000","00000","00000","01100","01100"),
",": _g("00000","00000","00000","00000","01100","00100","01000"),
":": _g("00000","01100","01100","00000","01100","01100","00000"),
";": _g("00000","01100","01100","00000","01100","00100","01000"),
"'": _g("00100","00100","01000","00000","00000","00000","00000"),
'"': _g("01010","01010","00000","00000","00000","00000","00000"),
"-": _g("00000","00000","00000","11111","00000","00000","00000"),
"/": _g("00001","00010","00010","00100","01000","01000","10000"),
"%": _g("11001","11010","00010","00100","01000","01011","10011"),
"+": _g("00000","00100","00100","11111","00100","00100","00000"),
"=": _g("00000","00000","11111","00000","11111","00000","00000"),
"&": _g("01100","10010","10100","01000","10101","10010","01101"),
"!": _g("00100","00100","00100","00100","00100","00000","00100"),
"?": _g("01110","10001","00001","00110","00100","00000","00100"),
"(": _g("00010","00100","01000","01000","01000","00100","00010"),
")": _g("01000","00100","00010","00010","00010","00100","01000"),
"#": _g("01010","01010","11111","01010","11111","01010","01010"),
"@": _g("01110","10001","10111","10101","10110","10000","01110"),
"$": _g("00100","01111","10100","01110","00101","11110","00100"),
"*": _g("00000","00100","10101","01110","10101","00100","00000"),
"•": _g("00000","00000","01100","01100","01100","00000","00000"),
"·": _g("00000","00000","00000","01100","01100","00000","00000"),
"[": _g("01110","01000","01000","01000","01000","01000","01110"),
"]": _g("01110","00010","00010","00010","00010","00010","01110"),
"_": _g("00000","00000","00000","00000","00000","00000","11111"),
}
UNKNOWN_GLYPH = FONT["?"]

class Canvas:
    def __init__(self, w, h, bg):
        self.w = w; self.h = h
        self.data = bytearray(bytes(bg) * (w * h))
    def fill_rect(self, x, y, w, h, color):
        if w <= 0 or h <= 0: return
        x0 = max(0, x); y0 = max(0, y)
        x1 = min(self.w, x + w); y1 = min(self.h, y + h)
        if x1 <= x0 or y1 <= y0: return
        row = bytes(color) * (x1 - x0)
        d = self.data; W = self.w
        for yy in range(y0, y1):
            s = (yy * W + x0) * 3
            d[s:s + len(row)] = row
    def set_px(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.data[i] = color[0]; self.data[i+1] = color[1]; self.data[i+2] = color[2]
    def draw_line(self, x0, y0, x1, y1, color, thick=1):
        dx = abs(x1 - x0); dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1; sy = 1 if y0 < y1 else -1
        err = dx + dy
        while True:
            if thick <= 1: self.set_px(x0, y0, color)
            else: self.fill_rect(x0 - thick // 2, y0 - thick // 2, thick, thick, color)
            if x0 == x1 and y0 == y1: break
            e2 = 2 * err
            if e2 >= dy: err += dy; x0 += sx
            if e2 <= dx: err += dx; y0 += sy
    def draw_rect(self, x, y, w, h, color, thick=1):
        self.fill_rect(x, y, w, thick, color)
        self.fill_rect(x, y + h - thick, w, thick, color)
        self.fill_rect(x, y, thick, h, color)
        self.fill_rect(x + w - thick, y, thick, h, color)
    def fill_circle(self, cx, cy, r, color):
        for dy in range(-r, r + 1):
            dx = int(sqrt(r * r - dy * dy))
            self.fill_rect(cx - dx, cy + dy, 2 * dx + 1, 1, color)
    def draw_circle(self, cx, cy, r, color):
        for a in range(0, 360, 3):
            self.set_px(int(cx + r * cos(radians(a))), int(cy + r * sin(radians(a))), color)
    def fill_poly(self, pts, color):
        if len(pts) < 3: return
        ys = [p[1] for p in pts]
        y0, y1 = max(0, min(ys)), min(self.h - 1, max(ys))
        n = len(pts)
        for y in range(y0, y1 + 1):
            xs = []
            for i in range(n):
                x0, yy0 = pts[i]; x1, yy1 = pts[(i + 1) % n]
                if (yy0 <= y < yy1) or (yy1 <= y < yy0):
                    if yy1 != yy0:
                        xs.append(x0 + (y - yy0) * (x1 - x0) / (yy1 - yy0))
            xs.sort()
            for k in range(0, len(xs) - 1, 2):
                self.fill_rect(int(xs[k]), y, int(xs[k+1]) - int(xs[k]) + 1, 1, color)
    def poly_outline(self, pts, color):
        n = len(pts)
        for i in range(n):
            self.draw_line(pts[i][0], pts[i][1], pts[(i+1) % n][0], pts[(i+1) % n][1], color)
    def text_width(self, s, scale):
        return len(s) * 6 * scale - scale if s else 0
    def draw_text(self, x, y, s, scale, color, align="left"):
        if align == "center": x = x - self.text_width(s, scale) // 2
        elif align == "right": x = x - self.text_width(s, scale)
        cx = x
        for ch in s:
            glyph = FONT.get(ch, UNKNOWN_GLYPH)
            for r in range(7):
                row = glyph[r]
                for c in range(5):
                    if row[c] == "1":
                        if scale == 1: self.set_px(cx + c, y + r, color)
                        else: self.fill_rect(cx + c * scale, y + r * scale, scale, scale, color)
            cx += 6 * scale
        return cx

def wrap_text(cv, text, max_w, scale):
    words = text.split(" "); lines, cur = [], ""
    for wd in words:
        trial = wd if not cur else cur + " " + wd
        if cv.text_width(trial, scale) <= max_w: cur = trial
        else:
            if cur: lines.append(cur)
            cur = wd
    if cur: lines.append(cur)
    return lines

def write_png(cv, path):
    raw = bytearray(); stride = W * 3
    for y in range(H):
        raw.append(0); raw += cv.data[y * stride:(y + 1) * stride]
    comp = zlib.compress(bytes(raw), 9)
    def chunk(typ, data):
        c = struct.pack(">I", len(data)) + typ + data
        c += struct.pack(">I", zlib.crc32(typ + data) & 0xffffffff)
        return c
    ihdr = struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0)
    png = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr) + chunk(b"IDAT", comp) + chunk(b"IEND", b"")
    with open(path, "wb") as f: f.write(png)
    return len(png)

# ---- World map (bottom-left, large) ----
MAP_X, MAP_Y, MAP_W, MAP_H = 16, 662, 340, 274
def ll(lon, lat):
    x = MAP_X + (lon + 180.0) / 360.0 * MAP_W
    y = MAP_Y + (83.0 - lat) / 143.0 * MAP_H
    return (int(x), int(y))

CONTINENTS = [
    [(-168,66),(-140,70),(-125,72),(-110,73),(-95,80),(-85,80),(-80,73),(-75,72),(-65,60),(-55,52),(-60,47),(-70,42),(-75,35),(-80,32),(-81,26),(-84,30),(-90,21),(-97,26),(-105,23),(-110,24),(-115,30),(-125,40),(-125,49),(-140,60),(-155,58),(-165,60)],
    [(-58,64),(-45,60),(-30,68),(-20,70),(-30,76),(-55,76),(-60,74)],
    [(-80,9),(-77,4),(-80,-3),(-81,-6),(-77,-12),(-72,-18),(-70,-23),(-70,-30),(-72,-37),(-73,-44),(-70,-52),(-65,-55),(-68,-50),(-62,-41),(-57,-38),(-48,-28),(-40,-22),(-35,-9),(-35,-6),(-43,-3),(-50,0),(-55,5),(-60,8),(-70,11),(-75,10)],
    [(-10,36),(-9,43),(-2,44),(-1,46),(-4,48),(-2,50),(0,51),(3,53),(8,57),(10,59),(5,60),(5,62),(12,65),(18,69),(25,71),(30,70),(35,68),(40,67),(45,68),(55,68),(65,69),(68,66),(60,66),(50,64),(40,60),(30,60),(24,59),(20,55),(15,55),(12,55),(8,57)],
    [(-17,15),(-16,20),(-10,30),(-5,35),(0,36),(10,37),(11,34),(20,32),(30,31),(32,31),(35,28),(37,22),(39,20),(43,12),(48,11),(51,11),(51,2),(48,-2),(42,-5),(40,-10),(39,-15),(36,-20),(32,-26),(28,-33),(20,-35),(17,-32),(15,-27),(12,-18),(13,-12),(12,-6),(9,4),(4,6),(-8,5),(-13,8),(-17,12)],
    [(30,36),(36,36),(40,32),(43,30),(48,30),(50,29),(54,26),(57,26),(60,25),(66,25),(70,22),(72,20),(75,15),(77,8),(80,7),(80,13),(85,19),(88,22),(91,22),(93,16),(95,16),(98,10),(100,8),(103,2),(105,9),(108,12),(109,15),(106,20),(108,22),(110,20),(114,22),(118,25),(120,28),(122,32),(120,35),(122,38),(126,40),(128,38),(130,42),(135,44),(138,46),(141,50),(142,53),(140,55),(138,58),(140,62),(145,60),(150,60),(155,60),(158,55),(162,58),(165,60),(170,66),(178,65),(180,65),(170,70),(160,70),(150,70),(140,72),(130,72),(120,73),(110,74),(100,76),(90,75),(80,73),(70,72),(60,68),(50,68),(40,67),(35,68)],
    [(113,-22),(114,-30),(115,-33),(118,-35),(124,-33),(129,-32),(132,-32),(135,-35),(138,-35),(140,-38),(145,-38),(150,-37),(153,-32),(153,-27),(150,-22),(146,-19),(142,-11),(141,-13),(136,-12),(132,-11),(130,-13),(126,-14),(122,-17),(118,-20)],
    [(-5,50),(-3,53),(-5,56),(-3,58),(-1,57),(0,53),(1,51)],
    [(130,31),(132,33),(135,34),(137,35),(139,37),(141,39),(142,42),(144,44),(142,45),(140,42),(138,38),(136,35),(133,34)],
    [(44,-16),(47,-15),(50,-16),(49,-20),(45,-25),(43,-22)],
    [(131,-1),(136,-2),(141,-3),(146,-6),(150,-8),(147,-9),(142,-8),(138,-7),(134,-4)],
    [(167,-45),(170,-43),(174,-41),(176,-38),(178,-37),(174,-39),(172,-42),(168,-46)],
    [(109,1),(113,4),(117,6),(119,1),(117,-3),(113,-3),(110,-2)],
    [(95,5),(98,3),(101,0),(104,-3),(106,-6),(103,-5),(100,0),(97,4)],
]
# 11 pins only (Nov 24 featured stories 1-11). dx,dy = leader offset so none overlap.
PINS = [
    (1, 56.3, 26.5, 0, -18),      # Strait of Hormuz
    (2, 20.1, 32.1, 0, 0),        # Benghazi, Libya
    (3, 114.05, 22.55, 0, 0),     # Shenzhen (Huawei HQ)
    (4, 46.7, 24.7, -16, 14),     # Riyadh
    (5, 4.35, 50.85, 0, 0),       # Brussels (NATO)
    (6, -17.45, 14.69, 0, 0),     # Dakar, Senegal
    (7, 130.9, 37.5, 0, 0),       # Ulleungdo, South Korea
    (8, 34.47, 31.5, 18, 10),     # Gaza
    (9, -74.01, 40.71, 0, 0),     # New York (NYSE)
    (10, -108.5, 25.57, 0, 0),    # Guasave, Sinaloa
    (11, 149.13, -35.28, 0, 0),   # Canberra, Australia
]
PIN_REGIONS = ["WORLD", "EUROPE", "AMERICAS", "MIDDLE EAST", "EUROPE",
               "AFRICA", "ASIA-PACIFIC", "MIDDLE EAST", "AMERICAS",
               "AMERICAS", "OCEANIA"]

# ---- Small illustration scenes (medium cards, ~34px tall, from v1) ----
def draw_scene(cv, x, y, w, h, kind):
    cv.fill_rect(x, y, w, h, (232, 228, 216))
    cx = x + w // 2
    if kind == "summit":
        cv.fill_rect(x, y + 22, w, 12, (200, 190, 160))
        cv.fill_rect(cx - 52, y + 8, 104, 16, NAVY)
        cv.fill_poly([(cx - 58, y + 8), (cx + 58, y + 8), (cx, y + 1)], GOLD)
        for dx in (-36, -12, 12, 36):
            cv.fill_rect(cx + dx - 3, y + 12, 6, 10, IVORY)
        for dx, col in ((-78, RED), (78, BLUE)):
            cv.draw_line(cx + dx, y + 4, cx + dx, y + 22, NAVY, 2)
            cv.fill_rect(cx + dx + 1, y + 4, 14, 8, col)
    elif kind == "naval":
        cv.fill_rect(x, y + 20, w, 14, BLUE)
        cv.draw_line(x + 8, y + 24, x + w - 8, y + 24, WHITE, 1)
        cv.fill_poly([(cx - 70, y + 8), (cx + 70, y + 8), (cx + 55, y + 20), (cx - 55, y + 20)], NAVY)
        cv.fill_rect(cx - 8, y + 1, 4, 8, NAVY)
        cv.fill_rect(cx + 4, y + 3, 12, 5, RED)
        for dx in (-95, 95):
            cv.fill_circle(cx + dx, y + 7, 3, GOLD)
            cv.draw_line(cx + dx, y + 10, cx + dx, y + 13, NAVY, 1)
    elif kind == "tech":
        cv.fill_rect(x, y, w, h, NAVY)
        cv.fill_rect(cx - 22, y + 7, 44, 20, (40, 70, 110))
        cv.draw_rect(cx - 22, y + 7, 44, 20, GOLD, 2)
        cv.fill_rect(cx - 7, y + 14, 14, 6, GOLD)
        for dx in (-38, -28, 28, 38):
            cv.draw_line(cx + dx, y + 17, cx - 22 if dx < 0 else cx + 22, y + 17, GOLD, 1)
            cv.fill_circle(cx + dx, y + 17, 3, GOLD)
    elif kind == "health":
        cv.fill_rect(x, y + 24, w, 10, (190, 200, 170))
        cv.fill_poly([(cx - 60, y + 24), (cx + 60, y + 24), (cx, y + 6)], WHITE)
        cv.poly_outline([(cx - 60, y + 24), (cx + 60, y + 24), (cx, y + 6)], NAVY)
        cv.fill_rect(cx - 42, y + 12, 20, 20, WHITE)
        cv.draw_rect(cx - 42, y + 12, 20, 20, RED, 1)
        cv.fill_rect(cx - 36, y + 19, 8, 6, RED)
        cv.fill_rect(cx - 39, y + 16, 14, 6, RED)
        cv.fill_circle(cx + 55, y + 8, 5, GOLD)
    elif kind == "hospital":
        cv.fill_rect(x, y + 26, w, 8, (190, 200, 170))
        cv.fill_rect(cx - 55, y + 8, 110, 18, WHITE)
        cv.draw_rect(cx - 55, y + 8, 110, 18, NAVY, 1)
        cv.fill_rect(cx - 14, y + 1, 28, 12, WHITE)
        cv.draw_rect(cx - 14, y + 1, 28, 12, RED, 1)
        cv.fill_rect(cx - 3, y + 3, 6, 8, RED)
        cv.fill_rect(cx - 6, y + 5, 12, 4, RED)
        for dx in (-40, -12, 16, 44):
            cv.fill_rect(cx + dx, y + 16, 8, 10, (180, 210, 235))
            cv.draw_rect(cx + dx, y + 16, 8, 10, NAVY, 1)
        cv.fill_circle(cx + 78, y + 7, 5, GOLD)
    elif kind == "protest":
        cv.fill_rect(x, y + 26, w, 8, (200, 190, 160))
        for dx, col in ((-70, RED), (0, BLUE), (70, TEAL)):
            cv.draw_line(cx + dx, y + 10, cx + dx, y + 28, NAVY, 2)
            cv.fill_rect(cx + dx - 22, y + 2, 44, 12, col)
            cv.draw_rect(cx + dx - 22, y + 2, 44, 12, NAVY, 1)
            cv.fill_rect(cx + dx - 14, y + 6, 28, 2, WHITE)
            cv.fill_rect(cx + dx - 14, y + 10, 18, 2, WHITE)
    elif kind == "finance":
        cv.draw_line(x + 18, y + 4, x + 18, y + 30, NAVY, 2)
        cv.draw_line(x + 18, y + 30, x + w - 10, y + 30, NAVY, 2)
        for bx, bh in [(40, 10), (80, 16), (120, 12), (160, 22), (200, 26)]:
            cv.fill_rect(x + bx, y + 30 - bh, 22, bh, TEAL if bh < 20 else GOLD)
        cv.draw_line(x + 40, y + 18, x + 90, y + 12, RED, 2)
        cv.draw_line(x + 90, y + 12, x + 150, y + 16, RED, 2)
        cv.draw_line(x + 150, y + 16, x + 210, y + 6, RED, 2)
    elif kind == "energy":
        cv.fill_rect(x, y + 26, w, 8, (200, 190, 160))
        cv.fill_poly([(cx - 34, y + 26), (cx + 34, y + 26), (cx + 12, y + 4), (cx - 12, y + 4)], NAVY)
        cv.fill_poly([(cx + 2, y + 8), (cx + 10, y + 2), (cx + 14, y + 10)], (230, 120, 30))
        cv.fill_rect(cx - 70, y + 18, 18, 12, RED)
        cv.fill_rect(cx + 52, y + 18, 18, 12, AMBER)
    elif kind == "elections":
        cv.fill_rect(x, y + 26, w, 8, (200, 190, 160))
        cv.fill_rect(cx - 52, y + 14, 104, 12, WHITE)
        cv.draw_rect(cx - 52, y + 14, 104, 12, NAVY, 1)
        dome = [(int(cx + 20 * cos(radians(a))), int((y + 14) - 20 * sin(radians(a)))) for a in range(0, 181, 15)]
        cv.fill_poly(dome + [(cx + 20, y + 14), (cx - 20, y + 14)], NAVY)
        cv.fill_rect(cx - 20, y + 14, 40, 3, GOLD)
        for dx in (-40, -14, 14, 40):
            cv.fill_rect(cx + dx - 3, y + 16, 6, 10, NAVY)
        cv.fill_rect(cx + 62, y + 10, 26, 18, GOLD)
        cv.draw_rect(cx + 62, y + 10, 26, 18, NAVY, 1)
        cv.draw_line(cx + 66, y + 20, cx + 72, y + 25, NAVY, 2)
        cv.draw_line(cx + 72, y + 25, cx + 84, y + 13, NAVY, 2)
    elif kind == "sports":
        cv.fill_rect(x, y + 20, w, 14, (60, 140, 70))
        cv.draw_line(x, y + 20, x + w, y + 20, WHITE, 1)
        cv.fill_circle(cx - 30, y + 15, 11, WHITE)
        cv.draw_circle(cx - 30, y + 15, 11, NAVY)
        cv.fill_poly([(cx - 30, y + 9), (cx - 24, y + 13), (cx - 26, y + 20), (cx - 34, y + 20), (cx - 36, y + 13)], NAVY)
        cv.fill_poly([(cx + 28, y + 4), (cx + 52, y + 4), (cx + 48, y + 18), (cx + 32, y + 18)], GOLD)
        cv.fill_rect(cx + 36, y + 18, 8, 8, GOLD)
        cv.fill_rect(cx + 30, y + 26, 20, 3, GOLD)
    elif kind == "climate":
        cv.fill_rect(x, y + 22, w, 12, BLUE)
        cv.draw_line(x + 8, y + 26, x + w - 8, y + 26, WHITE, 1)
        cv.fill_poly([(cx - 70, y + 22), (cx + 70, y + 22), (cx, y + 10)], (190, 170, 120))
        cv.draw_line(cx + 18, y + 10, cx + 18, y - 2, (90, 70, 40), 2)
        for dx, dy in ((-8, -4), (8, -4), (0, -6)):
            cv.draw_line(cx + 18, y + 0, cx + 18 + dx, y + dy, TEAL, 2)
        cv.fill_circle(cx - 80, y + 7, 5, GOLD)
        cv.fill_circle(cx + 85, y + 28, 3, WHITE)

# ---- Large hero scenes (110px tall, heroes 1-3 only) ----
def draw_hero(cv, x, y, w, h, kind):
    cx = x + w // 2
    if kind == "summit":
        cv.fill_rect(x, y, w, h, (214, 232, 238))
        cv.fill_rect(x, y + h - 18, w, 18, (200, 190, 160))
        # globe, left
        gx, gy, gr = x + 78, y + 52, 38
        cv.fill_circle(gx, gy, gr, (90, 160, 170))
        cv.draw_circle(gx, gy, gr, NAVY)
        cv.fill_poly([(gx - 20, gy - 10), (gx + 5, gy - 22), (gx + 18, gy - 5), (gx - 5, gy + 8)], GREEN)
        cv.fill_poly([(gx - 25, gy + 18), (gx - 5, gy + 12), (gx + 10, gy + 28), (gx - 18, gy + 30)], GREEN)
        # thermometer, right
        cv.fill_rect(x + w - 62, y + 18, 16, 62, WHITE)
        cv.draw_rect(x + w - 62, y + 18, 16, 62, NAVY, 2)
        cv.fill_circle(x + w - 54, y + 86, 11, RED)
        cv.fill_rect(x + w - 58, y + 48, 8, 38, RED)
        cv.fill_rect(x + w - 66, y + 40, 24, 3, NAVY)
        # summit table + flags
        cv.fill_rect(cx - 52, y + h - 34, 104, 10, NAVY)
        cv.fill_rect(cx - 52, y + h - 44, 104, 10, GOLD)
        for dx, col in ((-70, RED), (70, BLUE)):
            cv.draw_line(cx + dx, y + 22, cx + dx, y + h - 44, NAVY, 2)
            cv.fill_rect(cx + dx + 1, y + 22, 26, 14, col)
        cv.draw_text(cx, y + h - 14, "BRUSSELS", 1, NAVY, align="center")
    elif kind == "naval":
        cv.fill_rect(x, y, w, h, (200, 220, 235))
        cv.fill_rect(x, y + 72, w, h - 72, BLUE)
        cv.draw_line(x + 10, y + 80, x + w - 10, y + 80, WHITE, 1)
        cv.draw_line(x + 30, y + 92, x + w - 30, y + 92, (180, 210, 235), 1)
        cv.draw_line(x + 50, y + 102, x + w - 50, y + 102, WHITE, 1)
        cv.fill_poly([(cx - 110, y + 38), (cx + 110, y + 38), (cx + 88, y + 72), (cx - 88, y + 72)], NAVY)
        cv.fill_rect(cx - 14, y + 12, 8, 26, NAVY)
        cv.fill_rect(cx + 8, y + 18, 26, 12, RED)
        cv.fill_circle(cx - 90, y + 20, 6, GOLD)
        cv.fill_circle(cx + 95, y + 14, 6, GOLD)
        cv.draw_line(cx - 90, y + 26, cx - 90, y + 32, NAVY, 1)
        cv.draw_line(cx + 95, y + 20, cx + 95, y + 26, NAVY, 1)
        cv.fill_circle(cx + 40, y + 52, 4, WHITE)
        cv.fill_circle(cx + 60, y + 52, 4, WHITE)
        cv.fill_circle(cx + 80, y + 52, 4, WHITE)
        cv.draw_text(x + 10, y + h - 14, "AT SEA", 1, WHITE)
    elif kind == "tech":
        cv.fill_rect(x, y, w, h, NAVY)
        # rising chart bars, left
        for i, bh in enumerate((22, 34, 28, 46, 62)):
            bx = x + 18 + i * 26
            cv.fill_rect(bx, y + h - 24 - bh, 18, bh, TEAL if i < 3 else GOLD)
        cv.draw_line(x + 18, y + h - 62, x + 140, y + h - 84, GOLD, 2)
        cv.draw_line(x + 140, y + h - 84, x + 150, y + h - 66, GOLD, 2)
        # big chip, right
        chip_x, chip_y = x + w - 118, y + 22
        cv.fill_rect(chip_x, chip_y, 92, 62, (40, 70, 110))
        cv.draw_rect(chip_x, chip_y, 92, 62, GOLD, 3)
        cv.fill_rect(chip_x + 32, chip_y + 22, 28, 18, GOLD)
        for dx in (-14, 0, 14):
            cv.draw_line(chip_x + 46 + dx, chip_y, chip_x + 46 + dx, chip_y - 12, GOLD, 2)
            cv.draw_line(chip_x + 46 + dx, chip_y + 62, chip_x + 46 + dx, chip_y + 74, GOLD, 2)
        cv.draw_text(x + w - 72, y + h - 16, "10/12", 2, GOLD, align="center")

# ---- Data: 35 stories, all first reported / happened Tuesday 24 Nov 2026 ----
# Sources: Daily Summary Of (30 stories, first-reported times 24 Nov UTC),
# Reuters, AP, BBC, ISW, USA Today. ICJ Myanmar ruling (19 Nov) NOT used as a
# Nov 24 story — the Nov 24 item is Malaysia's return plan instead. The
# Villavicencio car bomb happened Monday night but was first reported Tuesday.
# Sparta II was hit Sat 21 Nov; the Nov 24 news is Zelenskyy's confirmation.
# Lahj bus strike happened Mon 23 Nov, reported Tue 24 Nov; attribution contested.
# #11 was the Solomons treaty — REPLACED: it was signed Wed 25 Nov in Canberra,
# so #11 is now Australia's Tue 24 Nov online-safety deal (Labor-Greens agreement).
FEATURES = [
    (1, "WORLD", "AP", "naval",
     "IRAN SAYS FOUR TANKERS HIT MINES",
     "IRGC says four tankers hit naval mines in the Strait of Hormuz and caught fire."),
    (2, "EUROPE", "Reuters", "naval",
     "UKRAINE SAYS DRONES HIT SHIPS",
     "Zelenskyy says Ukraine hit Sparta II in the Gulf of Finland; Kyiv says corvette sunk off Libya."),
    (3, "AMERICAS", "AP", "tech",
     "HUAWEI GUILTY ON 10 OF 12 COUNTS",
     "US jury convicts Huawei of trade-secret theft and bank fraud; racketeering acquitted."),
    (4, "MIDDLE EAST", "Reuters", "energy",
     "HOUTHI DRONE HITS RIYADH PIF TOWER",
     "Saudi says Houthi attack on PIF tower wounds at least 11; second hit in under a week."),
    (5, "EUROPE", "BBC", "summit",
     "NATO VOWS TO DEFEND SPACE",
     "Rutte says alliance will defend against space threats after Russian satellite reports."),
    (6, "AFRICA", "Reuters", "sports",
     "SENEGAL BACK AS AFCON CHAMPIONS",
     "CAS upholds Senegal appeal on Tuesday; title restored after CAF stripped it in March."),
    (7, "ASIA-PACIFIC", "Reuters", "tech",
     "KOREA JETS SCRAMBLE AS RUSSIA NEARS",
     "South Korea orders Ulleungdo residents to shelter as Russian jets enter defence zone."),
    (8, "MIDDLE EAST", "Reuters", "hospital",
     "ISRAEL KILLS HAMAS SECURITY CHIEF",
     "Strike kills Brig. Gen. Naeem Abu Mohammed Nahel in Gaza; six others die in strikes."),
    (9, "AMERICAS", "AP", "finance",
     "DOW RECLAIMS 50,000",
     "Dow closes at 50,019, up 0.85%, back above 50,000 for the first time in a week."),
    (10, "AMERICAS", "AP", "elections",
     "US DRONE HELPS CATCH EL CHAPO ISIDRO",
     "Mexico says US drone helped capture cartel boss; Mexico will try him."),
    (11, "OCEANIA", "AP", "tech",
     "AUSTRALIA STRIKES TECH SAFETY DEAL",
     "Labor and Greens agree digital duty of care; fines up to 5% of global revenue."),
]
DIGEST = [
    (12, "IRGC SAYS IT HIT SHIP IN HORMUZ", "IRGC says its navy hit a ship that went dark."),
    (13, "HOUTHIS 60 KM FROM ADEN", "Yemen army: Houthis near Aden, poised to attack."),
    (14, "UK SANCTIONS HOUTHIS", "UK freezes assets, bans travel for four officials."),
    (15, "IRAQ TAKES KURDISH OILFIELDS", "Baghdad takes control of fields; Barzani objects."),
    (16, "SAUDI STRIKES HIT BUSES IN YEMEN", "Houthis blame Saudi jets; 25 dead or missing."),
    (17, "GAZA MENINGITIS ALERT", "Ministry reports 272 cases in October, 15 deaths."),
    (18, "TURKISH HELICOPTER CRASH KILLS 5", "AS-532 crashes after takeoff from Eskisehir."),
    (19, "HAFTAR VISITS TURKEY", "Libyan commander meets Erdogan in Ankara."),
    (20, "CARTAGENA HOSTAGES HELD", "Gunmen hold 25 hostage; five older women freed."),
    (21, "CAR BOMB INJURES 23 IN COLOMBIA", "Blast hits offices; president blames narco-terror."),
    (22, "ZELENSKY URGES FOUR-WAY TALKS", "Kyiv ready to meet Russia, US, Europe on Tuesday."),
    (23, "PUTIN ADMITS FUEL STRAIN", "Putin says Ukraine strikes burden the fuel market."),
    (24, "PENTAGON REBUKES CANADA", "US says Ottawa falls short on defence, F-35 review."),
    (25, "US BLACKLISTS NVIDIA-LINKED FIRM", "Megaspeed, six firms put on Entity List over chips."),
    (26, "MALAYSIA TO RETURN MIGRANTS", "Anwar: thousands to return, 1,500 by ship in Dec."),
    (27, "HASINA PLANS DECEMBER RETURN", "Hasina plans Dec 16 return; jail awaits, says govt."),
    (28, "INDONESIA PICKS VP CANDIDATES", "Prabowo nominates Amran Sulaiman and Sugiono."),
    (29, "HANOI BLAST KILLS SIX", "Hot pot blast in Dong Da; gas leak suspected."),
    (30, "CHINA SENTENCES SPY TO DEATH", "Official gave 35 secrets to a foreign country."),
    (31, "US LOSES MEASLES-FREE STATUS", "US loses measles-free status after 25-plus years."),
    (32, "US TARIFFS THREAT ON CHINA, EU", "US may tariff China, EU over subsidies, AP says."),
    (33, "NORTH KOREA EXPELS SWISS DIPLOMAT", "Pyongyang demands Swiss office in capital shut."),
    (34, "BUKELE NAMES SOLDIERS KILLED IN HAITI", "Three Salvadorans die in accidental blast in Haiti."),
    (35, "CONGO PLANE MISSING, REBELS CLAIM HIT", "DRC plane missing; rebels claim they shot it down."),
]
KPI_TEXT = "DOW 50,019 • NASDAQ -1.5% • HUAWEI GUILTY 10/12 • HORMUZ 4 TANKERS • SENEGAL AFCON BACK • HOUTHIS 60 KM FROM ADEN"

def build():
    cv = Canvas(W, H, IVORY)
    # Kicker y8-24
    cv.draw_text(16, 10, "THE WORLD'S NEWS IN ONE PICTURE - ALL 7 REGIONS", 1, RED)
    cv.draw_text(1008, 10, "35 STORIES - 7 REGIONS - ALL FROM TUESDAY", 1, INK, align="right")
    cv.fill_rect(16, 24, 992, 2, NAVY)
    # Title scale 6 = 42px tall, ~900px wide for the 25-char Tuesday title
    # (scale 7 would be ~1050px, wider than the 992px frame)
    cv.draw_text(512, 32, "Tuesday 24 November 2026", 6, NAVY, align="center")
    # Thin KPI bar under the title (kept: it fits, 633px wide centred)
    cv.draw_text(512, 82, KPI_TEXT, 1, NAVY, align="center")
    cv.fill_rect(16, 94, 992, 2, GOLD)
    # Hero row y100-340, 3 cards x 325
    hero_x = [16, 349, 682]
    for idx, feat in enumerate(FEATURES[:3]):
        num, region, outlet, kind, headline, summary = feat
        x, y, w, h = hero_x[idx], 100, 325, 240
        col = REGION_COLORS[region]
        cv.fill_rect(x, y, w, h, WHITE)
        cv.draw_rect(x, y, w, h, NAVY, 1)
        draw_hero(cv, x + 1, y + 1, w - 2, 110, kind)
        cv.fill_circle(x + 20, y + 122, 9, col)
        cv.draw_text(x + 20, y + 119, str(num), 1, WHITE, align="center")
        cv.fill_rect(x + 34, y + 114, 120, 13, col)
        cv.draw_text(x + 38, y + 116, region, 1, WHITE)
        cv.draw_text(x + w - 8, y + 116, outlet.upper(), 1, NAVY, align="right")
        lines = wrap_text(cv, headline, w - 16, 3)
        hy = y + 134
        for li, ln in enumerate(lines[:3]):
            cv.draw_text(x + 8, hy + li * 24, ln, 3, NAVY)
        sy = hy + len(lines[:3]) * 24 + 3
        for li, ln in enumerate(wrap_text(cv, summary, w - 16, 1)[:2]):
            cv.draw_text(x + 8, sy + li * 11, ln, 1, INK)
    # Medium rows: 8 cards, 2 rows x 4, 242w x 140h
    med_x = [16, 266, 516, 766]
    med_y = [348, 496]
    for idx, feat in enumerate(FEATURES[3:]):
        num, region, outlet, kind, headline, summary = feat
        r, c = divmod(idx, 4)
        x, y, w, h = med_x[c], med_y[r], 242, 140
        col = REGION_COLORS[region]
        cv.fill_rect(x, y, w, h, WHITE)
        cv.draw_rect(x, y, w, h, NAVY, 1)
        draw_scene(cv, x + 1, y + 8, w - 2, 34, kind)
        cv.fill_circle(x + 16, y + 56, 8, col)
        cv.draw_text(x + 16, y + 53, str(num), 1, WHITE, align="center")
        cv.fill_rect(x + 28, y + 49, 96, 12, col)
        cv.draw_text(x + 32, y + 51, region, 1, WHITE)
        cv.draw_text(x + w - 6, y + 51, outlet.upper(), 1, NAVY, align="right")
        lines = wrap_text(cv, headline, w - 16, 2)
        hy = y + 66
        for li, ln in enumerate(lines[:3]):
            cv.draw_text(x + 8, hy + li * 17, ln, 2, NAVY)
        sy = hy + len(lines[:3]) * 17 + 2
        for li, ln in enumerate(wrap_text(cv, summary, w - 16, 1)[:3]):
            cv.draw_text(x + 8, sy + li * 10, ln, 1, INK)
    # Bottom: map left, digest right
    cv.draw_text(16, 644, "WHERE IT HAPPENED", 2, NAVY)
    cv.draw_text(368, 644, "ALSO ON TUESDAY 24 NOVEMBER", 2, NAVY)
    cv.fill_rect(16, 662, 2, 2, NAVY)
    cv.fill_rect(MAP_X, MAP_Y, MAP_W, MAP_H, SEA)
    for lon in range(-150, 181, 30):
        gx = MAP_X + (lon + 180) / 360.0 * MAP_W
        cv.draw_line(int(gx), MAP_Y, int(gx), MAP_Y + MAP_H, (200, 215, 228), 1)
    for lat in (-30, 0, 30, 60):
        gy = MAP_Y + (83 - lat) / 143.0 * MAP_H
        cv.draw_line(MAP_X, int(gy), MAP_X + MAP_W, int(gy), (200, 215, 228), 1)
    for poly in CONTINENTS:
        pts = [ll(lon, lat) for lon, lat in poly]
        cv.fill_poly(pts, LAND)
        cv.poly_outline(pts, LAND_LINE)
    cv.draw_rect(MAP_X, MAP_Y, MAP_W, MAP_H, NAVY, 2)
    for num, lon, lat, dx, dy in PINS:
        tx, ty = ll(lon, lat)
        px, py = tx + dx, ty + dy
        cv.fill_circle(tx, ty, 2, NAVY)
        if dx or dy:
            cv.draw_line(tx, ty, px, py, NAVY, 1)
        col = REGION_COLORS[PIN_REGIONS[num - 1]]
        cv.fill_circle(px, py, 8, col)
        cv.draw_circle(px, py, 8, NAVY)
        cv.draw_text(px, py - 3, str(num), 1, WHITE, align="center")
    # Legend with region counts (WORLD 1, EUROPE 6, AMERICAS 10, MID EAST 7, ASIA-PAC 7, AFRICA 3, OCEANIA 1)
    legend = [("Americas 10", RED), ("Europe 6", BLUE), ("Mid East 7", ORANGE),
              ("Asia 7", PURPLE), ("Africa 3", GREEN), ("Oceania 1", TEAL), ("World 1", DARKGREY)]
    lx = 16
    for i, (lab, col) in enumerate(legend):
        yy = 944 if i < 4 else 958
        xx = 16 if i < 4 else 16 + (i - 4) * 110
        if i < 4:
            xx = 16 + i * 88
        cv.fill_circle(xx + 5, yy + 4, 4, col)
        cv.draw_text(xx + 12, yy + 1, lab, 1, INK)
    # Digest: 2 columns x 12 rows, stories 12-35, headline + detail
    dig_x = [368, 692]
    for i, (num, head, detail) in enumerate(DIGEST):
        col, row = divmod(i, 12)
        x = dig_x[col]; yy = 668 + row * 25
        cv.fill_circle(x + 7, yy + 3, 7, NAVY)
        cv.draw_text(x + 7, yy, str(num), 1, WHITE, align="center")
        cv.draw_text(x + 18, yy, head, 1, NAVY)
        cv.draw_text(x + 18, yy + 9, detail, 1, GREY)
        cv.draw_line(x, yy + 20, x + 308, yy + 20, (225, 220, 210), 1)
    # Footer y984-1016
    cv.fill_rect(8, 984, 1008, 32, NAVY)
    cv.fill_rect(8, 984, 1008, 3, GOLD)
    cv.draw_text(512, 992, "Every story here happened or was first reported on Tuesday 24 November 2026. Contested claims are marked as claims.", 1, WHITE, align="center")
    cv.draw_text(512, 1004, "Sources: Reuters, AP, BBC, Al Jazeera, UN, CAS, ISW. Original drawings.", 1, GOLD, align="center")
    return cv

def main():
    cv = build()
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR") or ("/output" if os.path.exists("/output") else "./output")
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, "entry.png")
    size = write_png(cv, path)
    print("wrote %s (%d bytes, %dx%d)" % (path, size, W, H))

if __name__ == "__main__":
    main()
