"""Draw the 19 November 2026 world-news front page.

One deterministic PIL poster, 1024x1024, no network, no clock, no
randomness: the same run always writes the same bytes. The program is
run by main.py only to copy the finished entry.png; everything visual
lives here.

Sources for every story were checked against live reporting of
Thursday 19 November 2026 (AP, Reuters, UKMTO, ICJ, CENTCOM, IMD,
IAEA, White House, Treasury/OFAC). Items that broke on Wednesday
18 November are not presented as Thursday news: they are named in the
DATE CHECK box instead. Items scheduled later on Thursday (the ICJ
verdict at 09:00 UTC, the trilateral at 06:30 UTC, Anthropic's first
trade at 14:30 UTC) are framed as due today, with the time given.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 26
CW = W - 2 * MARGIN  # 972 usable

PAPER = (246, 239, 220)
INK = (22, 33, 62)
INK_SOFT = (74, 82, 104)
RED = (168, 35, 42)
BLUE = (36, 86, 166)
TEAL = (15, 118, 110)
GOLD = (176, 124, 16)
NAVY = (18, 30, 58)
SKY = (174, 214, 235)
SEA = (46, 111, 160)
SAND = (226, 205, 158)
RULE = (22, 33, 62)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def text_w(draw, s, f):
    return draw.textlength(s, font=f)


def wrap(draw, s, f, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    words = s.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if text_w(draw, trial, f) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_wrap(draw, s, f, max_w, max_lines, min_size):
    """Wrap text, shrinking the font until it fits max_lines lines.

    Returns (lines, font). Guarantees no overflow: at min_size the
    caller still gets wrapped lines, and the block is drawn clipped
    to max_lines.
    """
    size = f.size
    while size > min_size:
        lines = wrap(draw, s, font(f.path, size), max_w)
        if len(lines) <= max_lines:
            return lines, font(f.path, size)
        size -= 1
    lines = wrap(draw, s, font(f.path, min_size), max_w)
    return lines[:max_lines], font(f.path, min_size)


def draw_lines(draw, lines, f, x, y, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=f, fill=fill)
        y += leading
    return y


def hline(draw, y, x0, x1, fill=INK, width=1):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


# ---------------------------------------------------------------- stories
# (number, kicker, region, headline, standfirst, source)

LEADS = [
    (1, "SHENZHEN", "ASIA",
     "THREE PRESIDENTS, ONE TABLE",
     "Trump, Xi and Putin meet in Shenzhen today - the first "
     "trilateral of the three nuclear powers, on nuclear arms, "
     "Iran and Ukraine. No breakthrough is expected.",
     "AP / REUTERS"),
    (2, "WALL ST", "AMERICAS",
     "ANTHROPIC'S $83 RECORD DEBUT",
     "Priced above the $70-78 range: $81.3bn raised, a $1.5tn "
     "valuation - the biggest IPO ever. First trade today as ANT "
     "on the Nasdaq.",
     "REUTERS / AP"),
    (3, "GAMING", "GLOBAL",
     "GTA VI IS OUT - 13 YEARS ON",
     "Vice City returns as Rockstar's sequel launches worldwide "
     "today. Metacritic 99, $1.54bn in pre-orders, 8 Game Awards "
     "nominations already.",
     "POLYGON / CNN"),
]

CARDS = [
    (4, "THE HAGUE", "GLOBAL",
     "ICJ TO RULE ON ROHINGYA GENOCIDE",
     "At 09:00 UTC the World Court decides whether Myanmar "
     "committed genocide - a first-ever state verdict.",
     "ICJ / REUTERS"),
    (5, "HORMUZ", "MIDDLE EAST",
     "TANKER HIT OFF KHASAB",
     "UKMTO: a projectile strikes an oil tanker's engine room "
     "6 miles north of Oman. Crew safe, no one blamed yet.",
     "UKMTO"),
    (6, "HORMUZ", "MIDDLE EAST",
     "IRAN CLAIMS 3 MORE TANKERS HIT MINES (CLAIM)",
     "Tehran says three tankers caught fire on mines east of "
     "Hormuz. No ship named; Reuters could not confirm it.",
     "IRIB / AL JAZEERA"),
    (7, "KERCH", "EUROPE",
     "KERCH BRIDGE SHUT AGAIN",
     "Aksyonov halts traffic after another attack; damage is "
     "being assessed. The fourth closure in days.",
     "AP"),
    (8, "ISRAEL", "MIDDLE EAST",
     "HERZOG TAPS EISENKOT TO GOVERN",
     "Israel's president asks the ex-army chief to form the next "
     "government, bypassing Netanyahu.",
     "AP"),
    (9, "AKVAN", "ASIA",
     "CYCLONE AKVAN BEARS DOWN ON ODISHA",
     "Landfall due Fri 20 Nov; ~50,000 moved to safety and "
     "schools shut as the storm nears the coast.",
     "IMD / AP"),
    (10, "MANILA", "ASIA",
     "US-PHILIPPINES IN $2BN+ LOAN PUSH",
     "The White House says the allies will pursue a financing "
     "package over $2bn through military aid channels.",
     "WHITE HOUSE"),
    (11, "TOKYO", "ASIA",
     "INDIA-JAPAN 2+2 IN TOKYO",
     "Defence and foreign ministers meet for the 2+2 dialogue "
     "as both sides deepen security ties.",
     "MEA"),
    (12, "PYONGYANG", "ASIA",
     "NORTH KOREA ENRICHMENT GROWS",
     "The IAEA reports an expansion of uranium-enrichment "
     "facilities, raising fresh nuclear-security fears.",
     "IAEA"),
    (13, "WASHINGTON", "AMERICAS",
     "US SANCTIONS HEZBOLLAH NETWORK",
     "Treasury adds three entities and three people to its "
     "sanctions list over alleged Hezbollah funding.",
     "TREASURY / OFAC"),
]

ALSO = [
    "GAZA AID: 4 NATIONS DEMAND ACCESS AS FLOODS HIT",
    "US DETAILS $12BN VENEZUELA OIL REVENUE",
    "YEMEN COALITION: MISSILE THREAT TOWARD RIYADH",
    "SAUDI: DANGER PASSED IN 3 SOUTHERN CITIES",
    "PANAMA: 2ND ARREST IN JOURNALIST ATTACK CASE",
    "CANADA SANCTIONS ISRAELI SETTLERS OVER WEST BANK",
    "FRANCE: 4TH WEEKEND OF COST-OF-LIVING PROTESTS",
    "MELENCHON COULD WIN PRESIDENCY, MINISTER SAYS",
    "CANADA ADJUSTS CHINA TIES, CARNEY SEEKS US DEAL",
    "NGO: ISRAEL LIMITS CARE FOR 1,100 CHILD AMPUTEES",
    "ETHIOPIA-ERITREA: CLASH REPORTS NEAR BADME, DENIED",
    "BANGLADESH: ARSON AMID HASINA-RETURN TALK",
    "DELHI SCHOOLS REOPEN AS GRAP-III CURBS LIFTED",
    "INDIA VS NZ: FIRST TEST BEGINS IN WELLINGTON",
    "SINDHU BACK TO WORLD TOP FIVE IN BADMINTON",
    "US SENATORS WARN AI CYBER THREATS OUTPACE DEFENCES",
    "RUSSIAN MILITARY PLANE CRASH IN SIBERIA KILLS 19",
    "PEW: ISLAM SET TO BE WORLD'S LARGEST FAITH BY 2035",
    "AMAZON PLEDGES $7BN FOR RENEWABLES IN INDIA BY 2030",
    "NATURE: EARTH'S 'MISSING BILLION YEARS' EXPLAINED",
    "PALO ALTO +9% AFTER HOURS ON EARNINGS",
    "COCAINE, MILLIONS OF PILLS SEIZED IN EASTERN LIBYA",
    "SENSEX, NIFTY SLIP AS IT DRAGS; FED SIGNALS WEIGH",
    "S&P FUTURES +0.6%, NASDAQ-100 +0.9% ON ANT",
    "GOLD ~$3,742; BITCOIN ~$62.3K; WTI ~$82.3",
    "LISBOA GAMES WEEK OPENS ON GTA VI LAUNCH DAY",
    "INDIA IMPOSES 162.5% DUTY ON BULK SCOTCH IMPORTS",
    "GOLDMAN SACHS UPGRADES INDIA TO OVERWEIGHT",
    "RELIANCE EXPANDS SATELLITE CAPACITY VS STARLINK",
]

REGION_BAND = ("AMERICAS 6  •  EUROPE 5  •  ASIA 14  •  MIDDLE EAST 8  •  "
               "AFRICA 2  •  GLOBAL 6  •  OCEANIA 1")
TIMELINE = ("TIMELINE  •  00:49 UTC TANKER HIT  •  02:06 UTC KERCH SHUT  •  "
            "04:45 UTC XI-TRUMP  •  06:30 UTC TRILATERAL  •  09:00 UTC "
            "ICJ RULING  •  14:30 UTC ANT TRADE")
MARKETS = ("MARKETS (WED CLOSE)  S&P 500 7,323.63 -0.23%  •  DOW 50,198.17 "
           "-1.11%  •  NASDAQ 24,429.88 +0.42%  •  BRENT $91.48 -1.8%  •  "
           "10-YR 5.06%")
NUMBERS = ("BY THE NUMBERS   •   $81.3bn Anthropic raise   •   $1.5tn "
           "valuation   •   99 GTA VI Metacritic   •   $1.54bn pre-orders   "
           "•   ~50,000 moved ahead of Akvan   •   $2bn+ loan push")
FOOTER = ("THE WORLD IN ONE DAY  •  THURSDAY 19 NOVEMBER 2026  •  SOURCES: "
          "AP, REUTERS, UKMTO, ICJ, CENTCOM, IMD, IAEA, WHITE HOUSE, OFAC")

DATE_CHECK = [
    ("LEFT OUT - BROKE WED 18 NOV:",
     "Fed minutes • Voyager 1 light-day • Jeffries speaker nod • "
     "Anthropic priced $83 • GTA VI reviews 99 • Nvidia results • "
     "Ebola CDC update • COP31 draft • EU EUR 45bn loan • UK inflation"),
    ("ALSO EARLIER:",
     "Qeshm strike (17 Nov) • Peltola • Measles • Waymo • An-12 • "
     "Sudan 2,230 • Dhoni • Kandinsky $85.8m • Hathaway • Van Gogh $180m"),
    ("NOT YET:",
     "ICJ verdict outcome • Summit joint statement • Anthropic "
     "first-trade price • Akvan landfall (Fri 20 Nov) • GTA VI US rollout"),
]

# Dot-matrix world map: 72 columns x 15 rows, '#' is land.
MAP_ROWS = [
    "........#########.....................#########################........",
    "...##################...###............############################...",
    "...#################......######......##############################.",
    "....###############.........#######...##############################.",
    ".....#############............######..############################...",
    "......###########..............####...##########################.....",
    ".......#######.................####...######################.......",
    "..........#####...........#########....##################...........",
    "............###...........########......###########.................",
    "................#######..#######........#########................#.",
    ".................#######..#####..........########...................",
    "..................######...###..........#######.....................",
    "...................####..................##...................##....",
    "....................##.............................................",
    "....................................................................",
]

# (pin number, map column, map row)
PINS = [
    (1, 54, 5), (2, 14, 4), (4, 33, 3), (5, 44, 7),
    (7, 38, 4), (8, 46, 6), (10, 58, 8), (12, 64, 4),
]


# ------------------------------------------------------------- illustrations
# Every scene is drawn from fixed coordinates only: no clock, no
# randomness, so repeated runs are byte-identical.

def illo_apec(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    d.ellipse([x + 18, y + 6, x + 66, y + 20], fill=(255, 255, 255))
    d.ellipse([x + w - 70, y + 12, x + w - 20, y + 24], fill=(255, 255, 255))
    d.rectangle([x, y + int(h * 0.72), x + w, y + h], fill=(52, 58, 68))
    for wx in range(4, w, 30):
        d.line([(x + wx, y + int(h * 0.85)), (x + wx + 16, y + int(h * 0.85))],
               fill=(255, 255, 255), width=3)
    d.ellipse([x + int(w * 0.30), y + int(h * 0.34), x + int(w * 0.74), y + int(h * 0.58)],
              fill=(255, 255, 255))
    d.polygon([(x + int(w * 0.44), y + int(h * 0.40)), (x + int(w * 0.58), y + int(h * 0.62)),
               (x + int(w * 0.40), y + int(h * 0.62))], fill=(210, 220, 230))
    d.polygon([(x + int(w * 0.70), y + int(h * 0.30)), (x + int(w * 0.76), y + int(h * 0.52)),
               (x + int(w * 0.68), y + int(h * 0.52))], fill=(210, 220, 230))
    d.rectangle([x + int(w * 0.10), y + int(h * 0.30), x + int(w * 0.13), y + int(h * 0.72)],
                fill=(120, 90, 60))
    d.polygon([(x + int(w * 0.13), y + int(h * 0.30)), (x + int(w * 0.30), y + int(h * 0.38)),
               (x + int(w * 0.13), y + int(h * 0.46))], fill=RED)


def illo_anthropic(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=NAVY)
    cx = x + int(w * 0.30)
    d.polygon([(cx, y + 6), (cx - 7, y + 20), (cx + 7, y + 20)], fill=RED)
    d.rectangle([cx - 7, y + 20, cx + 7, y + 38], fill=(255, 255, 255))
    d.polygon([(cx - 7, y + 38), (cx, y + 46), (cx - 2, y + 36)], fill=(240, 196, 64))
    d.line([(x + int(w * 0.55), y + h - 8), (x + int(w * 0.68), y + int(h * 0.55)),
            (x + int(w * 0.78), y + int(h * 0.68)), (x + w - 8, y + 10)],
           fill=(120, 220, 120), width=3)
    d.polygon([(x + w - 16, y + 8), (x + w - 6, y + 8), (x + w - 8, y + 18)],
              fill=(120, 220, 120))


def illo_gta(d, x, y, w, h):
    # Neon Vice City skyline at dusk, palm silhouette, big VI.
    d.rectangle([x, y, x + w, y + h], fill=(24, 8, 48))
    d.ellipse([x + w - 40, y + 6, x + w - 12, y + 34], fill=(255, 120, 180))
    for i, (bx, bw, bh) in enumerate(((6, 26, 30), (36, 18, 44), (58, 24, 26),
                                      (86, 16, 38), (106, 30, 20))):
        d.rectangle([x + bx, y + h - bh, x + bx + bw, y + h], fill=(52, 24, 88))
        for wy in range(y + h - bh + 4, y + h - 4, 8):
            d.rectangle([x + bx + 4, wy, x + bx + 8, wy + 3], fill=(255, 220, 90))
    d.line([(x + 8, y + h - 2), (x + w - 8, y + h - 2)], fill=(255, 120, 180), width=2)
    d.text((x + int(w * 0.62), y + 2), "VI", font=font(SERIF_B, 26),
           fill=(255, 220, 90))
    # palm
    px, py = x + int(w * 0.86), y + int(h * 0.55)
    d.line([(px, py), (px + 4, py + 14)], fill=(20, 120, 60), width=3)
    for dx, dy in ((-12, -8), (-6, -12), (4, -13), (12, -9), (14, -2)):
        d.line([(px + 2, py), (px + dx, py + dy)], fill=(30, 160, 70), width=2)


def illo_icj(d, x, y, w, h):
    # Peace Palace columns and scales of justice.
    d.rectangle([x, y, x + w, y + h], fill=(226, 232, 240))
    cx = x + w // 2
    d.polygon([(cx - 34, y + 4), (cx + 34, y + 4), (cx, y + 16)], fill=(120, 130, 150))
    for i in range(3):
        px = cx - 24 + i * 24
        d.rectangle([px - 4, y + 18, px + 4, y + h - 10], fill=(120, 130, 150))
    d.rectangle([x + 8, y + h - 10, x + w - 8, y + h - 6], fill=(120, 130, 150))
    # scales, small, at right
    sx, sy = x + w - 26, y + 8
    d.line([(sx, sy), (sx, sy + 14)], fill=INK, width=2)
    d.line([(sx - 8, sy + 2), (sx + 8, sy + 2)], fill=INK, width=2)
    d.pieslice([sx - 11, sy + 10, sx - 3, sy + 16], 0, 180, fill=GOLD)
    d.pieslice([sx + 3, sy + 10, sx + 11, sy + 16], 0, 180, fill=GOLD)


def illo_tanker(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    d.rectangle([x, y + int(h * 0.62), x + w, y + h], fill=SEA)
    d.ellipse([x + 8, y + 6, x + 30, y + 28], fill=(240, 196, 64))
    # hull + superstructure
    d.polygon([(x + 10, y + int(h * 0.55)), (x + w - 10, y + int(h * 0.55)),
               (x + w - 22, y + int(h * 0.78)), (x + 22, y + int(h * 0.78))],
              fill=(120, 30, 30))
    d.rectangle([x + int(w * 0.62), y + int(h * 0.34), x + int(w * 0.80), y + int(h * 0.55)],
                fill=(240, 240, 240))
    # smoke from the engine-room hit
    for i, (ox, oy, r) in enumerate(((int(w * 0.22), int(h * 0.30), 6),
                                     (int(w * 0.28), int(h * 0.20), 8),
                                     (int(w * 0.36), int(h * 0.12), 9))):
        d.ellipse([x + ox - r, y + oy - r, x + ox + r, y + oy + r], fill=(90, 90, 90))
    d.polygon([(x + int(w * 0.20), y + int(h * 0.44)), (x + int(w * 0.26), y + int(h * 0.34)),
               (x + int(w * 0.30), y + int(h * 0.46))], fill=(255, 140, 0))


def illo_mines(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(20, 40, 70))
    for wx in range(0, w, 24):
        yy = y + int(h * 0.55) + (wx % 3) * 2
        d.arc([x + wx, yy, x + wx + 20, yy + 8], 0, 180, fill=(120, 180, 220), width=2)
    for ox, oy, r in ((int(w * 0.30), int(h * 0.45), 9), (int(w * 0.65), int(h * 0.60), 8),
                      (int(w * 0.80), int(h * 0.30), 6)):
        cx, cy = x + ox, y + oy
        import math
        for k in range(8):
            a = k * math.pi / 4
            d.line([(cx + int(r * 0.9 * math.cos(a)), cy + int(r * 0.9 * math.sin(a))),
                    (cx + int((r + 4) * math.cos(a)), cy + int((r + 4) * math.sin(a)))],
                   fill=(200, 200, 200), width=2)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(60, 60, 60),
                  outline=(200, 200, 200), width=2)
    d.ellipse([x + 8, y + 6, x + 26, y + 24], fill=(240, 196, 64))


def illo_kerch(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    d.rectangle([x, y + int(h * 0.66), x + w, y + h], fill=SEA)
    d.ellipse([x + w - 34, y + 6, x + w - 12, y + 28], fill=(240, 196, 64))
    d.line([(x + 6, y + int(h * 0.52)), (x + w - 6, y + int(h * 0.52))],
           fill=(70, 74, 82), width=4)
    for px in (int(w * 0.25), int(w * 0.55), int(w * 0.82)):
        d.line([(x + px, y + int(h * 0.52)), (x + px, y + int(h * 0.66))],
               fill=(70, 74, 82), width=3)
    d.arc([x + int(w * 0.30), y + int(h * 0.18), x + int(w * 0.70), y + int(h * 0.52)],
          180, 360, fill=(70, 74, 82), width=3)
    d.ellipse([x + int(w * 0.58), y + int(h * 0.30), x + int(w * 0.68), y + int(h * 0.42)],
              fill=(150, 150, 150))
    d.ellipse([x + int(w * 0.64), y + int(h * 0.22), x + int(w * 0.74), y + int(h * 0.34)],
              fill=(170, 170, 170))


def illo_eisenkot(d, x, y, w, h):
    # Knesset-style dome and columns.
    d.rectangle([x, y, x + w, y + h], fill=(214, 226, 240))
    cx = x + w // 2
    d.pieslice([cx - 22, y + 2, cx + 22, y + 30], 180, 360, fill=(120, 130, 150))
    d.rectangle([cx - 26, y + 16, cx + 26, y + 22], fill=(120, 130, 150))
    for i in range(4):
        px = cx - 27 + i * 18
        d.rectangle([px, y + 22, px + 8, y + h - 8], fill=(120, 130, 150))
    d.rectangle([x + 8, y + h - 8, x + w - 8, y + h - 4], fill=(120, 130, 150))
    d.rectangle([x + 6, y + 6, x + 26, y + 16], fill=BLUE)
    d.text((x + 8, y + 7), "66", font=font(SANS_B, 9), fill=(255, 255, 255))


def illo_akvan(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(174, 214, 235))
    cx, cy = x + w // 2, y + h // 2
    for r in (6, 12, 18):
        d.arc([cx - r, cy - r, cx + r, cy + r], 20, 300, fill=(255, 255, 255), width=3)
    for i in range(6):
        rx = x + 8 + i * 12
        d.line([(rx, y + h - 12), (rx + 5, y + h - 4)], fill=SEA, width=2)


def illo_ph(d, x, y, w, h):
    # Two flags on poles + handshake band.
    d.rectangle([x, y, x + w, y + h], fill=(226, 232, 240))
    d.rectangle([x + 8, y + 6, x + 44, y + 22], fill=(0, 56, 168))
    d.rectangle([x + 8, y + 22, x + 44, y + 38], fill=(206, 17, 38))
    d.polygon([(x + 8, y + 6), (x + 24, y + 22), (x + 8, y + 38)], fill=(255, 255, 255))
    d.rectangle([x + w - 44, y + 6, x + w - 8, y + 38], fill=(255, 255, 255))
    for i, col in enumerate(((191, 10, 48), (255, 255, 255), (0, 56, 168))):
        d.rectangle([x + w - 44, y + 6 + i * 11, x + w - 8, y + 17 + i * 11], fill=col)
    d.rectangle([x, y + h - 10, x + w, y + h - 6], fill=GOLD)
    d.text((x + int(w * 0.42), y + h - 22), "$2bn+", font=font(SANS_B, 11), fill=INK)


def illo_indiajapan(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(226, 232, 240))
    # India saffron/white/green + wheel
    d.rectangle([x + 8, y + 6, x + 52, y + 16], fill=(255, 153, 51))
    d.rectangle([x + 8, y + 16, x + 52, y + 26], fill=(255, 255, 255))
    d.rectangle([x + 8, y + 26, x + 52, y + 36], fill=(19, 136, 8))
    d.ellipse([x + 26, y + 16, x + 34, y + 26], outline=NAVY, width=1)
    # Japan red disc
    d.ellipse([x + w - 40, y + 8, x + w - 16, y + 32], fill=(188, 0, 45))
    d.rectangle([x, y + h - 10, x + w, y + h - 6], fill=NAVY)
    d.text((x + int(w * 0.36), y + h - 22), "2+2", font=font(SANS_B, 11), fill=INK)


def illo_nk(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(30, 30, 46))
    cx, cy = x + w // 2, y + h // 2
    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(240, 196, 64))
    for ang in (0, 60, 120):
        import math
        a = math.radians(ang)
        rx, ry = int(20 * math.cos(a)), int(8 * math.sin(a))
        d.ellipse([cx - 20, cy - 8, cx + 20, cy + 8], outline=(120, 180, 255), width=2)
        # rotate by drawing three ellipses is not possible; use arcs
        d.arc([cx - 20, cy - 8, cx + 20, cy + 8], ang, ang + 180, fill=(120, 180, 255), width=2)
    d.text((x + 6, y + 4), "U-235", font=font(SANS_B, 9), fill=(255, 255, 255))


def illo_ofac(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(240, 236, 222))
    d.rectangle([x + 10, y + 6, x + w - 10, y + h - 6], outline=INK, width=1)
    for i in range(3):
        d.line([(x + 16, y + 14 + i * 7), (x + w - 26, y + 14 + i * 7)],
               fill=INK_SOFT, width=2)
    d.ellipse([x + 10, y + h - 24, x + 34, y + h - 4], outline=RED, width=2)
    d.text((x + 17, y + h - 19), "X", font=font(SANS_B, 12), fill=RED)


ILLOS = {1: illo_apec, 2: illo_anthropic, 3: illo_gta, 4: illo_icj,
         5: illo_tanker, 6: illo_mines, 7: illo_kerch, 8: illo_eisenkot,
         9: illo_akvan, 10: illo_ph, 11: illo_indiajapan, 12: illo_nk,
         13: illo_ofac}


def draw_dot_map(d, x, y, cell=8):
    """Stylised dot-matrix world map; returns (width, height)."""
    rows = MAP_ROWS[:14]
    for ri, row in enumerate(rows):
        for ci, ch in enumerate(row):
            if ch == "#":
                px, py = x + ci * cell, y + ri * cell
                d.ellipse([px, py, px + 5, py + 5], fill=(36, 86, 166))
    for num, col, row in PINS:
        px = x + col * cell + 2
        py = y + row * cell + 2
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED,
                  outline=(255, 255, 255), width=2)
        f = font(SANS_B, 11)
        tw = d.textlength(str(num), font=f)
        d.text((px - tw / 2, py - 8), str(num), font=f, fill=(255, 255, 255))
    return 72 * cell, 14 * cell


# ------------------------------------------------------------------- layout

def centered(draw, y, s, f, fill, x0=MARGIN, x1=W - MARGIN):
    tw = draw.textlength(s, font=f)
    draw.text(((x0 + x1 - tw) / 2, y), s, font=f, fill=fill)
    return tw


def draw_masthead(d, y):
    centered(d, y, "THE WORLD IN ONE DAY", font(SERIF_B, 42), INK)
    centered(d, y + 52, "THURSDAY 19 NOVEMBER 2026", font(SERIF_B, 21), RED)
    centered(d, y + 82, "42 STORIES  •  SEVEN REGIONS  •  ONE PAGE",
             font(SANS_B, 13), INK)
    centered(d, y + 100,
             "Everything on this page happened, or was first reported, "
             "on Thursday 19 November 2026.",
             font(SANS, 11), INK_SOFT)
    hline(d, y + 118, MARGIN, W - MARGIN, INK, 2)
    hline(d, y + 122, MARGIN, W - MARGIN, INK, 1)
    return y + 128


def draw_band(d, y, s, fill, text_fill):
    size = 11
    while size > 9 and d.textlength(s, font=font(SANS_B, size)) > CW:
        size -= 1
    d.rectangle([MARGIN, y, W - MARGIN, y + 18], fill=fill)
    centered(d, y + 2, s, font(SANS_B, size), text_fill)
    return y + 18


def draw_lead(d, x, y, w, story):
    num, kicker, region, head, sub, src = story
    d.text((x, y), "%d  •  %s  •  %s" % (num, kicker, region),
           font=font(SANS_B, 11), fill=RED)
    lines, hf = fit_wrap(d, head, font(SERIF_B, 20), w, 3, 16)
    y = draw_lines(d, lines, hf, x, y + 16, INK, hf.size + 4)
    lines, sf = fit_wrap(d, sub, font(SANS, 11), w, 3, 9)
    y = draw_lines(d, lines, sf, x, y + 3, INK_SOFT, sf.size + 3)
    return y


def draw_lead_illo(d, x, y, w, h, story):
    num = story[0]
    ILLOS[num](d, x, y, w, h)
    src = story[5]
    f = font(SANS_B, 8)
    tw = d.textlength(src, font=f)
    d.rectangle([x + w - tw - 6, y + h - 13, x + w - 1, y + h - 1], fill=INK)
    d.text((x + w - tw - 3, y + h - 12), src, font=f, fill=(255, 255, 255))


def draw_card(d, x, y, w, story):
    num, kicker, region, head, sub, src = story
    d.text((x, y), "%d  •  %s  •  %s" % (num, kicker, region),
           font=font(SANS_B, 10), fill=RED)
    lines, hf = fit_wrap(d, head, font(SERIF_B, 15), w, 2, 11)
    y = draw_lines(d, lines, hf, x, y + 14, INK, hf.size + 3)
    lines, sf = fit_wrap(d, sub, font(SANS, 10), w, 2, 9)
    y = draw_lines(d, lines, sf, x, y + 2, INK_SOFT, sf.size + 3)
    return y


def draw_card_illo(d, x, y, w, h, story):
    num = story[0]
    ILLOS[num](d, x, y, w, h)
    src = story[5]
    f = font(SANS_B, 8)
    tw = d.textlength(src, font=f)
    d.rectangle([x + w - tw - 6, y + h - 13, x + w - 1, y + h - 1], fill=INK)
    d.text((x + w - tw - 3, y + h - 12), src, font=f, fill=(255, 255, 255))


def draw_date_check(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], outline=RED, width=2)
    d.text((x + 10, y + 6), "DATE CHECK", font=font(SANS_B, 12), fill=RED)
    yy = y + 24
    for label, body in DATE_CHECK:
        d.text((x + 10, yy), label, font=font(SANS_B, 10), fill=RED)
        yy += 12
        lines = wrap(d, body, font(SANS, 9), w - 20)
        for line in lines[:2]:
            d.text((x + 10, yy), line, font=font(SANS, 9), fill=INK)
            yy += 11
        yy += 2
    return y + h


def draw_also(d, y):
    d.text((MARGIN, y), "ALSO ON THURSDAY 19 NOVEMBER",
           font=font(SANS_B, 12), fill=RED)
    legend = ("HOW SURE:  CONFIRMED = on the record   •   CLAIM = one "
              "side's account, not independently verified")
    f = font(SANS, 9)
    tw = d.textlength(legend, font=f)
    d.text((W - MARGIN - tw, y + 1), legend, font=f, fill=INK_SOFT)
    col_w = 314
    starts = [14, 24, 34]
    counts = [10, 10, 9]
    for ci, (start, count) in enumerate(zip(starts, counts)):
        cx = MARGIN + ci * (col_w + 15)
        yy = y + 16
        for i, item in enumerate(ALSO[start - 14:start - 14 + count]):
            n = start + i
            num_s = "%d " % n
            nf = font(SANS_B, 9)
            tf = font(SANS_B, 9)
            while d.textlength(num_s + item, font=tf) > col_w and tf.size > 8:
                tf = font(SANS_B, tf.size - 1)
            d.text((cx, yy), num_s, font=nf, fill=RED)
            d.text((cx + d.textlength(num_s, font=nf), yy), item, font=tf, fill=INK)
            yy += 11
    return y + 16 + 10 * 11


def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    y = draw_masthead(d, 12)
    centered(d, y, REGION_BAND, font(SANS_B, 11), INK)
    y += 18
    y = draw_band(d, y, TIMELINE, NAVY, (255, 255, 255))
    lead_y = y + 8
    lead_w = 314
    lead_xs = [MARGIN, MARGIN + lead_w + 15, MARGIN + 2 * (lead_w + 15)]
    illo_y = lead_y + 124
    for x, story in zip(lead_xs, LEADS):
        draw_lead(d, x, lead_y, lead_w, story)
        draw_lead_illo(d, x, illo_y, lead_w, 48, story)
    y = illo_y + 48 + 8
    card_w = 234
    card_xs = [MARGIN + i * (card_w + 12) for i in range(4)]
    # 10 cards: rows of 4, 4, 2
    rows = (CARDS[:4], CARDS[4:8], CARDS[8:])
    for row, stories in enumerate(rows):
        ry = y + row * 112
        for x, story in zip(card_xs, stories):
            draw_card(d, x, ry, card_w, story)
            draw_card_illo(d, x, ry + 80, card_w, 30, story)
    y = y + 3 * 112 + 8
    d.text((MARGIN, y), "WHERE IT HAPPENED", font=font(SANS_B, 12), fill=RED)
    draw_dot_map(d, MARGIN, y + 16, cell=7)
    draw_date_check(d, MARGIN + 600 + 14, y, 358, 132)
    y = y + 136
    y = draw_also(d, y)
    y = draw_band(d, y + 6, MARKETS, NAVY, (255, 255, 255))
    centered(d, y + 4, NUMBERS, font(SANS, 11), INK)
    centered(d, y + 20, FOOTER, font(SANS, 9), INK_SOFT)
    print("layout: footer baseline y =", y + 20)
    return img


def main():
    import hashlib
    import os
    img = render()
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, format="PNG")
    data = open(out, "rb").read()
    print("wrote", out, len(data), "bytes")
    print("sha256", hashlib.sha256(data).hexdigest())


if __name__ == "__main__":
    main()
