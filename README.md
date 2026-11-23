# Global Briefing — 23 November 2026 in One Image

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/hiduplahzomb/news-image-20261123-ka-resubmit/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard)
[![reward](https://make.fun/badge/news-image-20261123/hiduplahzomb/news-image-20261123-ka-resubmit/reward.svg)](https://make.fun/bounty/news-image-20261123)

A high-density situation-room dashboard that sums up the world's news of
Monday 23 November 2026 in a single 1024×1024 image: 8 verified stories
(1 lead + 3 major + 4 minor), each with a Subject + Action + Metric
headline and three concrete facts.

## Stories

| # | Story | Metric |
|---|-------|--------|
| 1 | COP31 collapses in Antalya — 200 nations, no deal | 0 DEAL |
| 2 | Russian strikes kill 11 in the Kyiv region | 11 KILLED |
| 3 | Ukraine sinks Russian frigate Merkury off Libya | 1 FRIGATE SUNK |
| 4 | Democrats clinch 258 House seats | 258 SEATS |
| 5 | South Korea exports top $1 trillion, first time ever | $1T |
| 6 | Taiwan stocks swing 1,666 points intraday | +2.16% |
| 7 | Indonesia candy factory fire kills 24 | 24 DEAD |
| 8 | Trump: strike Iran if no deal by New Year | JAN 1 |

Every fact was verified against wire reporting (AP, Reuters, Xinhua,
Al Jazeera) — see [SOURCES.md](SOURCES.md). No invented numbers, names,
or quotes.

## How it is built

`draw_dashboard.py` (Python 3 + Pillow) renders `entry.png` — a strict
grid, sans-serif type (Liberation Sans), black on white with a single red
accent, minimum 13px type for tags and 15px+ for body text. `main.py`
(the entrypoint) simply copies the pre-rendered image to the grader's
output directory, so the run is fully deterministic.

```sh
python3 draw_dashboard.py   # renders entry.png (1024x1024)
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## License

MIT — see [LICENSE](LICENSE).
