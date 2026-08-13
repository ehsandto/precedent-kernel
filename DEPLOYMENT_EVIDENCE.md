# StudioNet deployment and live proof

- Contract: https://explorer-studio.genlayer.com/address/0x59422e4f6Ef82FA8ecEe6396D872a806eDDF908F
- Deployment: https://explorer-studio.genlayer.com/tx/0xf28e2f55f3d67d7508654bba33f64d3b0c2582274c97c58d44fa8ee31226cc0b
- Source SHA-256: `3a2ec5fa1d45e207def9bb0ea08d286f1dd08edcd5a6e9389a46dcdf5835e28b`
- Policy registration: https://explorer-studio.genlayer.com/tx/0x75f03429ecd27485aac1f09eddc92f118606ff212ac5ec83dc09425b141030e8
- Precedent creation: https://explorer-studio.genlayer.com/tx/0x5f1fab1c7120dc1b8c0197ca24f3da6ec369e2ebc9b023801f2e8296703a5599
- Deterministic reuse: https://explorer-studio.genlayer.com/tx/0xcb7e5e9e0be69609f20a9c915591a7f656773fb26bc14b8db285df2fbf315777

All transactions finalized with `MAJORITY_AGREE`. Explorer source exactly
matches the repository contract.

Both cases independently produced the canonical facts:

```json
{"artifact_delivered":"YES","critical_failure":"NO","scope_complete":"PARTIAL"}
```

Case A proposed and finalized `REJECT`, creating precedent
`4c094031e4332eb5d46407067394e79b8e5c9e508b58089fd20e7749d93115c2`.
Case B used different evidence bytes and proposed `ACCEPT`, but stored
`precedent_reused=true` and finalized `REJECT` under the same pattern hash.

Final state: `policies=1;cases=2;precedents=1`.
