"""spp.interconnection.queue.v1 — the Southwest Power Pool queue, and the requests it deletes.

WHAT PERISHES. SPP publishes one report, `Studies/GIActive`, and it contains
only live requests. The report carries a `Date Withdrawn` column and that column
is populated on ZERO of 1,024 rows; there is no /GIInactive, /GIWithdrawn or
/GICompleted companion (all 404). A withdrawn request is simply removed. So
"this request existed on this date, at this stage, promising this in-service
date" exists only if a capture was taken, which is the whole reason this source
is captured rather than cited.

THE EXIT VOCABULARY IS PARTIAL, AND THAT IS THE FINDING. SPP does record two
ways of stopping -- `Cessation Date` on 18 rows, and 25 projects at
`IA FULLY EXECUTED/ON SUSPENSION` -- so it is not that SPP cannot express an
ending. It publishes the endings it is comfortable publishing and drops the
withdrawals.

CONTRAST WITH ISO-NE, FROM THE SAME COLUMN NAME. ISO-NE's public queue has an
identically named withdrawal-date column, populated on 67.6% of its rows, which
makes it a larder and correctly kept out of this repository. Reading column
NAMES rather than column CONTENTS gets these two exactly backwards.

THE KEY IS REAL. `Generation Interconnection Number` is 100% filled and 1,024
distinct across 1,024 rows, formatted TI-18-0827, so the across-capture join
that makes disappearance visible is exact rather than fuzzy.

THREE TRAPS, ALL PAID FOR ALREADY:

  * The table has NO `<tbody>`. A parser that slices on it returns zero rows
    and reports a healthy empty queue.
  * `Fuel Type` is filled on 36% of rows while `Generation Type` is filled on
    100% with seven values. The obvious column is the wrong one.
  * `Associated Studies`, `Facility Report` and `Executed GIA` contain the
    anchor text "View" and nothing else; the documents live behind hrefs, so
    those columns carry presence, not content.

SPP TIMES OUT FROM A RESIDENTIAL CONNECTION and answers normally from a GitHub
runner -- the opposite of nyiso.interconnection.queue in this same repository,
which a runner cannot capture at all. See the registry entry.
"""

import html
import re

from wss import derive

PARSER_VERSION = "1"

MIN_ROWS = 300          # 1,024 on 2026-09-14; half of that is already alarming
KEY = "Generation Interconnection Number"

# Column title -> metric. Titles are taken verbatim from the <th> cells.
# Anything not listed is deliberately dropped rather than emitted blindly.
FIELDS = {
    "Status": "status",
    "Current Cluster": "cluster",
    "Cluster Group": "cluster_group",
    "IFS Queue Number": "ifs_queue_number",
    "Nearest Town or County": "place",
    "State": "state",
    "TO at POI": "transmission_owner",
    "Substation or Line": "substation",
    "Service Type": "service_type",
    "Generation Type": "generation_type",
    "Fuel Type": "fuel_type",
    "Request Received": "requested_at",
    "In-Service Date (proposed)": "proposed_in_service",
    "Commercial Operation Date": "commercial_operation_date",
    "Cessation Date": "cessation_date",
    "Date Withdrawn": "withdrawn_at",
    "Original Generator Commercial Op. Date": "original_cod",
    "Cause of Delay": "cause_of_delay",
    "JTIQ Participant": "jtiq_participant",
}
NUMERIC = {
    "Capacity (MW)": "capacity_mw",
    "MAX Summer MW": "summer_mw",
    "MAX Winter MW": "winter_mw",
    "Nameplate Capacity": "nameplate_mw",
    "Requested Maximum Injection Capability (MW)": "requested_injection_mw",
    "Requested Network Resource Deliverability (MW)": "requested_deliverability_mw",
}
# Columns whose cell is a link with the word "View" -- presence is the datum.
LINKS = {
    "Associated Studies": "has_associated_studies",
    "Facility Report": "has_facility_report",
    "Executed GIA": "has_executed_gia",
}

_TAG = re.compile(r"<[^>]+>")
_WS = re.compile(r"\s+")


