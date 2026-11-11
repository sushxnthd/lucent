#!/usr/bin/env python3
"""E002-500 preregistered synthetic source-provenance attack; no human imagery."""
import json
import os
from pathlib import Path
import shutil
import struct
import tempfile
import unittest
import zlib
from unittest.mock import patch

from e002_492_anatomical_review import build_manifest, template
from e002_496_packet_integrity import validate as legacy_validate
from e002_500_source_replay import NAMES, compare_private_frames, verify_against_source

def chunk(name, data):
    return struct.pack('>I', len(data)) + name + data + struct.pack('>I', zlib.crc32(name + data))

def png(gray):
    ihdr = struct.pack('>IIBBBBB', 320, 288, 8, 0, 0, 0, 0)
    rows = (b'\x00' + bytes([gray]) * 320) * 288
    return (b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', ihdr)
            + chunk(b'IDAT', zlib.compress(rows)) + chunk(b'IEND', b''))

class SourceReplayTests(unittest.TestCase):
    def setUp(self):
        self.td = tempfile.TemporaryDirectory()
        self.addCleanup(self.td.cleanup)
        root = Path(self.td.name)
        self.packet = root / 'packet'
        self.packet.mkdir(mode=0o700)
        os.chmod(self.packet, 0o700)
        (self.packet / 'OWNER_ONLY_MAPPING.json').write_text(json.dumps(build_manifest()))
        for r in ('A', 'B'):
            (self.packet / f'RATER_{r}_TEMPLATE.json').write_text(
                json.dumps(template(build_manifest(), r)))
        self.images = self.packet / 'PRIVATE_FRAMES_DO_NOT_UPLOAD'
        self.images.mkdir(mode=0o700)
        os.chmod(self.images, 0o700)
        self.reference = root / 'reference'
        self.reference.mkdir(mode=0o700)
        for name in NAMES:
            data = png(10)
            (self.images / name).write_bytes(data)
            (self.reference / name).write_bytes(data)

    def test_old_checker_accepts_synthetic_forged_packet(self):
        self.assertEqual(legacy_validate(self.packet)['status'], 'TECHNICAL_PACKET_INTEGRITY_PASS')

    def test_exact_source_replay_passes(self):
        self.assertTrue(compare_private_frames(self.images, self.reference))

    def test_one_substituted_valid_png_passes_old_checker_but_fails_replay(self):
        (self.images / NAMES[0]).write_bytes(png(11))
        self.assertEqual(legacy_validate(self.packet)['status'], 'TECHNICAL_PACKET_INTEGRITY_PASS')
        with self.assertRaisesRegex(ValueError, '^SOURCE_FRAME_CONTENT_MISMATCH$'):
            compare_private_frames(self.images, self.reference)

    def test_last_frame_substitution_fails(self):
        (self.images / NAMES[-1]).write_bytes(png(12))
        with self.assertRaisesRegex(ValueError, '^SOURCE_FRAME_CONTENT_MISMATCH$'):
            compare_private_frames(self.images, self.reference)

    def test_extra_reference_file_fails(self):
        (self.reference / 'extra.png').write_bytes(png(10))
        with self.assertRaisesRegex(ValueError, '^SOURCE_FRAME_SET_MISMATCH$'):
            compare_private_frames(self.images, self.reference)

    def test_missing_reference_file_fails(self):
        (self.reference / NAMES[12]).unlink()
        with self.assertRaisesRegex(ValueError, '^SOURCE_FRAME_SET_MISMATCH$'):
            compare_private_frames(self.images, self.reference)

    def test_reference_symlink_fails(self):
        (self.reference / NAMES[2]).unlink()
        (self.reference / NAMES[2]).symlink_to(self.reference / NAMES[1])
        with self.assertRaisesRegex(ValueError, '^SOURCE_FRAME_CONTENT_MISMATCH$'):
            compare_private_frames(self.images, self.reference)

    def replay_stub(self, _archive, target, _manifest):
        out = Path(target) / 'PRIVATE_FRAMES_DO_NOT_UPLOAD'
        out.mkdir(mode=0o700)
        for name in NAMES:
            shutil.copyfile(self.reference / name, out / name)

    def test_fresh_extraction_research_only(self):
        with patch('e002_500_source_replay.extract_frames_local_only',
                   side_effect=self.replay_stub) as f:
            result = verify_against_source(self.packet, 'synthetic-fixture.zip')
        self.assertEqual(f.call_count, 1)
        self.assertEqual(result['status'], 'SOURCE_REPLAY_MATCH')
        self.assertEqual(result['release'], 'BLOCKED')
        self.assertFalse(result['physical_hidden_closure_certified'])

    def test_replay_rejects_post_extraction_swap(self):
        (self.images / NAMES[150]).write_bytes(png(11))
        with patch('e002_500_source_replay.extract_frames_local_only',
                   side_effect=self.replay_stub):
            with self.assertRaisesRegex(ValueError, '^SOURCE_FRAME_CONTENT_MISMATCH$'):
                verify_against_source(self.packet, 'synthetic-fixture.zip')

if __name__ == '__main__':
    unittest.main()
