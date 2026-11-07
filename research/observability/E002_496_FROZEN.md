# E002-496 | Frozen authentic S01 blinded packet end-to-end integrity test

Date 2026-10-28. Primary E002-371 human-validation track. This is an **authentic-data annotation-handoff feasibility experiment**, not anatomical labeling, camera calibration, or another mathematical bound.

## Motivation and priority correction
E002-495 independently replayed an exact formula already established in E002-421; its claimed novelty was killed. Do not revisit the theorem. E002-492 prepared a local-only dual-rater protocol but did not verify that the **real S01 archive** can actually yield the promised 260 reviewable native PNG files and blinded rater templates end to end.

## Frozen predictions before execution
Use only checksum-verified S01.zip (MD5 fb56109542a13aa7879778833fe4cbaa), without touching S21–S31 held-out anatomy. Invoke the existing E002-492 packet builder with authentic S01.zip on an ephemeral GitHub runner. Do not change the frozen 20 centers, candidate at 5356, 19 controls or 13-frame windows.

P1: exactly 260 distinct 320x288 native PNG files, named only clip_XX_frame_YY.png, will be generated; no missing or empty file. Exactly 20 distinct clip identifiers with 13 frames each.
P2: the two rater templates contain the same 20 blinded clip IDs and 13 frame positions each, but **no source frame indices, candidate bit or owner mapping**. Rater templates start UNREVIEWED. The owner-only manifest is present locally but must never be uploaded or included in an artifact.
P3: a fresh independent integrity checker will reject missing PNGs, bad PNG dimensions, duplicate/out-of-range clip filenames, template candidate/source leaks, invalid private directory, and a wrong 20x13 manifest. The aggregate report contains only counts and hashes of fixed protocol/template structures, no human imagery, per-frame image hashes, image pixels, individual ratings or native source indices.

## Hosted decision
Run the checker first on synthetic file fixtures (adversarial negative controls), then on authentic extracted S01. Publish only a JSON aggregate with technical integrity verdict. A successful packet is **not** proof that human raters can anatomically annotate it or that S01 has authenticated camera timing. Failure remains visible; no retuning or unblinding.

No images or individual annotations in GitHub artifacts or commits. Product ABSTAIN_UNCALIBRATED; release BLOCKED. Hush PR #45 and other Lucent workstreams untouched.
