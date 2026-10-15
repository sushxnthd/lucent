# E002-205 exact-source provenance
- E002-204 source Git blob SHA1: d7cfbea86c38f98bcdceac12ac16b04127bbef88.
- Local reconstruction of source bytes yielded the same Git blob SHA1, independently of the connector.
- Local synthetic replay of actual E002-204 trial() function: 9/9 expected cases passed, four original-gate false acceptances.
- Local independent checker: 9/9 case SHA256s, exact edge arithmetic, exhaustive sharp bound n<=10: PASS.
- Adversarial mutation changing an expected edge rejection to acceptance: checker REJECTED.
- Human TSV downloaded in E002-205: NO. Human physiology, RGB observability, device holdouts: NOT TESTED.
- GitHub CI execution: UNKNOWN; GitHub connector commit-run lookup filters pull_request events, so zero returned runs cannot establish absence of push-triggered workflow.
- Dataset MD5 from E002-203 source: 5e04a7b5e50f7508775e1daea527246b; metadata 369d9446b62fd00888a6d51e152697bd. No source dataset bytes claimed here.
- Smallest supported claim: E002-204's internal-gap-only gate can accept 5-second 120-Hz reference windows with >250 ms boundary censoring. The boundary-inclusive gate rejects these deterministic cases.
