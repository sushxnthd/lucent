#!/usr/bin/env python3
"""E002-274 EVE published loader sampling eligibility audit; NOT human validation."""
import argparse,ast,hashlib,json,pathlib,urllib.request
UPSTREAM='82757eb2ffb4dd198db36dbfea71601098b597f0'
FILES={
'src/core/config_default.py':'34e4b2fe80f52ae734b2c462c1f3e3324a375edb',
'src/datasources/eve_sequences.py':'8b03f60068cc40f2d2ffacac46a1638a31e2117d',
'src/datasources/common.py':'a03d78504526532f8c8a894ca082f7d6037f59cf'}
# OFFLINE IS A FIXTURE ONLY, NOT INDEPENDENT SOURCE VERIFICATION.
FIXTURE={
'src/core/config_default.py':"class DefaultConfig:\n    assumed_frame_rate = 10\n    max_sequence_len = 30\n",
'src/datasources/eve_sequences.py':"source_to_fps = {'screen': 30, 'basler': 60, 'webcam_l': 30, 'webcam_c': 30, 'webcam_r': 30}\nindex_interval = int(fps / config.assumed_frame_rate)\npicked_indices = list(range(start_index, end_index, index_interval))\n",
'src/datasources/common.py':"if self.video_path.endswith('_eyes.mp4'):\n    self.timestamps_path = video_path.replace('_eyes.mp4', '.timestamps.txt')\nelif self.video_path.endswith('_face.mp4'):\n    self.timestamps_path = video_path.replace('_eyes.mp4', '.timestamps.txt')\n"}
def blob_sha(data):
    return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
def sources(online):
    if not online:return FIXTURE.copy(),False,{k:None for k in FILES}
    found,hashes={},{}
    for path,expected in FILES.items():
        url=f'https://raw.githubusercontent.com/swook/EVE/{UPSTREAM}/{path}'
        with urllib.request.urlopen(url,timeout=45) as resp:data=resp.read()
        got=blob_sha(data)
        if got!=expected:raise RuntimeError(f'source mismatch {path}: {got} != {expected}')
        found[path]=data.decode('utf-8');hashes[path]=got
    return found,True,hashes
def constant(tree,name):
    for node in ast.walk(tree):
        if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id==name for t in node.targets):
            try:return ast.literal_eval(node.value)
            except (ValueError,TypeError):pass
    raise ValueError('constant not found: '+name)
def inspect(s):
    cfg=s['src/core/config_default.py'];loader=s['src/datasources/eve_sequences.py'];common=s['src/datasources/common.py']
    hz=constant(ast.parse(cfg),'assumed_frame_rate')
    fps=constant(ast.parse(loader),'source_to_fps')
    for needle in ['index_interval = int(fps / config.assumed_frame_rate)','picked_indices = list(range(start_index, end_index, index_interval))']:
        if needle not in loader:raise RuntimeError('frame selection changed: '+needle)
    assert hz==10 and fps['basler']==60 and fps['webcam_c']==30
    stride=int(fps['basler']/hz);indices=list(range(0,60,stride))
    assert indices==list(range(0,60,6))
    def aperture(t):return 1.0-0.8*max(0.0,1.0-abs(t-0.05)/0.02)
    raw=[aperture(i/60) for i in range(60)];down=[raw[i] for i in indices]
    assert min(raw)<0.5 and min(down)==1.0
    return dict(raw_basler_hz=60,published_loader_hz=hz,published_loader_basler_stride=stride,
      basler_frames_per_second=60,published_loader_frames_per_second=len(indices),
      discarded_frame_fraction=(60-len(indices))/60,loader_nyquist_hz=hz/2,
      selected_frame_indices_first_second=indices,synthetic_blink_like_event_width_ms=40,
      synthetic_raw_min_aperture=round(min(raw),6),synthetic_downsampled_min_aperture=round(min(down),6),
      face_timestamp_suffix_issue_in_source=("_face.mp4" in common and "video_path.replace('_eyes.mp4', '.timestamps.txt')" in common),
      physiological_waveform_tested=False,product_gate='REJECT_10HZ_PUBLISHED_LOADER_FOR_60HZ_WAVEFORM_CERTIFICATION',
      smallest_supported_claim='EVE published default training loader selects 1 in 6 Basler frames; it is not the native 60-Hz evaluation stream.')
def main():
    p=argparse.ArgumentParser();p.add_argument('--online',action='store_true');p.add_argument('--output',default='RESULTS.json')
    a=p.parse_args()
    try:
        s,verified,hashes=sources(a.online);r=inspect(s)
        r.update(run='E002-274',upstream_commit=UPSTREAM,source_bytes_verified=verified,
          source_blob_sha_actual=hashes,source_blob_sha_expected=FILES,
          result_kind='primary_source_replay' if verified else 'offline_fixture_replay',human_waveform_result=False)
    except Exception as exc:
        r=dict(run='E002-274',status='SOURCE_VERIFICATION_BLOCKED',error_type=type(exc).__name__,
               error=str(exc),source_bytes_verified=False,human_waveform_result=False)
    pathlib.Path(a.output).write_text(json.dumps(r,sort_keys=True,indent=2)+'\n')
    print(json.dumps(r,sort_keys=True,indent=2))
    if r.get('status')=='SOURCE_VERIFICATION_BLOCKED':raise SystemExit(2)
if __name__=='__main__':main()
