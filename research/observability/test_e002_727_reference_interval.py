"""E002-727: independent reference edges are interval-censored, not point events.
Run: python -m unittest research.observability.test_e002_727_reference_interval
"""
import unittest
from research.observability.e002_726_capture_alignment import analyze

class ReferenceIntervalTests(unittest.TestCase):
    def test_edge_is_not_observed_at_sample_timestamp(self):
        frames={"frames":[{"best_effort_timestamp_time":x} for x in ("0","0.033","0.066")]}
        reference=[{"time_s":"0.000","closed":"0"},{"time_s":"0.010","closed":"0"},
                   {"time_s":"0.020","closed":"1"},{"time_s":"0.030","closed":"1"}]
        result=analyze(frames,reference)
        self.assertEqual(result["status"],"TIMELINE_PARSED_NOT_SYNCHRONIZED")
        # Event time lies in (0.010,0.020] for point samples; assigning 0.020
        # as the true event instant is unsupported.
        self.assertEqual(result["reference_transition_intervals_s"],
                         [{"after_s":"0.010","at_or_before_s":"0.020","from":"0","to":"1"}])
        self.assertNotIn("reference_transitions_at_sample_s",result)
    def test_no_transition(self):
        frames={"frames":[{"best_effort_timestamp_time":x} for x in ("0","0.03","0.06")]}
        ref=[{"time_s":"0","closed":"0"},{"time_s":"0.01","closed":"0"}]
        self.assertEqual(analyze(frames,ref)["reference_transition_intervals_s"],[])
if __name__=="__main__": unittest.main()
