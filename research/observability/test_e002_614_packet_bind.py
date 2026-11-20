"""E002-614 private-packet integrity tests with synthetic PNGs only."""
import copy
import tempfile
import unittest
from pathlib import Path
from PIL import Image
from e002_614_packet_bind import bind, verify, audit, packet_hash

class PacketBindingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.root = Path(cls.tmp.name)
        cls.clips = {}
        for c in range(10):
            name = f'clip_{c:04d}'
            cls.clips[name] = [dict(frame=i,upper_y=None,lower_y=None,iris_diameter=None,uncertainty_px=None,flags=['UNREVIEWED']) for i in range(6)]
            folder = cls.root / 'clips' / name
            folder.mkdir(parents=True)
            for i in range(6):
                Image.new('RGB',(640,480),(c*11,i*21,17)).save(folder/f'frame_{i:02d}.png')
        cls.template = {'experiment':'E002-595','rater':'A','arm':'ARM_0','clips':cls.clips}
        cls.bound = bind(cls.template, cls.root)
    @classmethod
    def tearDownClass(cls): cls.tmp.cleanup()
    def test_exact_packet(self):
        digest, keys = verify(self.bound, self.root)
        self.assertEqual(digest,self.bound['packet_sha256'])
        self.assertEqual(len(keys),60)
    def test_packet_hash_stable(self):
        self.assertEqual(packet_hash(dict(reversed(list(self.bound['frame_sha256'].items())))),self.bound['packet_sha256'])
    def test_changed_frame_rejected(self):
        path=self.root/'clips/clip_0000/frame_00.png'
        original=path.read_bytes()
        try:
            Image.new('RGB',(640,480),(255,0,0)).save(path)
            with self.assertRaisesRegex(ValueError,'SOURCE_FRAME_SUBSTITUTION'):verify(self.bound,self.root)
        finally:path.write_bytes(original)
    def test_changed_manifest_rejected(self):
        t=copy.deepcopy(self.bound);t['frame_sha256']['clip_0000::0']='0'*64
        with self.assertRaisesRegex(ValueError,'INVALID_PACKET_DIGEST'):verify(t,self.root)
    def test_unbound_rejected(self):
        with self.assertRaisesRegex(ValueError,'INVALID_FRAME_HASH_MANIFEST'):verify(self.template,self.root)
    def test_missing_image_rejected(self):
        path=self.root/'clips/clip_0000/frame_00.png'; other=path.with_suffix('.tmp');path.rename(other)
        try:
            with self.assertRaisesRegex(ValueError,'MISSING_OR_EXTRA_PNG'):verify(self.bound,self.root)
        finally:other.rename(path)
    def test_valid_export_audit(self):
        ratings={k:copy.deepcopy(v) for k,v in self.template.items()}
        ratings['source_integrity']={'status':'SHA256_PACKET_MATCH','packet_sha256':self.bound['packet_sha256']}
        self.assertEqual(audit(self.bound,self.root,ratings)['frames'],60)
    def test_unbound_export_rejected(self):
        ratings={k:copy.deepcopy(v) for k,v in self.template.items()}
        ratings['source_integrity']={'status':'UNBOUND_DEMONSTRATION_ONLY','packet_sha256':None}
        with self.assertRaisesRegex(ValueError,'UNBOUND_OR_WRONG_RATER_EXPORT'):audit(self.bound,self.root,ratings)
    def test_extra_image_rejected(self):
        p=self.root/'clips/clip_0000/extra.png';p.write_bytes(b'bad')
        try:
            with self.assertRaisesRegex(ValueError,'MISSING_OR_EXTRA_PNG'):verify(self.bound,self.root)
        finally:p.unlink()

if __name__=='__main__':unittest.main()
