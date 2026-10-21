# E002-352 — 10-part measurement-science kernel

1. Signal/reference: native RGB manual bilateral 90–100% closure labels versus human-annotated blink intervals on the SAME RGB video; NOT independent high-speed reference.
2. Frontier: Fogelton & Benesova EyeBlink8; 2026 Navascues-Cornago high-speed IR frame-rate study; E002-351 exposure mismatch.
3. Metric: mean fraction of native clean-closure-positive events losing all positive evidence under all m decimation phases.
4. Confounds: gaze, glasses, lighting, eye occlusion, shutter exposure and unverified timestamp units.
5. Model: I_k(x)=Q_k[∫K_k(t)R(x;a(t),r(t),scale(t),gaze(t),lighting(t),glasses(t))dt]+noise. Annotation reduction z_k=1 iff blink_id>=0, NF=LE_NV=RE_NV=X and LE_FC=RE_FC=C. m-fold phase sampling retains frame_id mod m = phase.
6. Falsification: any k>=m consecutive positive frames erased by m-fold decimation refutes combinatorial checker; clip-1 erasure >5% (m2) or >15% (m3) refutes precommitted empirical transfer bands.
7. Exact boundary: k consecutive positives are erased for max(0,m-k) of m phases. k=m-1 -> 1/m, k=m -> 0. Nonconsecutive events require exact residue coverage.
8. Untouched human test: clip 1 not used in preceding 7-clip aggregation; 38 blink IDs, 32 eligible (1 with one clean positive, 7 with two, 24 with >=3). All eligible positives consecutive. Erasure 1/64=1.5625% m2, 9/96=9.375% m3; predeclared broad bands pass. This is CLIP holdout, not verified participant/device holdout.
9. Publication threshold FAIL: no independent reference, no calibrated shutter/clock, no device/participant holdout, no intervention controls, and elementary sampling identity.
10. Product: allow frame-supported blink observations with abstention; reject absence-of-blink inference from missing frames, millisecond duration, pupil waveform and five-second fatigue certification.

Other rates: m4 27/128=21.09375%; m5 53/160=33.125%; m6 82/192=42.70833%. Per-phase erasures m2 [0,1], m3 [4,2,3], m4 [8,6,5,8], m5 [9,9,13,13,9], m6 [16,15,12,11,12,16]. Event-phase pairs are dependent, not independent participants.

Primary annotation protocol: https://www.blinkingmatters.com/research
Source clip 1 immutable Git blob 048ae496568af1c14fb53001917f220829e9039c.
Remote preregistration before outcome access FAILED (two GitHub contents writes blocked); local preregistration SHA256 5dee0291b69f999939e8b00c88ce24708017c0f2fdb8758f72776ae5f691bfe7 was frozen before access. Remote commits postdate outcomes. Do not misrepresent chronology.
