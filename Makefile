VENV=.venv
PY=$(VENV)/bin/python
PIP=$(VENV)/bin/pip

.PHONY: venv deps validate validate-examples validate-stewarded-learning-artifact validate-generated-explanation validate-generated-search-record validate-generated-memory-record validate-explanation-server validate-memory-writer validate-search-publisher validate-explanation-bundle validate-explanation-bundle-e2e validate-templates verify-diagrams validate-strict validate-changeset-provenance

venv:
	python3 -m venv $(VENV)

deps: venv
	$(PIP) install -r atlas-codex/validators/requirements.txt

validate: deps verify-diagrams validate-examples validate-stewarded-learning-artifact validate-generated-explanation validate-generated-search-record validate-generated-memory-record validate-explanation-server validate-memory-writer validate-search-publisher validate-explanation-bundle validate-explanation-bundle-e2e validate-templates validate-changeset-provenance

validate-examples: deps
	$(PY) atlas-codex/validators/validate_object.py platform-contracts/examples/curriculum-plan.sandbox.json
	$(PY) atlas-codex/validators/validate_object.py platform-contracts/examples/curriculum-plan.canon.json
	$(PY) atlas-codex/validators/validate_object.py platform-contracts/examples/learning-loop-record.example.json
	$(PY) atlas-codex/validators/validate_object.py platform-contracts/examples/learning-action-explanation.example.json
	$(PY) atlas-codex/validators/validate_object.py platform-contracts/examples/learning-search-record.example.json
	$(PY) atlas-codex/validators/validate_object.py platform-contracts/examples/learning-memory-record.example.json

validate-stewarded-learning-artifact: deps
	$(PY) tools/tests/test_stewarded_learning_artifact.py

validate-generated-explanation: deps
	$(PY) tools/explain_learning_action.py platform-contracts/examples/learning-loop-record.example.json /tmp/alexandrian-learning-action-explanation.generated.json
	$(PY) atlas-codex/validators/validate_object.py /tmp/alexandrian-learning-action-explanation.generated.json

validate-generated-search-record: deps
	$(PY) tools/explain_learning_action.py platform-contracts/examples/learning-loop-record.example.json /tmp/alexandrian-learning-action-explanation.generated.json
	$(PY) tools/export_learning_search_record.py /tmp/alexandrian-learning-action-explanation.generated.json /tmp/alexandrian-learning-search-record.generated.json
	$(PY) atlas-codex/validators/validate_object.py /tmp/alexandrian-learning-search-record.generated.json

validate-generated-memory-record: deps
	$(PY) tools/explain_learning_action.py platform-contracts/examples/learning-loop-record.example.json /tmp/alexandrian-learning-action-explanation.generated.json
	$(PY) tools/export_learning_memory_record.py /tmp/alexandrian-learning-action-explanation.generated.json /tmp/alexandrian-learning-memory-record.generated.json
	$(PY) atlas-codex/validators/validate_object.py /tmp/alexandrian-learning-memory-record.generated.json

validate-explanation-server: deps
	PYTHONPATH=tools $(PY) tools/test_learning_loop_explanation_server.py

validate-memory-writer: deps
	PYTHONPATH=tools $(PY) tools/test_write_learning_memory.py

validate-search-publisher: deps
	PYTHONPATH=tools $(PY) tools/test_publish_learning_search_record.py

validate-explanation-bundle: deps
	PYTHONPATH=tools $(PY) tools/test_publish_learning_explanation_bundle.py

validate-explanation-bundle-e2e: deps
	PYTHONPATH=tools $(PY) tools/test_publish_learning_explanation_bundle_e2e.py

validate-templates: deps
	$(PY) atlas-codex/validators/validate_object.py templates/curriculum-builder/v1/curriculum-plan.template.json || true
	$(PY) atlas-codex/validators/validate_object.py templates/curriculum-builder/v1/unit-map.template.json || true
	$(PY) atlas-codex/validators/validate_object.py templates/curriculum-builder/v1/assessment-plan.template.json || true

validate-changeset-provenance: deps
	$(PY) atlas-codex/validators/validate_changeset.py moirai-ledger/changesets/examples/changeset-0001.promote-curriculum-plan.json
	$(PY) atlas-codex/validators/validate_changeset.py moirai-ledger/changesets/examples/changeset-0002.neurosymbolic-candidate.valid.json
	$(PY) atlas-codex/validators/validate_changeset.py moirai-ledger/changesets/examples/changeset-0003.neurosymbolic-candidate.rejected.missing-provenance.json || true
	$(PY) atlas-codex/validators/validate_changeset.py moirai-ledger/changesets/examples/changeset-0004.neurosymbolic-candidate.rejected.claims-authority.json || true
	$(PY) tools/tests/test_changeset_provenance.py

verify-diagrams:
	python3 tools/verify_diagrams.py

validate-strict: deps verify-diagrams
	$(PY) atlas-codex/validators/validate_strict.py platform-contracts/examples/curriculum-plan.sandbox.json --expect-state draft
	$(PY) atlas-codex/validators/validate_strict.py platform-contracts/examples/curriculum-plan.canon.json --expect-state accepted
