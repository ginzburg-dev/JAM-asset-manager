PYTHON ?= python3
RUFF ?= ruff
MAYAPY ?= mayapy

.PHONY: help setup init-config install lint format test check build

help:
	@echo "Available targets:"
	@echo "  setup        Create config.json and print Maya module setup"
	@echo "  init-config  Copy config.example.json without overwriting"
	@echo "  install      Install an editable package with MAYAPY"
	@echo "  lint         Run Ruff lint and formatting checks"
	@echo "  format       Format source code and tests"
	@echo "  test         Run the unit test suite"
	@echo "  check        Run lint and tests"
	@echo "  build        Build the wheel package"

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

lint:
	$(RUFF) check --no-cache src tests
	$(RUFF) format --check --no-cache src tests

format:
	$(RUFF) format src tests

test:
	PYTHONPYCACHEPREFIX=/tmp/jam-asset-manager-pycache PYTHONPATH=src \
		$(PYTHON) -m unittest discover -s tests -v

check: lint test

build:
	uv build