def _cell(fragment: str) -> str:
    return _WS.sub(" ", html.unescape(_TAG.sub(" ", fragment))).strip()


def parse(body: bytes, ctx: derive.ParseContext):
    raw = body.decode("utf-8", errors="replace")
    titles = [_cell(t) for t in re.findall(r"<th[^>]*>(.*?)</th>", raw, re.S)]
    titles = [t for t in titles if t]
    if KEY not in titles:
        raise ValueError(
            f"spp.interconnection.queue.v1: no {KEY!r} column. Found {titles[:6]}. SPP has "
            f"changed the report's shape")

    # NO <tbody>. Slicing on one yields nothing and looks like an empty queue,
    # so the whole document is scanned and rows are recognised by arity.
    rows = []
    for tr in re.findall(r"<tr[^>]*>(.*?)</tr>", raw, re.S):
        cells = [_cell(c) for c in re.findall(r"<td[^>]*>(.*?)</td>", tr, re.S)]
        if len(cells) == len(titles):
            rows.append(dict(zip(titles, cells)))

    if len(rows) < MIN_ROWS:
        raise ValueError(
            f"spp.interconnection.queue.v1: parsed {len(rows)} rows against {len(titles)} columns. "
            f"The report held 1,024 on 2026-09-14. Either SPP changed the table "
            f"or the row/column arity match broke -- and an empty queue and a "
            f"broken parse are not allowed to look alike")

    seen: set[str] = set()
    by_status: dict[str, int] = {}
    by_type: dict[str, int] = {}
    withdrawn = ceased = 0

    for row in rows:
        gi = row.get(KEY, "").strip()
        if not gi or gi in seen:
            continue
        seen.add(gi)
        eid = f"request:{gi}"

        # PRESENCE IS THE OBSERVATION. SPP publishes no withdrawal event, so
        # "was in the report on this date" is the only thing that makes a later
        # disappearance mean anything.
        yield derive.Observation(eid, "listed", "yes", "state")

        for title, metric in FIELDS.items():
            value = row.get(title, "").strip()
            if value:
                yield derive.Observation(eid, metric, value, "text")
        for title, metric in NUMERIC.items():
            value = row.get(title, "").strip().replace(",", "")
            if not value:
                continue
            try:
                yield derive.Observation(eid, metric, float(value), "mw")
            except ValueError:
                # Kept verbatim rather than dropped: a unit or a footnote
                # appearing in a capacity column is a schema change worth seeing.
                yield derive.Observation(eid, f"{metric}_raw", value, "text")
        for title, metric in LINKS.items():
            if row.get(title, "").strip():
                yield derive.Observation(eid, metric, "yes", "state")

        by_status[row.get("Status", "") or "unknown"] = \
            by_status.get(row.get("Status", "") or "unknown", 0) + 1
        gtype = row.get("Generation Type", "") or "unknown"
        by_type[gtype] = by_type.get(gtype, 0) + 1
        if row.get("Date Withdrawn", "").strip():
            withdrawn += 1
        if row.get("Cessation Date", "").strip():
            ceased += 1

    feed = "feed:spp_giq"
    yield derive.Observation(feed, "requests_listed", len(seen), "count")
    yield derive.Observation(feed, "columns_published", len(titles), "count")
    # WATCH THIS ONE. It is 0 today, and the argument for capturing SPP at all
    # is that it stays 0 while requests vanish. If it ever moves, SPP has begun
    # publishing its withdrawals and this source becomes a larder.
    yield derive.Observation(feed, "rows_with_withdrawal_date", withdrawn, "count")
    yield derive.Observation(feed, "rows_with_cessation_date", ceased, "count")
    for status, n in sorted(by_status.items()):
        yield derive.Observation(f"status:{status}", "requests_listed", n, "count")
    for gtype, n in sorted(by_type.items()):
        yield derive.Observation(f"generationtype:{gtype}", "requests_listed", n, "count")


derive.register("spp.interconnection.queue.v1", parse, PARSER_VERSION)
