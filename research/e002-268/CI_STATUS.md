# E002-268 CI and infrastructure

Local replay against a functionally matching E002-267 transcription: PASS. Independent synthetic checker: PASS. Two strict-guard regression tests: PASS locally. A dedicated E002-268 GitHub Actions workflow create attempt was **blocked by connector safety**; no E002-268 workflow ran remotely. Inherited E002-220 source-verification workflow run 39070732994 completed **successfully** for initial E002-268 commit 7a7458c427a0e31c2548dedcfbcaa6e292bb0dd2; this is NOT an E002-268 evaluator replay. Exact original evaluator import on a remote runner is unverified. CI/plumbing is not a scientific failure.

To replay on a clean checkout: `python3 research/e002-268/audit.py`; `python3 research/e002-268/independent_check.py`; `python3 -m unittest discover -s research/e002-268 -p 'test_*.py' -v`. Check `git hash-object research/e002-267/evaluate.py` equals `c97fcdc77ca27235e5dc8186529cdbd3e87f6bd4`.
