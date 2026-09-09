"""miso.schedule26.v1 — the ratepayer end of the transmission pipe.

Schedule 26 and 26-A are MISO's *indicative* annual transmission charges: what
each pricing zone is told it will pay, projected five to six years out. They are
the other half of the MTEP story — MTEP says what the grid costs to build,
Schedule 26 says who is billed for it.

**These are projections, and only the current one is published.** Today's
estimate of 2027 charges overwrites last year's estimate of 2027, at a fixed
URL, so the revision history exists nowhere. That is the whole reason to capture
them.

The workbooks carry a `Variance` sheet, but the caption never says variance
*from what* — it names the project categories and stops. It is emitted as
`variance_<year>` without interpretation. Successive captures settle what the
baseline is; guessing would put a number in a chart that nobody can defend.

Grain: one entity per pricing zone, one metric per projected year, so
`charge_2027` on zone `ATC` is a series that moves as MISO re-projects it.
MVP projects from 26-A are a second entity type, keyed by project id, which is
what joins this source to the MTEP workbooks.
"""

from wss import derive

from ._xlsx import Workbook, excel_date

PARSER_VERSION = "1"

ZONE_SHEETS = {
    "Projected Sch 26 Annual Charges": "charge",
    "Projected Sch 26 Variance": "variance",
    "Projected 12 CP Demand": "demand",
}
MVP_SHEET = "Sch 26-A Projections_2011MVP"


def _year_table(rows):
    """Find the header row of years and yield (label, {year: value}).

    The sheets differ in how many preamble rows they carry — one has the legal
    disclaimer on row 2, another on rows 2 and 3 — so the header is located by
    looking for a row of four-digit years rather than by counting down.
    """
    hdr_i, years = None, {}
    for i, row in enumerate(rows[:12]):
        found = {j: int(str(c)) for j, c in enumerate(row)
                 if c is not None and str(c).strip().isdigit()
                 and 2000 <= int(str(c).strip()) <= 2100}
        if len(found) >= 3:
            hdr_i, years = i, found
            break
    if hdr_i is None:
        return
    for row in rows[hdr_i + 1:]:
        # The demand sheet puts a numeric ZONE ID in column A and the zone NAME
        # in column B. Taking the first string cell picks the id, because "1"
        # is a string here -- which produced zones called '1', '10' and '13AG'
        # that join to nothing. Prefer a label with a letter in it.
        # "has a letter" is not enough: the demand sheet's ZONE ID column holds
        # values like 3A and 13ANG, which passed that test and won on position
        # over the real name in the next column. Pick the most alphabetic
        # candidate instead -- AMIL beats 3A, and a tie keeps the leftmost.
        cands = [str(c).strip() for c in row[:3] if isinstance(c, str) and c.strip()]
        label = max((c for c in cands if any(ch.isalpha() for ch in c)),
                    key=lambda c: sum(ch.isalpha() for ch in c) / len(c), default=None)
        if not label:
            continue
        vals = {}
        for j, yr in years.items():
            if j < len(row) and row[j] is not None:
                try:
                    vals[yr] = float(row[j])
                except (TypeError, ValueError):
                    pass
        if vals:
            yield label, vals


def parse(body: bytes, ctx: derive.ParseContext):
    wb = Workbook(body)

    for sheet, prefix in ZONE_SHEETS.items():
        if sheet not in wb.sheets:
            continue
        for zone, vals in _year_table(wb.rows(sheet)):
            # The demand sheet carries a numeric ZONE ID in column A and the
            # zone name in column B; _year_table already prefers the first
            # non-numeric label, but a stray total row still slips through.
            # Summary rows sit in the same table as the zones. Matching on
            # startswith missed "MISO Total" and "Percentage Change", which
            # then appeared as pricing zones and would have been charted as if
            # a ratepayer lived in them.
            low = zone.lower()
            if (low.startswith(("figure", "note", "source"))
                    or "total" in low or "percentage" in low or "change" in low):
                continue
            for yr, v in vals.items():
                yield derive.Observation(entity_id=f"zone:{zone}",
                                         metric=f"{prefix}_{yr}", value=v,
                                         unit="usd" if prefix != "demand" else "mw")

    if MVP_SHEET in wb.sheets:
        rows = wb.rows(MVP_SHEET)
        hdr_i = next((i for i, r in enumerate(rows[:12])
                      if any(isinstance(c, str) and c.strip() == "Project ID" for c in r)), None)
        if hdr_i is not None:
            hdr = [str(c).strip() if c else "" for c in rows[hdr_i]]
            idx = {name: i for i, name in enumerate(hdr) if name}
            for row in rows[hdr_i + 1:]:
                def get(name):
                    i = idx.get(name)
                    return row[i] if i is not None and i < len(row) else None
                pid = get("Project ID")
                if not pid or not str(pid).strip().isdigit():
                    continue
                pid = str(pid).strip()
                gross = get("Project Gross Plant")
                if gross is not None:
                    try:
                        yield derive.Observation(entity_id=f"mvp:{pid}",
                                                 metric="gross_plant",
                                                 value=float(gross), unit="usd")
                    except (TypeError, ValueError):
                        pass
                isd = get("In-Service Date")
                iso = excel_date(isd) or (str(isd)[:10] if isd and str(isd)[:4].isdigit() else None)
                if iso:
                    yield derive.Observation(entity_id=f"mvp:{pid}",
                                             metric="mvp_in_service", value=iso, unit="date")
                name = get("Project Name")
                if name:
                    yield derive.Observation(entity_id=f"mvp:{pid}", metric="mvp_name",
                                             value=str(name).strip(), unit="name")
                loc = get("Geographic Location of Project")
                if loc:
                    yield derive.Observation(entity_id=f"mvp:{pid}", metric="mvp_owners",
                                             value=str(loc).strip(), unit="name")


derive.register("miso.schedule26.v1", parse, PARSER_VERSION)
