import unittest
import e002_605_human_blink_alias as m

class TestAlias(unittest.TestCase):
    def test_phase_law(self):
        for width,misses in [(1,2),(2,1),(3,0),(4,0),(11,0)]:
            for lo in range(0,20):
                a=m.evaluate([('S5',lo,lo+width-1,'fully_closed')])['counts']['holdout']['fully_closed']
                self.assertEqual(a['missed_phases'],misses)
                self.assertEqual(a['total_phases'],3)
    def test_event_not_closure(self):
        r=m.evaluate([('S5',0,20,'blink_event')]);self.assertEqual(r['counts']['holdout']['fully_closed']['events'],0)
    def test_missingness_abstains(self):
        r=m.evaluate([('S5',4,4,'fully_closed')],missing={'S5':{4}})
        self.assertEqual(r['counts']['holdout']['fully_closed']['unknown_phases'],3)
        self.assertEqual(r['counts']['holdout']['fully_closed']['total_phases'],0)
    def test_invalid_columns(self):
        with self.assertRaisesRegex(ValueError,'MISSING_KIND'):m.read_rows([['subject','start_frame','end_frame'],['S5','1','2']])
    def test_unknown_kind_excluded(self):
        ev,rej=m.read_rows([['subject','start_frame','end_frame','kind'],['S5','1','2','blink'],['S5','4','5','fully_closed']])
        self.assertEqual(len(ev),1);self.assertEqual(rej['AMBIGUOUS_EVENT_KIND'],1)
    def test_subject_bounds(self):
        ev,rej=m.read_rows([['subject','start_frame','end_frame','kind'],['S13','1','2','fully_closed'],['S5','34355','34356','fully_closed']])
        self.assertEqual(len(ev),0);self.assertEqual(sum(rej.values()),2)
    def test_reject_duplicates(self):
        with self.assertRaisesRegex(ValueError,'DUPLICATE'):m.evaluate([('S5',1,1,'fully_closed')]*2)
    def test_split(self):
        r=m.evaluate([('S1',1,1,'blink_event'),('S5',1,1,'fully_closed')]);self.assertEqual(r['counts']['development']['blink_event']['participants'],1)
        self.assertEqual(r['counts']['holdout']['fully_closed']['participants'],1)

if __name__=='__main__':unittest.main()
