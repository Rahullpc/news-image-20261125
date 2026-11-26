# BUILD — news-image-20261125

## The poster in one sentence

A one-page English broadsheet, "THE WORLD", dated Wednesday 25 November 2026,
that sums up the day's world news with one big lead story, six illustrated
stories and a three-item "ALSO TODAY" strip.

## Layout plan (figure first)

The page is a 1024 x 1024 grid. Every zone has one job; nothing overlaps.

```
+----------------------------------------------------------+
| 28px margin                                              |
|  THE WORLD                      (masthead, serif, ~88px) |
|  No. 330  |  WEDNESDAY 25 NOVEMBER 2026  |  WORLD EDITION|
+----------------------------------------------------------+
| LEAD STORY — MIDDLE EAST                                 |
| +------------------+  TANKERS ABLAZE IN HORMUZ          |
| | tanker illustration|  AS WAR SPREADS TO SAUDI OIL      |
| | (sea, 2 tankers,  |  HEARTLAND                         |
| |  flames, refinery)|  4-5 lines of summary text         |
| +------------------+  (Ras Tanura, Riyadh tower, 11     |
|                        injured)                          |
+----------------------------------------------------------+
|  G1 TARIFFS      |  G2 HUAWEI                            |
|  [small art]     |  [small art]                          |
|  headline + 3 lines headline + 3 lines                  |
+------------------+---------------------------------------+
|  G3 SPACE        |  G4 CAIRO FIRE                        |
+------------------+---------------------------------------+
|  G5 SOLOMONS     |  G6 SUDAN                             |
+----------------------------------------------------------+
| ALSO TODAY:  US economy hot  |  Brazil fiscal  |  Bogor  |
|              PCE 3.8%, GDP 4.3%  cap 2%       mine, 9 dead|
+----------------------------------------------------------+
| Sources: Reuters · AP · CNN · Xinhua · Just Security     |
| THE WORLD — Wednesday 25 November 2026 · All stories     |
| reported on 25 November 2026.                           |
+----------------------------------------------------------+
```

Key point: the date is named twice (dateline under the masthead and in the
footer), the lead takes the top third, and the six grid stories cover trade,
tech, space, disaster, diplomacy and conflict — three continents and six
fields, so no single country or beat dominates.

## Design decisions

- **Paper look:** warm off-white paper (#F7F2E7), near-black ink, one red
  accent (#A41E22) for kickers and rules, one deep blue (#1F3A5F) for
  secondary accents. Classic newspaper, not a poster gradient.
- **Type:** DejaVu Serif Bold for masthead and headlines (newspaper voice),
  DejaVu Sans for body and labels. All fonts are system fonts, so the build
  needs no network and no downloads.
- **Hierarchy (motion-design staging):** the masthead is the hero, the lead
  story is the primary layer, the 2x3 grid is the secondary layer, and the
  small drawn details inside each illustration (waves, birds, stars, smoke,
  containers, flags) are the ambient layer that makes the page feel alive
  instead of empty.
- **Density:** every story gets its own small illustration drawn in code
  (tankers and flames, cargo containers, a courthouse, a rocket and station,
  a tipped tanker truck, two flags, a drone over rooftops). Rich, busy,
  specific — never a bare headline on white space.
- **Legibility at ~300 px:** headlines 20-26 px bold, body 15-16 px, kickers
  12-13 px tracked. No text smaller than 12 px. All text is wrapped by
  measuring with the real font, never by guessing character counts.

## Facts used (from RESEARCH.md)

- Lead: two tankers hit naval mines in the Strait of Hormuz, engine-room
  fires (IRGC Navy statement via IRNA, reported by Reuters); Houthis say
  they hit Ras Tanura, Saudi Arabia's largest refinery; 11 injured in the
  Riyadh tower strike the day before. No tanker names, no flags, no crew
  figures were published, and no third-tanker claim is used.
- G1 tariffs: Trump administration proposes new tariffs on 14 partners after
  an eight-month Section 301 probe; proposed maximum rates 20-40%, trade
  deals generally capping them at 10-20%.
- G2 Huawei: Brooklyn jury convicts on 10 of 12 counts (bank and wire fraud,
  sanctions violations, trade-secret conspiracy); acquitted of racketeering;
  sentencing set for 14 September 2027.
- G3 space: Shenzhou-24 launches 08:18 Beijing time, docks with Tiangong
  about 3.5 hours later; Muhammad Zeeshan Ali is the first Pakistani in
  orbit and the first foreign astronaut to visit Tiangong.
- G4 Cairo: fuel tanker overturns and burns on the Ring Road, Al-Warraq,
  Giza; 31 dead, 21 injured; fire spreads to 27 vehicles.
- G5 Solomons: Australia and Solomon Islands sign a treaty in Canberra
  making Australia the primary security partner, precluding any foreign
  military or security base on Solomon Islands soil.
- G6 Sudan: RSF drone strikes kill 19 civilians and wound 20 in Damazin
  and Roseires, Blue Nile state.
- Also today: US October PCE inflation 3.8% y/y (core 3.3%), Q3 GDP revised
  to 4.3% annualised; Brazil's lower house approves a fiscal package capping
  spending growth at 2%; Bogor gold-mine flood, 9 dead, 17 believed trapped.
- Deliberately NOT used: any Brent oil price (sources conflict), the
  third-tanker claim, tanker names, and the Dow 50,000 claim (single source).

## Implementation

- `draw_poster.py` — draws the poster from scratch with Pillow. Pure
  stdlib + PIL, no network, no downloaded assets, no timestamps, so two
  runs produce byte-identical PNGs. Run: `python3 draw_poster.py`
  (writes `entry.png` next to the script).
- `main.py` — the entrypoint. Stdlib only: copies `entry.png` from the
  repository folder to the output directory (`MAKEFUN_OUTPUT_DIR` if set,
  else `/output`), checks the copy is at most 1 MiB, and verifies the
  copy's sha256 matches the source.
- `entry.png` — the rendered poster, 1024 x 1024, at most 1 MiB.

## Verification

1. Run `python3 draw_poster.py`, check `entry.png` is 1024 x 1024 and
   at most 1048576 bytes.
2. Run `main.py` twice into a scratch output directory and compare the
   sha256 of both copies — they must match exactly.
3. Read the PNG as an image and check every headline and line of body text
   for clipping, typos and doubled words, and confirm the date reads
   "Wednesday 25 November 2026".
