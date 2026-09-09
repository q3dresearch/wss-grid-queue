#!/usr/bin/env python3
"""Render charts from derived/observations/*.csv as SVG.

    python3 examples/visualize.py

Every chart here answers a numbered question from `docs/research-questions.md`
and says which. A chart that answers no question does not belong in the repo.

Three rules the fleet learned the hard way:

  * **Axes start at zero and step by 1, 2 or 5 times a power of ten.** The step
    matters more than the ceiling: allowing a 2.5 multiplier once produced
    `0 / 2 / 5 / 7 / 10 / 12`, which is round-looking and unreadable.
  * **Name the entities.** A count sends the reader back to look up who.
  * **Every SVG is XML-parsed before it is written.** A renderer that reports
    success having emitted invalid markup is not hypothetical; it shipped once.

Note the grain. The Approved workbook is one row per FACILITY: 3,211 rows carry
1,497 distinct projects, and `Current Cost` differs across a project's
facilities. Counts here say which grain they are in, every time.
"""
from __future__ import annotations

import csv
import datetime
import math
from collections import defaultdict
from pathlib import Path
from xml.etree import ElementTree
from xml.sax.saxutils import escape

REPO = Path(__file__).resolve().parents[1]
OUT_DIR = REPO / "examples" / "charts"
OBS_DIR = REPO / "derived" / "observations"
TODAY = datetime.date(2026, 9, 9)

SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK2 = "#52514e"
MUTED = "#898781"
GRID = "#e1e0d9"
BASELINE = "#c3c2b7"
SLOTS = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4"]
FONT = "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"


# ── primitives ──────────────────────────────────────────────────────────────

def txt(x, y, s, *, size, fill, anchor="start", weight="normal", tab=False):
    style = "font-variant-numeric: tabular-nums;" if tab else ""
    # The attribute must be DOUBLE-quoted: FONT contains 'Segoe UI', and a
    # single-quoted attribute ends at that apostrophe, producing markup that
    # some renderers accept and an XML parser does not.
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FONT}" '
            f'font-size="{size}" fill="{fill}" text-anchor="{anchor}" '
            f'font-weight="{weight}" style="{style}">{escape(s)}</text>')


def para(x, y, text, *, size, fill, chars, leading=17.0):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = f"{cur} {w}".strip()
        if len(trial) > chars and cur:
            lines.append(cur); cur = w
        else:
            cur = trial
    if cur:
        lines.append(cur)
    return ([txt(x, y + i * leading, ln, size=size, fill=fill)
             for i, ln in enumerate(lines)], len(lines) * leading)


def nice_axis(value, allowed=(3, 4, 5, 6)):
    """(ceiling, ticks) — the tightest axis whose ticks are all round numbers.

    Steps are 1, 2 or 5 times a power of ten and nothing else. Never 2.5: it
    produces a fractional step and an axis that reads as noise.
    """
    if value <= 0:
        return 1.0, 4
    best = None
    for steps in allowed:
        rough = value / steps
        mag = 10 ** math.floor(math.log10(rough))
        for mult in (1, 2, 5, 10):
            top = mult * mag * steps
            if top >= value:
                if best is None or top < best[0]:
                    best = (top, steps)
                break
    return best


def bar(x, y, w, h, colour, r=4):
    r = min(r, max(w / 2, 0.1), h / 2)
    return (f'<path d="M{x:.1f},{y:.1f} h{w - r:.1f} q{r},0 {r},{r} '
            f'v{h - 2 * r:.1f} q0,{r} -{r},{r} h-{w - r:.1f} z" fill="{colour}"/>')


def wrap(w, h, title, desc, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}" role="img" aria-label="{escape(title)}">\n'
            f"<title>{escape(title)}</title>\n<desc>{escape(desc)}</desc>\n"
            f'<rect width="{w}" height="{h}" fill="{SURFACE}"/>\n{body}\n</svg>\n')


def header(title, subtitle, *, chars=118, y=38):
    """Title + wrapped subtitle. Returns (elements, y of the first free line).

    The plot top must come from this, not from a constant. `already-late` was
    laid out with a hardcoded top that fitted a one-line subtitle; the real one
    ran to two lines and printed straight through the axis labels. SVG has no
    text flow, so nothing complains -- it just renders on top of itself.
    """
    els = [txt(40, y, title, size=19, fill=INK, weight="600")]
    lines, h = para(40, y + 24, subtitle, size=12.5, fill=INK2, chars=chars)
    return els + lines, y + 24 + h


def write(name: str, svg: str) -> None:
    """Parse before writing. An invalid SVG that reports success is worse than
    a crash, because it reaches a README before anyone looks."""
    ElementTree.fromstring(svg)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / name).write_text(svg)
    print(f"  wrote examples/charts/{name}")


# ── data ────────────────────────────────────────────────────────────────────

def load():
    """(source, entity) -> {metric: value}. One capture per month per entity."""
    rows = []
    for f in sorted(OBS_DIR.glob("*.csv")):
        rows += list(csv.DictReader(f.open()))
    by = defaultdict(dict)
    for r in rows:
        by[(r["source_id"], r["entity_id"])][r["metric"]] = r["value"]
    return by


