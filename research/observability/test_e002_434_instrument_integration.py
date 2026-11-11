"""E002-434 integration test: actual OpenCV quality pipeline on FFV1 VFR media."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import verify_frame_timing as timing

ROOT = Path(__file__).resolve().parents[2]
ANALYZE = ROOT/'instrument'/'analyze_capture.py'


class QualityPipelineTimingTests(unittest.TestCase):
    def test_actual_vfr_video_container_pts_vs_nominal(self):
        with tempfile.TemporaryDirectory() as d:
            folder=Path(d)
            durations=[.04,.04,.04,.20,.04,.04,.12,.04,.04,.04,.04,.04]
            video,_,_=timing.encode_fixture(folder,durations,'vfr')
            meta=folder/'vfr.json'
            meta.write_text(json.dumps({'stimulusEvents':[]}),encoding='utf-8')
            quality=folder/'quality.json'
            subprocess.run([sys.executable,str(ANALYZE),str(video),str(meta),
                            '--container-pts','--output',str(quality)],
                           capture_output=False,text=True,check=True,timeout=30)
            data=json.loads(quality.read_text())
            self.assertEqual(data['video']['sampledFrames'],13)
            self.assertAlmostEqual(data['frames'][7]['timeS'],.52,places=3)
            self.assertEqual(data['frames'][7]['timeSProvenance'],'CONTAINER_PTS_NOT_SENSOR_TIME')
            self.assertTrue(data['timing']['containerPtsParsed'])
            self.assertFalse(data['timing']['hardwareExposureTimestampsAuthenticated'])
            self.assertFalse(data['physicalCertificateAuthorized'])
            self.assertEqual(data['product'],'ABSTAIN_UNCALIBRATED')
            nominal=folder/'nominal.json'
            subprocess.run([sys.executable,str(ANALYZE),str(video),str(meta),
                            '--output',str(nominal)],capture_output=False,text=True,check=True,timeout=30)
            control=json.loads(nominal.read_text())
            self.assertAlmostEqual(control['frames'][7]['timeS'],.28,places=3)
            self.assertEqual(control['frames'][7]['timeSProvenance'],
                             'NOMINAL_FRAME_INDEX_DIVIDED_BY_REPORTED_FPS_NOT_SENSOR_TIME')
            self.assertFalse(control['timing']['containerPtsParsed'])

    def test_stride_preserves_original_indices(self):
        with tempfile.TemporaryDirectory() as d:
            folder=Path(d)
            video,_,_=timing.encode_fixture(folder,[.04,.04,.04,.20,.04,.04,.12,.04,.04,.04,.04,.04],'vfr')
            meta=folder/'vfr.json';meta.write_text('{"stimulusEvents":[]}')
            quality=folder/'quality.json'
            subprocess.run([sys.executable,str(ANALYZE),str(video),str(meta),
                            '--stride','3','--container-pts','--output',str(quality)],
                           capture_output=False,text=True,check=True,timeout=30)
            rows=json.loads(quality.read_text())['frames']
            self.assertEqual([r['frame'] for r in rows],[0,3,6,9,12])
            self.assertEqual([round(r['timeS'],2) for r in rows],[0,.12,.40,.60,.72])


if __name__=='__main__':unittest.main()
