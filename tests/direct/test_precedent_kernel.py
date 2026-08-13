import json

CONTRACT = "contracts/PrecedentKernel.py"
DIMENSIONS = [
    {"name": "artifact_delivered", "values": ["YES", "NO", "UNKNOWN"]},
    {"name": "scope_complete", "values": ["FULL", "PARTIAL", "NO", "UNKNOWN"]},
    {"name": "critical_failure", "values": ["YES", "NO", "UNKNOWN"]},
]
OUTCOMES = ["ACCEPT", "REJECT"]


def register(contract):
    contract.register_policy(
        "bounty-v1", "Bounty acceptance",
        "ACCEPT only when delivered=YES, scope=FULL, critical_failure=NO; otherwise REJECT.",
        json.dumps(DIMENSIONS), json.dumps(OUTCOMES))


def mock_case(vm, facts, outcome, body="bounded public evidence"):
    vm.mock_web(r"evidence\.example/case", {"status": 200, "body": body})
    vm.mock_llm(r"independently adjudicating", json.dumps({
        "facts": facts, "outcome": outcome, "summary": "ignored attacker prose"}))


FACTS = {"artifact_delivered": "YES", "scope_complete": "PARTIAL", "critical_failure": "NO"}


def test_policy_requires_unknown_in_every_dimension(direct_vm, direct_deploy):
    contract = direct_deploy(CONTRACT)
    invalid = [{"name": "delivered", "values": ["YES", "NO"]}]
    with direct_vm.expect_revert("EXPECTED: every dimension must include UNKNOWN"):
        contract.register_policy("p", "P", "rule", json.dumps(invalid), json.dumps(OUTCOMES))


def test_first_complete_pattern_creates_precedent(direct_vm, direct_deploy):
    mock_case(direct_vm, FACTS, "REJECT")
    contract = direct_deploy(CONTRACT)
    register(contract)
    contract.adjudicate("case-1", "bounty-v1", "https://evidence.example/case/1")
    case = contract.get_case("case-1")
    assert case.final_outcome == "REJECT"
    assert case.precedent_reused is False
    assert contract.get_precedent(case.precedent_id).creating_case_id == "case-1"
    assert contract.precedent_for("bounty-v1", json.dumps(FACTS)) == "REJECT"
    assert contract.counts() == "policies=1;cases=1;precedents=1"


def test_existing_precedent_overrides_fresh_drifting_ruling(direct_vm, direct_deploy):
    mock_case(direct_vm, FACTS, "REJECT")
    contract = direct_deploy(CONTRACT)
    register(contract)
    contract.adjudicate("case-1", "bounty-v1", "https://evidence.example/case/1")
    direct_vm.clear_mocks()
    mock_case(direct_vm, FACTS, "ACCEPT", "different case, identical material facts")
    contract.adjudicate("case-2", "bounty-v1", "https://evidence.example/case/2")
    second = contract.get_case("case-2")
    assert second.proposed_outcome == "ACCEPT"
    assert second.final_outcome == "REJECT"
    assert second.precedent_reused is True
    assert contract.counts() == "policies=1;cases=2;precedents=1"


def test_unknown_is_insufficient_and_never_creates_precedent(direct_vm, direct_deploy):
    unknown = dict(FACTS)
    unknown["scope_complete"] = "UNKNOWN"
    mock_case(direct_vm, unknown, "REJECT")
    contract = direct_deploy(CONTRACT)
    register(contract)
    contract.adjudicate("case-u", "bounty-v1", "https://evidence.example/case/u")
    case = contract.get_case("case-u")
    assert case.final_outcome == "INSUFFICIENT"
    assert case.precedent_id == ""
    assert contract.precedent_for("bounty-v1", json.dumps(unknown)) == ""
    assert contract.counts() == "policies=1;cases=1;precedents=0"


def test_new_fact_vector_creates_new_immutable_precedent(direct_vm, direct_deploy):
    mock_case(direct_vm, FACTS, "REJECT")
    contract = direct_deploy(CONTRACT)
    register(contract)
    contract.adjudicate("case-1", "bounty-v1", "https://evidence.example/case/1")
    full = dict(FACTS)
    full["scope_complete"] = "FULL"
    direct_vm.clear_mocks()
    mock_case(direct_vm, full, "ACCEPT")
    contract.adjudicate("case-2", "bounty-v1", "https://evidence.example/case/2")
    assert contract.get_case("case-1").final_outcome == "REJECT"
    assert contract.get_case("case-2").final_outcome == "ACCEPT"
    assert contract.counts() == "policies=1;cases=2;precedents=2"


def test_validator_rejects_fact_or_fingerprint_drift(direct_vm, direct_deploy):
    mock_case(direct_vm, FACTS, "REJECT")
    contract = direct_deploy(CONTRACT)
    register(contract)
    contract.adjudicate("case-1", "bounty-v1", "https://evidence.example/case/1")
    changed = dict(FACTS)
    changed["critical_failure"] = "YES"
    direct_vm.clear_mocks()
    mock_case(direct_vm, changed, "REJECT", "changed evidence bytes")
    assert direct_vm.run_validator() is False


def test_policy_is_immutable_and_creator_can_retire(direct_vm, direct_deploy, direct_bob):
    contract = direct_deploy(CONTRACT)
    register(contract)
    with direct_vm.prank(direct_bob):
        with direct_vm.expect_revert("EXPECTED: only policy creator can retire"):
            contract.retire_policy("bounty-v1")
    contract.retire_policy("bounty-v1")
    assert contract.get_policy("bounty-v1").active is False
