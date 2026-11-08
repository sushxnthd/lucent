"""E002-728 regression: importability and strict interval-censored edge reporting.
Run: python -m unittest research.observability.test_e002_728_capture_syntax
"""
import ast
import inspect
import unittest
from research.observability import e002_726_capture_alignment as alignment

class CaptureSyntaxRegression(unittest.TestCase):
    def test_source_parses(self):
        ast.parse(inspect.getsource(alignment))
    def test_reference_edge(self):
        frames={"frames":[{"best_effort_timestamp_time":t} for t in ("0","0.033","0.066")]}
        reference=[{"time_s":t,"closed":s} for t,s in
                   (("0.000","0"),("0.010","0"),("0.020","1"),("0.030","1"))]
        result=alignment.analyze(frames,reference)
        self.assertEqual(result["status"],"TIMELINE_PARSED_NOT_SYNCHRONIZED")
        self.assertEqual(result["reference_transition_intervals_s"],
                         [{"after_s":"0.010","at_or_before_s":"0.020","from":"0","to":"1"}])
        self.assertNotIn("reference_transitions_at_sample_s",result)
if __name__=="__main__":
    unittest.main()
