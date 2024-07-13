.DEFAULT_GOAL:= help  # because it's is a safe task.

clean:  # Remove all build, test, coverage and Python artifacts.
	rm -rf .venv
	rm -rf *.egg-info
	find . -name "*.pyc" -exec rm -f {} \;
	find . -type f -name "*.py[co]" -delete -or -type d -name "__pycache__" -delete

flask:  # Run the Flask application.
	.venv/bin/python ./src/jim_bob/main.py

.PHONY: help
help: # Show help for each of the makefile recipes.
	@grep -E '^[a-zA-Z0-9 -]+:.*#'  Makefile | sort | while read -r l; do printf "\033[1;32m$$(echo $$l | cut -f 1 -d':')\033[00m:$$(echo $$l | cut -f 2- -d'#')\n"; done

lint:  # Lint the code with ruff and mypy.
	.venv/bin/python -m ruff check ./src ./tests
	.venv/bin/python -m mypy ./src ./tests

lock:  # Create the lock file and requirements file.
	rm -f requirements.*
	.venv/bin/python -m piptools compile --output-file=requirements.txt
	.venv/bin/python -m piptools compile --extra=dev --output-file=requirements.dev.txt

report:  # Report the python version and pip list.
	.venv/bin/python --version
	.venv/bin/python -m pip list -v

test:  # Run tests.
	.venv/bin/python -m pytest ./tests --verbose --color=yes

venv:  # Create an empty virtual environment (enough to create the requirements files).
	-python3 -m venv .venv  # Skip failure that happens in Github Action due to permissions.
	.venv/bin/python -m pip install --upgrade pip setuptools pip-tools

venv-dev:  # Create the development virtual environment.
	$(MAKE) venv
	.venv/bin/python -m pip install -r requirements.dev.txt
	.venv/bin/python -m pip install --editable .

venv-prod:  # Create the production virtual environment.
	$(MAKE) venv
	.venv/bin/python -m pip install -r requirements.txt
	.venv/bin/python -m pip install --editable .
