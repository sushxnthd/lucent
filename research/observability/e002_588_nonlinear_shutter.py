#!/usr/bin/env python3
"""E002-588 exact synthetic camera-response identifiability kill test.

No human data or physical sensor measurements. Uses fractions only.
"""
from __future__ import annotations
import argparse
import json
from fractions import Fraction as F

ROWS = (0, 20, 40)
PHASES = tuple(F(k, 2) for k in range(25))
D = F(1, 10)
A_START, A_EXP = F(21, 10), F(4)
B_START, B_EXP = F(2), F(9, 2)
LUT = ((F(0), F(0)), (F(1, 9), F(1, 40)),
       (F(8, 9), F(9, 10)), (F(1), F(1)))


def clip(x: F) -> F:
    return min(F(1), max(F(0), x))


def raw_fraction(row: int, phase: F, start: F, exposure: F, delay: F = D) -> F:
    assert exposure > 0
    return clip((start + row * delay + exposure - phase) / exposure)


def validate_lut(knots: tuple[tuple[F, F], ...]) -> None:
    if len(knots) < 2 or knots[0] != (F(0), F(0)) or knots[-1] != (F(1), F(1)):
        raise ValueError('LUT must span the exact black and white anchors')
    for (x0, y0), (x1, y1) in zip(knots, knots[1:]):
        if not (x1 > x0 and y1 > y0):
            raise ValueError('LUT must be strictly increasing in both coordinates')


def tone(x: F, knots: tuple[tuple[F, F], ...] = LUT) -> F:
    validate_lut(knots)
    if not F(0) <= x <= F(1):
        raise ValueError('raw intensity outside [0,1]')
    for (x0, y0), (x1, y1) in zip(knots, knots[1:]):
        if x <= x1:
            return y0 + (x - x0) * (y1 - y0) / (x1 - x0)
    raise AssertionError('LUT failed to cover input')


def a(row: int, phase: F) -> F:
    return raw_fraction(row, phase, A_START, A_EXP)


def b(row: int, phase: F, delay: F = D) -> F:
    return tone(raw_fraction(row, phase, B_START, B_EXP, delay))


def exposure_support(row: int, start: F, exp: F) -> tuple[F, F]:
    return start + row * D, start + row * D + exp


def uncovered_gap(start: F, exp: F) -> F:
    return F(100, 3) - (ROWS[-1] * D + exp)  # 30 Hz = 100/3 ms


def as_fraction(x: F) -> str:
    return f'{x.numerator}/{x.denominator}'


def run() -> dict:
    validate_lut(LUT)
    samples = []
    saturated = 0
    for row in ROWS:
        for phase in PHASES:
            ya, yb = a(row, phase), b(row, phase)
            assert ya == yb, f'counterexample killed at row={row}, phase={phase}: {ya} != {yb}'
            saturated += ya in (F(0), F(1))
            samples.append({'row': row, 'phase': as_fraction(phase),
                            'A': as_fraction(ya), 'B': as_fraction(yb)})
    assert len(samples) == 75 and saturated > 0 and saturated < 75
    assert [exposure_support(r, A_START, A_EXP) for r in ROWS] == [
        (F(21, 10), F(61, 10)), (F(41, 10), F(81, 10)), (F(61, 10), F(101, 10))]
    assert [exposure_support(r, B_START, B_EXP) for r in ROWS] == [
        (F(2), F(13, 2)), (F(4), F(17, 2)), (F(6), F(21, 2))]
    assert uncovered_gap(A_START, A_EXP) - uncovered_gap(B_START, B_EXP) == F(1, 2)
    assert a(0, F(25, 4)) == F(0)
    assert b(0, F(25, 4)) == F(1, 80)
    assert tone(F(1, 2)) != F(1, 2)  # nonlinear transfer
    assert b(0, F(6)) != b(0, F(25, 4))  # swapped-phase negative control
    assert raw_fraction(0, F(6), B_START, B_EXP) != a(0, F(6))  # identity-B control
    assert b(20, F(5), F(101, 1000)) != a(20, F(5))  # delay-change control
    try:
        validate_lut(((F(0), F(0)), (F(1, 2), F(3, 4)), (F(1), F(1, 2))))
        raise AssertionError('nonmonotone LUT accepted')
    except ValueError:
        pass
    return {
        'evidence_tier': 'exact synthetic, no physical or human data',
        'protocol': 'E002_588_FROZEN.md',
        'sample_count': len(samples),
        'saturated_count': saturated,
        'rows': list(ROWS),
        'gap_A_ms': as_fraction(uncovered_gap(A_START, A_EXP)),
        'gap_B_ms': as_fraction(uncovered_gap(B_START, B_EXP)),
        'gap_difference_ms': as_fraction(F(1, 2)),
        'heldout_phase_ms': '25/4',
        'heldout_A': '0/1',
        'heldout_B': '1/80',
        'samples': samples,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--emit-json', action='store_true')
    args = parser.parse_args()
    result = run()
    if args.emit_json:
        print(json.dumps(result, sort_keys=True))
    else:
        print('PASS: 75/75 exact synthetic observations indistinguishable; '
              '30-Hz uncovered gap differs by 1/2 ms; heldout 0 versus 1/80; '
              'adversarial controls passed')


if __name__ == '__main__':
    main()
