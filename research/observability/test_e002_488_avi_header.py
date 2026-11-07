#!/usr/bin/env python3
"""Standard-library synthetic AVI regression suite; no network or ffmpeg required."""
import hashlib
from pathlib import Path
import struct
import tempfile
import unittest
import zipfile
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from e002_488_avi_header import inspect, parse_avi_header

def chunk(name, body):
    return name + struct.pack('<I',len(body)) + body + (b'\x00' if len(body)%2 else b'')

def avi(fps):
    avih=struct.pack('<10I',round(1_000_000/fps),0,0,0,15,0,1,0,32,24)+bytes(16)
    strh=b'vidsMJPG'+bytes(12)+struct.pack('<4I',1,fps,0,15)+bytes(20)
    hdrl=chunk(b'LIST',b'hdrl'+chunk(b'avih',avih)+chunk(b'LIST',b'strl'+chunk(b'strh',strh)))
    body=b'AVI '+hdrl+chunk(b'LIST',b'movi'+chunk(b'00dc',b'fake'))
    return b'RIFF'+struct.pack('<I',len(body))+body

class TestAvi(unittest.TestCase):
    def test_rates(self):
        for fps in (150,500):
            x=parse_avi_header(avi(fps))
            self.assertAlmostEqual(x['stream_header_nominal_fps'],fps,places=3)
            self.assertEqual(x['stream_header_matches_paper_150fps_2pct'],fps==150)
            self.assertFalse(x['independent_hardware_clock_authenticated'])

    def test_zip_end_to_end(self):
        with tempfile.TemporaryDirectory() as d:
            z=Path(d)/'S24.zip'
            with zipfile.ZipFile(z,'w',compression=zipfile.ZIP_DEFLATED) as a:
                a.writestr('S24_01_phantom.avi',avi(150))
            digest=hashlib.md5(z.read_bytes()).hexdigest()
            r=inspect(z,digest)
            self.assertEqual(r['pilot_acquisition_status'],'PASS_AUTHENTIC_ARCHIVE_HEADER_ONLY')
            self.assertEqual(r['anatomical_reference_sequences_annotated'],0)
            self.assertEqual(r['product_release'],'BLOCKED')
            with self.assertRaisesRegex(ValueError,'CHECKSUM_MISMATCH'):
                inspect(z,'0'*32)

    def test_reject_traversal(self):
        with tempfile.TemporaryDirectory() as d:
            z=Path(d)/'S24.zip'
            with zipfile.ZipFile(z,'w') as a:
                a.writestr('../bad_phantom.avi',avi(150))
            with self.assertRaisesRegex(ValueError,'UNSAFE_ZIP_MEMBER'):
                inspect(z,hashlib.md5(z.read_bytes()).hexdigest())

    def test_bad_riff(self):
        with self.assertRaisesRegex(ValueError,'NOT_RIFF_AVI'):
            parse_avi_header(b'not a real AVI')

    def test_malformed_rate(self):
        x=bytearray(avi(150))
        at=x.index(b'avih')+8
        struct.pack_into('<I',x,at,0)
        with self.assertRaisesRegex(ValueError,'INVALID_AVI_RATE_FIELDS'):
            parse_avi_header(bytes(x))

    def test_no_anatomical_inference(self):
        x=parse_avi_header(avi(150))
        self.assertEqual(x['timestamp_evidence'],'AVI_DECLARED_RATE_ONLY_NOT_INDEPENDENT_FRAME_TIMESTAMPS')

if __name__=='__main__':
    unittest.main(verbosity=2)
