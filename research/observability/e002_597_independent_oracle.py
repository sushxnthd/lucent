#!/usr/bin/env python3
"""E002-597 independent pure-Python oracle for frozen small grayscale fixtures.

Does not import numpy, Pillow, or the primary measurement implementation.
"""


def measure_rows(rows):
    if (not isinstance(rows, (list, tuple)) or len(rows) < 2 or
            not isinstance(rows[0], (list, tuple)) or len(rows[0]) < 1):
        raise ValueError("INVALID_GRAYSCALE_ARRAY")
    h = len(rows)
    w = len(rows[0])
    if any(not isinstance(row, (list, tuple)) or len(row) != w for row in rows):
        raise ValueError("RAGGED_ARRAY")
    if any(type(x) is not int or not 0 <= x <= 255 for row in rows for x in row):
        raise ValueError("INVALID_PIXEL")
    dark = sum(1 for row in rows for x in row if x < 80) / (h * w)
    total = sum(abs(rows[y + 1][x] - rows[y][x])
                for y in range(h - 1) for x in range(w))
    edge = total / ((h - 1) * w * 255)
    return dark, edge


if __name__ == "__main__":
    assert measure_rows([[0, 255], [255, 0]]) == (0.5, 1.0)
    for bad in ([], [[1]], [[1, 2], [3]], [[-1], [0]], [[256], [0]], [[True], [0]]):
        try:
            measure_rows(bad)
        except ValueError:
            pass
        else:
            raise AssertionError("INVALID_ARRAY_ACCEPTED")
    print("E002-597 independent oracle PASS")
