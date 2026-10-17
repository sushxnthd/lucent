# E002-255 provenance and license

- Upstream EyeDentify: Shah, Watanabe, Moser, Dengel, 2024/2025. 51 participants; RGB eye crops plus Tobii pupil labels; 30 fps webcam, 90 Hz tracker. Papers https://arxiv.org/abs/2407.11204v1 and https://arxiv.org/abs/2407.11204v2 .
- Public independent reproduction: CondadosAI/pupil-diameter-webcam, pinned commit aa9bddf498a3b6e4104c2c000d2cc0c06a816aae (2026-08-25). Derived human participant summaries; not raw video and not Lucent-collected measurements.
- Source Git blob SHA1: left 509e14d61455dc6ee119a0fc2ba9e7448eedc9fc; right 9f55dd52fc6c11c9903ec9c7b0c735192cd4a790; pooled summary 4d51cd922ce11aa040cfc491bce09bab249d5ede.
- `audit.py` downloads three immutable raw GitHub files, independently verifies Git blob identity from bytes, records SHA-256, and recomputes participant metrics. `independent_check.py` re-fetches and recomputes with a separate implementation; `test_identity.py` checks the least-squares identity on synthetic pairs. Workflow must execute real source fetch and upload derived evidence; static CI is not sufficient.
- EyeDentify data and released checkpoints: CC BY-NC 4.0; no raw human eye crops or model weights redistributed. Research-only use; any future commercial deployment requires separate rights and validation.
- Predecessor: research/e002-254-native-reference-clock-certification at 72b7846c54ec7b6fa54c10afa20b32921a66ebc4. EOTT clock certification remains unresolved.
