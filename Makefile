PREFIX ?= /usr/local
BIN_DIR = $(PREFIX)/bin
LIB_DIR = $(PREFIX)/lib/python2.7/dist-packages


INSTALL_TARGETS = install-dir install-package clean

install: $(INSTALL_TARGETS)

install-dir:
	install -d $(PREFIX) $(BIN_DIR) $(LIB_DIR)

install-package: install-dir
	java -jar ./lib/antlr-4.5-complete.jar -Dlanguage=Python2 ./lactose/grammar/lactose.g4
	PYTHONPATH=$(LIB_DIR) python setup.py -q install --prefix=$(PREFIX)

clean: install-package
	find . -name \*.pyc -delete
	rm -rf build
	rm -rf dist
	rm -rf lactose.egg-info