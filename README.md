# PrecedentKernel

PrecedentKernel is a standalone GenLayer primitive that converts previously
finalized semantic adjudication into deterministic future behavior.

## Consensus once, deterministic precedent thereafter

For each case, the leader and validators independently fetch the exact HTTPS
evidence, hash its normalized bytes, reconstruct every bounded material fact,
and propose an allowed outcome. Consensus requires exact equality of the full
fact vector, proposed outcome, UNKNOWN flag, and SHA-256 evidence fingerprint.

The contract computes:

`sha256("precedentkernel-v1" | policy_id | canonical_facts_json)`

If that key already exists, its immutable outcome overrides the new proposal.
Otherwise a complete fact vector creates a new precedent. Any `UNKNOWN` fact
forces `INSUFFICIENT` and cannot create precedent.

There are no summaries, similarity thresholds, confidence tolerances, mutable
precedents, or caller-supplied hashes. Policy changes require a new policy ID.

## Reusable applications

Bounty acceptance, marketplace disputes, DAO enforcement, agent-task review,
grant milestones, moderation, claims, and compliance decisions.

## Validation

```bash
genvm-lint check contracts/PrecedentKernel.py --json
pytest tests/direct -q
npm run check:discovery
npm run typecheck
```

See [ARCHITECTURE.md](ARCHITECTURE.md), [SECURITY.md](SECURITY.md), and
[SUBMISSION.md](SUBMISSION.md).

## StudioNet proof

- [Deployed contract](https://explorer-studio.genlayer.com/address/0x59422e4f6Ef82FA8ecEe6396D872a806eDDF908F)
- [Precedent creation](https://explorer-studio.genlayer.com/tx/0x5f1fab1c7120dc1b8c0197ca24f3da6ec369e2ebc9b023801f2e8296703a5599)
- [Conflicting proposal deterministically reused precedent](https://explorer-studio.genlayer.com/tx/0xcb7e5e9e0be69609f20a9c915591a7f656773fb26bc14b8db285df2fbf315777)

See [DEPLOYMENT_EVIDENCE.md](DEPLOYMENT_EVIDENCE.md) for exact stored state and
source verification.
