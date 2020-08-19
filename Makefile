DIST=dist
REPOSITORY=pypi

include .env
export


all: install

upgrade:
	pip install --upgrade pip pip-tools setuptools
	pip-compile --upgrade --build-isolation --generate-hashes -o requirements.txt
	pip install -r requirements.txt

install:
	pip install --no-deps --editable .[dev]
	pip install -r requirements.txt

simon:
	simon

test:
	pytest

coverage:
	pytest --cov=simon

sdist:
	python setup.py sdist

bdist:
	pip install --upgrade wheel
	python setup.py bdist_wheel

dist: sdist bdist

release: clean dist
	pip install --upgrade twine
	twine upload --repository $(REPOSITORY) "$(DIST)/*"

clean:
	rm -rf build dist

.PHONY: all upgrade install simon test coverage sdist bdist dist release clean
