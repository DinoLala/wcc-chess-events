# Makefile for Python Project

# Variables
PYTHON = python3
PIP = pip3
VENV_DIR = venv
APP = app.py  # Replace with your main Python app file (e.g., Streamlit app)
# REQUIREMENTS = requirements.txt
TEST_DIR = tests  # Directory containing your test files (e.g., pytest)
LINTER = pylint  # Linter (pylint or another tool)

# Default target: install dependencies, run lint, and run app
.PHONY: all
all: install lint run

# Create a virtual environment
.PHONY: venv
venv:
	$(PYTHON) -m venv $(VENV_DIR)

# Install dependencies from requirements.txt
.PHONY: install
install: venv
	$(VENV_DIR)/bin/$(PIP) install -r $(REQUIREMENTS)

# Run the application (e.g., Streamlit app)
.PHONY: run
run:
	$(VENV_DIR)/bin/python -m streamlit run $(APP)

# Run tests using pytest (or another testing tool)
.PHONY: test
test:
	$(VENV_DIR)/bin/pytest $(TEST_DIR)

# Lint the code using pylint
.PHONY: lint
lint:
	$(VENV_DIR)/bin/$(LINTER) $(APP)

# Clean up virtual environment and other generated files
.PHONY: clean
clean:
	rm -rf $(VENV_DIR)
	rm
