#!/usr/bin/env python3
"""Draw entry.png: a one-page newspaper front page summing up the world
news of Thursday 19 November 2026. Pure PIL, flat colours, no assets."""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 232)
CARD = (255, 253, 246)
INK = (26, 26, 26)
MUTED = (74, 74, 66)
RED = (176, 42, 30)
BLUE = (31, 78, 121)
TEAL = (14, 94, 84)
RULE = (26, 26, 26)

FONT_DIR = "/usr/share/fonts/truetype/noto/"
F_SERIF_BLACK = FONT_DIR + "NotoSerifDisplay-Black.ttf"
F_SERIF_BOLD = FONT_DIR + "NotoSerif-Bold.ttf"
F_SANS_BOLD = FONT_DIR + "NotoSans-Bold.ttf"
F_SANS = FONT_DIR + "NotoSans-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, f, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_lines(d, lines, x, y, f, fill, leading):
    for ln in lines:
        d.text((x, y), ln, font=f, fill=fill)
        y += leading
    return y


def kicker(d, x, y, text, color):
    f = font(F_SANS_BOLD, 18)
    d.text((x, y), text, font=f, fill=color)
    return y + 26


def headline(d, x, y, text, size, max_w, max_lines=3):
    f = font(F_SERIF_BOLD, size)
    lines = wrap(d, text, f, max_w)[:max_lines]
    return draw_lines(d, lines, x, y, f, INK, int(size * 1.12))


def summary(d, x, y, text, size, max_w, max_lines=3):
    f = font(F_SANS, size)
    lines = wrap(d, text, f, max_w)[:max_lines]
    return draw_lines(d, lines, x, y, f, MUTED, int(size * 1.32))


def card(d, x, y, w, h, accent):
    d.rounded_rectangle([x, y, x + w, y + h], radius=4, fill=CARD,
                        outline=INK, width=2)
    d.rectangle([x + 2, y + 2, x + w - 2, y + 10], fill=accent)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead -------------------------------------------------------
    title_f = font(F_SERIF_BLACK, 88)
    title = "THE WORLD TODAY"
    tw = d.textlength(title, font=title_f)
    d.text(((W - tw) / 2, 12), title, font=title_f, fill=INK)
    d.line([(28, 118), (W - 28, 118)], fill=RULE, width=3)
    d.line([(28, 124), (W - 28, 124)], fill=RULE, width=1)

    date_f = font(F_SANS_BOLD, 28)
    date = "THURSDAY  ·  19 NOVEMBER 2026"
    dw = d.textlength(date, font=date_f)
    d.text(((W - dw) / 2, 134), date, font=date_f, fill=RED)
    d.line([(28, 172), (W - 28, 172)], fill=RULE, width=3)

    # ---- Lead story: Shenzhen trilateral -------------------------------
    x, y, w, h = 28, 186, W - 56, 200
    card(d, x, y, w, h, RED)
    ix = x + 22
    iy = y + 20
    iy = kicker(d, ix, iy, "SHENZHEN  ·  APEC SUMMIT", RED)
    iy = headline(d, ix, iy + 2, "Trump, Xi and Putin meet in Shenzhen",
                  42, w - 44, max_lines=2)
    summary(d, ix, iy + 6,
            "The first-ever trilateral summit of the US, China and Russia, "
            "with Ukraine, Iran, nuclear arms and trade on the table. "
            "Officials say no deal is expected to be announced.",
            20, w - 44, max_lines=2)

    # ---- Two-column grid: four stories ----------------------------------
    gx, gy = 28, 398
    cw = (W - 56 - 16) // 2
    ch = 180
    gap = 12

    stories = [
        ("THE HAGUE  ·  WORLD COURT", RED,
         "Court rules on Rohingya genocide",
         "The ICJ delivers its final verdict today in The Gambia's case "
         "against Myanmar — the first time it could hold a state "
         "responsible for genocide."),
        ("WASHINGTON  ·  CONGRESS", BLUE,
         "Jeffries set to be first Black Speaker",
         "Democrats nominate Hakeem Jeffries to lead the House after "
         "their midterm win, a first for a Black American."),
        ("THE GULF  ·  CONFLICT", RED,
         "US and Iran trade fire across the Gulf",
         "Iran widens its attacks to Kuwait and Bahrain after US "
         "strikes on Qeshm Island; oil prices fall as tensions rise."),
        ("INDIA  ·  WEATHER", TEAL,
         "Cyclone Akvan bears down on India's east coast",
         "The storm is expected to cross between Machilipatnam and "
         "Puri, with heavy rain and high winds forecast."),
    ]
    for i, (kick, color, head, summ) in enumerate(stories):
        cx = gx + (i % 2) * (cw + 16)
        cy = gy + (i // 2) * (ch + gap)
        card(d, cx, cy, cw, ch, color)
        ix = cx + 18
        iy = cy + 18
        iy = kicker(d, ix, iy, kick, color)
        iy = headline(d, ix, iy + 2, head, 27, cw - 36, max_lines=2)
        summary(d, ix, iy + 4, summ, 18, cw - 36, max_lines=3)

    # ---- Wide strip: GTA VI ---------------------------------------------
    sy, sh = 782, 84
    card(d, 28, sy, W - 56, sh, BLUE)
    ix = 28 + 22
    iy = sy + 16
    iy = kicker(d, ix, iy, "CULTURE  ·  GAMING", BLUE)
    d.text((ix, iy + 2), "Grand Theft Auto VI rolls out worldwide",
           font=font(F_SERIF_BOLD, 28), fill=INK)

    # ---- Also today strip ------------------------------------------------
    ay = 878
    d.line([(28, ay), (W - 28, ay)], fill=RULE, width=2)
    af = font(F_SANS_BOLD, 17)
    d.text((28, ay + 8), "ALSO TODAY", font=af, fill=INK)
    d.line([(28, ay + 32), (W - 28, ay + 32)], fill=RULE, width=1)

    also = [
        ("Crimean Bridge hit again",
         "Russia says the bridge to Crimea was attacked overnight."),
        ("Van Gogh sells for $190.4m",
         "A record price at auction, after a row over its Nazi-era past."),
        ("Voyager 1, one light-day out",
         "NASA's 49-year-old probe passes a new distance milestone."),
    ]
    col_w = (W - 56) // 3
    iy0 = ay + 42
    for i, (head, summ) in enumerate(also):
        cx = 28 + i * col_w
        iy = iy0
        hf = font(F_SERIF_BOLD, 20)
        lines = wrap(d, head, hf, col_w - 24)
        iy = draw_lines(d, lines, cx, iy, hf, INK, 24)
        summary(d, cx, iy + 2, summ, 15, col_w - 24, max_lines=2)
        if i:
            d.line([(cx - 10, iy0), (cx - 10, iy0 + 62)],
                   fill=(200, 192, 175), width=1)

    # ---- Footer ----------------------------------------------------------
    d.line([(28, 994), (W - 28, 994)], fill=RULE, width=1)
    ff = font(F_SANS, 13)
    foot = "Compiled from wire reports  ·  The World Today  ·  19 November 2026"
    fw = d.textlength(foot, font=ff)
    d.text(((W - fw) / 2, 1000), foot, font=ff, fill=MUTED)

    img.save("entry.png", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    main()
