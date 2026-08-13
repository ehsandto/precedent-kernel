import { createAccount, createClient } from "genlayer-js";
import { studionet } from "genlayer-js/chains";
import { TransactionStatus } from "genlayer-js/types";

const address = process.env.CONTRACT_ADDRESS as `0x${string}` | undefined;
const evidenceCommit = process.env.EVIDENCE_COMMIT;
if (!address || !evidenceCommit) throw new Error("Set CONTRACT_ADDRESS and EVIDENCE_COMMIT.");
const contractAddress = address;
const suffix = process.env.PROOF_SUFFIX ?? String(Date.now());
const policyId = `precedent-demo-v1-${suffix}`;
const firstCaseId = `precedent-create-${suffix}`;
const secondCaseId = `precedent-reuse-${suffix}`;
const base = `https://raw.githubusercontent.com/ehsandto/precedent-kernel/${evidenceCommit}/evidence`;
const account = createAccount();
const client = createClient({ chain: studionet, account });

async function write(functionName: string, args: any[]) {
  const hash = await client.writeContract({ address: contractAddress, functionName, args, account, value: 0n });
  console.log(`${functionName}=${hash}`);
  const receipt = await client.waitForTransactionReceipt({
    hash: hash as never, status: TransactionStatus.FINALIZED, interval: 5000, retries: 180,
  }) as any;
  const executions = receipt.consensus_data?.leader_receipt ?? [];
  const fatal = executions.filter((item: any) => item.execution_result !== "SUCCESS" &&
    item.genvm_result?.error_code !== "CONSENSUS_VALIDATOR_QUORUM_REACHED");
  if (receipt.result_name !== "MAJORITY_AGREE" || fatal.length) {
    throw new Error(`${functionName} failed: ${JSON.stringify({ hash, consensus: receipt.result_name, fatal })}`);
  }
  return { hash, status: receipt.status_name, consensus: receipt.result_name,
    explorer: `https://explorer-studio.genlayer.com/tx/${hash}` };
}

const dimensions = [
  { name: "artifact_delivered", values: ["YES", "NO", "UNKNOWN"] },
  { name: "scope_complete", values: ["FULL", "PARTIAL", "NO", "UNKNOWN"] },
  { name: "critical_failure", values: ["YES", "NO", "UNKNOWN"] },
];
const policy = await write("register_policy", [
  policyId,
  "Precedent reuse demonstration",
  "Extract the three material facts exactly. For this public demonstration, proposed_outcome is the evidence page's explicit submitted disposition. This lets the contract prove that an existing precedent overrides later disposition drift.",
  JSON.stringify(dimensions), JSON.stringify(["ACCEPT", "REJECT"]),
]);
const first = await write("adjudicate", [firstCaseId, policyId, `${base}/case-reject.md`]);
const firstState = await client.readContract({ address: contractAddress, functionName: "get_case", args: [firstCaseId] }) as any;
const second = await write("adjudicate", [secondCaseId, policyId, `${base}/case-accept.md`]);
const [secondState, counts, precedent] = await Promise.all([
  client.readContract({ address: contractAddress, functionName: "get_case", args: [secondCaseId] }),
  client.readContract({ address: contractAddress, functionName: "counts", args: [] }),
  client.readContract({ address: contractAddress, functionName: "get_precedent", args: [firstState.fact_pattern_hash] }),
]);
console.log(JSON.stringify({
  contractAddress, evidenceCommit, policyId, firstCaseId, secondCaseId,
  policy, first, second, firstState, secondState, precedent, counts,
}, null, 2));
