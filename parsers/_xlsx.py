"""Minimal .xlsx reader — no openpyxl, because derive runs against the engine alone.

An .xlsx is a zip of XML. This pulls out named worksheets and returns rows of
cell values, which is all any parser here needs.

Sheet order in `workbook.xml` is NOT the order of `sheet1.xml`, `sheet2.xml`
files inside the zip. The mapping goes through `xl/_rels/workbook.xml.rels`:
each `<sheet>` carries an `r:id`, and the rels file maps that id to a target
path. Reading `sheet1.xml` because a sheet is listed first is a coin flip that
lands wrong often enough to matter.
"""
from __future__ import annotations

import datetime
import io
import zipfile
from xml.etree import ElementTree as ET

MAIN = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
REL = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
PKGREL = "{http://schemas.openxmlformats.org/package/2006/relationships}"


def _col(ref: str) -> int:
    """'BC12' -> 54. Column letters are base-26 with no zero."""
    n = 0
    for ch in ref:
        if ch.isalpha():
            n = n * 26 + (ord(ch.upper()) - 64)
        else:
            break
    return n - 1


def excel_date(value) -> str | None:
    """Excel serial -> ISO date. Returns None for anything that is not a date."""
    try:
        n = float(value)
    except (TypeError, ValueError):
        return None
    if n < 1 or n > 100_000:
        return None
    return (datetime.date(1899, 12, 30) + datetime.timedelta(days=int(n))).isoformat()


class Workbook:
    def __init__(self, body: bytes):
        self.z = zipfile.ZipFile(io.BytesIO(body))
        self.shared: list[str] = []
        if "xl/sharedStrings.xml" in self.z.namelist():
            root = ET.fromstring(self.z.read("xl/sharedStrings.xml"))
            self.shared = ["".join(t.text or "" for t in si.iter(f"{MAIN}t"))
                           for si in root.findall(f"{MAIN}si")]
        rels = {}
        if "xl/_rels/workbook.xml.rels" in self.z.namelist():
            root = ET.fromstring(self.z.read("xl/_rels/workbook.xml.rels"))
            for r in root:
                rels[r.get("Id")] = r.get("Target")
        wb = ET.fromstring(self.z.read("xl/workbook.xml"))
        self.sheets: dict[str, str] = {}
        for s in wb.iter(f"{MAIN}sheet"):
            target = rels.get(s.get(f"{REL}id"), "")
            if target:
                self.sheets[s.get("name")] = "xl/" + target.lstrip("/").removeprefix("xl/")

    def rows(self, sheet_name: str) -> list[list]:
        """Rows of a named sheet, as ragged lists indexed by real column."""
        path = self.sheets.get(sheet_name)
        if not path or path not in self.z.namelist():
            return []
        root = ET.fromstring(self.z.read(path))
        out = []
        for row in root.iter(f"{MAIN}row"):
            cells: dict[int, object] = {}
            for c in row.findall(f"{MAIN}c"):
                i = _col(c.get("r", "A"))
                v = c.find(f"{MAIN}v")
                text = v.text if v is not None else None
                if text is None:
                    is_el = c.find(f"{MAIN}is")
                    text = ("".join(t.text or "" for t in is_el.iter(f"{MAIN}t"))
                            if is_el is not None else None)
                if text is None:
                    continue
                if c.get("t") == "s":
                    idx = int(text)
                    text = self.shared[idx] if idx < len(self.shared) else ""
                cells[i] = text
            if cells:
                width = max(cells) + 1
                out.append([cells.get(i) for i in range(width)])
        return out
