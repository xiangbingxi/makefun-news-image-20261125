# THE WORLD IN ONE DAY — Wednesday, 25 November 2026

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/xiangbingxi/makefun-news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/xiangbingxi/makefun-news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

Built for make.fun's ["Sum up 25 November's world news in one image" bounty](https://make.fun/bounty/news-image-20261125), $100 in USDC.

A single 1024×1024 hand-drawn flat-vector newspaper page covering 36 verified
news stories from one day: 3 big headlines, 10 illustrated small stories,
a world map with 13 numbered pins, and 23 numbered briefs (14–36).

## Files

- `entry.png` — the finished page (1024×1024, RGB, PNG, ≤ 1 MiB)
- `main.py` — entry point. Pure standard library. It only copies `entry.png`
  to `$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output`) after validating the
  PNG magic bytes, the 1 MiB size limit, every chunk CRC through IEND, and
  the 1024×1024 RGB header. It never renders anything.
- `tools/gen_image.py` — the development renderer (PIL, hand-written). Run it
  to rebuild `entry.png`: `python3 tools/gen_image.py`. It also runs the
  land-pixel ring check for all 13 pins.
- `tools/mapdata.json` — Natural Earth 50m coastline + border data,
  pre-projected to the map's pixel space (reused from the 24 Nov page).
- `NEWS.md` — all 36 stories in full, with sources, region counts and pins.
- `HANDOFF.md` — competition info, what is on the page, and the change log.
- `prompt.txt` — the user's original request, one line.
- `LICENSE` — MIT.

## What's on the page

- Top stories: 1 Iran says two tankers hit mines in the Strait of Hormuz,
  2 Shenzhou-24 docks with the first foreign astronaut aboard Tiangong,
  3 Colombia frees all Cartagena hostages.
- Small stories 4–13: Houthis hit Ras Tanura, Ukraine hits two refineries,
  Israel kills a Hamas security chief, Asian tech stocks tumble, Sudan drone
  strikes kill 19, Solomons treaty with Australia, Tuesday: Huawei convicted,
  Tuesday: Senegal champions, Indonesia mine toll rises, Trump plans new tariffs.
- Map "WHERE IT HAPPENED": 13 pins — Strait of Hormuz, Jiuquan, Cartagena,
  Ras Tanura, Gaza City, Damazin, Canberra, New York, Bogor, Odesa,
  Middletown (Iowa), Ras Al Khaimah, Buenos Aires. Pins 1 and 27 sit close
  together in the Gulf but have their own precise coordinates (1: 26.6N
  56.3E, 27: 25.8N 55.9E); each marker is offset from its true spot and
  joined to it by a thin red leader line, so the two pins read as separate.
- Briefs 14–36, one line each, with follow-ups labelled in the item itself:
  Tuesday (10, 11, 19, 20, 23, 24, 34).
- Red DATE CHECK box: 25 NOV NEWS & FOLLOW-UPS.
- Regions: Europe 5, North America 7, Asia 7, Middle East 6, Africa 5,
  South America 3, Global 3 — total 36.

## Notes

- Map drawn from public coastline data (Natural Earth 50m); all other
  illustrations are hand-drawn flat-vector art made with PIL. No
  photographs and no wire-service images are used.
- All figures are as reported on 25 Nov 2026, not later updates.
- Fonts: local DejaVu (DejaVuSans, DejaVuSans-Bold).
  The judging machine has no font library, so `main.py` never renders —
  it only copies the pre-rendered `entry.png`.
