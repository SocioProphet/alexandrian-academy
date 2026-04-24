#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from explain_learning_action import load_json


def build_search_record(explanation: dict[str, Any]) -> dict[str, Any]:
    header = explanation["header"]
    answer = explanation["answer"]
    evidence = explanation["evidence"]
    governance = explanation["governance"]
    explanation_id = header["object_id"]
    loop_ref = explanation["learning_loop_record_ref"]

    governance_refs: list[str] = []
    governance_refs.extend(governance.get("oracle_evaluation_refs", []))
    governance_refs.extend(governance.get("moirai_changeset_refs", []))
    governance_refs.extend(governance.get("policy_check_refs", []))

    return {
        "header": {
            "object_id": "lsr_" + explanation_id.removeprefix("lae_"),
            "object_type": "LearningSearchRecord",
            "object_version": header.get("object_version", "0.1.0"),
            "created_at": header["created_at"],
            "created_by_contributor_id": header["created_by_contributor_id"],
            "created_by_role": "system",
            "status": "draft",
            "policy_tags": ["learning-loop", "search", "evidence-first"],
        },
        "source": "ALEXANDRIAN_ACADEMY",
        "entity_type": "LEARNING_ACTION_EXPLANATION",
        "title": "Why next learning action was recommended",
        "text": answer["recommended_action"] + " " + answer["plain_language_reason"],
        "target_ref": loop_ref,
        "evidence_ref_ids": evidence.get("evidence_anchor_refs", []),
        "memory_ref_ids": evidence.get("memory_refs", []),
        "search_ref_ids": evidence.get("search_refs", []),
        "governance_ref_ids": governance_refs,
        "agentplane_run_ref_ids": evidence.get("agentplane_run_refs", []),
        "final_score": 1.0,
    }


def main() -> int:
    if len(sys.argv) not in {2, 3}:
        print("Usage: export_learning_search_record.py <learning-action-explanation.json> [output.json]", file=sys.stderr)
        return 2

    explanation = load_json(Path(sys.argv[1]))
    search_record = build_search_record(explanation)
    output = json.dumps(search_record, indent=2, sort_keys=False) + "\n"

    if len(sys.argv) == 3:
        Path(sys.argv[2]).write_text(output, encoding="utf-8")
    else:
        sys.stdout.write(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
