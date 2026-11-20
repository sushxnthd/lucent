import json
import tempfile
import unittest
from pathlib import Path

from e002_448_blind_annotation import WIDTH, HEIGHT, grayscale_png, aperture
from e002_451_repeat_challenge import create_challenge, mirrored_png, _decode_frozen_png


def pack(root, symmetric=False, tamper=None):
    root=Path(root)
    frames=root/'rater_pack'/'frames'
    frames.mkdir(parents=True)
    image = bytes((x if not symmetric else min(x, WIDTH-1-x)) % 256
                  for y in range(HEIGHT) for x in range(WIDTH))
    other = bytes((x*3+y)%256 for y in range(HEIGHT) for x in range(WIDTH))
    a=grayscale_png(image)
    b=grayscale_png(other)
    (frames/'a.png').write_bytes(a)
    (frames/'ar.png').write_bytes(a)
    (frames/'b.png').write_bytes(b)
    master={'experiment':'E002-448','pilot':'S19','private_blind_key':'secret-not-published',
            'medium_intervals':[1], 'control_intervals':[2],
            'views':[{'view_id':'a','frame_index':0,'repeat':False},
                     {'view_id':'ar','frame_index':0,'repeat':True},
                     {'view_id':'b','frame_index':1,'repeat':False}]}
    if tamper:
        tamper(master)
    (root/'PRIVATE_MASTER_DO_NOT_SHARE.json').write_text(json.dumps(master))
    (root/'rater_pack'/'manifest.json').write_text(json.dumps({'views':[{'view_id':v['view_id'],'image':'frames/'+v['view_id']+'.png'} for v in master['views']]}))
    (root/'rater_pack'/'rater.html').write_text('offline')
    return root


class TestMirrorChallenge(unittest.TestCase):
    def test_original_repeat_is_trivially_hash_linkable_and_challenge_breaks_byte_match(self):
        with tempfile.TemporaryDirectory() as td:
            src=pack(Path(td)/'src')
            self.assertEqual((src/'rater_pack/frames/a.png').read_bytes(),(src/'rater_pack/frames/ar.png').read_bytes())
            summary=create_challenge(src,Path(td)/'dst')
            self.assertEqual(summary['original_hash_linkable_pairs'],1)
            self.assertEqual(summary['challenge_byte_identical_repeat_pairs'],0)
            self.assertNotEqual((Path(td)/'dst/rater_pack/frames/a.png').read_bytes(),(Path(td)/'dst/rater_pack/frames/ar.png').read_bytes())
            self.assertEqual((src/'rater_pack/frames/a.png').read_bytes(),(src/'rater_pack/frames/ar.png').read_bytes())
            self.assertNotIn('secret-not-published',json.dumps(summary))

    def test_mirror_pixels(self):
        img=bytes(x%256 for y in range(HEIGHT) for x in range(WIDTH))
        rows=_decode_frozen_png(mirrored_png(grayscale_png(img)))
        self.assertEqual(rows[0][0],(WIDTH-1)%256)
        self.assertEqual(rows[0][-1],0)

    def test_symmetric_fails_closed(self):
        with tempfile.TemporaryDirectory() as td:
            src=pack(Path(td)/'src',symmetric=True)
            with self.assertRaisesRegex(ValueError,'mirror-symmetric'):
                create_challenge(src,Path(td)/'dst')
            self.assertFalse((Path(td)/'dst').exists())

    def test_overwrite_fails_closed(self):
        with tempfile.TemporaryDirectory() as td:
            src=pack(Path(td)/'src')
            dest=Path(td)/'dst';dest.mkdir()
            with self.assertRaises(FileExistsError):create_challenge(src,dest)

    def test_tampered_repeat_mapping_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            src=pack(Path(td)/'src',tamper=lambda m:m['views'][2].update({'repeat':True}))
            with self.assertRaisesRegex(ValueError,'invalid repeat mapping'):
                create_challenge(src,Path(td)/'dst')

    def test_missing_frame_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            src=pack(Path(td)/'src')
            (src/'rater_pack/frames/b.png').unlink()
            with self.assertRaisesRegex(ValueError,'missing PNG'):
                create_challenge(src,Path(td)/'dst')

    def test_bad_crc_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            src=pack(Path(td)/'src')
            p=src/'rater_pack/frames/ar.png'
            d=bytearray(p.read_bytes());d[-9]^=1;p.write_bytes(d)
            with self.assertRaises(ValueError):create_challenge(src,Path(td)/'dst')

    def test_aperture_mirror_invariance(self):
        # Display-space left/right labels swap after reflection; U and D are reflected.
        points={'L':(40,130),'R':(230,145),'U':(131,122),'D':(139,160)}
        rec={'status':'valid','flags':[],'points':points}
        a=aperture(rec)
        self.assertIsNotNone(a)
        mirror=lambda p:(WIDTH-1-p[0],p[1])
        m={'L':mirror(points['R']),'R':mirror(points['L']),
           'U':mirror(points['U']),'D':mirror(points['D'])}
        b=aperture({'status':'valid','flags':[],'points':m})
        self.assertAlmostEqual(a,b,delta=1e-12)

    def test_no_private_fields_in_summary(self):
        with tempfile.TemporaryDirectory() as td:
            src=pack(Path(td)/'src')
            summary=create_challenge(src,Path(td)/'dst')
            self.assertNotIn('private_blind_key',summary)
            self.assertNotIn('frame_index',json.dumps(summary))
            self.assertEqual(summary['product_claim'],'ABSTAIN_UNCALIBRATED')


if __name__=='__main__':
    unittest.main()
