import math

def threshold(epsilon, weights):
    return 2 * epsilon * (1 + sum(abs(w) for w in weights))

assert math.isclose(threshold(.005, [.25,.25,.25,.25]), .02)
