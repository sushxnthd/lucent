"""Independent E002-434 adversarial codec and parser tests."""
import unittest
import verify_frame_timing as m


def valid():
    return {'streams':[{'codec_type':'video','avg_frame_rate':'25/1'}],
            'frames':[{'best_effort_timestamp_time':f'{t:.6f}'} for t in (0,.04,.08,.12,.32,.36)]}


class TimingAuditTests(unittest.TestCase):
    def test_real_ffmpeg_vfr_and_cfr_controls(self):
        a=m.experiment()
        self.assertTrue(a['primary_prediction_passed'])
        self.assertGreater(a['vfr']['max_abs_naive_time_error_s'],.05)
        self.assertGreaterEqual(a['vfr']['max_gap_s'],.10)
        self.assertLessEqual(a['cfr']['max_abs_naive_time_error_s'],.01)
        self.assertEqual(a['human_sequences'],0)
        self.assertFalse(a['physical_certificate_authorized'])

    def test_presentation_gaps_not_equated_with_sensor_loss(self):
        r=m.analyze_probe(valid())
        self.assertAlmostEqual(r['max_presentation_gap_s'],.20)
        self.assertEqual(r['large_presentation_intervals'][0]['after_frame'],3)
        self.assertIn('not proof of sensor frame loss',r['limitations'])
        self.assertFalse(r['sensor_exposure_start_end_authenticated'])
        self.assertEqual(r['product'],'ABSTAIN_UNCALIBRATED')

    def test_missing_and_nonfinite_pts_rejected(self):
        for bad in (None,'N/A','nan','inf','-inf','garbage'):
            p=valid()
            p['frames'][2]['best_effort_timestamp_time']=bad
            with self.subTest(bad=bad),self.assertRaises(m.TimingError):m.analyze_probe(p)

    def test_nonmonotone_duplicate_negative_pts_rejected(self):
        for bad in ('0.040000','0.020000','-0.001000'):
            p=valid()
            p['frames'][2]['best_effort_timestamp_time']=bad
            with self.subTest(bad=bad),self.assertRaises(m.TimingError):m.analyze_probe(p)

    def test_bad_fps_and_malformed_streams_rejected(self):
        for bad in ('0/0','0/1','-30/1','nan','garbage',None):
            p=valid();p['streams'][0]['avg_frame_rate']=bad
            with self.subTest(bad=bad),self.assertRaises(m.TimingError):m.analyze_probe(p)
        for p in ({}, {'streams':[], 'frames':valid()['frames']},
                  {'streams':valid()['streams'],'frames':[]},
                  {'streams':valid()['streams']*2,'frames':valid()['frames']}):
            with self.assertRaises(m.TimingError):m.analyze_probe(p)

    def test_no_physical_upgrade_with_perfect_pts(self):
        p={'streams':[{'codec_type':'video','avg_frame_rate':'25/1'}],
           'frames':[{'best_effort_timestamp_time':str(i/25)} for i in range(20)]}
        r=m.analyze_probe(p)
        self.assertAlmostEqual(r['max_abs_nominal_clock_error_s'],0,places=12)
        self.assertFalse(r['physical_certificate_authorized'])
        self.assertEqual(r['time_basis'],'CONTAINER_PRESENTATION_TIME_NOT_SENSOR_EXPOSURE_TIME')


if __name__=='__main__':unittest.main()
