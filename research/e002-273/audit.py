#!/usr/bin/env python3
"""E002-273: fail-closed primary-source AFFEC v2 modality audit.

--online verifies exact upstream Git blob bytes. --offline only checks local
code and mock-file classification, and MUST NOT assert upstream verification.
"""
import argparse
import ast
import hashlib
import json
import pathlib
import tempfile
import urllib.request

HERE = pathlib.Path(__file__).resolve().parent
COMMIT = 'f1759103f501282a41a04d6b474a3e89d6f36a6b'
SOURCES = {
    'data/raw/README.md': '3cbb2b243fe934eb42ba0a28b1c5dc9dd4cba365',
    'scripts/prepare_zenodo_upload.py': '1b29a7e7b4646c7674ab48e23a7326761da79bb2',
}
EXPECTED_ARCHIVE_MD5 = 'b7efc90ca02bc4e571fa90fe2634f0f4'
PATTERN = 'sub-*/beh/*_recording-videostream_physio.*'

def git_blob_sha(payload):
    return hashlib.sha1(b'blob ' + str(len(payload)).encode() + b'\0' + payload).hexdigest()

def fetch_verified(path, expected):
    url = 'https://raw.githubusercontent.com/itubrainlab/AFFEC/' + COMMIT + '/' + path
    req = urllib.request.Request(url, headers={'User-Agent': 'Lucent-E002-273/1.0'})
    with urllib.request.urlopen(req, timeout=35) as response:
        data = response.read(1_000_000)
    actual = git_blob_sha(data)
    if actual != expected:
        raise ValueError('UPSTREAM_BLOB_SHA_MISMATCH:' + path)
    return data.decode('utf-8')

def extract_glob(script):
    tree = ast.parse(script)
    matches = [n for n in ast.walk(tree) if isinstance(n, ast.Call)
               and isinstance(n.func, ast.Attribute) and n.func.attr == 'glob'
               and n.args and isinstance(n.args[0], ast.Constant)
               and isinstance(n.args[0].value, str)
               and 'recording-videostream' in n.args[0].value]
    if len(matches) != 1:
        raise ValueError('UNEXPECTED_GLOB_STRUCTURE')
    return matches[0].args[0].value

def wildcard_probe(pattern):
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        directory = root / 'sub-test' / 'beh'
        directory.mkdir(parents=True)
        for suffix in ['json', 'tsv.gz', 'mp4']:
            (directory / ('sub-test_task-fer_run-0_recording-videostream_physio.' + suffix)).write_bytes(b'fixture')
        found = {p.name.rsplit('.', 1)[-1] for p in root.glob(pattern)}
        return {'mock_json_selected': 'json' in found,
                'mock_tsvgz_selected': 'gz' in found,
                'mock_mp4_selected': 'mp4' in found}

def run(online):
    result = {
        'run': 'E002-273', 'source': '10.5281/zenodo.19408373',
        'upstream_repository': 'itubrainlab/AFFEC', 'upstream_commit': COMMIT,
        'source_git_blob_shas': SOURCES,
        'publisher_v2_videostream_md5_unverified': EXPECTED_ARCHIVE_MD5,
        'upstream_source_bytes_verified': False,
        'archive_bytes_verified': False, 'archive_member_listing_verified': False,
        'raw_rgb_eye_frames_verified': False, 'same_eye_reference_verified': False,
        'clock_alignment_verified': False, 'human_waveform_evaluated': False,
        'documented_modality': 'face-derived features in JSON/TSV.gz',
        'documented_v2_repaired_sidecars': 91,
        'documented_v2_forced_surrogate_sidecars': 22,
        'documented_v2_affected_subjects': 24,
        'decision': 'REJECT_FOR_RGB_WAVEFORM_CERTIFICATION_PENDING_RAW_RGB_PROOF',
        'wildcard_probe': wildcard_probe(PATTERN),
    }
    if online:
        try:
            sources = {p: fetch_verified(p, sha) for p, sha in SOURCES.items()}
            script = sources['scripts/prepare_zenodo_upload.py']
            readme = sources['data/raw/README.md']
            actual_pattern = extract_glob(script)
            if actual_pattern != PATTERN:
                raise ValueError('UPSTREAM_PATTERN_CHANGED')
            for marker in ['715', '91 JSON sidecars', '22', '24 subjects',
                           'Facial Action Units', 'TSV']:
                if marker not in readme:
                    raise ValueError('README_MARKER_MISSING:' + marker)
            if 'Contains every' not in script or 'tsv.gz' not in script:
                raise ValueError('ARCHIVE_DOCSTRING_MISMATCH')
            result['upstream_source_bytes_verified'] = True
            result['source_provenance_status'] = 'PINNED_BLOBS_VERIFIED'
        except Exception as exc:
            result['source_provenance_status'] = 'UNVERIFIED_ACCESS_OR_SOURCE'
            result['source_error'] = type(exc).__name__ + ':' + str(exc)[:180]
    else:
        result['source_provenance_status'] = 'CONNECTOR_OBSERVED_BLOB_IDS_NOT_REPLAYED'
    result['wildcard_nonexclusion'] = result['wildcard_probe']['mock_mp4_selected']
    result['source_only_excludes_rgb_archive_members'] = False
    return result

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--online', action='store_true')
    args = parser.parse_args()
    result = run(args.online)
    (HERE / 'RESULTS.json').write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(json.dumps(result, sort_keys=True))
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
