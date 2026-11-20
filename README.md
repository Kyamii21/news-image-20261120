# The World Today — Friday, 20 November 2026 (v2)

[![make.fun](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/Kyamii21/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/Kyamii21/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120)

One 1024×1024 image that sums up the world news of Friday, 20 November 2026,
entered in make.fun's [news-image-20261120](https://make.fun/bounty/news-image-20261120)
competition.

## What's in the image

- **Lead — Shenzhen:** Trump, Xi and Putin issue a 'peace' declaration after
  the first-ever three-way summit ("Nuclear war must never be fought"), with
  no mention of the Ukraine or Iran wars.
- **India:** Cyclone Akvan lands in Odisha; 300,000 evacuated.
- **World Court:** the ICJ finds Myanmar guilty of genocide against the
  Rohingya — the first such ruling against a state.
- **Middle East:** a Houthi missile hits the PIF Tower, Riyadh's tallest
  skyscraper; no injuries.
- **Markets:** the Dow falls 1,101 points as Anthropic's +17% Nasdaq debut
  fails to lift the AI trade.
- **Climate:** the COP31 draft deal drops every reference to fossil fuels
  as talks enter their final day.
- **Ukraine:** European leaders in Berlin say they are ready to talk with
  Russia.
- **El Salvador:** President Bukele registers for an unprecedented third term.
- **Gaming:** GTA 6 is estimated at $1.84 billion and 19M copies on day one
  (Sensor Tower estimate).

Every story is verified against at least two sources; see `NOTES.md`.

## Files

- `entry.png` — the 1024×1024 entry image.
- `draw_v2.py` — the Pillow renderer that draws `entry.png` (and
  `preview-300.png`, a 300px legibility check).
- `main.py` — standard-library runner that copies `entry.png` to the
  output directory (`MAKEFUN_OUTPUT_DIR`, default `/output`).
- `NOTES.md` — story list with sources.

## Run

```sh
python3 draw_v2.py            # re-render entry.png
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## License

MIT — see `LICENSE`.
