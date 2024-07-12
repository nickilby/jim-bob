# Stage 1: Base image
#####################
FROM mcr.microsoft.com/devcontainers/python:1-3.12-bullseye AS base

RUN apt-get update \
 && apt-get install -y build-essential curl

# This is where the production app will be run from and where the virtual environment
# will be prebuilt for use in testing.
WORKDIR /app

# Add some labels so it looks nice in Github packages.
LABEL org.opencontainers.image.source=https://github.com/nickilby/jim-bob/

# Stage 2a: Development and test image
######################################
# Includes a prebuild virtual environment with all the developer dependencies, but no
# source files, so is only rebuilt when the requirements.dev.txt or Dockerfile change.
# The prebuilt virtual environment is used to speed up testing so we don't have to wait
# for the dependencies to install before the tests can be run.
FROM base AS development

LABEL org.opencontainers.image.description="jim-bob development container."

# Copy only the necessary files and prebuild the virtual environment.
COPY Makefile pyproject.toml requirements.dev.txt ./
RUN make venv-dev

# Stage 2b: Production image
############################
# Include a prebuilt virtual environment with only the production dependencies and all
# the source files.  This will be used to run the app in production.
FROM base AS production

LABEL org.opencontainers.image.description="jim-bob production container."

# Copy everything and build the virtual environment without the dev dependencies.
COPY . .
RUN make venv-prod

# Run the Flask app with the poetry script in the virtual environment.
CMD [".venv/bin/run"]
