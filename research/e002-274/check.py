#!/usr/bin/env python3
"""Independent arithmetic/provenance checker, including three mutations."""
import json,math,pathlib,sys
r=json.loads(pathlib.Path(sys.argv[1] if len(sys.argv)>1 else 'RESULTS.json').read_text())
def check(x):
    assert x['run']=='E002-274'
    assert x['raw_basler_hz']==60 and x['published_loader_hz']==10
    assert x['published_loader_basler_stride']==6
    assert x['selected_frame_indices_first_second']==[6*i for i in range(10)]
    assert math.isclose(x['discarded_frame_fraction'],5/6,abs_tol=1e-14)
    assert x['loader_nyquist_hz']==5
    assert x['synthetic_raw_min_aperture']<0.5 and x['synthetic_downsampled_min_aperture']==1.0
    assert x['human_waveform_result'] is False
    assert x['result_kind'] in ('offline_fixture_replay','primary_source_replay')
    assert x['source_bytes_verified'] is (x['result_kind']=='primary_source_replay')
    if x['source_bytes_verified']:assert x['source_blob_sha_actual']==x['source_blob_sha_expected']
check(r)
for mutation in ({'published_loader_hz':60},{'source_bytes_verified':True},{'synthetic_downsampled_min_aperture':0.2}):
    try:check({**r,**mutation})
    except AssertionError:continue
    raise AssertionError('Mutation escaped independent checker')
print('E002-274 checker passed; three mutations rejected')
