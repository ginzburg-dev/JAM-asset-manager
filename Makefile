PYTHON ?= python3
RUFF ?= ruff
MAYAPY ?= mayapy

.PHONY: help setup init-config install sync-version lint format test compile check build ui

help:
	@echo "Available targets:"
	@echo "  setup        Create config.json and print Maya module setup"
	@echo "  init-config  Copy config.example.json without overwriting"
	@echo "  install      Install an editable package with MAYAPY"
	@echo "  sync-version Synchronize JAM.mod from pyproject.toml"
	@echo "  lint         Run Ruff lint and formatting checks"
	@echo "  format       Format source code and tests"
	@echo "  test         Run the unit test suite"
	@echo "  compile      Compile source and tests"
	@echo "  check        Run all local quality checks"
	@echo "  build        Build wheel and source distributions"
	@echo "  ui           Regenerate Qt forms with PySide compatibility"

setup: init-config
	@echo "Add this directory to MAYA_MODULE_PATH in Maya.env:"
	@echo "MAYA_MODULE_PATH=$(CURDIR)"

init-config:
	@if [ -e config.json ]; then \
		echo "config.json already exists; leaving it unchanged."; \
	else \
		cp config.example.json config.json; \
		echo "Created config.json from config.example.json."; \
	fi

install:
	$(MAYAPY) -m pip install --editable .

sync-version:
	$(PYTHON) -m scripts.sync_version

lint:
	$(RUFF) check --no-cache src tests scripts
	$(RUFF) format --check --no-cache src tests scripts

format:
	$(RUFF) format src tests scripts

test:
	PYTHONPYCACHEPREFIX=/tmp/jam-asset-manager-pycache PYTHONPATH=src \
		$(PYTHON) -m unittest discover -s tests -v

compile:
	PYTHONPYCACHEPREFIX=/tmp/jam-asset-manager-pycache \
		$(PYTHON) -m compileall -q src tests scripts

check: lint test compile

build:
	$(PYTHON) -m build

ui:
	$(PYTHON) scripts/generate_ui.py
