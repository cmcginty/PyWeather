# Makefile for installing and testing PyWeather
#
# Author: 	Patrick C. McGinty
# Date: 		Thursday, June 10 2010


NAME=weather
VER=$(shell python -c 'import weather;print weather.__version__')
DIST_DIR=dist
TAR=${DIST_DIR}/${NAME}-${VER}.tar.gz
SRC_DIR=${DIST_DIR}/${NAME}-${VER}

.PHONY: help
help:
	@echo "The following targets are defined:"
	@echo ""
	@echo "  clean      remove tmp files"
	@echo "  dist       create distribution archive file"
	@echo "  help 	     print usage instructions for the Makefile"
	@echo "  install    install program into system dirs"
	@echo "  test       execute all unit tests"
	@echo "  release    perform a full test/dist/install"
	@echo "  register   update the PyPI registration"
	@echo ""

.PHONY: test
test:
	nosetests

.PHONY: install
install:
	python setup.py install

.PHONY: clean
clean:
	python setup.py clean

.PHONY: dist
dist:
	python setup.py sdist --force-manifest
	make clean

.PHONY: dist-test
dist-test:
	tar xzf ${TAR} -C ${DIST_DIR}
	sudo make -C ${SRC_DIR} install
	sudo rm -rf ${SRC_DIR}

.PHONY: release
release: test dist dist-test

.PHONY: register
register:
	python setup.py register

