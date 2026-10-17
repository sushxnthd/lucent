from pathlib import Path
from tempfile import TemporaryDirectory
from independent_check import check
s=Path(__file__).with_name('WITNESS.csv').read_text()
with TemporaryDirectory() as d:
    p=Path(d)/'test.csv'
    p.write_text(s.replace('-11,-71','-11,-70'))
    try:
        check(p)
    except AssertionError:
        print('NEGATIVE_TEST_PASS')
    else:
        raise RuntimeError('Negative test did not reject changed witness')
