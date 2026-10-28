# E002-500 | Human annotation packet source-binding falsification

Date: 2026-10-28. Frozen prediction: [E002_500_FROZEN.md](E002_500_FROZEN.md). This is an **evidence-chain falsification** and an instrument-integrity repair, not new physiology, a new theorem, or real anatomical annotation.

## Scientific issue

The previous E002-496 checker attested `TECHNICAL_PACKET_INTEGRITY_PASS` after checking the manifest, 260 filenames, PNG headers, image geometry, rater templates and permissions. It **did not bind the pixels in the review packet to the pinned S01 archive**. A syntactically valid 320x288 PNG with unrelated image content would satisfy those checks. Consequently the previous status must not be interpreted as independently authenticated image content or a valid source-to-rating chain.

## Frozen adversarial experiment

The preregistered attack constructs 260 syntactically valid synthetic grayscale PNGs and the actual frozen E002-492 manifest/templates. It predicts the old E002-496 checker will accept the forged packet, even after changing one image to a different valid PNG, whereas the new source replay must reject it.

Nine software tests exercise the legacy acceptance prediction, source replay success, first/last-frame substitution, extra/missing frames, symlink substitution, independent extraction invocation and post-extraction tampering. **Hosted verification:** [E002-500 run 40622624177](https://github.com/sushxnthd/lucent/actions/runs/40622624177) completed the **nine synthetic adversarial tests successfully**, including the frozen prediction that the old E002-496 checker accepts a complete forged packet and a single valid-PNG substitution while the source-bound comparator rejects it. The authentic S01 replay stage was still running at the latest check; no authentic replay success is claimed yet.

## New source-bound evidence gate

`e002_500_source_replay.py` first runs the old structural checker. It then **re-extracts all 260 frames from the MD5-pinned S01.zip in a fresh private directory** using the existing native FFmpeg extraction path, comparing each resulting PNG byte-for-byte to the proposed rater packet. Any mismatch fails closed without printing source indices, image bytes or hashes. The hosted workflow downloads the authentic archive and performs the private replay, publishing only an aggregate status. The second extraction uses the same decoder and source; it is an independent extraction pass, **not** independent decoder validation or physical camera timing.

If the hosted authentic replay succeeds, it establishes only `SOURCE_BOUND_PACKET_ONLY` for the newly generated ephemeral packet. It does not retroactively authenticate any separately copied packet; that packet must itself be rechecked before raters use it. The private frames are deleted on the runner and are not available for remote human review.

## Completion gate

No human anatomical ratings, independently authenticated camera clock, calibrated shutter or certified continuous-time eyelid velocity bound were obtained. No participant-disjoint physical prediction has been tested. The E002-491 motion proxy remains rejected under jitter/subsampling. E002-371 stays `ABSTAIN_UNCALIBRATED`; release `BLOCKED`.

Next: verify the hosted source-replay result, then obtain **two genuinely independent, blinded human anatomical review sheets** on a locally reverified packet. Do not substitute further provenance or software work for those human observations. Hush PR #45 and the hourly primary workflow remain unchanged.
