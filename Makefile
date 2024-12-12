PYTHON ?= python

PROTO_DIR = src/xcvr_emu/proto
PROT_FILE = $(PROTO_DIR)/emulator.proto
OUT_DIR = $(PROTO_DIR)

VERSION ?= $(shell git describe --tags --always --dirty)

.PHONY: generate-grpc
generate-grpc:
	$(PYTHON) -m grpc.tools.protoc -I$(PROTO_DIR) --python_out=$(OUT_DIR) --grpc_python_out=$(OUT_DIR) --mypy_out=$(OUT_DIR) $(PROT_FILE)

.PHONY: generate-cmis
generate-cmis:
	cd src/cmis && $(PYTHON) -m base.gen > cmis.py && black cmis.py

test: ruff mypy pytest

pytest:
	$(PYTHON) -m pytest -v

ruff:
	$(PYTHON) -m ruff check .

mypy:
	$(PYTHON) -m mypy src/xcvr_emu src/cmis tests

docker:
	docker build -t xcvr_emu:$(VERSION) .
