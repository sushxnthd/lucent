from parser import parse
from count import windows
from stats import summarize

def fixture(ids):
    return '#start\n' + '\n'.join(f'{i+1}:{v}:' + ':'.join(['X']*17) for i,v in enumerate(ids)) + '\n#end'

rows = parse(fixture([-1, 0, 0, -1, 1, -1, -1, -1, -1, -1]))
assert [w[2] for w in windows(rows, width=5)] == [2, 0]
summary = summarize([[2, 0]], reps=100)
assert summary['observed_zero'] == 0.5
assert summary['conditional_expected_zero'] == 0.25
print('E002_177_FIXTURE_PASS')
