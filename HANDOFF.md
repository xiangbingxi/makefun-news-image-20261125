# HANDOFF — news-image-20261125

## Competition

- Bounty: make.fun news image, 25 November 2026 edition ("THE WORLD IN ONE DAY").
- Competition page: https://make.fun/bounty/news-image-20261125 ($100).
- Deadline: 08:00 Beijing time, 27 November 2026.
- Deliverable: one 1024×1024 RGB PNG (≤ 1 MiB), produced by `main.py`
  copying the pre-rendered `entry.png`. No submission has been made from
  this repo; no GitHub repo or bundle was created here.

## What I did (render worker only)

- Wrote `tools/gen_image.py` by hand (PIL, DejaVu fonts), following the
  24 Nov page's layout: header, 3 big headlines, 10 small cards, world map
  with 13 numbered pins, region bars, 23 one-line briefs, red DATE CHECK box.
- Reused the 24 Nov `tools/mapdata.json` (Natural Earth 50m coastline +
  borders, pre-projected to map pixel space) as the map data file.
- Wrote `main.py` (pure standard library copy shim with PNG validation),
  `README.md`, `LICENSE` (MIT, SPDX line), `prompt.txt` (user's words),
  `.makefun/owner.json`, and this file, each by hand.
- Ran the renderer, inspected the finished image at full size and at 2x
  zoom (headlines, small cards, Middle East pin cluster, briefs), and
  fixed what I found (see change log).

## What's in the image

- Header: "THE WORLD IN ONE DAY", "WEDNESDAY, 25 NOVEMBER 2026 · 36 STORIES, ONE DAY".
- 3 big headlines with hand-drawn illustrations: Hormuz tankers (two
  burning tankers between cliffs + mine), Shenzhou-24 docking (space
  station above Earth, Pakistani + Chinese flags on the capsule),
  Cartagena supermarket (storefront + police cordon + helicopter +
  officers leading hostages out).
- 10 small story cards (4–13), each with a small hand-drawn illustration.
- Map "WHERE IT HAPPENED" with 13 numbered red pins, equirectangular
  projection (lon −180…180, lat 75…−55). Pins 1 and 27 share the Hormuz
  coordinates (26N 56E): both markers sit on the same spot, labels offset
  in opposite directions (1 left, 27 below-right).
- 23 numbered briefs (14–36), one line each: bold title + body.
- Red DATE CHECK box: "DATE CHECK · ALL 36 STORIES ARE 25 NOV 2026".
- Region bars: Europe 5, North America 7, Asia 7, Middle East 6, Africa 5,
  South America 3, Global 3 (total 36).
- Footer: hand-drawn / no-photos note, source line, follow-up labelling
  note (Tuesday: 10, 11, 19, 20, 23, 24, 34).

## Verification (all passed)

- `entry.png`: 1024×1024, RGB, 219,389 bytes (≤ 1,048,576), PIL verifies OK.
- sha256: `a1ac337de7502ad3cac1b203d03a2265724800f58b0d62e78147c4ed4bd014b4`
- `main.py` run twice with different `MAKEFUN_OUTPUT_DIR` values
  (`/tmp/out1`, `/tmp/out2`): identical sha256 both times, byte-identical
  to the rendered `entry.png`.
- Counts: 3 + 10 + 23 = 36 stories; region bars total 36; 13 pins.
- All 13 pins pass the land/coastline-pixel ring check run by
  `tools/gen_image.py` on every run (disc counts: 1: 578, 2: 797, 3: 448,
  4: 703, 6: 634, 8: 748, 9: 419, 10: 477, 12: 214, 14: 667, 22: 742,
  27: 578, 33: 480).
- Visual check: title date correct; all 36 stories present; pin numbers
  match story numbers (verified at 2x zoom on the Middle East cluster);
  no garbled or overlapping text; every small-card body ends with a
  complete sentence.

## Change log (fixes made after looking at the rendered image)

1. First render: most body text came out almost invisible — the `d.text`
   calls had no `fill` argument. Added `fill=INK` to every headline,
   small-card, map-header, region-panel and brief text call.
2. Shenzhou illustration: the Earth ellipse spilled outside its box and
   covered headline 1's title (drawn later in the loop). Clamped the
   ellipse horizontally to the box and erased the spill below the box.
3. Small cards 5, 8, 9, 10, 11: two-line titles left only one body line,
   which truncated the body mid-sentence. Shortened those titles to one
   line and hand-shortened the bodies so each ends cleanly in two lines
   (e.g. 10 is now "10 TUESDAY: HUAWEI GUILTY", 11 is "11 TUESDAY:
   SENEGAL WINS").
4. Card 9 again: "9 AUSTRALIA-SOLOMONS TREATY" still wrapped to two
   lines, so the body was cut to "Solomons named Australia its."
   Shortened the title to "9 SOLOMONS TREATY" and the body to fit two
   lines exactly.

## v2 (user review fixes, 2026-11-26)

The user reviewed v1 and asked for two fixes; both are done here.

1. **Date box vs Tuesday labels.** The red box said "ALL 36 STORIES ARE
   25 NOV 2026" while items 10, 11, 19, 20, 23, 24, 34 are labelled
   TUESDAY. The box now reads "DATE CHECK · 25 NOV NEWS & FOLLOW-UPS".
   Each Tuesday item's body now states its 25 Nov development, taken
   from NEWS.md (no new facts invented): 10 Huawei will appeal and
   Beijing accused Washington; 11 Morocco vowed legal action after the
   CAS ruling; 19 Homeland Security said Abrego Garcia self-deported;
   20 the Justice Department had abandoned its lawsuit over the Alaska
   race; 23 the S&P 500 fell 0.5% alongside the Nasdaq; 24 Chen Jining
   is the fourth top leader probed since 2025; 34 police clashed with
   wage protesters as the debt framework went to restructuring talks.
   NEWS.md's intro now matches the new box wording.
2. **Pins 1 and 27 shared a dot.** Both were (26N 56E). They now carry
   one-decimal coordinates — pin 1 Strait of Hormuz 26.6N 56.3E, pin 27
   Ras Al Khaimah 25.8N 55.9E — and their markers are offset from the
   true spot with a thin red leader line back to it (pin 1 up-left,
   pin 27 down-right), so the two are visibly separate dots. Pin 1's
   label sits directly above its marker; pin 27's label sits to its
   right. NEWS.md's pin table carries the precise coordinates. The
   pin land/coastline ring check still passes 13/13 (disc counts:
   1: 599, 27: 587).

## Verification (v2, all passed)

- `entry.png`: 1024×1024, RGB, 220,051 bytes (≤ 1,048,576), PIL verifies OK.
- sha256: `2c1a3a5fab75ba8fabd03152f240d870a28f62613e625ad51c38f23bb396d5ec`
- `main.py` run twice: identical sha256 both times, byte-identical to
  the rendered `entry.png` (see below).
- Counts: 3 + 10 + 23 = 36 stories; region bars total 36; 13 pins.
- Visual check at full size and 5x zoom on the Gulf cluster: date box
  reads "25 NOV NEWS & FOLLOW-UPS"; pins 1 and 27 are two separate
  markers with leader lines and legible labels; all 36 stories present;
  pin numbers match story numbers; no garbled or overlapping text.