def money(v: float) -> str:
    return f"${v/1e9:.1f}B" if v >= 1e9 else f"${v/1e6:.0f}M"


# ── Q2: how much of the approved pipeline is already late? ──────────────────

def chart_already_late(by):
    live = {e: v for (s, e), v in by.items()
            if s == "miso.mtep.approved"
            and v.get("planning_status", "").startswith(("M2", "M3"))}
    late = {e: v for e, v in live.items()
            if v.get("expected_isd")
            and datetime.date.fromisoformat(v["expected_isd"]) < TODAY}
    buckets = [(0, 1, "under 1 year"), (1, 2, "1–2 years"),
               (2, 3, "2–3 years"), (3, 99, "over 3 years")]
    counts, caps = [], []
    for lo, hi, _ in buckets:
        sel = [v for v in late.values()
               if lo <= (TODAY - datetime.date.fromisoformat(v["expected_isd"])).days / 365.25 < hi]
        counts.append(len(sel))
        caps.append(sum(float(v["current_cost"]) for v in sel if v.get("current_cost")))

    W, L = 860, 150
    plot_w, row_h = W - L - 190, 52
    top, ticks = nice_axis(max(counts))
    body, after = header(
        "The approved pipeline is already behind",
        f"{len({v.get('project_id', e) for e, v in late.items()})} of "
        f"{len({v.get('project_id', e) for e, v in live.items()})} live MISO projects "
        f"({len(late)} of {len(live)} facilities) are past the in-service date MISO itself "
        f"publishes, carrying {money(sum(caps))}. MISO does not publish what those dates "
        f"used to be — only the current one.")
    T = after + 54          # room for the axis title and the tick row
    H = T + row_h * len(buckets) + 78

    for i in range(ticks + 1):
        x = L + plot_w * i / ticks
        body.append(f'<line x1="{x:.1f}" y1="{T-8}" x2="{x:.1f}" '
                    f'y2="{T + row_h*len(buckets):.1f}" stroke="{GRID}" stroke-width="1"/>')
        body.append(txt(x, T - 16, f"{int(top*i/ticks):,}", size=10.5, fill=MUTED, anchor="middle", tab=True))
    body.append(txt(L + plot_w / 2, T - 34, "facilities past their published in-service date",
                    size=11, fill=INK2, anchor="middle"))

    for i, ((_, _, label), n, cap) in enumerate(zip(buckets, counts, caps)):
        y = T + i * row_h
        body.append(txt(L - 14, y + 26, label, size=12.5, fill=INK, anchor="end"))
        w = plot_w * n / top if top else 0
        body.append(bar(L, y + 8, max(w, 2), 30, SLOTS[min(i, 1)] if i < 2 else SLOTS[1]))
        # A gap of spaces collapses in SVG; the separator has to be a glyph.
        body.append(txt(L + max(w, 2) + 10, y + 28, f"{n:,}  ·  {money(cap)}",
                        size=12, fill=INK2, tab=True))
    body.append(f'<line x1="{L}" y1="{T-8}" x2="{L}" y2="{T + row_h*len(buckets):.1f}" '
                f'stroke="{BASELINE}" stroke-width="1.5"/>')
    foot, _ = para(40, H - 50, (
        "Q2 in docs/research-questions.md. Answerable from a single capture — which is why it "
        "is recorded as answered, not as a reason to build an archive. Grain: the Approved "
        "workbook is one row per facility."), size=11, fill=MUTED, chars=132)
    body += foot
    return wrap(W, H, "The approved pipeline is already behind",
                "MISO Appendix A projects past their published in-service date, by how late.",
                "\n".join(body))


# ── Q5: the negative result — duration is already archived ──────────────────

