PYTHON ?= python
VENV_DIR ?= .venv
IMG ?= test.jpg

.PHONY: venv run lint format clean

venv:
	@echo "Creating virtual environment..."
	@bash src/utils/create_venv.sh

run:
	@echo "Running pipeline for $(IMG)..."
	PYTHONPATH=. $(PYTHON) scripts/run_pipeline.py $(IMG)

lint:
	@echo "Running linter..."
	@bash utils/check_style.sh

format:
	@echo "Formatting code..."
	@bash utils/format.sh

clean:
	@echo "Cleaning up temporary files..."
	@rm -rf data/interim/bboxes/* \
	        data/interim/filtered/* \
	        data/processed/crops/* \
	        data/annotations/raw/* \
	        data/annotations/filtered/*
	@echo "Clean complete."