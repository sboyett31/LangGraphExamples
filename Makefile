# Makefile for LangGraph Examples Project

# Configuration variables
PYTHON := python

# Default target
.PHONY: all
all: install run

# Install dependencies
.PHONY: install
install:
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r requirements.txt

# Run the application
.PHONY: run
run:
	$(PYTHON) main.py

# Clean up
.PHONY: clean
clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Help target
.PHONY: help
help:
	@echo "Available targets:"
	@echo "  make install  - Install dependencies using system Python"
	@echo "  make run      - Run the main application"
	@echo "  make all      - Install dependencies and run the application"
	@echo "  make clean    - Remove Python cache files"
	@echo "  make help     - Display this help message"