# The World Today — Friday, 20 November 2026

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/Kyamii21/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/Kyamii21/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

One 1024×1024 image summing up the world news of Friday, 20 November 2026,
built for the make.fun bounty `news-image-20261120`.

## What is in the picture

- **Lead story — Shenzhen:** Donald Trump, Xi Jinping and Vladimir Putin
  release a four-point "peace declaration" after their first-ever three-way
  summit, reaffirming that nuclear war must never be fought — while making
  no mention of the wars in Ukraine or Iran.
- **India — Cyclone Akvan:** the severe cyclonic storm makes landfall on the
  Odisha coast today; about 300,000 people have been evacuated.
- **World Court — ICJ:** Myanmar is found guilty of genocide against the
  Rohingya, the first time the court has held a state responsible for genocide.
- **Iran war:** Trump says he is in "no rush" to decide next steps, pushing
  any decision into 2027.
- **Ukraine war:** European leaders in Berlin say they are ready for talks
  with Russia on ending the war.
- **GTA 6 launch:** an estimated $1.84 billion and 19 million copies on day
  one (Sensor Tower estimate, not an official figure).
- The masthead also marks **World Children's Day**, the UN observance held
  every 20 November.

Design: one dominant lead panel with a globe and the three flags, then five
large cards with big headlines, simple icons and key numbers. No text is
smaller than 28 px, so every headline stays legible at 300 px wide
(see `preview-300.png`).

## Run it

```sh
python3 main.py
```

`main.py` (Python standard library only) validates `entry.png` — PNG magic
bytes, a 1024×1024 IHDR, and the 1 MiB size cap — then copies it to
`$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output`), verifies the copy
byte-for-byte, and prints its sha256. Running it twice writes identical
bytes. `draw.py` regenerates `entry.png` and `preview-300.png` from scratch
with Pillow.

## License

MIT — see `LICENSE`.
