# Stage 1: Base image
#####################
FROM mcr.microsoft.com/devcontainers/python:1-3.12-bullseye AS base

RUN apt-get update \ 
 && apt-get install -y build-essential curl

# Install poetry in its own virtual environment to isolated it.
RUN export POETRY_HOME=/opt/.venv-poetry \
 && python3 -m venv $POETRY_HOME \
 && $POETRY_HOME/bin/pip install poetry==1.8.3 \
 && $POETRY_HOME/bin/poetry --version \
 && $POETRY_HOME/bin/poetry config virtualenvs.in-project true

# This is where the production app will be run from and where the virtual environment
# will be prebuilt for use in testing.
WORKDIR /app

# Expose the port that the app runs on
EXPOSE 8000

# Add some labels so it looks nice in Github packages.
LABEL org.opencontainers.image.source=https://github.com/nickilby/jim-bob/

# Stage 2a: Development and test image
######################################
# Includes a prebuild virtual environment with all the developer dependencies, but no
# source files, so is only rebuilt when the poetry.lock or Dockerfile change.  The 
# prebuilt virtual environment is used to speed up testing so we don't have to wait for
# the dependencies to install before the tests can be run.
FROM base AS development

# Copy only the necessary files and prebuild the virtual environment.
COPY pyproject.toml poetry.lock ./
RUN export POETRY_HOME=/opt/.venv-poetry \
 && $POETRY_HOME/bin/poetry install --no-interaction --no-ansi \
 && $POETRY_HOME/bin/poetry completions bash >> ~/.bash_completion

LABEL org.opencontainers.image.description="jim-bob development container."

# Stage 2b: Production image
############################
# Include a prebuilt virtual environment with only the production dependencies and all
# the source files.  This will be used to run the app in production.
FROM base AS production

# Copy everything and build the virtual environment without the dev dependencies.
COPY . .
RUN export POETRY_HOME=/opt/.venv-poetry \
 && $POETRY_HOME/bin/poetry install --without dev

# Define environment variable
ENV FLASK_APP=app.py

# Run the Flask app with Gunicorn
CMD ["poetry", "run", "gunicorn", "--bind", "0.0.0.0:5000", "app:app"]

LABEL org.opencontainers.image.description="jim-bob production container."
