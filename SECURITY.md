# Security invariants

- Validators independently fetch evidence; the leader cannot supply source data.
- Evidence fingerprints, complete facts, UNKNOWN status, and proposed outcome match exactly.
- Every stored semantic value is exact consensus output or deterministic derivation.
- Caller-provided summaries, hashes, confidence values, and similarity claims are ignored.
- SHA-256 keys bind policy version and canonical complete facts.
- UNKNOWN never creates precedent.
- Existing precedents cannot mutate; fresh LLM drift cannot change their outcome.
- Public HTTPS/DNS checks exclude localhost, IP literals, userinfo, and malformed authorities.
- Repository discovery must identify exactly one deployable Python contract.
