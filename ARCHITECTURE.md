# Architecture

1. A creator registers an immutable policy version with bounded dimensions and outcomes.
2. Every dimension must explicitly admit `UNKNOWN`.
3. A case points to public HTTPS evidence.
4. Every validator independently fetches the evidence and reproduces the exact candidate.
5. The contract computes the fact-pattern SHA-256 from policy ID and canonical facts.
6. UNKNOWN yields `INSUFFICIENT`; an existing key reuses precedent; a new complete key creates it.
7. Cases and precedents are immutable. A changed policy requires a new policy ID.

The frontend owns presentation and indexing. The contract owns evidence
normalization, consensus, precedent identity, immutable decisions, and reads.
