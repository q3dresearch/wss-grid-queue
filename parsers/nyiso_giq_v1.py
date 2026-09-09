"""nyiso.giq.v1 — the New York generator queue, and the promise it erases.

Nine sheets that together form a state machine keyed on `Queue Pos.`:

    Interconnection Queue -> (Withdrawn | In Service)

**The sheet a project is on IS the observation.** NYISO publishes no transition
event, so "moved from the active queue to Withdrawn between two captures" only
exists if both captures were taken. Every row therefore emits a `queue_state`
metric naming its sheet, which is what makes the move visible later.

What perishes is the promise. On the In Service sheet, `Proposed In-Service`
and `Proposed COD` have been overwritten with status markers -- I/S, IS, N/A --
for 147 of 149 completed projects. NYISO erases the promised date at the exact
moment completion makes the slip measurable, so filed-versus-actual cannot be
reconstructed from its own file. That is the whole reason this source is
captured rather than cited, and it is what separates it from CAISO, which
keeps `Proposed On-line Date (as filed with IR)` beside the actual.

The header is not on row 1. Several sheets split their column titles across two
rows -- "Queue" above "Pos.", "Date" above "of IR" -- so the header is located
by looking for the row containing a queue-position cell rather than by counting
down from the top.
"""

from wss import derive

from ._xlsx import Workbook, excel_date

PARSER_VERSION = "1"

# sheet name -> the state it represents. Sheets not listed are skipped: the
# zonal map is an image, and the tracking sheet is a pivot rather than rows.
SHEETS = {
    "Interconnection Queue": "active",
    " Cluster Projects": "active_cluster",
    "Load Projects": "load",
    "Affected System Studies": "affected_system",
    "Withdrawn": "withdrawn",
    "Cluster Projects-Withdrawn": "withdrawn_cluster",
    "In Service": "in_service",
}

# Column title (normalised) -> metric. Titles differ slightly between sheets,
# which is why they are matched loosely rather than by exact string.
FIELDS = {
    "queue pos.": None,          # the key, not a metric
    "queue number": None,
    "pos.": None,
    "developer/interconnection customer": "developer",
    "interconnection customer name": "developer",
    "owner/developer": "developer",
    "developer name": "developer",
    "project name": "project_name",
    "project: project name": "project_name",
    "date of ir": "requested_at",
    "of ir": "requested_at",
    "ir submission date": "requested_at",
    "sp (mw)": "summer_mw",
    "(mw)": "summer_mw",
    "wp (mw)": "winter_mw",
    "peak mw load": "peak_load_mw",
    "end-use": "end_use",
    "type/ fuel": "fuel",
    "type/fuel": "fuel",
    "fuel": "fuel",
    "county": "county",
    "state": "state",
    "nyiso zone": "zone",
    "z": "zone",
    "utility": "utility",
    "project status #": "project_status",
    "s": "project_status",
    "last updated date": "status_updated",
    "last update": "status_updated",
    "availability of studies": "studies_available",
    "of studies": "studies_available",
    "proposed in-service/initial backfeed date": "proposed_in_service",
    "proposed in-service": "proposed_in_service",
    # Header cells are stripped before lookup, so a key with a leading space
    # can never match. " In-Service" on the In Service sheet arrives as
    # "in-service", and the mismatch silently reported ZERO erased dates on the
    # sheet whose erasure is the entire reason this source exists.
    "in-service": "proposed_in_service",
    "proposed sync date": "proposed_sync",
    "proposed cod": "proposed_cod",
    "cod": "proposed_cod",
}


def _header_row(rows):
    """The row carrying the queue-position column, plus the one above it.

    Titles are split across two rows on several sheets: "Queue" sits above
    "Pos." and "Date" above "of IR". Reading only the lower row loses half the
    names, and reading only the upper loses the rest.
    """
    for i, row in enumerate(rows[:8]):
        cells = [str(c).strip().lower() if c else "" for c in row]
        if any(c in ("pos.", "queue pos.", "queue number") for c in cells):
            above = [str(c).strip() if c else "" for c in rows[i - 1]] if i else []
            return i, cells, above
    return None, [], []


def parse(body: bytes, ctx: derive.ParseContext):
    wb = Workbook(body)
    for sheet, state in SHEETS.items():
        if sheet not in wb.sheets:
            continue
        rows = wb.rows(sheet)
        i, header, above = _header_row(rows)
        if i is None:
            continue
        # Where the lower row is blank, fall back to the cell above it.
        titles = []
        for j, h in enumerate(header):
            if not h and j < len(above) and above[j]:
                h = above[j].strip().lower()
            titles.append(h)

        key_col = next((j for j, h in enumerate(titles)
                        if h in ("queue pos.", "pos.", "queue number")), None)
        if key_col is None:
            continue

        for row in rows[i + 1:]:
            if key_col >= len(row) or row[key_col] is None:
                continue
            pos = str(row[key_col]).strip()
            if not pos or not any(ch.isdigit() for ch in pos):
                continue
            eid = f"queue:{pos}"
            # The sheet itself. NYISO publishes no transition event, so this is
            # the only thing that makes "it moved" visible across captures.
            yield derive.Observation(eid, "queue_state", state, "state")
            for j, title in enumerate(titles):
                metric = FIELDS.get(title)
                if not metric or j >= len(row) or row[j] is None:
                    continue
                value = str(row[j]).strip()
                if not value:
                    continue
                if metric in ("requested_at", "status_updated"):
                    value = excel_date(value) or value
                yield derive.Observation(eid, metric, value, "text")


derive.register("nyiso.giq.v1", parse, PARSER_VERSION)
