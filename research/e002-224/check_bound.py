import math

def correlation_floor(epsilon):
    return math.sqrt(1 - epsilon * epsilon) if epsilon < 1 else -1.0

for epsilon in (0.2, 0.5, 0.8):
    assert 0 < correlation_floor(epsilon) < 1
print('Bound check passed')
