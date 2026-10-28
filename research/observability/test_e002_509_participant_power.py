import unittest
from e002_509_participant_power import evaluate, minimum_zero_failure_n, zero_failure_upper


def participant(i, **updates):
    r = dict(participant_id=f'p{i:04}', eligible_windows=5, certificates=1,
             false_exclusions=0, unresolved_certificates=0, reference_resolved=True)
    r.update(updates)
    return r


class TestParticipantPower(unittest.TestCase):
    def test_frozen_numerics(self):
        self.assertAlmostEqual(zero_failure_upper(8), 0.31234397806636793, places=13)
        self.assertAlmostEqual(zero_failure_upper(24), 0.1173461561549487, places=13)
        self.assertAlmostEqual(zero_failure_upper(80), 0.03675419777998234, places=10)

    def test_minimal_299(self):
        self.assertEqual(minimum_zero_failure_n(), 299)
        self.assertGreater(zero_failure_upper(298), 0.01)
        self.assertLessEqual(zero_failure_upper(299), 0.01)
        self.assertLess(zero_failure_upper(300), zero_failure_upper(299))

    def test_invalid_inputs(self):
        for n in (0, -1, True, 2.5):
            with self.assertRaises(ValueError): zero_failure_upper(n)
        for a in (0, 1, float('nan'), True):
            with self.assertRaises(ValueError): zero_failure_upper(8, a)
        with self.assertRaises(ValueError): zero_failure_upper(8, failures=1)
        with self.assertRaises(ValueError): minimum_zero_failure_n(0)

    def test_eight_participant_pilot_cannot_clear(self):
        r = evaluate([participant(i) for i in range(8)])
        self.assertEqual(r['risk_gate'], 'INSUFFICIENT_PARTICIPANTS')
        self.assertEqual(r['participants_with_certificate'], 8)
        self.assertEqual(r['release'], 'BLOCKED')

    def test_299_passes_statistical_gate_only(self):
        r = evaluate([participant(i) for i in range(299)])
        self.assertEqual(r['risk_gate'], 'PASSES_STATISTICAL_ZERO_EVENT_GATE_ONLY')
        self.assertFalse(r['hard_physical_guarantee'])
        self.assertEqual(r['product'], 'ABSTAIN_UNCALIBRATED')

    def test_all_abstain_cannot_pass(self):
        r = evaluate([participant(i, certificates=0) for i in range(299)])
        self.assertEqual(r['risk_gate'], 'NO_USEFUL_COVERAGE')

    def test_failure_never_silently_zero(self):
        r = evaluate([participant(0, false_exclusions=1)] + [participant(i) for i in range(1, 299)])
        self.assertEqual(r['risk_gate'], 'NONZERO_FAILURES_REQUIRE_EXACT_INTERVAL')
        self.assertIsNone(r['zero_failure_upper'])

    def test_unknown_reference_rejected(self):
        with self.assertRaises(ValueError): evaluate([participant(1, unresolved_certificates=1)])
        with self.assertRaises(ValueError): evaluate([participant(1, reference_resolved=False)])

    def test_duplicate_or_missing_identity_rejected(self):
        with self.assertRaises(ValueError): evaluate([participant(1), participant(1)])
        with self.assertRaises(ValueError): evaluate([participant(1, participant_id='')])

    def test_count_inconsistencies_rejected(self):
        for kw in (dict(eligible_windows=0), dict(certificates=6),
                   dict(certificates=-1), dict(certificates=1, false_exclusions=1, unresolved_certificates=1),
                   dict(eligible_windows=True)):
            with self.assertRaises(ValueError): evaluate([participant(1, **kw)])

    def test_empty_and_wrong_schema_rejected(self):
        with self.assertRaises(ValueError): evaluate([])
        r = participant(1)
        r['extra'] = 1
        with self.assertRaises(ValueError): evaluate([r])


if __name__ == '__main__':
    unittest.main()
