# E002-335 independent checker
# Reproduce using public EyeBlink8 .tag annotations.
# See PROTOCOL_FROZEN.md for source limitations.
def mask(frames):
    return sum(1 << p for p in range(3) if any(n % 3 == p for n in frames))
def verify(frames):
    m = mask(frames)
    for p in range(3):
        assert bool(m & (1 << p)) == any(n % 3 == p for n in frames)
    if any(frames[i+2] == frames[i]+2 and frames[i+1] == frames[i]+1
           for i in range(len(frames)-2)):
        assert m == 7
    return m
if __name__ == "__main__":
    assert verify([7]) == 2
    assert verify([7,8]) == 6
    assert verify([7,8,9]) == 7
    print("phase-mask invariants passed")
