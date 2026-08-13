# Portal submission

## Title

PrecedentKernel — Consensus Once, Deterministic Precedent Thereafter

## Notes

PrecedentKernel is a reusable semantic-adjudication primitive. Policy creators define immutable bounded material dimensions and allowed outcomes; every dimension must include UNKNOWN. For a new case, validators independently fetch public HTTPS evidence and require exact agreement on its SHA-256 fingerprint, complete canonical fact vector, UNKNOWN status and proposed ruling. The contract hashes policy ID plus canonical facts. A new complete pattern creates an immutable precedent; an existing pattern deterministically reuses its ruling even if a fresh model proposes differently. Any UNKNOWN fact yields INSUFFICIENT and cannot create precedent. No summaries, confidence tolerances, caller hashes or similarity judgments enter state. Policies and precedents cannot mutate; new interpretation requires policy-v2. Direct tests cover ruling drift, UNKNOWN suppression, new-pattern isolation, fingerprint disagreement, access control and repository discovery.

## Evidence

- Repository: https://github.com/ehsandto/precedent-kernel
- Contract: https://explorer-studio.genlayer.com/address/0x59422e4f6Ef82FA8ecEe6396D872a806eDDF908F
- Deployment: https://explorer-studio.genlayer.com/tx/0xf28e2f55f3d67d7508654bba33f64d3b0c2582274c97c58d44fa8ee31226cc0b
- Precedent creation: https://explorer-studio.genlayer.com/tx/0x5f1fab1c7120dc1b8c0197ca24f3da6ec369e2ebc9b023801f2e8296703a5599
- Precedent reuse: https://explorer-studio.genlayer.com/tx/0xcb7e5e9e0be69609f20a9c915591a7f656773fb26bc14b8db285df2fbf315777
