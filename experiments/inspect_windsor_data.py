"""Inspect the public University of Windsor eye-tracking + DRT dataset.

Temporary research utility for WIND-REALDATA-001. It prints only schema/timing
metadata, never participant-level sensitive content beyond a few column names
and time ranges.
"""

from __future__ import annotations

import io
import urllib.request
import zipfile

import openpyxl


DATASET_ID = "dp8g983t38"
VERSION = 1
ZIP_URL = (
    f"https://api.data.mendeley.com/datasets/{DATASET_ID}"
    f"/zip/file_downloaded?version={VERSION}"
)


def download() -> bytes:
    req = urllib.request.Request(
        ZIP_URL,
        headers={"User-Agent": "lucent-research/0.1"},
    )
    with urllib.request.urlopen(req, timeout=120) as response:
        payload = response.read()
        print("download final url:", response.geturl())
        print("content type:", response.headers.get("Content-Type"))
        print("bytes:", len(payload))
        return payload


def workbook_preview(zf: zipfile.ZipFile, name: str) -> None:
    payload = zf.read(name)
    wb = openpyxl.load_workbook(io.BytesIO(payload), read_only=True, data_only=True)
    ws = wb[wb.sheetnames[0]]
    rows = ws.iter_rows(values_only=True)
    header = next(rows, ())
    first = next(rows, ())
    second = next(rows, ())
    print("workbook:", name)
    print("sheet:", ws.title)
    print("header:", list(header)[:35])
    print("row1:", list(first)[:8])
    print("row2:", list(second)[:8])


def main() -> None:
    payload = download()
    with zipfile.ZipFile(io.BytesIO(payload)) as zf:
        names = zf.namelist()
        print("entries:", len(names))
        xlsx = [n for n in names if n.lower().endswith(".xlsx")]
        print("xlsx:", len(xlsx))
        print("first entries:")
        for name in names[:80]:
            print(" ", name)

        et = next((n for n in xlsx if "_ET_" in n.upper()), None)
        drt = next((n for n in xlsx if "_DRT_" in n.upper()), None)
        print("sample ET:", et)
        print("sample DRT:", drt)

        if et:
            workbook_preview(zf, et)
        if drt:
            workbook_preview(zf, drt)


if __name__ == "__main__":
    main()