def chart_duration_archived(by):
    def cyc(v):
        s = str(v or "")
        return 2000 + int(s[4:6]) if s.startswith("MTEP") and s[4:6].isdigit() else None

    yrs = []
    for (s, _e), v in by.items():
        if s != "miso.mtep.in-service":
            continue
        c, isd = cyc(v.get("target_cycle")), v.get("expected_isd")
        if c and isd:
            d = datetime.date.fromisoformat(isd).year - c
            if -1 <= d <= 20:
                yrs.append(d)
    hist = defaultdict(int)
    for d in yrs:
        hist[min(d, 10)] += 1
    xs = sorted(hist)

    W, H, L, T = 860, 400, 70, 112
    plot_w, plot_h = W - L - 40, 190
    top, ticks = nice_axis(max(hist.values()))
    body = [txt(40, 38, "MISO already publishes how long a project takes", size=19, fill=INK, weight="600")]
    lines, _ = para(40, 62, (
        f"{len(yrs):,} delivered projects, measured from the MTEP cycle that proposed them to the "
        f"in-service date. Median {sorted(yrs)[len(yrs)//2]} year(s). Because `Target MTEP Cycle` "
        f"survives beside the delivered date, this needs no archive — so it is the one question "
        f"this repo does NOT exist to answer."), size=12.5, fill=INK2, chars=118)
    body += lines

    for i in range(ticks + 1):
        y = T + plot_h - plot_h * i / ticks
        body.append(f'<line x1="{L}" y1="{y:.1f}" x2="{L+plot_w}" y2="{y:.1f}" '
                    f'stroke="{GRID}" stroke-width="1"/>')
        body.append(txt(L - 10, y + 4, f"{int(top*i/ticks):,}", size=10.5,
                        fill=MUTED, anchor="end", tab=True))
    bw = plot_w / len(xs)
    for i, x in enumerate(xs):
        h = plot_h * hist[x] / top
        body.append(bar(L + i * bw + bw * 0.16, T + plot_h - h, bw * 0.68, max(h, 2), SLOTS[2]))
        label = "10+" if x == 10 else str(x)
        body.append(txt(L + i * bw + bw / 2, T + plot_h + 18, label, size=11,
                        fill=INK2, anchor="middle", tab=True))
    body.append(f'<line x1="{L}" y1="{T+plot_h:.1f}" x2="{L+plot_w}" y2="{T+plot_h:.1f}" '
                f'stroke="{BASELINE}" stroke-width="1.5"/>')
    body.append(txt(L + plot_w / 2, T + plot_h + 40, "years from proposal cycle to in-service",
                    size=11.5, fill=INK2, anchor="middle"))
    foot, _ = para(40, H - 40, (
        "Q5. Recorded as an answered negative result: the obvious pitch for this repo was already "
        "archived by the publisher, and capturing it would have added nothing."),
        size=11, fill=MUTED, chars=132)
    body += foot
    return wrap(W, H, "MISO already publishes how long a project takes",
                "Histogram of years from MTEP proposal cycle to in-service, 5,182 delivered projects.",
                "\n".join(body))


# ── the state machine, and what each stage is worth ─────────────────────────

def chart_pipeline(by):
    stages = [("miso.mtep.under-evaluation", "Under evaluation", "M1/M2"),
              ("miso.mtep.approved", "Appendix A approved", "M2/M3"),
              ("miso.mtep.in-service", "Delivered", "M4")]
    rows = []
    for src, label, _ in stages:
        ent = {e: v for (s, e), v in by.items() if s == src}
        proj = len({v.get("project_id", e) for e, v in ent.items()})
        cap = sum(float(v["current_cost"]) for v in ent.values() if v.get("current_cost"))
        rows.append((label, proj, cap))

    W, L = 860, 210
    plot_w, row_h = W - L - 170, 62
    top, ticks = nice_axis(max(c for _, _, c in rows) / 1e9)
    undelivered = sum(c for lab, _, c in rows if lab != "Delivered")
    body, after = header(
        f"{money(undelivered)} is carried at a cost that overwrites its own history",
        "MISO publishes `Current Cost`. There is no original-cost column anywhere, and the "
        "workbooks sit at fixed URLs that are overwritten in place — so what a project was "
        "approved at is unrecoverable from MISO's own record.")
    T = after + 40
    H = T + row_h * len(rows) + 78

    for i in range(ticks + 1):
        x = L + plot_w * i / ticks
        body.append(f'<line x1="{x:.1f}" y1="{T-8}" x2="{x:.1f}" '
                    f'y2="{T + row_h*len(rows):.1f}" stroke="{GRID}" stroke-width="1"/>')
        body.append(txt(x, T - 16, f"${int(top*i/ticks)}B", size=10.5, fill=MUTED,
                        anchor="middle", tab=True))
    for i, (label, proj, cap) in enumerate(rows):
        y = T + i * row_h
        body.append(txt(L - 14, y + 30, label, size=13, fill=INK, anchor="end"))
        w = plot_w * (cap / 1e9) / top if top else 0
        body.append(bar(L, y + 10, max(w, 2), 36, SLOTS[i]))
        body.append(txt(L + max(w, 2) + 10, y + 33, f"{money(cap)}  ·  {proj:,} projects",
                        size=12, fill=INK2, tab=True))
    body.append(f'<line x1="{L}" y1="{T-8}" x2="{L}" y2="{T + row_h*len(rows):.1f}" '
                f'stroke="{BASELINE}" stroke-width="1.5"/>')
    foot, _ = para(40, H - 50, (
        "Q1, the founding question. Only repeated capture can say what these figures were "
        "before today. Counts are distinct MTEP Project IDs; the Approved workbook's 1,497 "
        "projects arrive as 3,211 facility rows."), size=11, fill=MUTED, chars=132)
    body += foot
    return wrap(W, H, "Capital carried at a cost that overwrites its own history",
                "MISO MTEP pipeline by stage: capital and distinct project count.",
                "\n".join(body))


def main():
    by = load()
    if not by:
        raise SystemExit("no observations — run `wss derive` first")
    write("pipeline-capital.svg", chart_pipeline(by))
    write("already-late.svg", chart_already_late(by))
    write("duration-is-archived.svg", chart_duration_archived(by))


if __name__ == "__main__":
    main()
