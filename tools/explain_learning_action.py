#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"expected JSON object: {path}")
    return data


def build_explanation(record: dict[str, Any]) -> dict[str, Any]:
    header = record["header"]
    recommendation = record["recommendation"]
    evidence_trace = record["evidence_trace"]
    governance_trace = record["governance_trace"]

    loop_id = header["object_id"]
    explanation_id = "lae_" + loop_id.removeprefix("llr_")

    reason = (
        "This action was recommended because the learning loop links the current "
        "curriculum object to standards, evidence anchors, memory context, search "
        "retrieval, Oracle evaluation records, Moirai governance state, and policy checks."
    )

    return {
        "header": {
            "object_id": explanation_id,
            "object_type": "LearningActionExplanation",
            "object_version": header.get("object_version", "0.1.0"),
            "created_at": header["created_at"],
            "created_by_contributor_id": header["created_by_contributor_id"],
            "created_by_role": "system",
            "status": "draft",
            "policy_tags": ["learning-loop", "explanation", "evidence-first"],
        },
        "learning_loop_record_ref": loop_id,
        "answer": {
            "recommended_action": recommendation["summary"],
            "plain_language_reason": reason,
            "channel": recommendation["channel"],
        },
        "evidence": {
            "standards_refs": evidence_trace.get("standards_refs", []),
            "evidence_anchor_refs": evidence_trace.get("evidence_anchor_refs", []),
            "memory_refs": evidence_trace.get("memory_refs", []),
            "search_refs": evidence_trace.get("search_refs", []),
            "agentplane_run_refs": evidence_trace.get("agentplane_run_refs", []),
        },
        "governance": {
            "oracle_evaluation_refs": governance_trace.get("oracle_evaluation_refs", []),
            "moirai_changeset_refs": governance_trace.get("moirai_changeset_refs", []),
            "policy_check_refs": governance_trace.get("policy_check_refs", []),
        },
    }


def main() -> int:
    if len(sys.argv) not in {2, 3}:
        print("Usage: explain_learning_action.py <learning-loop-record.json> [output.json]", file=sys.stderr)
        return 2

    record = load_json(Path(sys.argv[1]))
    explanation = build_explanation(record)
    output = json.dumps(explanation, indent=2, sort_keys=False) + "\n"

    if len(sys.argv) == 3:
        Path(sys.argv[2]).write_text(output, encoding="utf-8")
    else:
        sys.stdout.write(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
