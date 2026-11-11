import math
import unittest
from e002_537_participant_calibration import threshold, participant_score, decide, run


class CalibrationTests(unittest.TestCase):
    def test_12_abstains(self):
        self.assertTrue(math.isinf(threshold(list(range(12)))))
        self.assertEqual(decide(1.0, threshold(list(range(12))), True), 'ABSTAIN')

    def test_minimum_19(self):
        self.assertEqual(threshold(list(range(19))), 18)
        self.assertEqual(decide(19, 18, True), 'EXCLUDE_CONDITIONALLY')
        self.assertEqual(decide(18, 18, True), 'ABSTAIN')

    def test_39_order_statistic(self):
        self.assertEqual(threshold(list(range(39))), 37)

    def test_ties_conservative(self):
        self.assertEqual(threshold([1]*19), 1)
        self.assertEqual(decide(1, 1, True), 'ABSTAIN')

    def test_unknown_fails_closed(self):
        self.assertEqual(participant_score([0.1, 0.2], [0, None]), math.inf)
        self.assertEqual(participant_score([0.1], [0], evidence_ok=False), math.inf)

    def test_no_closure_negative_infinity(self):
        self.assertEqual(participant_score([0.1, 0.2], [0,0]), -math.inf)
        self.assertEqual(participant_score([0.1, 0.2], [1,0]), 0.1)

    def test_bad_reference_and_geometry(self):
        self.assertEqual(participant_score([0.1], [1,0]), math.inf)
        self.assertEqual(participant_score([float('nan')], [1]), math.inf)
        self.assertEqual(participant_score([], []), math.inf)
        self.assertEqual(participant_score([0.2], [2]), math.inf)

    def test_missing_instrument_abstains(self):
        self.assertEqual(decide(99, -1, False), 'ABSTAIN')
        self.assertEqual(decide(float('nan'), -1, True), 'ABSTAIN')

    def test_invalid_alpha(self):
        for alpha in (0, 1, -0.1):
            with self.assertRaises(ValueError):
                threshold([1,2,3],alpha)
        with self.assertRaises(ValueError):
            threshold([])

    def test_independent_rank_enumeration(self):
        # For four distinct calibration scores and one test score, all five
        # possible test ranks are equally likely. At alpha=1/5, k=4.
        # Exactly one of the five ranks exceeds the calibration maximum.
        self.assertEqual(sum(rank == 5 for rank in range(1,6)),1)
        self.assertEqual(threshold([1,2,3,4], 0.2),4)

    def test_frozen_simulation(self):
        r=run()
        self.assertEqual(r['participant_conditions'][0]['iid_failures'],0)
        self.assertTrue(all(c['iid_within_5se'] for c in r['participant_conditions']))
        self.assertGreater(r['pseudoreplication']['familywise_risk'],.05)
        self.assertEqual(r['release'],'BLOCKED')


if __name__=='__main__':
    unittest.main()
