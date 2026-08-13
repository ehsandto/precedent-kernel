# Portal submission

## Title

PrecedentKernel — Consensus Once, Deterministic Precedent Thereafter

## Notes

PrecedentKernel is a reusable semantic-adjudication primitive. Policy creators define immutable bounded material dimensions and allowed outcomes; every dimension must include UNKNOWN. For a new case, validators independently fetch public HTTPS evidence and require exact agreement on its SHA-256 fingerprint, complete canonical fact vector, UNKNOWN status and proposed ruling. The contract hashes policy ID plus canonical facts. A new complete pattern creates an immutable precedent; an existing pattern deterministically reuses its ruling even if a fresh model proposes differently. Any UNKNOWN fact yields INSUFFICIENT and cannot create precedent. No summaries, confidence tolerances, caller hashes or similarity judgments enter state. Policies and precedents cannot mutate; new interpretation requires policy-v2. Direct tests cover ruling drift, UNKNOWN suppression, new-pattern isolation, fingerprint disagreement, access control and repository discovery.
