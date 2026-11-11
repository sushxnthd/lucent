#!/usr/bin/env python3
"""E002-593: synthetic shutter-gap prospective certificate test.
Integer-only comparisons. No human or physical validation.
"""
import json

MASK = (1 << 32) - 1

class RNG:
    def __init__(self, seed):
        self.x = seed
    def next(self):
        x = self.x
        x ^= (x << 13) & MASK
        x ^= x >> 17
        x ^= (x << 5) & MASK
        self.x = x & MASK
        return self.x
    def between(self, lo, hi):
        return lo + self.next() % (hi-lo+1)

def trial(rng):
    c = rng.between(300,800)       # aperture milliunits
    g = rng.between(12000,30000)   # true shutter gap microseconds
    r = rng.between(850,1150)      # V*g / [2(c-tau)], in milliunits
    left = c + rng.between(-20,20)
    right = c + rng.between(-20,20)
    observed_gap = g + rng.between(-1500,1500)
    numerator = 2 * (c-100) * r
    scale = 1000*g
    naive = numerator*observed_gap < (left+right-200)*scale
    robust = numerator*(observed_gap+1500) < (left+right-240)*scale
    actual_closure = r >= 1000
    oracle = r < 1000
    return actual_closure, naive, robust, oracle

def experiment(seed=593, n=12000):
    rng=RNG(seed)
    counts={"total":n,"true_hidden_closure":0,"true_no_closure":0,
            "naive_exclusions":0,"naive_false_exclusions":0,
            "robust_exclusions":0,"robust_false_exclusions":0,"oracle_exclusions":0}
    for _ in range(n):
        truth,naive,robust,oracle=trial(rng)
        counts["true_hidden_closure" if truth else "true_no_closure"]+=1
        for label,decision in (("naive",naive),("robust",robust)):
            if decision:
                counts[f"{label}_exclusions"]+=1
                if truth:counts[f"{label}_false_exclusions"]+=1
        if oracle:counts["oracle_exclusions"]+=1
    return counts

def tests():
    x=experiment()
    assert x["robust_false_exclusions"]==0
    assert x["naive_false_exclusions"]>0
    assert x["robust_exclusions"]<=x["naive_exclusions"]
    # At the exact certified boundary equality abstains.
    assert not (2*400*1000*20000 < (520+520-240)*1000*20000)
    # With +30 endpoint errors exceeding declared +20, false exclusion occurs.
    assert 2*400*1000*20000 < (530+530-240)*1000*20000
    return x

if __name__=='__main__':
    print(json.dumps(tests(),sort_keys=True,indent=2))
