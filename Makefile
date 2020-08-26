.PHONY: all prepare-dev venv lint test clean build test_upload upload
PROJECT=telegraf_pyplug

SHELL:=/bin/bash

VENV_NAME?=venv
PYTHON=$(shell pwd)/${VENV_NAME}/bin/python


all:
	@echo "make prepare-dev"
	@echo "    Create python virtual environment and install dependencies."
	@echo "make lint"
	@echo "    Run lint on project."
	@echo "make test"
	@echo "    Run tests on project."
	@echo "make clean"
	@echo "    Remove python artifacts, docker/ and virtualenv"
	@echo "make build"
	@echo "    Creates Python package."
	@echo "make test_upload"
	@echo "    Uploads package to TEST PyPI."
	@echo "make upload"
	@echo "    Uploads package to PyPI."

prepare-dev:
	which virtualenv || python3 -m pip install virtualenv
	make venv

venv: $(VENV_NAME)/bin/activate
$(VENV_NAME)/bin/activate: setup.py
	test -d $(VENV_NAME) || virtualenv -p python3 $(VENV_NAME)
	${PYTHON} -m pip install -U pip setuptools
	${PYTHON} -m pip install -e .[devel]
	touch $(VENV_NAME)/bin/activate

lint: venv
	${PYTHON} -m pylint --rcfile=.pylintrc *.py ${PROJECT}
	${PYTHON} -m mypy --namespace-packages ${PROJECT}

test: venv
	${PYTHON} -m unittest

clean:
	find . -name '*.pyc' -delete
	rm -rf $(VENV_NAME) *.eggs *.egg-info dist build docs/_build .cache

build: venv
	rm -rf dist/*
	${PYTHON} setup.py sdist bdist_wheel

test_upload: venv
	${PYTHON} -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*

upload: venv
	${PYTHON} -m twine upload dist/*
