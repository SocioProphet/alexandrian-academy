VENV=.venv
PY=$(VENV)/bin/python
PIP=$(VENV)/bin/pip

.PHONY: venv deps validate validate-examples validate-templates

venv:
python3 -m venv $(VENV)

deps: venv
$(PIP) install -r atlas-codex/validators/requirements.txt

validate: deps validate-examples validate-templates

validate-examples: deps
$(PY) atlas-codex/validators/validate_object.py platform-contracts/examples/curriculum-plan.sandbox.json
$(PY) atlas-codex/validators/validate_object.py platform-contracts/examples/curriculum-plan.canon.json

validate-templates: deps
$(PY) atlas-codex/validators/validate_object.py templates/curriculum-builder/v1/curriculum-plan.template.json || true
$(PY) atlas-codex/validators/validate_object.py templates/curriculum-builder/v1/unit-map.template.json || true
$(PY) atlas-codex/validators/validate_object.py templates/curriculum-builder/v1/assessment-plan.template.json || true
