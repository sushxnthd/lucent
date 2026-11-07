import hashlib
import json
import os
from pathlib import Path
import struct
import tempfile
import unittest
import zlib

from e002_496_packet_integrity import validate


def _png():
    def chunk(tag, data):
        return struct.pack('>I',len(data))+tag+data+struct.pack('>I',zlib.crc32(tag+data)&0xffffffff)
    # Synthetic 320x288 1-bit grayscale PNG, not human imagery.
    raw = b''.join(b'\0'+bytes((i*j+j*3)%256 for j in range(40)) for i in range(288))
    return b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',320,288,1,0,0,0,0))+chunk(b'IDAT',zlib.compress(raw))+chunk(b'IEND',b'')


def _manifest():
    h=lambda s:hashlib.sha256(s.encode('ascii')).hexdigest()
    controls=[]
    for i in sorted(range(6,11994),key=lambda i:h(f'E002-492-control-{i}')):
        if abs(i-5356)<=20 or any(abs(i-j)<20 for j in controls):continue
        controls.append(i)
        if len(controls)==19:break
    centers=sorted([5356]+controls,key=lambda i:h(f'E002-492-blind-{i}'))
    return {'experiment':'E002-492','subject':'S01_CALIBRATION_ONLY',
            'camera_timing_authenticated':False,'review_clips':[
                {'clip':f'clip_{j:02d}','center_native_frame':i,
                 'native_frames':list(range(i-6,i+7)),'candidate':i==5356}
                for j,i in enumerate(centers)]}


def _packet(root):
    root.mkdir(mode=0o700)
    (root/'OWNER_ONLY_MAPPING.json').write_text(json.dumps(_manifest()))
    clips={f'clip_{j:02d}':[
        {'frame':i,'upper_y':None,'lower_y':None,'iris_diameter':None,
         'uncertainty_px':None,'flags':['UNREVIEWED']} for i in range(13)]
        for j in range(20)}
    for r in ('A','B'):
        (root/f'RATER_{r}_TEMPLATE.json').write_text(json.dumps({'experiment':'E002-492','rater':r,'clips':clips}))
    d=root/'PRIVATE_FRAMES_DO_NOT_UPLOAD';d.mkdir(mode=0o700)
    img=_png()
    for j in range(20):
        for i in range(13):
            (d/f'clip_{j:02d}_frame_{i:02d}.png').write_bytes(img)


class PacketIntegrityTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)/'packet'
        _packet(self.root)

    def test_complete_packet(self):
        r=validate(self.root)
        self.assertEqual(r['private_native_png_frames'],260)
        self.assertEqual(r['release'],'BLOCKED')
        self.assertEqual(r['human_anatomical_labels'],0)

    def test_missing_png(self):
        next((self.root/'PRIVATE_FRAMES_DO_NOT_UPLOAD').iterdir()).unlink()
        with self.assertRaises(ValueError):validate(self.root)

    def test_corrupt_geometry(self):
        p=next((self.root/'PRIVATE_FRAMES_DO_NOT_UPLOAD').iterdir())
        b=bytearray(p.read_bytes());b[16:20]=(321).to_bytes(4,'big');p.write_bytes(b)
        with self.assertRaises(ValueError):validate(self.root)

    def test_source_index_filename_leak(self):
        p=next((self.root/'PRIVATE_FRAMES_DO_NOT_UPLOAD').iterdir())
        p.rename(p.with_name('native_5356.png'))
        with self.assertRaises(ValueError):validate(self.root)

    def test_rater_candidate_leak(self):
        p=self.root/'RATER_A_TEMPLATE.json';o=json.loads(p.read_text());o['candidate']=True;p.write_text(json.dumps(o))
        with self.assertRaises(ValueError):validate(self.root)

    def test_rater_prepopulated_label(self):
        p=self.root/'RATER_B_TEMPLATE.json';o=json.loads(p.read_text());o['clips']['clip_00'][0]['upper_y']=10;p.write_text(json.dumps(o))
        with self.assertRaises(ValueError):validate(self.root)

    def test_owner_mapping_tamper(self):
        p=self.root/'OWNER_ONLY_MAPPING.json';o=json.loads(p.read_text());o['review_clips'][0]['candidate']=True;p.write_text(json.dumps(o))
        with self.assertRaises(ValueError):validate(self.root)

    def test_permissions(self):
        if os.name!='nt':
            os.chmod(self.root,0o755)
            with self.assertRaises(ValueError):validate(self.root)

    def test_image_directory_permissions(self):
        if os.name!='nt':
            os.chmod(self.root/'PRIVATE_FRAMES_DO_NOT_UPLOAD',0o755)
            with self.assertRaises(ValueError):validate(self.root)

    def test_symlink_image(self):
        d=self.root/'PRIVATE_FRAMES_DO_NOT_UPLOAD';p=next(d.iterdir());q=d/'link.png';q.symlink_to(p)
        with self.assertRaises(ValueError):validate(self.root)


if __name__=='__main__':unittest.main()
