.DEFAULT_GOAL:= help  # because it's is a safe task.

# poetry has been installed in a virtual environment in the Docker image.
POETRY = /opt/.venv-poetry/bin/poetry

clean:  # Remove all build, test, coverage and Python artifacts.
	rm -rf .venv
	rm -rf *.egg-info
	find . -name "*.pyc" -exec rm -f {} \;
	find . -type f -name "*.py[co]" -delete -or -type d -name "__pycache__" -delete

.PHONY: help
help: # Show help for each of the makefile recipes.
	@grep -E '^[a-zA-Z0-9 -]+:.*#'  Makefile | sort | while read -r l; do printf "\033[1;32m$$(echo $$l | cut -f 1 -d':')\033[00m:$$(echo $$l | cut -f 2- -d'#')\n"; done

lock:  # Create the lock file.
	$(POETRY) lock

report:  # Report the python version and pip list.
	.venv/bin/python --version
	.venv/bin/python -m pip list -v

test:  # Run tests.
	.venv/bin/python -m pytest ./tests --verbose --color=yes

# poetry has been installed in a virtual environment in the Docker image.
POETRY = /opt/.venv-poetry/bin/poetry

venv:  # Recreate the virtual environment using poetry.
	$(POETRY) config virtualenvs.in-project true
	$(POETRY) install --no-interaction --no-ansi
