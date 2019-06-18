# simple makefile to simplify repetetive build env management tasks under posix

# caution: testing won't work on windows, see README

PYTHON ?= python
PYTEST ?= pytest
CTAGS ?= ctags

all: clean inplace test

clean-pyc:
	find . -name "*.pyc" | xargs rm -f

clean-so:
	find . -name "*.so" | xargs rm -f
	find . -name "*.pyd" | xargs rm -f

clean-build:
	rm -rf build

clean-ctags:
	rm -f tags

clean: clean-build clean-pyc clean-so clean-ctags

flake:
	if command -v flake8 > /dev/null; then \
	    flake8 --count pyeparse examples; \
	fi

in: inplace # just a shortcut
inplace:
	$(PYTHON) setup.py build_ext -i

pytest:
	rm -f .coverage
	$(PYTEST) pyeparse

test: clean pytest flake
