# This Makefile builds the proejct.
# It defines several targets and their dependencies.

# TODO:
#  - Figure out how to build a dev environment
#    vs. a production environment
#  - Figure out how to bump the version number


## HEADER MACROS
## ========================
# PHONY defines actions for the Makefile to perform which
# are not files. It is not strictly necessary to do this.
# These actions are tyically referred to as `targets` since
# in Makefiles they are often represnted by files.

# Some actions, like `lint`, `release` and others are
# widely understood to be actions and not files, so are
# typically not listed in the .PHONY list.

# TODO: break out Saskantinon and Saskantinize builds?
# Or at least make than an option?
# I made up the build vs. install distinction.
# May not be meaningful? Need to review.
.PHONY: help test build install docs clean clean-test clean-build clean-install

# DEFAULT_GOAL is the default target. If no target is specified,
# by the make command, then this target is executed.
.DEFAULT_GOAL := help


## IN-LINE PYTHON SCRIPTS
## ========================
define BROWSER_PYSCRIPT
import os, webbrowser, sys

try:
	from urllib import pathname2url
except:
	from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

BROWSER := python -c "$$BROWSER_PYSCRIPT"


## TARGETS
## ========================
help:
    @echo "Available targets:"
    @echo "  help           Get help on make targets"
    @echo "  lint           Run linting tools on all"
    @echo "  lint-saskantinon	Run linting tools"
    @echo "  lint-saskantinize	Run linting tools"
    @echo "  coverage       Run test coverage tool"
    @echo "  test           Run all tests"
    @echo "  test_saskantinon	Run unit tests"
    @echo "  test_saskantinize  Run unit tests"
    @echo "  build         	Build the project"
    @echo "  install       	Install the project"
    @echo "  dist       	Package and upload a release"
    @echo "  docs          	Generate documentation"
    @echo "  clean    	    Clean all"
    @echo "  clean-build   	Clean up build artifacts"
    @echo "  clean-pyc    	Clean up pyc files"
    @echo "  clean-test  	Clean up test artifacts"
    @echo ""
    @echo "Usage: make <target>"
    @echo ""

# Run tests quickly with the default Python.
# May need to tweak this to run the tests for each
# test directory correctly
test: test_saskantinon test_saskantinize

test_saskantinon:
	python -m pytest
test_saskantinize:
	python -m pytest

build:
    @echo "Building Saskantinon and Saskantinize..."
	python setup.py sdist bdist_wheel

install:
    @echo "Installing Saskantinon and Saskantinize..."
    python3 -m venv venv
    . venv/bin/activate; \
    pip install --upgrade pip setuptools wheel; \
    pip install .

# Run all of the clean-ups
# cleans remove temporary files created by the other processes.
# For example, the __pycache__ directory and the .pyc files or
# a build directory.  Not sure whether a venv would be deployed.
# Will want to review all of this and adjust as needed.
clean: clean-build clean-test clean-install

clean-build:
    @echo "Cleaning up temp files from build..."
    rm -rf venv
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc:
    @echo "Cleaning up pyc files from build..."
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +
	rm -rf debug/
	rm -rf log/

clean-test:
    @echo "Cleaning up temp files from test..."
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache

# generate Sphinx HTML documentation, including API docs
# `#(MAKE)` execute the make command on the Makefile in the
#   docs directory.
docs:
	rm -f docs/saskantinon.rst
	rm -f docs/saskantinize.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ saskantinon
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	$(BROWSER) docs/_build/html/index.html

servedocs: docs ## compile the docs watching for changes
	watchmedo shell-command -p '*.rst' -c '$(MAKE) -C docs html' -R -D .


## Standard non-file action tools/targets
## ========================================

# check style, etc.
# It may be useful to break out separate tests and
# examples for the two apps. Or figure out a way
# to separate them within the tests and examples
# directories.
# The `examples` is a place to provide examples of
# how things are to be done, going beyond the scope
# of unit and integration tests. These can be on the
# order of tutorials or just examples to developers
# or admins.
lint: lint-saskantinon lint-saskantinize

lint-saskantinon:
	isort Saskantinon examples tests
	black Saskantinon examples tests
	flake8 Saskantinon examples tests

lint-saskantinize:
	isort Saskantinize examples tests
	black Saskantinize examples tests
	flake8 Saskantinize examples tests

# check code coverage
# Probably need to play around with this to make
# sure the syntax works for the two apps and with
# having the test environments defined in setup.cfg
# rather than setup.py
coverage: lint
	coverage run setup.py test
	coverage report -m
	coverage html
	$(BROWSER) htmlcov/index.html

