VENV=.venv
PY=$(VENV)/bin/python
PIP=$(VENV)/bin/pip

.PHONY: venv deps validate validate-examples validate-templates verify-diagrams validate-strict

venv:
	python3 -m venv $(VENV)

deps: venv
	$(PIP) install -r atlas-codex/validators/requirements.txt

validate: deps verify-diagrams validate-examples validate-templates

validate-examples: deps
	$(PY) atlas-codex/validators/validate_object.py platform-contracts/examples/curriculum-plan.sandbox.json
	$(PY) atlas-codex/validators/validate_object.py platform-contracts/examples/curriculum-plan.canon.json
	$(PY) atlas-codex/validators/validate_object.py platform-contracts/examples/learning-loop-record.example.json

validate-templates: deps
	$(PY) atlas-codex/validators/validate_object.py templates/curriculum-builder/v1/curriculum-plan.template.json || true
	$(PY) atlas-codex/validators/validate_object.py templates/curriculum-builder/v1/unit-map.template.json || true
	$(PY) atlas-codex/validators/validate_object.py templates/curriculum-builder/v1/assessment-plan.template.json || true

verify-diagrams:
	python3 tools/verify_diagrams.py

validate-strict: deps verify-diagrams
	$(PY) atlas-codex/validators/validate_strict.py platform-contracts/examples/curriculum-plan.sandbox.json --expect-state draft
	$(PY) atlas-codex/validators/validate_strict.py platform-contracts/examples/curriculum-plan.canon.json --expect-state accepted
