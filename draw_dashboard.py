#!/usr/bin/env python3
"""Render the Global Intelligence Dashboard entry.png (1024x1024).

Build-time renderer for the news-image-20261123 make.fun entry.
Pure Python 3 standard library + Pillow. Deterministic: the same
input always produces byte-identical PNG output (no timestamps,
no randomness, fixed font files).

Layout (1024x1024, white background, black text, one red accent):
  Masthead  y  30-104   title + date + black rule
  Lead      y 116-372   COP31 collapse (1 story, 3 facts, metric box)
  Row A     y 388-648   3 major stories (Europe / Libya / US)
  Row B     y 664-924   4 minor stories (economy / markets / disaster / politics)
  Footer    y 936-988   totals + sources

Every fact below was verified against wire reporting on 23 Nov 2026
(see SOURCES.md). No invented numbers, names, or quotes.
"""

import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W = H = 1024
MARGIN = 36
RIGHT = W - MARGIN

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (110, 110, 110)
BORDER = (204, 204, 204)
CARD = (245, 245, 245)
ACCENT = (208, 0, 0)  # #D00000, the single accent color

FONT_DIR = "/usr/share/fonts/truetype/liberation"


def font(bold, size):
    name = "LiberationSans-Bold.ttf" if bold else "LiberationSans-Regular.ttf"
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def wrap(draw, text, fnt, max_width):
    """Greedy word wrap. Returns a list of lines that fit max_width."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, fnt, max_width, fill, max_lines, line_h):
    """Draw wrapped text; raise if it would exceed max_lines (no clipping)."""
    lines = wrap(draw, text, fnt, max_width)
    if len(lines) > max_lines:
        raise ValueError("text overflows %d lines: %r -> %r" % (max_lines, text, lines))
    for i, line in enumerate(lines):
        draw.text((x, y + i * line_h), line, font=fnt, fill=fill)
    return y + len(lines) * line_h


def card(draw, x, y, w, h):
    draw.rectangle([x, y, x + w - 1, y + h - 1], fill=CARD, outline=BORDER, width=1)
    draw.rectangle([x, y, x + w - 1, y + 4], fill=ACCENT)


def main():
    img = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(img)

    # ---- Masthead -------------------------------------------------------
    f_title = font(True, 38)
    f_date = font(True, 28)
    d.text((MARGIN, 34), "GLOBAL BRIEFING", font=f_title, fill=BLACK)
    date = "23 NOV 2026"
    d.text((RIGHT - d.textlength(date, font=f_date), 40), date, font=f_date, fill=ACCENT)
    d.rectangle([MARGIN, 96, RIGHT, 99], fill=BLACK)

    # ---- Lead story: COP31 collapse --------------------------------------
    tag = "ANTALYA, TURKIYE  ·  CLIMATE"
    f_tag = font(True, 16)
    d.text((MARGIN, 116), tag, font=f_tag, fill=ACCENT)

    f_head = font(True, 30)
    head = "COP31 COLLAPSES: 200 NATIONS, NO DEAL"
    draw_wrapped(d, MARGIN, 144, head, f_head, 620, BLACK, 2, 36)

    f_bullet = font(False, 17)
    bullets = [
        "Talks ran 48 hours into overtime",
        "No agreement on fossil-fuel phase-out",
        "First full COP collapse since 2009",
    ]
    by = 224
    for b in bullets:
        d.text((MARGIN, by), "•", font=f_bullet, fill=ACCENT)
        d.text((MARGIN + 22, by), b, font=f_bullet, fill=BLACK)
        by += 26

    # Metric box (right of the lead story)
    mx, my, mw, mh = 700, 128, RIGHT - 700, 232
    d.rectangle([mx, my, mx + mw - 1, my + mh - 1], fill=CARD, outline=BORDER, width=1)
    d.rectangle([mx, my, mx + mw - 1, my + 4], fill=ACCENT)
    f_big = font(True, 84)
    f_unit = font(True, 30)
    d.text((mx + 24, my + 22), "0", font=f_big, fill=ACCENT)
    d.text((mx + 108, my + 62), "DEAL", font=f_unit, fill=BLACK)
    f_cap = font(False, 15)
    d.text((mx + 24, my + 128), "No agreement", font=f_cap, fill=GRAY)
    d.text((mx + 24, my + 152), "after 48h overtime", font=f_cap, fill=GRAY)
    f_src = font(False, 14)
    d.text((mx + 24, my + 196), "XINHUA · AP", font=f_src, fill=GRAY)

    # ---- Row A: 3 major stories ------------------------------------------
    row_a = [
        {
            "tag": "KYIV REGION  ·  EUROPE",
            "head": "DYMER STRIKE KILLS 11",
            "body": "Drone hits apartment block; teen among dead; toll rose to 11 on Monday.",
            "metric": "11 KILLED",
            "src": "AP · REUTERS",
        },
        {
            "tag": "BENGHAZI, LIBYA  ·  CONFLICT",
            "head": "UKRAINE SINKS RUSSIAN FRIGATE",
            "body": "Naval drones hit the Merkury off Libya; Zelenskyy claims the attack.",
            "metric": "1 FRIGATE SUNK",
            "src": "AL JAZEERA",
        },
        {
            "tag": "WASHINGTON  ·  POLITICS",
            "head": "DEMOCRATS CLINCH 258 HOUSE SEATS",
            "body": "Largest House majority for either party since 1992, AP projects.",
            "metric": "258 SEATS",
            "src": "AP",
        },
    ]
    ax, ay, aw, ah, gap = MARGIN, 388, 312, 260, 16
    f_atag = font(True, 14)
    f_ahead = font(True, 20)
    f_abody = font(False, 16)
    f_amet = font(True, 16)
    for i, s in enumerate(row_a):
        x = ax + i * (aw + gap)
        card(d, x, ay, aw, ah)
        px = x + 16
        d.text((px, ay + 20), s["tag"], font=f_atag, fill=ACCENT)
        draw_wrapped(d, px, ay + 48, s["head"], f_ahead, aw - 32, BLACK, 2, 25)
        draw_wrapped(d, px, ay + 108, s["body"], f_abody, aw - 32, BLACK, 3, 21)
        d.text((px, ay + ah - 58), s["metric"], font=f_amet, fill=ACCENT)
        d.text((px, ay + ah - 30), s["src"], font=f_src, fill=GRAY)

    # ---- Row B: 4 minor stories ------------------------------------------
    row_b = [
        {
            "tag": "TURIN  ·  SPORT",
            "head": "ALCARAZ WINS ATP FINALS",
            "body": "Beats world No. 1 Zverev 6-2, 7-6(7); maiden title; 5-0 week in Turin.",
            "metric": "5-0 WEEK",
        },
        {
            "tag": "TAIPEI  ·  MARKETS",
            "head": "TAIWAN STOCKS SWING 1,666 PTS",
            "body": "Index closes +778.6 (+2.16%) at 36,811.89; TSMC ends NT$2,030.",
            "metric": "+2.16%",
        },
        {
            "tag": "BANTEN  ·  DISASTER",
            "head": "FACTORY FIRE KILLS 24",
            "body": "Candy plant blaze; about 30 people still unaccounted for.",
            "metric": "24 DEAD",
        },
        {
            "tag": "US–IRAN  ·  POLITICS",
            "head": "TRUMP: STRIKE IRAN IF NO DEAL",
            "body": "“Inclined” to resume conflict unless a deal lands by New Year.",
            "metric": "JAN 1",
        },
    ]
    bx, by_, bw, bh = MARGIN, 664, 226, 260
    f_btag = font(True, 13)
    f_bhead = font(True, 18)
    f_bbody = font(False, 15)
    f_bmet = font(True, 16)
    for i, s in enumerate(row_b):
        x = bx + i * (bw + gap)
        card(d, x, by_, bw, bh)
        px = x + 14
        d.text((px, by_ + 18), s["tag"], font=f_btag, fill=ACCENT)
        draw_wrapped(d, px, by_ + 44, s["head"], f_bhead, bw - 28, BLACK, 2, 22)
        draw_wrapped(d, px, by_ + 96, s["body"], f_bbody, bw - 28, BLACK, 4, 19)
        d.text((px, by_ + bh - 30), s["metric"], font=f_bmet, fill=ACCENT)

    # ---- Footer ------------------------------------------------------------
    f_foot = font(False, 15)
    foot = "TOTAL EVENTS TRACKED: 8    •    SOURCES: AP · REUTERS · XINHUA · AL JAZEERA    •    MONDAY 23 NOVEMBER 2026"
    fw = d.textlength(foot, font=f_foot)
    d.text(((W - fw) / 2, 946), foot, font=f_foot, fill=GRAY)

    img.save(OUT, "PNG", compress_level=9)
    print("wrote %s (%d bytes)" % (OUT, os.path.getsize(OUT)))


if __name__ == "__main__":
    main()
