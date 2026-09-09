"""miso.mtep.v1 — one observation per MTEP project, per capture.

MISO publishes three workbooks that together form a state machine keyed on
`MTEP Project ID`:

    Under Evaluation  ->  Appendix A approved  ->  In Service

Every figure in them is a *current* value. There is no original cost column and
no promised in-service date, and the files sit at fixed URLs that are
overwritten in place. So the series this parser builds cannot be reconstructed
later by re-fetching: it only exists because captures accumulate.

Three metrics, deliberately:

  current_cost      the founding question. MISO publishes `Current Cost` and
                    nothing else -- what a project was approved at is published
                    nowhere, so escalation is invisible in any single fetch.
  expected_isd      the promise. Overwritten each time it slips, so the slip
                    is only visible across captures.
  planning_status   M1 Proposed / M2 Appendix A Approved / M3 Under
                    Construction / M4 Project in Service. The transition is the
                    event; MISO publishes only the current letter.

**Membership in a file is not the status.** 169 rows in the Approved workbook
and 12 in Under Evaluation already carry `M4 - Project in Service`. Reading
"3,211 approved projects" off the Approved file overstates the live pipeline by
5%. Every count here comes from the `Planning Status` column, never the source
the row arrived in.

`observed_at` is deliberately left unset. These are state snapshots -- "what
MISO says this project costs today" -- and the payload carries no observation
time of its own, so derive stamps each row with the capture that produced it.
`Board Approved Date` is an event date, but it is an attribute of the project,
not the time this measurement was true.
"""

import datetime
import io
import zipfile

from wss import derive

PARSER_VERSION = "1"

# Column names differ slightly between the three workbooks; the ones we need
# are spelled identically in all three, which is the only reason one parser
# covers them.
ID = "MTEP Project ID"
COST = "Current Cost"
ISD = "Expected ISD"
STATUS = "Planning Status"
CYCLE = "Target MTEP Cycle"
FACILITY = "Facility ID"
OWNER = "Submitting TO"


def _sheet_rows(body: bytes):
    """Yield dict rows from the first worksheet, without openpyxl.

    An .xlsx is a zip of XML. Pulling the one sheet we need out of it directly
    keeps the parser dependency-free, which matters because derive runs in CI
    against an engine install and nothing else.
    """
    import re
    from xml.etree import ElementTree as ET

    NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
    with zipfile.ZipFile(io.BytesIO(body)) as z:
        shared = []
        if "xl/sharedStrings.xml" in z.namelist():
            root = ET.fromstring(z.read("xl/sharedStrings.xml"))
            for si in root.findall(f"{NS}si"):
                shared.append("".join(t.text or "" for t in si.iter(f"{NS}t")))
        name = next((n for n in z.namelist()
                     if re.fullmatch(r"xl/worksheets/sheet1\.xml", n)), None)
        if name is None:
            return
        root = ET.fromstring(z.read(name))
        grid = []
        for row in root.iter(f"{NS}row"):
            cells = {}
            for c in row.findall(f"{NS}c"):
                ref = c.get("r", "")
                col = "".join(ch for ch in ref if ch.isalpha())
                v = c.find(f"{NS}v")
                text = v.text if v is not None else None
                if text is None:
                    is_el = c.find(f"{NS}is")
                    text = "".join(t.text or "" for t in is_el.iter(f"{NS}t")) if is_el is not None else None
                if text is None:
                    continue
                if c.get("t") == "s":
                    idx = int(text)
                    text = shared[idx] if idx < len(shared) else ""
                cells[col] = text
            grid.append(cells)

    header_i = max(range(min(6, len(grid))),
                   key=lambda i: sum(1 for v in grid[i].values() if v and not v.replace(".", "").isdigit()),
                   default=0)
    header = {col: str(val).strip().replace("\n", " ") for col, val in grid[header_i].items()}
    for cells in grid[header_i + 1:]:
        row = {header.get(col, col): val for col, val in cells.items()}
        if row.get(ID):
            yield row


def _excel_date(serial: str) -> str | None:
    """Excel stores dates as days since 1899-12-30. Return ISO, or None."""
    try:
        n = float(serial)
    except (TypeError, ValueError):
        return None
    if n < 1 or n > 100_000:
        return None
    return (datetime.date(1899, 12, 30) + datetime.timedelta(days=int(n))).isoformat()


def parse(body: bytes, ctx: derive.ParseContext):
    for row in _sheet_rows(body):
        pid = str(row[ID]).strip()
        # GRAIN. The Approved workbook is one row per FACILITY, not per project:
        # 3,211 rows carry 1,497 distinct MTEP Project IDs, and `Current Cost`
        # differs across a project's facility rows in 482 of the 496 projects
        # that have more than one. Keying on the project alone silently kept a
        # single facility's cost and threw the rest away -- $33.0B instead of
        # $68.6B, a headline halved without an error. The other two workbooks
        # are one row per project and carry no Facility ID.
        fac = str(row.get(FACILITY, "") or "").strip()
        eid = f"{pid}:{fac}" if fac else pid
        status = str(row.get(STATUS, "")).strip()

        cost = row.get(COST)
        if cost not in (None, ""):
            try:
                yield derive.Observation(entity_id=eid, metric="current_cost",
                                         value=float(cost), unit="usd")
            except ValueError:
                pass

        isd = _excel_date(row.get(ISD))
        if isd:
            yield derive.Observation(entity_id=eid, metric="expected_isd",
                                     value=isd, unit="date")
        if status:
            yield derive.Observation(entity_id=eid, metric="planning_status",
                                     value=status, unit="status")
        # Attributes that do not change, emitted once per capture so a chart can
        # group without re-reading the raw archive.
        if row.get(OWNER):
            yield derive.Observation(entity_id=eid, metric="submitting_to",
                                     value=str(row[OWNER]).strip(), unit="name")
        if row.get(CYCLE):
            yield derive.Observation(entity_id=eid, metric="target_cycle",
                                     value=str(row[CYCLE]).strip(), unit="cycle")
        if fac:
            # so a facility-grained row can still be rolled up to its project
            yield derive.Observation(entity_id=eid, metric="project_id",
                                     value=pid, unit="id")


derive.register("miso.mtep.v1", parse, PARSER_VERSION)
