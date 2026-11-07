"""E002-663: distribution-free finite-horizon velocity exceedance law.
Run: python research/observability/e002_663_horizon.py
No external dependencies. Synthetic/exact probability, NOT human validation.
"""
from fractions import Fraction

def exceedance_probability(n_calibration: int, m_future: int) -> Fraction:
    """P(max of m future iid continuous values > max of n calibration values).
    Exchangeability and no ties: overall maximum belongs to future block with
    probability m/(n+m). No parametric tail assumption.
    """
    if n_calibration < 1 or m_future < 1:
        raise ValueError("n_calibration and m_future must be positive")
    return Fraction(m_future, n_calibration + m_future)

def minimum_calibration(m_future: int, alpha: Fraction) -> int:
    """Smallest n for exceedance risk <= alpha under iid continuous sampling."""
    if not (0 < alpha < 1) or m_future < 1:
        raise ValueError("invalid horizon or risk")
    return (m_future * (alpha.denominator - alpha.numerator) +
            alpha.numerator - 1) // alpha.numerator

def test():
    assert exceedance_probability(100, 1) == Fraction(1, 101)
    assert exceedance_probability(100, 100) == Fraction(1, 2)
    assert minimum_calibration(100, Fraction(1, 20)) == 1900
    assert exceedance_probability(1900, 100) == Fraction(1, 20)
    assert exceedance_probability(1899, 100) > Fraction(1, 20)
    # One future sequence with 100 independent potential exceedance draws
    # is not certified by a calibration maximum of 100 draws.
    # Counterexample to distribution-free deployment guarantees without
    # exchangeability: calibration values all 1, future values all 2.
    calibration = [1] * 100
    future = [2] * 100
    assert max(future) > max(calibration)
    print("E002-663 PASS: n=100,m=100 risk=1/2; n=1900,m=100 risk=1/20")
if __name__ == "__main__":
    test()
