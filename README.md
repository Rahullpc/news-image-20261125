# news-image-20261125

![news-image-20261125](https://make.fun/badge/news-image-20261125.svg)
![rank](https://make.fun/badge/news-image-20261125/Rahullpc/news-image-20261125/rank.svg)
![reward](https://make.fun/badge/news-image-20261125/Rahullpc/news-image-20261125/reward.svg)

Bounty: [news-image-20261125](https://make.fun/bounty/news-image-20261125)

## What this is

A one-page newspaper poster — **THE WORLD, Wednesday 25 November 2026** —
that sums up the day's world news in a single 1024 x 1024 image. The lead
story is the tanker fires in the Strait of Hormuz and the Houthi strike on
Saudi Arabia's Ras Tanura refinery. Six more stories cover Trump's new
tariffs on 14 trading partners, Huawei's conviction on 10 of 12 counts,
Pakistan's first astronaut reaching China's Tiangong station, the Cairo Ring
Road tanker fire, the Australia–Solomon Islands security treaty, and the
RSF drone strikes in Sudan. A bottom strip adds the US economy, Brazil's
fiscal package and the Bogor mine flood.

Every illustration on the poster is drawn in code — no photographs, no
downloads, no network. See [RESEARCH.md](RESEARCH.md) for the facts and
their sources, and [BUILD.md](BUILD.md) for the layout plan.

## How it works

- `draw_poster.py` draws `entry.png` from scratch with Pillow.
- `main.py` (stdlib only) copies `entry.png` to the output directory
  (`MAKEFUN_OUTPUT_DIR`, or `/output` by default), checks it is at most
  1 MiB, and verifies the copy's sha256 matches the source.

```bash
python3 draw_poster.py
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## Verification

- `entry.png` is 1024 x 1024 and at most 1048576 bytes.
- Running `main.py` twice produces byte-identical output (same sha256).
- The poster was read as an image and checked by eye: no clipped text,
  no typos, no doubled words, and the date reads "Wednesday 25 November 2026".

## License

MIT — see [LICENSE](LICENSE).
