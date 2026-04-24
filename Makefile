VENV=.venv
PY=$(VENV)/bin/python
PIP=$(VENV)/bin/pip

.PHONY: venv deps validate validate-examples validate-generated-explanation validate-generated-search-record validate-generated-memory-record validate-explanation-server validate-templates verify-diagrams validate-strict

venv:
	python3 -m venv $(VENV)

deps: venv
	$(PIP) install -r atlas-codex/validators/requirements.txt

validate: deps verify-diagrams validate-examples validate-generated-explanation validate-generated-search-record validate-generated-memory-record validate-explanation-server validate-templates

validate-examples: deps
	$(PY) atlas-codex/validators/validate_object.py platform-contracts/examples/curriculum-plan.sandbox.json
	$(PY) atlas-codex/validators/validate_object.py platform-contracts/examples/curriculum-plan.canon.json
	$(PY) atlas-codex/validators/validate_object.py platform-contracts/examples/learning-loop-record.example.json
	$(PY) atlas-codex/validators/validate_object.py platform-contracts/examples/learning-action-explanation.example.json
	$(PY) atlas-codex/validators/validate_object.py platform-contracts/examples/learning-search-record.example.json
	$(PY) atlas-codex/validators/validate_object.py platform-contracts/examples/learning-memory-record.example.json

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

validate-templates: deps
	$(PY) atlas-codex/validators/validate_object.py templates/curriculum-builder/v1/curriculum-plan.template.json || true
	$(PY) atlas-codex/validators/validate_object.py templates/curriculum-builder/v1/unit-map.template.json || true
	$(PY) atlas-codex/validators/validate_object.py templates/curriculum-builder/v1/assessment-plan.template.json || true

verify-diagrams:
	python3 tools/verify_diagrams.py

validate-strict: deps verify-diagrams
	$(PY) atlas-codex/validators/validate_strict.py platform-contracts/examples/curriculum-plan.sandbox.json --expect-state draft
	$(PY) atlas-codex/validators/validate_strict.py platform-contracts/examples/curriculum-plan.canon.json --expect-state accepted
