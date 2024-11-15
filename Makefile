PYTHON ?= python

PROTO_DIR = xcvr_emu/proto
PROT_FILE = $(PROTO_DIR)/emulator.proto
OUT_DIR = $(PROTO_DIR)

.PHONY: generate-grpc
generate-grpc:
	$(PYTHON) -m grpc.tools.protoc -I$(PROTO_DIR) --python_out=$(OUT_DIR) --grpc_python_out=$(OUT_DIR) --mypy_out=$(OUT_DIR) $(PROT_FILE)
