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
	@echo "  help           		Get help on make targets"
	@echo "  lint           		Run linting tools on all"
	@echo "  lint-saskantinon		Run app linting tools"
	@echo "  lint-saskantinize		Run app linting tools"
	@echo "  coverage       		Run test coverage tool"
	@echo "  test           		Run all tests"
	@echo "  test_saskantinon		Run app unit tests"
	@echo "  test_saskantinize  		Run app unit tests"
	@echo "  docs          		Generate documentation"
	@echo "  install        	Install all"
	@echo "  install_saskantinon    	Install the app"
	@echo "  install_saskantinize		Install the app"
	@echo "  dist       			Package and upload a release to PyPI"
	@echo "  clean    	    		Clean all"
	@echo "  clean-build   		Clean up build artifacts"
	@echo "  clean-pyc    			Clean up pyc files"
	@echo "  clean-test  			Clean up test artifacts"
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

# Linters, etc.
# The `- method <params> || true` syntax continuing even if
#  the linter returns an error.
# N.B. isort and black modify the source code.\
#  use --check on black to just see list of candidates
#  use --diff on black to see what would be changed
# - black -t py312 --check Saskantinon || true
# black -t py312 --diff Saskantinon
# N.B. flake8 does everything pycodestyle does and more,
#  no need to run both of them
# - flake8 Saskantinon || true
# N.B. mypy throws tons of errors if strict typing is
#  not adhered too. I find this to be too much of good
#  thing so am not using it.
# N.B. `examples` is a place to provide examples of
# how things are to be done, going beyond the scope
# of unit and integration tests. These can be on the
# order of tutorials or just examples to developers
# or admins.
lint: lint-saskantinon lint-saskantinize

# This is set up to check only, not fix (other than isort)
# May want to provide a "fix it" version also
lint-saskantinon:
	isort Saskantinon examples_saskantinon tests_saskantinon
	black -t py312 Saskantinon
	flake8 Saskantinon

lint-saskantinize:
	isort Saskantinize examples_saskantinize tests_saskantinize
	black Saskantinize examples_saskantinize tests_saskantinize
	flake8 Saskantinize examples_saskantinize tests_saskantinize
	black Saskantinize examples_saskantinize tests_saskantinize

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


## builds source and wheel package
# does this do anything with github? I think not.
# This is literally the build of the ptyhon package
# Prior to this, maybe we want the makefile to also
# do something with github actions? For example,
# make sure we have done a build from develop --> main,
# that tests have passed, that history has been updated
# and so on?
dist: clean
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist

## package and upload a release
# Need to look into what twine does
# twine is a utility for publishing to PyPI
release: dist
	twine upload dist/*

## install the package to the active Python's site-packages
# I think the idea here is that we are now pulling the
# package from PyPi and installing it just like any user.
# Not entirely sure that this is the right way to do this.
# May need to always install both apps.
# Not sure about use of a venv here.
# Need to consider best way to handle construction
#  of database and storage of other files for the app,
#  such as images, sound files, html files, etc.
install: install-saskantinon install-saskantinize

install-saskantinon: clean
	@echo "Installing Saskantinon..."
	python3 -m venv venv
	. venv/bin/activate; \
	pip install --upgrade pip setuptools wheel; \
	pip install .
	python Saskantinon/install_saskantinon.py
	python Saskantinize/install_saskantinize.py

install-saskantinize: clean
	@echo "Installing Saskantinize..."
	python3 -m venv venv
	. venv/bin/activate; \
	pip install --upgrade pip setuptools wheel; \
	pip install .
	python Saskantinize/install_saskantinize.py
