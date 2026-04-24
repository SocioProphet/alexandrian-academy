#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from explain_learning_action import load_json


def build_memory_record(explanation: dict[str, Any]) -> dict[str, Any]:
    header = explanation["header"]
    answer = explanation["answer"]
    evidence = explanation["evidence"]
    governance = explanation["governance"]
    loop_ref = explanation["learning_loop_record_ref"]
    explanation_id = header["object_id"]

    governance_refs: list[str] = []
    governance_refs.extend(governance.get("oracle_evaluation_refs", []))
    governance_refs.extend(governance.get("moirai_changeset_refs", []))
    governance_refs.extend(governance.get("policy_check_refs", []))

    content = (
        "Learning action explanation: "
        + answer["recommended_action"]
        + " "
        + answer["plain_language_reason"]
    )

    return {
        "header": {
            "object_id": "lmr_" + explanation_id.removeprefix("lae_"),
            "object_type": "LearningMemoryRecord",
            "object_version": header.get("object_version", "0.1.0"),
            "created_at": header["created_at"],
            "created_by_contributor_id": header["created_by_contributor_id"],
            "created_by_role": "system",
            "status": "draft",
            "policy_tags": ["learning-loop", "memory", "evidence-first"],
        },
        "learning_loop_record_ref": loop_ref,
        "memoryd_write": {
            "envelope": {
                "user_id": "learner.example",
                "agent_id": "alexandrian.learning-agent",
                "run_id": (evidence.get("agentplane_run_refs") or ["agentplane://run/none"])[0],
                "workload_id": "alexandrian.learning-loop",
                "workspace_id": "academy.example",
                "channel": answer["channel"],
                "thread_id": "thread." + loop_ref,
                "source_interface": "alexandrian-academy",
                "metadata": {
                    "learning_loop_record_ref": loop_ref,
                    "learning_action_explanation_ref": explanation_id,
                },
            },
            "content": content,
            "memory_class": "decision",
            "persist_to_backend": True,
            "metadata": {
                "source": "ALEXANDRIAN_ACADEMY",
                "entity_type": "LEARNING_ACTION_EXPLANATION",
                "evidence_ref_ids": evidence.get("evidence_anchor_refs", []),
                "search_ref_ids": evidence.get("search_refs", []),
                "governance_ref_ids": governance_refs,
                "agentplane_run_ref_ids": evidence.get("agentplane_run_refs", []),
            },
            "tags": ["alexandrian-academy", "learning-loop", "why-recommended", "evidence-first"],
        },
    }


def main() -> int:
    if len(sys.argv) not in {2, 3}:
        print("Usage: export_learning_memory_record.py <learning-action-explanation.json> [output.json]", file=sys.stderr)
        return 2

    explanation = load_json(Path(sys.argv[1]))
    memory_record = build_memory_record(explanation)
    output = json.dumps(memory_record, indent=2, sort_keys=False) + "\n"

    if len(sys.argv) == 3:
        Path(sys.argv[2]).write_text(output, encoding="utf-8")
    else:
        sys.stdout.write(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
